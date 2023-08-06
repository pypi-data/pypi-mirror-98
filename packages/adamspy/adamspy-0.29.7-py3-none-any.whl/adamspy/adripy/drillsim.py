"""Module for the DrillSim class
"""
import os
import subprocess
import glob
import platform

from thornpy.signal import step_function, low_pass
from numpy import linspace, argmax, array
from ..postprocess.xml import get_results, shrink_results
from .utilities import build, add_splines_to_acf, add_splines_to_adm
from ..postprocess import launch_ppt
from .string import DrillString
from .event import DrillEvent
from .solver_settings import DrillSolverSettings
from ..adamspy import get_simdur_from_acf, get_simdur_from_msg
from . import modify_acf_solver_settings

class DrillSim(): #pylint: disable=too-many-instance-attributes
    """Contains data defining the files that make up an Adams Drill input deck.    

    Parameters
    ----------
    string : DrillString
        :class:`DrillString` object representing the string to be used in the simulation
    event : DrillEvent
        :class:`DrillEvent` object representing the string to be used in the simulation
    solver_settings : DrillSolverSettings
        :class:`DrillSolverSettings` object representing the string to be used in the simulation
    directory : str
        Path to the directory in which to put the simulation files
    analysis_name : str
        Name of the analysis.  Used for all file prefixes

    Attributes
    ----------
    string : DrillString
        :class:`DrillString` object representing the string to be used in the simulation
    event : DrillEvent
        :class:`DrillEvent` object representing the string to be used in the simulation
    solver_settings : DrillSolverSettings
        :class:`DrillSolverSettings` object representing the string to be used in the simulation
    directory : str
        Path to the directory in which to put the simulation files
    analysis_name : str
        Name of the analysis.  Used for all file prefixes
    string_filename : str
        Filename of the analysis' string file relative to :attr:`directory`
    adm_filename : str
        Filename of the analysis' adm file relative to :attr:`directory`
    acf_filename : str
        Filename of the analysis' acf file relative to :attr:`directory`
    cmd_filename : str
        Filename of the analysis' cmd file relative to :attr:`directory`
    res_filename : str
        Filename of the analysis' res file relative to :attr:`directory`
    results : dict
        Simulation results
    results_units : dict
        Units of simulation results
    pason_inputs : dict
        Contains the cleaned pason signals that will be used as inputs to the Adams model. Keys are 'time', 'rop', 'wob', 'rpm', and 'gpm'.  Each value is a :obj:`list` with two entries.  The first is the signal and the second is the associated time.
    built : bool
        Indicates whether the input deck (adm, acf, and cmd files) has been built yet for this DrillSim
    solved : bool
        Indicates whether the :class:`DrillSim` has been solved and results file (.res) has been generated.
    RAMP_TIME : dict
        Class attribute containing standard ramp times for rpm, gpm, wob, and rop
    CUTOFF_FREQ : dict
        Class attribute containing default cutoff frequencies for smoothing pason inputs.
        
    Example
    -------
    >>> my_drillsim = adripy.DrillSim(my_string, my_event, my_solversettings, os.getcwd(), 'MyAnalysis')
    
    """
    RAMP_TIME = {
        'rpm': 10,
        'gpm': 20
    }
    CUTOFF_FREQ = {
        'wob': .1,
        'rop': .1
    }

    def __init__(self, string, event, solver_settings, directory, analysis_name, write_TO_files=True): #pylint: disable=too-many-arguments
        """Sets instance attributes and writes the string, event, and solver settings files to `directory`.
        
        """
        self.string = string
        self.event = event
        self.solver_settings = solver_settings
        self.directory = directory
        self.analysis_name = analysis_name
        self.string_filename = ''
        self.adm_filename = ''
        self.acf_filename = ''
        self.cmd_filename = ''
        self.res_filename = ''  
        self.msg_filename = ''      
        self.results = None     
        self.results_units = None
        
        # If `directory` does not exist, create it
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        # Write the TO files to the `directory`
        if write_TO_files:
            self.write_tiem_orbit_files()
        
        self.run_proc = None
        self.pason_inputs = {}

        # Flags
        self.built = False
        self.solved = False

    @classmethod
    def read_from_directory(cls, directory):
        """Returns a :class:`DrillSim` object from an existing directory that was previously created by a :class:`DrillSim` object.
        
        Note
        ----
        This method does not read the `pason_inputs` attribute

        Parameters
        ----------
        directory : str
            Path to a directory previously created by a :class:`DrillSim` object.
        
        Returns
        -------
        DrillSim
            :class:`DrillSim` object created from an existing directory that was previously created by a :class:`DrillSim` object.

        """
        # If `directory` is not a directory, raise an error
        if not os.path.isdir(directory):
            raise OSError(f'No directory found with name {directory}!')

        # Get string, event, ssf filenames
        string_filename = glob.glob(os.path.join(directory, '*.' + DrillString._EXT))[0]
        event_filename  = glob.glob(os.path.join(directory, '*.' + DrillEvent._EXT))[0]
        solver_settings_filename = glob.glob(os.path.join(directory, '*.' + DrillSolverSettings._EXT))[0]

        # Create string, event, ssf objects
        string = DrillString.read_from_file(string_filename)
        event = DrillEvent.read_from_file(event_filename)
        solver_settings = DrillSolverSettings.read_from_file(solver_settings_filename)

        # Get analysis name
        analysis_name = string.parameters['ModelName']

        # Create the DrillSim object
        drill_sim = cls(string, event, solver_settings, directory, analysis_name, write_TO_files=False)

        # Define file names
        drill_sim.string_filename = os.path.relpath(string_filename, directory)
        
        adm_files = glob.glob(os.path.join(directory, '*.adm'))
        drill_sim.adm_filename = os.path.relpath(adm_files[0], directory) if adm_files else ''

        acf_files = glob.glob(os.path.join(directory, '*.acf'))
        drill_sim.acf_filename = os.path.relpath(acf_files[0], directory) if acf_files else ''

        cmd_files = glob.glob(os.path.join(directory, '*.cmd'))
        drill_sim.cmd_filename = os.path.relpath(cmd_files[0], directory) if cmd_files else ''

        res_files = glob.glob(os.path.join(directory, '*.res'))
        drill_sim.res_filename = os.path.relpath(res_files[0], directory) if res_files else ''

        msg_files = glob.glob(os.path.join(directory, '*.msg'))
        drill_sim.msg_filename = os.path.relpath(msg_files[0], directory) if msg_files else ''

        # Set the `built` flag
        if drill_sim.acf_filename and drill_sim.adm_filename:            
            drill_sim.built = True
        
        # set the `solved` flag
        if drill_sim.res_filename:
            drill_sim.solved = True

        return drill_sim

    def get_pason_inputs(self, pason_data, t_min=None, t_max=None, sig_types=['wob', 'rpm', 'gpm', 'rop'], show_plots=True):
        """Extracts the wob, rpm, gpm, and/or rop from a :class:`PasonData` object.  If this is run before :meth:`build` the pason data will be added to the adm file as model input splines.
        
        Parameters
        ----------
        pason_data : PasonData
            A :class:`PasonData` object from which input splines will be extracted.
        t_min : float, optional
            Minimum time to extract. (the default is None, which starts at the beginning of the dataset)
        t_max : float, optional
            Maximum time to extract (the default is None, which goes to the end of the dataset)
        sig_types : list, optional
            Signal types to extract.  Options are 'wob', 'rpm', 'gpm', 'rop'.  (the default is ['wob', 'rpm', 'gpm', 'rop'])
        
        """
        # Set t_min and t_max if they weren't supplied
        if t_min is None:
            t_min = pason_data.time[0]
        if t_max is None:
            t_max = pason_data.time[-1]

        # loop through the requested signal types
        for sig_type in sig_types:
            self.pason_inputs[sig_type], _time = self.clean_pason(pason_data, sig_type, t_min, t_max, show_plot=show_plots)
        
        # Get the index for the start of the requested time range
        i_min = argmax(pason_data.data.index>=t_min)

        # Add the time signal
        self.pason_inputs['time'] = list(pason_data.data.index - pason_data.data.index[i_min])

    def build(self, wait=True):
        """This method builds the input deck.  It launches Adams View in batch, reads in the `self.string.filename` and `self.solver_settings.filename` files, and runs the Adams Drill macro ``ds tostart`` to build a drill string model.  Then it saves the model files (.acf, .adm, and .cmd) to the `self.directory` directory.

        Parameters
        ----------
        wait : bool
            If True, code execution waits until the build process terminates before moving on. (default is True)

        """
        # Build the model
        adm, acf, cmd = build(os.path.join(self.directory, self.string_filename), self.solver_settings.filename, self.directory, wait=wait)  

        # store the new filenames as attributes
        self.adm_filename = os.path.relpath(adm, self.directory)
        self.acf_filename = os.path.relpath(acf, self.directory)
        self.cmd_filename = os.path.relpath(cmd, self.directory)

        if self.pason_inputs:
            self._add_adm_splines()
            self._add_acf_splines()

        # Flag this simulation as built
        self.built = True

    def run(self, wait=True): #pylint: disable=no-self-use
        """Run the simulation
        
        Parameters
        ----------
        wait : bool
            If True the application will wait for the process to complete before continuing.

        """                
        
        if platform.system() == 'Windows':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW        
            self.run_proc = subprocess.Popen('"{}" ru-s "{}"'.format(os.environ['ADAMS_LAUNCH_COMMAND'], self.acf_filename), cwd=self.directory, startupinfo=startupinfo)
        
        else:
            self.run_proc = subprocess.Popen([os.environ['ADAMS_LAUNCH_COMMAND'], '-c', 'ru-standard', 'i', self.acf_filename, 'exit'], cwd=self.directory)

        self.msg_filename = f'{self.analysis_name}.msg'
        self.res_filename = f'{self.analysis_name}.res'

        # Flag this simulation as solved
        self.solved = True
        
        # Wait for the process to complete before moving on.
        if wait:
            self.run_proc.wait()
    
    def write_tiem_orbit_files(self):
        """Writes the solver settings and event files and publishes the string file to the simulation directory.

        Note
        ----
        When the string file gets published, all the supporting tool files and the hole file are copied to the simulation directory.
        """     
        # solver settings file
        self.solver_settings.write_to_file(self.analysis_name, directory=self.directory)        

        # event file
        self.event.parameters['Event_Name'] = self.analysis_name
        self.event.write_to_file(directory=self.directory)
        
        # string file
        self.string.parameters['Event_Property_File'] = os.path.split(self.event.filename)[1]
        self.string.parameters['ModelName'] = self.analysis_name
        self.string.parameters['OutputName'] = self.analysis_name
        abs_str_file = self.string.write_to_file(directory=self.directory, publish=True)   
        self.string_filename = os.path.relpath(abs_str_file, self.directory)
    
    def read_results(self, reqs_to_read=None, t_min=None, t_max=None, shrink_results_file=False, overwrite_pickle=False, use_iterparse=False):
        """Reads results from the results file.
        
        Example
        -------
        >>> drillsim.run()
        >>> t_min = 70
        >>> t_max = 71
        >>> reqs_to_read = {}
        >>> reqs_to_read['MSE'] = ['Instantaneous_Bottom_MSE', 'Filtered_Surface_MSE']
        >>> reqs_to_read['ROP_controls'] = ['Command_ROP', 'True_WOB']
        >>> results, units = drillsim.read_results(reqs_to_read, t_min, t_max)
        >>> results['MSE']['Instantaneous_Bottom_MSE']
        [5000.5621, 5000.8913, ]

        Parameters
        ----------
        reqs_to_read : dict, optional
            Dictionary of results data (the default is None, which gets all the results)
        t_min : float, optional
            Mininmum time for which to get results (the default is None, which gets results starting at the first time step)
        t_max : float, optional
            Maximum time for which to get results (the default is None, which gets results up to the last time step)
        shrink_results_file : bool, optional
            If True, the results file will be rewritten to include only the requests in `reqs_to_read` and the time period between `t_max` and `t_min`.
        
        """
        self.results, self.results_units = get_results(os.path.join(self.directory, self.res_filename), reqs_to_read, t_min, t_max, return_units=True, overwrite_pickle=overwrite_pickle, use_iterparse=use_iterparse)

        if shrink_results_file and any([reqs_to_read is not None, t_min is not None, t_max is not None]):
            shrink_results(os.path.join(self.directory, self.res_filename), reqs_to_keep=reqs_to_read, t_min=t_min, t_max=t_max, in_place=True)


    def launch_ppt(self, wait=False):
        """Launches the postprocessor and loads :attr:`res_filename`
        
        Parameters
        ----------
        wait : bool, optional
            If `True`, code execution will freeze until the postprocessor is closed. (the default is False)
        
        Raises
        ------
        FileNotFoundError
            Raised if no results file exists in :attr:`directory`.
        
        """
        # Check for results file
        if not self.res_filename:
            res_files = glob.glob(os.path.join(self.directory, '*.res'))
            if not res_files:
                raise FileNotFoundError('No results file found!  You must run the simultion using DrillSim.solve before you can launch the postprocessor to view the results.')
            self.res_filename = os.path.relpath(res_files[0], self.directory)
        
        # Launch the postprocessor
        launch_ppt(os.path.join(self.directory, self.res_filename), wait=wait)

    @classmethod
    def clean_pason(cls, pason_data, sig_type, t_min=None, t_max=None, show_plot=True, ramp_time=None, cutoff_freq=None):
        """Returns a cleaned up pason signal to be used as input to an Adams Drill model.
        
        Parameters
        ----------
        pason_data : PasonData
            Pason signal to be used as input.
        sig_type : str
            Type of signal. Options are 'wob', 'rpm', 'gpm', or 'rop'.
        t_min : float
            Minimum time to crop to the dataset to. (default is None which uses the beginning of the dataset)
        t_max : float
            Maximum time to crop the dataset to. (default is None which uses the end of the dataset)
        show_plot : bool, optional
            If True, shows a plot of the resulting setpoints (the default is True)      
        
        Returns
        -------
        list
            Cleaned signal
        list
            Associated time signal

        """      

        def crop_signal(t_min, t_max, signal, time):            
            if t_min is None:
                t_min = time[0]
            if t_max is None:
                t_max = time[-1]
            i_min = argmax(array(time)>=t_min)
            i_max = argmax(array(time)>=t_max)
            signal = signal[i_min:i_max+1]
            time = time[i_min:i_max+1] - time[i_min]
            return signal, time   

        if sig_type in ['rpm', 'gpm']:
            # For rpm and gpm get a stepped signal
            if ramp_time is None:
                ramp_time = cls.RAMP_TIME[sig_type]            
            signal, time = cls.get_stepped_signal(pason_data, ramp_time, sig_type, show_plot=False)        
        
        elif sig_type in ['wob', 'rop']:
            # For wob and rop get a filterd signal
            signal, time = cls.get_filtered_signal(pason_data, sig_type, cutoff_freq=cutoff_freq)

        else:
            raise ValueError('Value given for sig_type must be rpm, gpm, rop, or wob.')

        # Crop the signals if t_min or t_max are given
        if t_min or t_max:
            signal, time = crop_signal(t_min, t_max, signal, time)

        # If show_plots is true
        if show_plot:
            pason_data.plt.Figure()
            pason_data.plt.plot(pason_data.time, pason_data.data[sig_type], linewidth=2)
            pason_data.plt.ylabel(sig_type)
            pason_data.plt.plot(time, signal, linewidth=1)
            pason_data.plt.xlabel('Time (sec)')
            pason_data.plt.title(sig_type.upper())
            pason_data.plt.show()

        return list(signal), list(time)
    
    @classmethod
    def get_filtered_signal(cls, pason_data, sig_type, cutoff_freq=None):
        """Gets a filtered signal from the wob or rop data of a :class:`PasonData` object.

        This method uses a digital zero-phase 5th order butterworth filter with a 
        
        Parameters
        ----------
        pason_data : PasonData
            A :class:`PasonData` object
        sig_type : str
            Type of signal. Options are 'wob' or 'rop'
        cutoff_freq : float, optional
            Cutoff frequency to be used in the lowpass filter. (the default is None, which uses value from PasonData.CUTOFF_FREQ)
        
        Raises
        ------
        ValueError
            Raised if `sig_type` isn't 'wob' or 'rop'
        
        Returns
        -------
        list
            Filtered signal
        list
            Time associated with filterd signal

        """        
        # Check that the correct sig_type was passed.
        if sig_type not in ['wob', 'rop']:
            raise ValueError('sig_type must be wob or rop')
        
        # Set the cutoff frequency if it wasn't given
        if cutoff_freq is None:
            cutoff_freq = cls.CUTOFF_FREQ[sig_type]
        
        signal, time = low_pass(pason_data.data[sig_type], pason_data.time, cutoff_freq)
        
        return signal, time

    @classmethod
    def get_stepped_signal(cls, pason_data, ramp_time, sig_type, show_plot=True):
        """Gets the stepped signal from the rpm or gpm setpoints of a :class:`PasonData` object.
        
        Parameters
        ----------
        pason_data : PasonData
            A :class:`PasonData` object.
        ramp_time : float
            Time it takes to ramp the signal
        sig_type : str
            Type of signal options are 'rpm' or 'gpm'
        show_plot : bool
            If True, shows a plot of the resulting setpoints (the default is True)
        
        Returns
        -------
        list
            Stepped signal
        list
            Associated time signal

        """        
        def make_index(start, stop, step, endpoint=False):
            num = (stop-start)/step
            if not num.is_integer():
                raise ValueError('(stop-start)/step must be a whole number.')
            num = int(num)
            index = list(linspace(start, stop, num if endpoint is False else num+1, endpoint=endpoint, dtype=float))
            return index  

        # Check that the correct sig_type was passed.
        if sig_type not in ['rpm', 'gpm']:
            raise ValueError('sig_type must be rpm or gpm')

        # Get the sample period
        samp_per = round(pason_data.time[1]-pason_data.time[0], 3)

        # Set the ramp time if it is given

        # Determine the half ramp time rounded to the sample period
        half_ramp_time = round(ramp_time/samp_per/2)*samp_per

        # Get the setpoints from the pason data
        set_points = pason_data.get_setpoints(sig_type, show_plot=show_plot)

        # Initialize time and signal lists with the segment from the begining of the dataset to the beginning of the first ramp
        time = make_index(set_points[0][0], set_points[0][0]+half_ramp_time, samp_per)
        signal = [set_points[0][1] for t in time]

        # Add intermediate time segments
        for (sp_time, sp_val), (nxt_sp_time, nxt_sp_val) in zip(set_points[:-1], set_points[1:]):
            time_seg = make_index(sp_time + half_ramp_time, nxt_sp_time + half_ramp_time, samp_per)                
            signal.extend(step_function(time_seg, nxt_sp_time-half_ramp_time, sp_val, nxt_sp_time+half_ramp_time, nxt_sp_val))
            time.extend(time_seg)

        # Add the segment from the end of the last ramp to the end of the dataset
        time_seg = make_index(set_points[-1][0]+half_ramp_time, pason_data.time[-1], samp_per, endpoint=True)
        signal.extend([set_points[-1][1] for t in time_seg])
        time.extend(time_seg)
        return signal, time
    
    def get_duration(self, use_acf=False):
        """Returns the duration of the :class:`DrillSim` simulation based on contents of the acf file or the msg file.
        
        Parameters
        ----------
        use_acf : bool (optional)
            Set this to `True` if you want to use the acf file even if the :class:`DrillSim` has been solved. (the default is `False`)

        Returns
        -------
        float
            Duration of the simulation

        """
        if use_acf is True:
            duration = get_simdur_from_acf(os.path.join(self.directory, self.acf_filename)) if self.built is True else None
        else:
            duration = get_simdur_from_msg(os.path.join(self.directory, self.msg_filename)) if self.solved is True else 0
                    
        return duration       

    def modify_solver_settings(self, new_solver_settings):
        """Modifies the contents of the Adams Command (.acf) file given in `acf_file` to apply the solver settings specified in the Solver Settings (.ssf) file given in `ssf_file`.
        
        Parameters
        ----------
        solver_settings : DrillSolverSettings
            Solver settings to use in updating the Adams Command file.

        Note
        ----
        If the DrillSim.built is True, Only the static equilibrium funnel and the integrator error are modified

        """        
        # Remove the current solver settings file
        os.remove(self.solver_settings.filename)

        # Check if this drill sim has already been built
        if self.built:
            # If already built, update the funnel
            for i, (maxit, stab, error, imbal, tlim, alim) in enumerate(new_solver_settings.parameters['_Funnel']):
                self.solver_settings.add_funnel_step(maxit, stab, error, imbal, tlim, alim, clear_existing=True if i==0 else False)
            
            # Update the integrator error
            self.solver_settings.parameters['Error'] = new_solver_settings.parameters['Error']
            
            # Modify the acf file
            modify_acf_solver_settings(os.path.join(self.directory, self.acf_filename), new_solver_settings.parameters['Funnel'], new_solver_settings.parameters['Error'])
        
        else:
            # If not already built, simply replace self.sover_settings
            self.solver_settings = new_solver_settings
        
        # Write the modified solver settings
        self.solver_settings.write_to_file(self.analysis_name, directory=self.directory)    

    def _add_adm_splines(self):
        """Adds splines to the adm file
        
        """
        add_splines_to_adm(os.path.join(self.directory, self.adm_filename), self.pason_inputs)
            
    def _add_acf_splines(self):
        """Adds splines to the acf file
        
        """
        add_splines_to_acf(os.path.join(self.directory, self.acf_filename))
    
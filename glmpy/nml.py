from typing import Union
from typing import List
import json


class NML:
    """Generate .nml files.

    .nml files store config information required for running a simulation with
    the General Lake Model (GLM). Instances of this class store values that can
    be written to .nml files and have methods to write .nml files.

    Attributes
    ----------
    setup : str
        String representation of the `glm_setup` component of the .nml file
    mixing : str
        String representation of the `mixing` component of the .nml file
    morphometry : str
        String representation of the `morphometry` component of the .nml file

    Examples
    --------
    >>> from glmpy import NML
    >>> from glmpy import JSONToNML
    >>> my_json = JSONToNML("config.json")
    >>> nml = NML(
    ...     setup=my_json.get_nml_attributes("setup"),
    ...     mixing=my_json.get_nml_attributes("mixing"),
    ...     morphometry=my_json.get_nml_attributes("morphometry"),
    ...     time=my_json.get_nml_attributes("time"),
    ...     output=my_json.get_nml_attributes("output"),
    ...     init_profiles=my_json.get_nml_attributes("init_profiles"),
    ...     meteorology=my_json.get_nml_attributes("meteorology"),
    ...     light=my_json.get_nml_attributes("light"),
    ...     bird_model=my_json.get_nml_attributes("bird_model"),
    ...     inflows=my_json.get_nml_attributes("inflows"),
    ...     outflows=my_json.get_nml_attributes("outflows"),
    ...     sediment=my_json.get_nml_attributes("sediment"),
    ...     ice_snow=my_json.get_nml_attributes("ice_snow"),
    ...     wq_setup=my_json.get_nml_attributes("wq_setup")
    ... )
    >>> nml.write_nml()
    """

    def __init__(
        self,
        setup: Union[str, None],
        mixing: Union[str, None],
        morphometry: Union[str, None],
        time: Union[str, None],
        output: Union[str, None],
        init_profiles: Union[str, None],
        meteorology: Union[str, None],
        light: Union[str, None],
        bird_model: Union[str, None],
        inflows: Union[str, None],
        outflows: Union[str, None],
        sediment: Union[str, None],
        ice_snow: Union[str, None],
        wq_setup: Union[str, None],
    ):
        self.setup = setup
        self.mixing = mixing
        self.morphometry = morphometry
        self.time = time
        self.output = output
        self.init_profiles = init_profiles
        self.meteorology = meteorology
        self.light = light
        self.bird_model = bird_model
        self.inflows = inflows
        self.outflows = outflows
        self.sediment = sediment
        self.ice_snow = ice_snow
        self.wq_setup = wq_setup

    def write_nml(self, nml_file_path: str = "sim.nml"):
        """Write a .nml file.

        Writes a .nml file to the file path specified in `nml_file_path`.
        The .nml file stores config for a GLM simulation.

        Parameters
        ----------
        nml_file_path : str, optional
            file path to save .nml file, by default "sim.nml"

        Examples
        --------
        >>> from glmpy import NML
        >>> nml = NML(
        ...     setup=my_json.get_nml_attributes("setup"),
        ...     mixing=my_json.get_nml_attributes("mixing"),
        ...     morphometry=my_json.get_nml_attributes("morphometry"),
        ...     time=my_json.get_nml_attributes("time"),
        ...     output=my_json.get_nml_attributes("output"),
        ...     init_profiles=my_json.get_nml_attributes("init_profiles"),
        ...     meteorology=my_json.get_nml_attributes("meteorology"),
        ...     light=my_json.get_nml_attributes("light"),
        ...     bird_model=my_json.get_nml_attributes("bird_model"),
        ...     inflows=my_json.get_nml_attributes("inflows"),
        ...     outflows=my_json.get_nml_attributes("outflows"),
        ...     sediment=my_json.get_nml_attributes("sediment"),
        ...     ice_snow=my_json.get_nml_attributes("ice_snow"),
        ...     wq_setup=my_json.get_nml_attributes("wq_setup")
        ... )
        >>> nml.write_nml(nml_file_path="sim.nml")
        """

        def nml_block(block_name, block):
            """Returns a .nml block string representation.

            Returns a string representation for a particular .nml block.

            Parameters
            ----------
            block_name : str
                the name of the .nml block
            block : str
                the string representation of the .nml block

            Returns
            -------
            str
                the string representation of the .nml block

            Examples
            --------
            >>> nml_block("morphometry", self.morphometry)
            """
            return f"&{block_name}\n{block}\n/\n"

        def nml_output():
            """Returns a string representation of the .nml file.

            Constructs a string representation of the .nml file from `nml_block()`.

            Returns
            -------
            str
                the string representation of the .nml file

            Examples
            --------
            >>> nml_output()
            """
            blocks = [
                (nml_block("glm_setup", self.setup), self.setup),
                (nml_block("mixing", self.mixing), self.mixing),
                (nml_block("morphometry", self.morphometry), self.morphometry),
                (nml_block("time", self.time), self.time),
                (nml_block("output", self.output), self.output),
                (
                    nml_block("init_profiles", self.init_profiles),
                    self.init_profiles,
                ),
                (nml_block("meteorology", self.meteorology), self.meteorology),
                (nml_block("light", self.light), self.light),
                (nml_block("bird_model", self.bird_model), self.bird_model),
                (nml_block("inflows", self.inflows), self.inflows),
                (nml_block("outflows", self.outflows), self.outflows),
                (nml_block("sediment", self.sediment), self.sediment),
                (nml_block("ice_snow", self.ice_snow), self.ice_snow),
                (nml_block("wq_setup", self.wq_setup), self.wq_setup),
            ]
            return "".join(
                block_str
                for block_str, block_val in blocks
                if block_val is not None
            )

        with open(file=nml_file_path, mode="w") as file:
            file.write(nml_output())


class NMLBase:
    """Base class for each  NML block class.

    Provides the `set_attributes()` method for assigning a dictionary of
    attributes any NML block class.

    Attributes
    ----------
    attrs_dict : dict
        A dictionary containing the GLM configuration options as keys and the
        corresponding values to set.
    update : dict
        A dictionary containing GLM configuration options/values to update or
        add to the `attrs_dict`.

    Examples
    --------
    >>> from glmpy import NMLBase
    >>> from glmpy import NMLMorphometry
    >>> morphometry = NMLMorphometry()
    >>> morphometry.set_attributes(
    ...     attrs_dict={
    ...         "lake_name": "Example Lake'",
    ...         "latitude":  32,
    ...         "longitude": 35,
    ...         "crest_elev": -203.9,
    ...         "bsn_len": 21000,
    ...         "bsn_wid": 13000,
    ...         "max_layer_thick": 0.1,
    ...         "density_model": 1
    ...     },
    ...     update={
    ...         "bsn_vals": "3",
    ...         "H": [-252.9,  -251.9,  -250.9],
    ...         "A": [0,  9250000,  15200000,],
    ...     }
    ... )
    """

    def set_attributes(self, attrs_dict, update: dict):
        """Set attributes for the NMLSetup class.

        Set the attributes of the NMLSetup object using a dictionary of attribute names and values.

        Parameters
        ----------
        attrs_dict : dict
            A dictionary containing the attribute names as keys and the corresponding values to set.
        custom : dict
            A dictionary containing custom attribute names and values to update the attrs_dict with.

        Returns
        -------
        None

        Examples
        --------
        >>> from glmpy import NMLBase
        >>> from glmpy import NMLMorphometry
        >>> morphometry = NMLMorphometry()
        >>> morphometry.set_attributes(
        ...     attrs_dict={
        ...         "lake_name": "Example Lake'",
        ...         "latitude":  32,
        ...         "longitude": 35,
        ...         "crest_elev": -203.9,
        ...         "bsn_len": 21000,
        ...         "bsn_wid": 13000,
        ...         "max_layer_thick": 0.1,
        ...         "density_model": 1
        ...     },
        ...     update={
        ...         "bsn_vals": "3",
        ...         "H": [-252.9,  -251.9,  -250.9],
        ...         "A": [0,  9250000,  15200000,],
        ...     }
        ... )
        """
        if update is not None:
            attrs_dict.update(update)
        for key, value in attrs_dict.items():
            setattr(self, key, value)


class NMLSetup(NMLBase):
    """Define the glm_setup block of a GLM simulation configuration.

    The glm_setup component is used to define the simulations layer details.
    Attributes are set using the `set_attributes()` method and returned as a
    formatted string using the `__str__()` method.

    Attributes
    ----------
    sim_name : str
        Title of simulation.
    max_layers : int
        Maximum number of layers.
    min_layer_vol : float
        Minimum layer volume.
    min_layer_thick : float
        Minimum thickness of a layer (m).
    max_layer_thick : float
        Maximum thickness of a layer (m).
    density_model : int
        Switch to set the density equation.

    Examples
    --------
    >>> from glmpy import NMLSetup
    >>> setup = NMLSetup()
    """

    def __init__(self):
        self.sim_name = None
        self.max_layers = 500
        self.min_layer_vol = None
        self.min_layer_thick = None
        self.max_layer_thick = None
        self.density_model = 1

    def __str__(self):
        """Return the string representation of the NMLSetup object.

        Returns a formatted string of the NMLSetup configution options and
        values.

        Returns
        -------
        str
            String representation of the NMLSetup object.

        Examples
        --------
        >>> from glmpy import NMLSetup
        >>> setup = NMLSetup()
        >>> setup.set_attributes(attributes)
        >>> print(setup)
        """
        params = [
            (f"   sim_name = '{self.sim_name}'", self.sim_name),
            (f"   max_layers = {self.max_layers}", self.max_layers),
            (f"   min_layer_vol = {self.min_layer_vol}", self.min_layer_vol),
            (
                f"   min_layer_thick = {self.min_layer_thick}",
                self.min_layer_thick,
            ),
            (
                f"   max_layer_thick = {self.max_layer_thick}",
                self.max_layer_thick,
            ),
            (f"   density_model = {self.density_model}", self.density_model),
        ]
        return "\n".join(
            param_str
            for param_str, param_val in params
            if param_val is not None
        )


class NMLMorphometry(NMLBase):
    """Define the morphometry block of a GLM simulation configuration.

    Used to configure the location, depth & hypsographic curve. Attributes are
    set using the `set_attributes()` method and returned as a formatted string
    using the `__str__()` method.

    Attributes
    ----------
    lake_name : str
        Site name.
    latitude : float
        Latitude, positive North.
    longitude : float
        Longitude, positive East.
    base_elev: float
        Elevation of the bottom-most point of the lake (m above datum).
    crest_elev : float
        Elevation of a weir crest, where overflow begins.
    bsn_len : float
        Length of the lake basin, at crest height (m).
    bsn_wid : float
        Width of the lake basin, at crest height (m).
    bsn_vals : float
        Number of points being provided to described the hyposgraphic details.
    H : list
        Comma-separated list of lake elevations (m above datum).
    A : list
        Comma-separated list of lake areas (m^2).

    Examples
    --------
    >>> from glmpy import NMLMorphometry
    >>> morphometry = NMLMorphometry()
    """

    def __init__(self):
        self.lake_name = None
        self.latitude = None
        self.longitude = None
        self.base_elev = None
        self.crest_elev = None
        self.bsn_len = None
        self.bsn_wid = None
        self.bsn_vals = None
        self.H = None
        self.A = None

    def __str__(self):
        """Return the string representation of the NMLMorphometry object.

        Returns a formatted string of the NMLMorphometry configution options and
        values.

        Returns
        -------
        str
            String representation of the NMLMorphometry object.

        Examples
        --------
        >>> from glmpy import NMLMorphometry
        >>> morphometry = NMLMorphometry()
        >>>  morphometry.set_attributes(
        ...     attrs_dict={
        ...         "lake_name": "Example Lake'",
        ...         "latitude":  32,
        ...         "longitude": 35,
        ...         "crest_elev": -203.9,
        ...         "bsn_len": 21000,
        ...         "bsn_wid": 13000,
        ...         "max_layer_thick": 0.1,
        ...         "density_model": 1
        ...     },
        ...     update={
        ...         "bsn_vals": "3",
        ...         "H": [-252.9,  -251.9,  -250.9],
        ...         "A": [0,  9250000,  15200000,],
        ...     }
        ... )
        >>> print(morphometry)
        """
        params = [
            (f"   lake_name = '{self.lake_name}'", self.lake_name),
            (f"   latitude = {self.latitude}", self.latitude),
            (f"   longitude = {self.longitude}", self.longitude),
            (f"   base_elev = {self.base_elev}", self.base_elev),
            (f"   crest_elev = {self.crest_elev}", self.crest_elev),
            (f"   bsn_len = {self.bsn_len}", self.bsn_len),
            (f"   bsn_wid = {self.bsn_wid}", self.bsn_wid),
            (f"   bsn_vals = {self.bsn_vals}", self.bsn_vals),
            (
                f"   H = {', '.join([str(num) for num in self.H]) if self.H else None}",
                self.H,
            ),
            (
                f"   A = {', '.join([str(num) for num in self.A]) if self.A else None}",
                self.A,
            ),
        ]
        return "\n".join(
            param_str
            for param_str, param_val in params
            if param_val is not None
        )


class NMLMixing(NMLBase):
    """Define the mixing block of a GLM simulation configuration.

    Used to configure mixing parameters. Attributes are set using the
    `set_attributes()` method and returned as a formatted string using the
    `__str__()` method.

    Attributes
    ----------
    surface_mixing : int
        Switch to select the options of the surface mixing model.
    coef_mix_conv : float
        Mixing efficiency - convective overturn.
    coef_wind_stir : float
        Mixing efficiency - wind stirring.
    coef_mix_shear : float
        Mixing efficiency - shear production.
    coef_mix_turb : float
        Mixing efficiency - unsteady turbulence effects
    coef_mix_KH : float
        Mixing efficiency - Kelvin-Helmholtz billowing.
    deep_mixing : int
        Switch to select the options of the deep (hypolimnetic) mixing model
        (0 = no deep mixing, 1 = constant diffusivity, 2 = weinstock model).
    coef_mix_hyp : float
        Mixing efficiency - hypolimnetic turbulence.
    diff : float
        Background (molecular) diffusivity in the hypolimnion.

    Examples
    --------
    >>> from glmpy import NMLMixing
    >>> mixing = NMLMixing()
    """

    def __init__(self):
        self.surface_mixing = 1
        self.coef_mix_conv = None
        self.coef_wind_stir = None
        self.coef_mix_shear = None
        self.coef_mix_turb = None
        self.coef_mix_KH = None
        self.deep_mixing = None
        self.coef_mix_hyp = None
        self.diff = None

    def __str__(self):
        """Return the string representation of the NMLMixing object.

        Returns a formatted string of the NMLMixing configution options and
        values.

        Returns
        -------
        str
            String representation of the NMLMixing object.
        """
        params = [
            (
                f"   surface_mixing = {self.surface_mixing}",
                self.surface_mixing,
            ),
            (f"   coef_mix_conv = {self.coef_mix_conv}", self.coef_mix_conv),
            (
                f"   coef_wind_stir = {self.coef_wind_stir}",
                self.coef_wind_stir,
            ),
            (
                f"   coef_mix_shear = {self.coef_mix_shear}",
                self.coef_mix_shear,
            ),
            (f"   coef_mix_turb = {self.coef_mix_turb}", self.coef_mix_turb),
            (f"   coef_mix_KH = {self.coef_mix_KH}", self.coef_mix_KH),
            (f"   deep_mixing = {self.deep_mixing}", self.deep_mixing),
            (f"   coef_mix_hyp = {self.coef_mix_hyp}", self.coef_mix_hyp),
            (f"   diff = {self.diff}", self.diff),
        ]
        return "\n".join(
            param_str
            for param_str, param_val in params
            if param_val is not None
        )


class NMLTime(NMLBase):
    """Define the time block of a GLM simulation configuration.

    Used to configure the simulation period, time step, and time zone.
    Attributes are set using the `set_attributes()` method and returned as a
    formatted string using the `__str__()` method.

    Attributes
    ----------
    timefmt : int
        Time configuration switch.
    start : str
        Start time/date of simulation in format 'yyyy-mm-dd hh:mm:ss'.
    stop : str
        End time/date of simulation in format 'yyyy-mm-dd hh:mm:ss'.
    dt : float
        Time step (seconds).
    num_days : int
        Number of days to simulate.
    timezone : float
        UTC time zone.

    Examples
    --------
    >>> from glmpy import NMLSetup
    >>> time = NMLTime()
    """

    def __init__(self):
        self.timefmt = None
        self.start = None
        self.stop = None
        self.dt = None
        self.num_days = None
        self.timezone = None

    def __str__(self):
        """Return the string representation of the NMLTime object.

        Returns a formatted string of the NMLTime configution options and
        values.

        Returns
        -------
        str
            String representation of the NMLTime object.
        """

        params = [
            (f"   timefmt = {self.timefmt}", self.timefmt),
            (f"   start = '{self.start}'", self.start),
            (f"   stop = '{self.stop}'", self.stop),
            (f"   dt = {self.dt}", self.dt),
            (f"   num_days = {self.num_days}", self.num_days),
            (f"   timezone = {self.timezone}", self.timezone),
        ]
        return "\n".join(
            param_str
            for param_str, param_val in params
            if param_val is not None
        )


class NMLOutput(NMLBase):
    """Define the output block of a GLM simulation configuration.

    Used to configure the netcdf & csv output details. Attributes are set using
    the `set_attributes()` method and returned as a formatted string using the
    `__str__()` method.

    Attributes
    ----------
    out_dir : str
        Directory to write the output files.
    out_fn : str
        Filename of the main NetCDF output file.
    nsave : int
        Frequency to write to the NetCDF and CSV point files.
    csv_lake_fname : str
        Filename for the daily summary file.
    csv_point_nlevs : float
        Number of specific level/depth csv files to be created.
    csv_point_fname : str
        Name to be appended to specified depth CSV files.
    csv_point_frombot : float
        Comma separated list identify whether each output point listed in
        csv_point_at is relative to the bottom (ie heights) or the surface
        (ie depths).
    csv_point_at : float
        Height or Depth of points to output at (comma separated list).
    csv_point_nvars : int
        Number of variables to output into the csv files.
    csv_point_vars : str
        Comma separated list of variable names.
    csv_outlet_allinone : string
        Switch to create an optional outlet file combining all outlets.
    csv_outlet_fname : str
        Name to be appended to each of the outlet CSV files.
    csv_outlet_nvars : int
        Number of variables to be written into the outlet file(s).
    csv_outlet_vars : str
        Comma separated list of variable names to be included in the output
        file(s)
    csv_ovrflw_fname : str
        Filename to be used for recording the overflow details.

    Examples
    --------
    >>> from glmpy import NMLOutput
    >>> output = NMLOutput()
    """

    def __init__(self):
        self.out_dir = None
        self.out_fn = None
        self.nsave = None
        self.csv_lake_fname = None
        self.csv_point_nlevs = None
        self.csv_point_fname = None
        self.csv_point_at = None
        self.csv_point_nvars = None
        self.csv_point_vars = None
        self.csv_outlet_allinone = None
        self.csv_outlet_fname = None
        self.csv_outlet_nvars = None
        self.csv_outlet_vars = None
        self.csv_ovrflw_fname = None

    def __str__(self):
        """Return the string representation of the NMLOutput object.

        Returns a formatted string of the NMLOutput configution options and
        values.

        Returns
        -------
        str
            String representation of the NMLOutput object.
        """
        params = [
            (f"   out_dir = '{self.out_dir}'", self.out_dir),
            (f"   out_fn = '{self.out_fn}'", self.out_fn),
            (f"   nsave = {self.nsave}", self.nsave),
            (
                f"   csv_lake_fname = '{self.csv_lake_fname}'",
                self.csv_lake_fname,
            ),
            (
                f"   csv_point_nlevs = {self.csv_point_nlevs}",
                self.csv_point_nlevs,
            ),
            (
                f"   csv_point_fname = '{self.csv_point_fname}'",
                self.csv_point_fname,
            ),
            (
                f"   csv_point_at = {', '.join([str(num) for num in self.csv_point_at]) if self.csv_point_at else None}",
                self.csv_point_at,
            ),
            (
                f"   csv_point_nvars = {self.csv_point_nvars}",
                self.csv_point_nvars,
            ),
            (
                f"   csv_point_vars = {', '.join([repr(var) for var in self.csv_point_vars]) if self.csv_point_vars else None}",
                self.csv_point_vars,
            ),
            (
                f"   csv_outlet_allinone = {str(self.csv_outlet_allinone)}",
                self.csv_outlet_allinone,
            ),
            (
                f"   csv_outlet_fname = '{self.csv_outlet_fname}'",
                self.csv_outlet_fname,
            ),
            (
                f"   csv_outlet_nvars = {self.csv_outlet_nvars}",
                self.csv_outlet_nvars,
            ),
            (
                f"   csv_outlet_vars = {', '.join([repr(var) for var in self.csv_outlet_vars]) if self.csv_outlet_vars else None}",
                self.csv_outlet_vars,
            ),
            (
                f"   csv_ovrflw_fname = '{self.csv_ovrflw_fname}'",
                self.csv_ovrflw_fname,
            ),
        ]
        return "\n".join(
            param_str
            for param_str, param_val in params
            if param_val is not None
        )


class NMLInitProfiles(NMLBase):
    """Define the initial profiles block of a GLM simulation configuration.

    Used to configure the initial temperature and salinity profiles.
    Attributes are set using the `set_attributes()` method and returned as a
    formatted string using the `__str__()` method.

    Attributes
    ----------
    lake_depth : float
        Initial lake height/depth (m).
    num_depths : int
        Number of depths provided for initial profiles.
    the_depths : list[float]
        The depths of the initial profile points (m).
    the_temps : list[float]
        The temperature (C) at each of the initial profile points.
    the_sals : list[float]
        The salinity (ppt) at each of the initial profile points.
    num_wq_vars : int
        Number of non GLM (ie FABM or AED2) variables to be initialised.
    wq_names : list[str]
        Names of non GLM (ie FABM or AED2) variables to be initialised.
    wq_init_vals : float
        Array of WQ variable initial data (rows = vars; cols = depths)

    Examples
    --------
    >>> from glmpy import NMLSetup
    >>> init_profiles = NMLInitProfiles()
    """

    def __init__(self):
        self.lake_depth = None
        self.num_depths = None
        self.the_depths = None
        self.the_temps = None
        self.the_sals = None

        print(getattr(self, key))

    def __str__(self):
        """Return the string representation of the NMLInitProfiles object.

        Returns a formatted string of the NMLInitProfiles configution options
        and values.

        Returns
        -------
        str
            String representation of the NMLInitProfiles object.
        """
        params = [
            (f"   lake_depth = {self.lake_depth}", self.lake_depth),
            (f"   num_depths = {self.num_depths}", self.num_depths),
            (
                f"   the_depths = {', '.join([str(num) for num in self.the_depths]) if self.the_depths else None}",
                self.the_depths,
            ),
            (
                f"   the_temps = {', '.join([str(num) for num in self.the_temps]) if self.the_temps else None}",
                self.the_temps,
            ),
            (
                f"   the_sals = {', '.join([str(num) for num in self.the_sals]) if self.the_sals else None}",
                self.the_sals,
            ),
        ]
        return "\n".join(
            param_str
            for param_str, param_val in params
            if param_val is not None
        )


class NMLMeteorology(NMLBase):
    """Define the meteorology block of a GLM simulation configuration.

    Used to configure the surface energy balance options, and  local run-off
    parameters. Attributes are set using the `set_attributes()` method and
    returned as a formatted string using the `__str__()` method.

    Attributes
    ----------
    met_sw : str
        Switch to enable the surface heating module
    lw_type : str
        Switch to configure which input approach is being used for
        longwave/cloud data in the meteo_fl.
    rain_sw : str
        Switch to configure rainfall input concentrations.
    atm_stab : int
        Switch to configure which approach to atmospheric stability is used.
    fetch_mode : int
        Switch to configure which wind-sheltering/fetch option to use.
    rad_mode : int
        Switch to configure which incoming radiation option to use.
    albedo_mode : int
        Switch to configure which albedo calculation option is used.
    cloud_mode : int
        Switch to configure which atmospheric emmissivity calculation
        option is used.
    subdaily : bool
        Switch to indicate the meteorological data is provided with sub-daily
        resolution, at an interval equivalent to Δt
    meteo_fl : str
        Filename of the meterological file.
    wind_factor : float
        Scaling factor to adjust the windspeed data provided in the meteo_fl
    lw_factor : float
        Scaling factor to adjust the longwave (or cloud) data provided in the
        meteo_fl
    lw_offset : float
        !!!!! Not sure what this is for - can't find it in the docs
    ce : float
        Bulk aerodynamic transfer coefficient for latent heat flux.
    ch : float
        Bulk aerodynamic transfer coefficient for sensible heat flux.
    cd : float
        Bulk aerodynamic transfer coefficient for momentum.

    Examples
    --------
    >>> from glmpy import NMLMeteorology
    >>> meteorology = NMLMeteorology()
    >>> print(meteorology)
    """

    def __init__(self):
        self.met_sw = None
        self.lw_type = None
        self.rain_sw = None
        self.atm_stab = None
        self.fetch_mode = None
        self.rad_mode = None
        self.albedo_mode = None
        self.cloud_mode = None
        self.subdaily = None
        self.meteo_fl = None
        self.wind_factor = None
        self.lw_factor = None
        self.lw_offset = None
        self.ce = None
        self.ch = None
        self.cd = None
        print(getattr(self, key))

    def __str__(self):
        """Return the string representation of the NMLMeteorology object.

        Returns a formatted string of the NMLMeteorology configution options
        and values.

        Returns
        -------
        str
            String representation of the NMLMeteorology object.
        """

        params = [
            (f"   met_sw = {str(self.met_sw)}", self.met_sw),
            (f"   lw_type = '{self.lw_type}'", self.lw_type),
            (f"   rain_sw = {str(self.rain_sw)}", self.rain_sw),
            (f"   atm_stab = {self.atm_stab}", self.atm_stab),
            (f"   fetch_mode = {self.fetch_mode}", self.fetch_mode),
            (f"   rad_mode = {self.rad_mode}", self.rad_mode),
            (f"   albedo_mode = {self.albedo_mode}", self.albedo_mode),
            (f"   cloud_mode = {self.cloud_mode}", self.cloud_mode),
            (f"   subdaily = {str(self.subdaily)}", self.subdaily),
            (f"   meteo_fl = '{self.meteo_fl}'", self.meteo_fl),
            (f"   wind_factor = {self.wind_factor}", self.wind_factor),
            (f"   lw_factor = {self.lw_factor}", self.lw_factor),
            (f"   lw_offset = {self.lw_offset}", self.lw_offset),
            (f"   ce = {self.ce}", self.ce),
            (f"   ch = {self.ch}", self.ch),
            (f"   cd = {self.cd}", self.cd),
        ]
        return "\n".join(
            param_str
            for param_str, param_val in params
            if param_val is not None
        )


class NMLLight(NMLBase):
    """Define the light block of a GLM simulation configuration.

    Used to configure the light settings. Attributes are set using the
    `set_attributes()` method and returned as a formatted string using the
    `__str__()` method.

    Attributes
    ----------
    light_mode : int
        Switch to configure the approach to light penetration.
    Kw : float
        Light extinction coefficient.
    n_bands : int
        Number of light bandwidths to simulate.
    light_extc : float
        Comma-separated list of light extinction coefficients for each waveband.
    energy_frac : float
        Comma-separated list of energy fraction captured by each waveband.
    Benthic_Imin : float
        Critical fraction of incident light reaching the benthos.

    Examples
    --------
    >>> from glmpy import NMLLight
    >>> light = NMLLight()
    >>> print(light)
    """

    def __init__(self):
        self.light_mode = None
        self.Kw = None
        self.n_bands = None
        self.light_extc = None
        self.energy_frac = None
        self.Benthic_Imin = None

        print(getattr(self, key))

    def __str__(self):
        """Return the string representation of the NMLLight object.

        Returns a formatted string of the NMLLight configution options
        and values.

        Returns
        -------
        str
            String representation of the NMLLight object.
        """
        params = [
            (f"   light_mode = {self.light_mode}", self.light_mode),
            (f"   Kw = {self.Kw}", self.Kw),
            (f"   n_bands = {self.n_bands}", self.n_bands),
            (
                f"   light_extc = {', '.join([str(num) for num in self.light_extc]) if self.light_extc else None}",
                self.light_extc,
            ),
            (
                f"   energy_frac = {', '.join([str(num) for num in self.energy_frac]) if self.energy_frac else None}",
                self.energy_frac,
            ),
            (f"   Benthic_Imin = {self.Benthic_Imin}", self.Benthic_Imin),
        ]
        return "\n".join(
            param_str
            for param_str, param_val in params
            if param_val is not None
        )


class NMLBirdModel(NMLBase):
    """Define the bird model block of a GLM simulation configuration.

    Used to configure the surface energy balance options, and  local run-off
    parameters. Attributes are set using the `set_attributes()` method and
    returned as a formatted string using the `__str__()` method.

    Attributes
    ----------
    AP : float
        Atmospheric pressure (hPa).
    Oz : float
        Ozone concentration (atm-cm).
    WatVap : float
        Total Precipitable water vapor (atm-cm).
    AOD500 : float
        Dimensionless Aerosol Optical Depth at wavelength 500 nm.
    AOD380 : float
        Dimensionless Aerosol Optical Depth at wavelength 380 nm.
    Albedo : float
        Albedo of the surface used for Bird Model insolation calculation.

    Examples
    --------
    >>> from glmpy import NMLBirdModel
    >>> bird = NMLBirdModel()
    >>> print(bird)
    """

    def __init__(self):
        self.AP = None
        self.Oz = None
        self.WatVap = None
        self.AOD500 = None
        self.AOD380 = None
        self.Albedo = None
        print(getattr(self, key))

    def __str__(self):
        """Return the string representation of the NMLBirdModel object.

        Returns a formatted string of the NMLBirdModel configution options
        and values.

        Returns
        -------
        str
            String representation of the NMLBirdModel object.
        """
        params = [
            (f"   AP = {self.AP}", self.AP),
            (f"   Oz = {self.Oz}", self.Oz),
            (f"   WatVap = {self.WatVap}", self.WatVap),
            (f"   AOD500 = {self.AOD500}", self.AOD500),
            (f"   AOD380 = {self.AOD380}", self.AOD380),
            (f"   Albedo = {self.Albedo}", self.Albedo),
        ]
        return "\n".join(
            param_str
            for param_str, param_val in params
            if param_val is not None
        )


class NMLInflows(NMLBase):
    """Define the inflows block of a GLM simulation configuration.

    Used to configure the number/type of inflows and inflow files. Attributes
    are set using the `set_attributes()` method and returned as a formatted
    string using the `__str__()` method.

    Attributes
    ----------
    num_inflows : int
        Number of inflows to be simulated in this simulation.
    names_of_strms : str
        Names of each inflow.
    subm_flag : str
        Switch indicating if the inflow I is entering as a submerged input.
    strm_hf_angle : float
        Angle describing the width of an inflow river channel ("half angle").
    strmbd_slope : float
        Slope of the streambed / river thalweg for each river (degrees)
    strmbd_drag : float
        Drag coefficient of the river inflow thalweg, to calculate entrainment
        during insertion
    inflow_factor : float
        Scaling factor that can be applied to adjust the provided input data.
    inflow_fl : str
        Filename(s) of the inflow CSV boundary condition files.
    inflow_varnum : int
        Number of variables being listed in the columns of inflow_fl
        (comma-separated list)
    inflow_vars : str
        Names of the variables in the inflow_fl
    coef_inf_entrain : float
    time_fmt : str
        Time format of the 1st column in the inflow_fl

    Examples
    --------
    >>> from glmpy import NMLInflows
    >>> inflows = NMLInflows()
    >>> print(inflows)
    """

    def __init__(self):
        self.num_inflows = None
        self.names_of_strms = None
        self.subm_flag = None
        self.strm_hf_angle = None
        self.strmbd_slope = None
        self.strmbd_drag = None
        self.inflow_factor = None
        self.inflow_fl = None
        self.inflow_varnum = None
        self.inflow_vars = None
        self.inflow_vars = None
        self.coef_inf_entrain = None
        self.time_fmt = None
        print(getattr(self, key))

    def __str__(self):
        """Return the string representation of the NMLInflows object.

        Returns a formatted string of the NMLInflows configution options
        and values.

        Returns
        -------
        str
            String representation of the NMLInflows object.
        """
        params = [
            (f"   num_inflows = {self.num_inflows}", self.num_inflows),
            (
                f"   names_of_strms = {', '.join([repr(var) for var in self.names_of_strms]) if self.names_of_strms else None}",
                self.names_of_strms,
            ),
            (
                f"   subm_flag = {', '.join([str(num) for num in self.subm_flag]) if self.subm_flag else None}",
                self.subm_flag,
            ),
            (
                f"   strm_hf_angle = {', '.join([str(num) for num in self.strm_hf_angle]) if self.strm_hf_angle else None}",
                self.strm_hf_angle,
            ),
            (
                f"   strmbd_slope = {', '.join([str(num) for num in self.strmbd_slope]) if self.strmbd_slope else None}",
                self.strmbd_slope,
            ),
            (
                f"   strmbd_drag = {', '.join([str(num) for num in self.strmbd_drag]) if self.strmbd_drag else None}",
                self.strmbd_drag,
            ),
            (
                f"   inflow_factor = {', '.join([str(num) for num in self.inflow_factor]) if self.inflow_factor else None}",
                self.inflow_factor,
            ),
            (
                f"   inflow_fl = {', '.join([repr(num) for num in self.inflow_fl]) if self.inflow_fl else None}",
                self.inflow_fl,
            ),
            (f"   inflow_varnum = {self.inflow_varnum}", self.inflow_varnum),
            (
                f"   inflow_vars = {', '.join([repr(var) for var in self.inflow_vars]) if self.inflow_vars else None}",
                self.inflow_vars,
            ),
            (
                f"   coef_inf_entrain = {self.coef_inf_entrain}",
                self.coef_inf_entrain,
            ),
            (f"   time_fmt = '{self.time_fmt}'", self.time_fmt),
        ]
        return "\n".join(
            param_str
            for param_str, param_val in params
            if param_val is not None
        )


class NMLOutflows(NMLBase):
    """Define the outflows block of a GLM simulation configuration.

    Used to configure the number/type of outflows and outflow files. Attributes
    are set using the `set_attributes()` method and returned as a formatted
    string using the `__str__()` method.

    Attributes
    ----------
    num_outlet : int
        Number of outflows (including withdrawals, outlets or offtakes) to be
        included in this simulation.
    flt_off_sw : str
        Switch to indicate if the outflows are floating offtakes
        (taking water from near the surface).
    outlet_type : int
        Switch to configure approach of each withdrawal.
    outl_elvs : float
        Outlet elevations (m)
    bsn_len_outl : float
        Basin length at the outlet height(s) (m)
    bsn_wid_outl : float
        Basin width at the outlet heights (m)
    outflow_fl : str
        Filename of the file containing the outflow time-series.
    outflow_factor : float
        Scaling factor used as a multiplier for outflows.
    outflow_thick_limit : float
        Maximum vertical limit of withdrawal entrainment.
    seepage : str
        Switch to enable the seepage of water from the lake bottom.
    seepage_rate : float
        Seepage rate of water, or, soil hydraulic conductivity

    Examples
    --------
    >>> from glmpy import NMLOutflows
    >>> outflows = NMLOutflows()
    >>> print(outflows)
    """

    def __init__(self):
        self.num_outlet = None
        self.flt_off_sw = None
        self.outlet_type = None
        self.outl_elvs = None
        self.bsn_len_outl = None
        self.bsn_wid_outl = None
        self.outflow_fl = None
        self.outflow_factor = None
        self.outflow_thick_limit = None
        self.seepage = None
        self.seepage_rate = None

        print(getattr(self, key))

    def __str__(self):
        """Return the string representation of the NMLOutflows object.

        Returns a formatted string of the NMLOutflows configution options
        and values.

        Returns
        -------
        str
            String representation of the NMLOutflows object.
        """
        params = [
            (f"   num_outlet = {self.num_outlet}", self.num_outlet),
            (f"   flt_off_sw = {self.flt_off_sw}", self.flt_off_sw),
            (f"   outlet_type = {self.outlet_type}", self.outlet_type),
            (f"   outl_elvs = {self.outl_elvs}", self.outl_elvs),
            (f"   bsn_len_outl = {self.bsn_len_outl}", self.bsn_len_outl),
            (f"   bsn_wid_outl = {self.bsn_wid_outl}", self.bsn_wid_outl),
            (f"   outflow_fl = '{self.outflow_fl}'", self.outflow_fl),
            (
                f"   outflow_factor = {self.outflow_factor}",
                self.outflow_factor,
            ),
            (
                f"   outflow_thick_limit = {self.outflow_thick_limit}",
                self.outflow_thick_limit,
            ),
            (f"   seepage = {self.seepage}", self.seepage),
            (f"   seepage_rate = {self.seepage_rate}", self.seepage_rate),
        ]
        return "\n".join(
            param_str
            for param_str, param_val in params
            if param_val is not None
        )


class NMLSediment(NMLBase):
    """Define the sediment block of a GLM simulation configuration.

    Used to configure the sediment thermal properties. Attributes are set using
    the `set_attributes()` method and returned as a formatted string using the
    `__str__()` method.

    Attributes
    ----------
    sed_heat_Ksoil : float
        Heat conductivity of soil/sediment.
    sed_temp_depth : float
        Depth of soil/sediment layer below the lake bottom, used for heat flux
        calculation.
    benthic_mode : int
        Switch to configure which mode of benthic interaction to apply.
    n_zones : int
        Number of sediment zones to simulate.
    zone_heights : float
        Upper height of zone boundary.
    sed_temp_mean : float
        Annual mean sediment temperature.
    sed_temp_amplitude : float
        Amplitude of temperature variation experienced in the sediment over one
        year.
    sed_temp_peak_doy : int
        Day of the year where the sediment temperature peaks.
    sed_reflectivity : float
        Sediment reflectivity.
    sed_roughness : float
        Sediment roughness.

    Examples
    --------
    >>> from glmpy import NMLSediment
    >>> sediment = NMLSediment()
    >>> print(sediment)
    """

    def __init__(self):
        self.sed_heat_Ksoil = None
        self.sed_temp_depth = None
        self.benthic_mode = None
        self.n_zones = None
        self.zone_heights = None
        self.sed_temp_mean = None
        self.sed_temp_amplitude = None
        self.sed_temp_peak_doy = None
        self.sed_reflectivity = None
        self.sed_roughness = None
        print(getattr(self, key))

    def __str__(self):
        """Return the string representation of the NMLSediment object.

        Returns a formatted string of the NMLSediment configution options
        and values.

        Returns
        -------
        str
            String representation of the NMLSediment object.
        """
        params = [
            (
                f"   sed_heat_Ksoil = {self.sed_heat_Ksoil}",
                self.sed_heat_Ksoil,
            ),
            (
                f"   sed_temp_depth = {self.sed_temp_depth}",
                self.sed_temp_depth,
            ),
            (f"   benthic_mode = {self.benthic_mode}", self.benthic_mode),
            (f"   n_zones = {self.n_zones}", self.n_zones),
            (
                f"   zone_heights = {', '.join([str(num) for num in self.zone_heights]) if self.zone_heights else None}",
                self.zone_heights,
            ),
            (
                f"   sed_temp_mean = {', '.join([str(num) for num in self.sed_temp_mean]) if self.sed_temp_mean else None}",
                self.sed_temp_mean,
            ),
            (
                f"   sed_temp_amplitude = {', '.join([str(num) for num in self.sed_temp_amplitude]) if self.sed_temp_amplitude else None}",
                self.sed_temp_amplitude,
            ),
            (
                f"   sed_temp_peak_doy = {', '.join([str(num) for num in self.sed_temp_peak_doy]) if self.sed_temp_peak_doy else None}",
                self.sed_temp_peak_doy,
            ),
            (
                f"   sed_reflectivity = {', '.join([str(num) for num in self.sed_reflectivity]) if self.sed_reflectivity else None}",
                self.sed_reflectivity,
            ),
            (
                f"   sed_roughness = {', '.join([str(num) for num in self.sed_roughness]) if self.sed_roughness else None}",
                self.sed_roughness,
            ),
        ]
        return "\n".join(
            param_str
            for param_str, param_val in params
            if param_val is not None
        )


class NMLIceSnow(NMLBase):
    """Define the ice/snow block of a GLM simulation configuration.

    Used to configure the surface energy balance options, and  local run-off
    parameters. Attributes are set using the `set_attributes()` method and
    returned as a formatted string using the `__str__()` method.

    Attributes
    ----------
    snow_albedo_factor : float
        Scaling factor used to as a multiplier to scale the snow/ice albedo
        estimate.
    snow_rho_max : float
        Minimum snow density allowable.
    snow_rho_min : float
        Maximum snow density allowable.

    Examples
    --------
    >>> from glmpy import NMLIceSnow
    >>> ice_snow = NMLIceSnow()
    >>> print(ice_snow)
    """

    def __init__(self):
        self.snow_albedo_factor = None
        self.snow_rho_max = (None,)
        self.snow_rho_min = None
        print(getattr(self, key))

    def __str__(self):
        """Return the string representation of the NMLIceSnow object.

        Returns a formatted string of the NMLIceSnow configution options
        and values.

        Returns
        -------
        str
            String representation of the NMLIceSnow object.
        """
        params = [
            (
                f"   snow_albedo_factor = {self.snow_albedo_factor}",
                self.snow_albedo_factor,
            ),
            (f"   snow_rho_max = {self.snow_rho_max}", self.snow_rho_max),
            (f"   snow_rho_min = {self.snow_rho_min}", self.snow_rho_min),
        ]
        return "\n".join(
            param_str
            for param_str, param_val in params
            if param_val is not None
        )


class NMLWQSetup(NMLBase):
    """Define the water quality setup block of a GLM simulation configuration.

    Used to configure the water quality library selection, solution options,
    and  benthic coupling mode. Attributes are set using the `set_attributes()`
    method and returned as a formatted string using the `__str__()` method.

    Attributes
    ----------
    wq_lib : str
        Water quality model selection.
    wq_nml_file : str
        Filename of WQ configuration file.
    ode_method : int
        Method to use for ODE solution of water quality module.
    split_factor : float
        Factor weighting implicit vs explicit numerical solution of the WQ
        model.
    bioshade_feedback : string
        Switch to enable Kw to be updated by the WQ model.
    repair_state : string
        Switch to correct negative or out of range WQ variables.
    mobility_off : string
        Switch to enable settling within the WQ model.

    Examples
    --------
    >>> from glmpy import NMLWQSetup
    >>> wq_setup = NMLWQSetup()
    >>> print(wq_setup)
    """

    def __init__(self):
        self.wq_lib = None
        self.wq_nml_file = None
        self.wq_lib = None
        self.wq_nml_file = None
        self.ode_method = None
        self.split_factor = None
        self.bioshade_feedback = None
        self.repair_state = None
        self.mobility_off = None

        print(getattr(self, key))

    def __str__(self):
        """Return the string representation of the NMLWQSetup object.

        Returns a formatted string of the NMLWQSetup configution options
        and values.

        Returns
        -------
        str
            String representation of the NMLWQSetup object.
        """
        params = [
            (f"   wq_lib = '{self.wq_lib}'", self.wq_lib),
            (f"   wq_nml_file = '{self.wq_nml_file}'", self.wq_nml_file),
            (f"   ode_method = {self.ode_method}", self.ode_method),
            (f"   split_factor = {self.split_factor}", self.split_factor),
            (
                f"   bioshade_feedback = {self.bioshade_feedback}",
                self.bioshade_feedback,
            ),
            (f"   repair_state = {self.repair_state}", self.repair_state),
            (f"   mobility_off = {self.mobility_off}", self.mobility_off),
        ]
        return "\n".join(
            param_str
            for param_str, param_val in params
            if param_val is not None
        )

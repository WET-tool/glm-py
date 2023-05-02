from typing import Union


class NML:
    """ Generate .nml files  

    .nml files store config information required for running a simulation with the General Lake Model (GLM). 
    Instances of this class store values that can be written to .nml files and have methods to write .nml files.

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
        wq_setup: Union[str, None]
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
        """ Write a .nml file

        Writes a .nml file to the file path specified in `nml_file_path`. 
        The .nml file stores config for a GLM simulation.

        Parameters
        ----------
        nml_file_path : str, optional
            file path to save .nml file, by default "sim.nml"

        Examples
        --------
        """

        def nml_block(block_name, block):
            return f"&{block_name}\n{block}\n/\n"

        def nml_output():
            blocks = [
                (nml_block("glm_setup", self.setup), self.setup),
                (nml_block("mixing", self.mixing), self.mixing),
                (nml_block("morphometry", self.morphometry), self.morphometry),
                (nml_block("time", self.time), self.time),
                (nml_block("output", self.output), self.output),
                (nml_block("init_profiles", self.init_profiles), self.init_profiles),
                (nml_block("meteorology", self.meteorology), self.meteorology),
                (nml_block("light", self.light), self.light),
                (nml_block("bird_model", self.bird_model), self.bird_model),
                (nml_block("inflows", self.inflows), self.inflows),
                (nml_block("outflows", self.outflows), self.outflows),
                (nml_block("sediment", self.sediment), self.sediment),
                (nml_block("ice_snow", self.ice_snow), self.ice_snow),
                (nml_block("wq_setup", self.wq_setup), self.wq_setup)
            ]
            return "".join(block_str for block_str, block_val in blocks if block_val is not None)

        with open(file=nml_file_path, mode='w') as file:
            file.write(nml_output())


class NMLSetup:

    """ Class for the configuring the &glm_setup component of a .nml file

    Attributes
    ----------
    sim_name : str
        Name of the simulation
    max_layers : int
        Maximum number of layers, default 500
    min_layer_vol : float
        Minimum layer volume
    min_layer_thick : float
        Minimum thickness of a layer (m)
    max_layer_thick : float
        Maximum thickness of a layer (m)
    density_model : int
        Switch to set the density equation, default 1

    Methods
    -------
    set_attributes(attrs_dict)
        Sets the attributes of the class to the values in the attrs_dict dictionary
    get_attributes(key)
        Prints the value of the attribute specified by the key
    __str__()
        Returns a string representation of the class attributes
    """

    def __init__(self):
        self.sim_name = None
        self.max_layers = 500
        self.min_layer_vol = None
        self.min_layer_thick = None
        self.max_layer_thick = None
        self.density_model = 1

    def set_attributes(self, attrs_dict, custom: dict):
        if custom is not None:
            attrs_dict.update(custom)
        for key, value in attrs_dict.items():
            setattr(self, key, value)

    def get_attributes(self, key):
        print(getattr(self, key))

    def __str__(self):
        params = [
            (f"   sim_name = '{self.sim_name}'", self.sim_name),
            (f"   max_layers = {self.max_layers}", self.max_layers),
            (f"   min_layer_vol = {self.min_layer_vol}", self.min_layer_vol),
            (f"   min_layer_thick = {self.min_layer_thick}",
             self.min_layer_thick),
            (f"   max_layer_thick = {self.max_layer_thick}",
             self.max_layer_thick),
            (f"   density_model = {self.density_model}", self.density_model),
        ]
        return "\n".join(param_str for param_str, param_val in params if param_val is not None)


class NMLMorphometry:

    """ Class for the configuring the &morphometry component of a .nml file

    Attributes
    ----------
    lake_name : str
        Site name
    latitude : float
        Latitude, positive North
    longitude : float
        Longitude, positive East
    crest_elev : float
        Elevation of the bottom-most point of the lake (m above datum)
    bsn_len : float
        Length of the lake basin, at crest height (m)
    bsn_wid : float
        Width of the lake basin, at crest height (m)
    bsn_vals : float
        Number of points being provided to described the hyposgraphic details
    H : list
        Comma-separated list of lake elevations (m above datum)
    A : list
        Comma-separated list of lake areas (m^2)

    Methods
    -------
    set_attributes(attrs_dict)
        Sets the attributes of the class to the values in the attrs_dict dictionary
    get_attributes(key)
        Prints the value of the attribute specified by the key
    __str__()
        Returns a string representation of the class attributes
    """

    def __init__(self):
        self.lake_name = None
        self.latitude = None
        self.longitude = None
        self.crest_elev = None
        self.bsn_len = None
        self.bsn_wid = None
        self.bsn_vals = None
        self.H = None
        self.A = None

    def set_attributes(self, attrs_dict, custom: dict):
        if custom is not None:
            attrs_dict.update(custom)
        for key, value in attrs_dict.items():
            setattr(self, key, value)

    def get_attributes(self, key):
        print(getattr(self, key))

    def __str__(self):
        params = [
            (f"   lake_name = '{self.lake_name}'", self.lake_name),
            (f"   latitude = {self.latitude}", self.latitude),
            (f"   longitude = {self.longitude}", self.longitude),
            (f"   crest_elev = {self.crest_elev}", self.crest_elev),
            (f"   bsn_len = {self.bsn_len}", self.bsn_len),
            (f"   bsn_wid = {self.bsn_wid}", self.bsn_wid),
            (f"   bsn_vals = {self.bsn_vals}", self.bsn_vals),
            (f"   H = {', '.join([str(num) for num in self.H]) if self.H else None}", self.H),
            (f"   A = {', '.join([str(num) for num in self.A]) if self.A else None}", self.A),
        ]
        return "\n".join(param_str for param_str, param_val in params if param_val is not None)


class NMLMixing:

    """ Class for the configuring the &mixing component of a .nml file

    Attributes
    ----------
    surface_mixing : int
        Switch to select the options of the surface mixing model
    coef_mix_conv : float
        Mixing efficiency - convective overturn
    coef_wind_stir : float
        Mixing efficiency - wind stirring
    coef_mix_shear : float
        Mixing efficiency - shear production
    coef_mix_turb : float
        Mixing efficiency - unsteady turbulence effects
    coef_mix_KH : float
        Mixing efficiency - Kelvin-Helmholtz billowing
    deep_mixing : int
        Switch to select the options of the deep (hypolimnetic) mixing model (0 = no deep mixing, 1 = constant diffusivity, 2 = weinstock model)
    coef_mix_hyp : float
        Mixing efficiency - hypolimnetic turbulence
    diff : float
        Background (molecular) diffusivity in the hypolimnion

    Methods
    -------
    set_attributes(attrs_dict)
        Sets the attributes of the class to the values in the attrs_dict dictionary
    get_attributes(key)
        Prints the value of the attribute specified by the key
    __str__()
        Returns a string representation of the class attributes
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

    def set_attributes(self, attrs_dict, custom: dict):
        if custom is not None:
            attrs_dict.update(custom)
        for key, value in attrs_dict.items():
            setattr(self, key, value)

    def get_attributes(self, key):
        print(getattr(self, key))

    def __str__(self):
        params = [
            (f"   surface_mixing = {self.surface_mixing}",
             self.surface_mixing),
            (f"   coef_mix_conv = {self.coef_mix_conv}", self.coef_mix_conv),
            (f"   coef_wind_stir = {self.coef_wind_stir}",
             self.coef_wind_stir),
            (f"   coef_mix_shear = {self.coef_mix_shear}",
             self.coef_mix_shear),
            (f"   coef_mix_turb = {self.coef_mix_turb}", self.coef_mix_turb),
            (f"   coef_mix_KH = {self.coef_mix_KH}", self.coef_mix_KH),
            (f"   deep_mixing = {self.deep_mixing}", self.deep_mixing),
            (f"   coef_mix_hyp = {self.coef_mix_hyp}", self.coef_mix_hyp),
            (f"   diff = {self.diff}", self.diff),
        ]
        return "\n".join(param_str for param_str, param_val in params if param_val is not None)


class NMLTime:
    """
    """

    def __init__(self):
        self.timefmt = None
        self.start = None
        self.stop = None
        self.dt = None
        self.num_days = None
        self.timezone = None

    def set_attributes(self, attrs_dict, custom: dict):
        if custom is not None:
            attrs_dict.update(custom)
        for key, value in attrs_dict.items():
            setattr(self, key, value)

    def get_attributes(self, key):
        print(getattr(self, key))

    def __str__(self):
        params = [
            (f"   timefmt = {self.timefmt}", self.timefmt),
            (f"   start = '{self.start}'", self.start),
            (f"   stop = '{self.stop}'", self.stop),
            (f"   dt = {self.dt}", self.dt),
            (f"   num_days = {self.num_days}", self.num_days),
            (f"   timezone = {self.timezone}", self.timezone),
        ]
        return "\n".join(param_str for param_str, param_val in params if param_val is not None)


class NMLOutput:
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

    def set_attributes(self, attrs_dict, custom: dict):
        if custom is not None:
            attrs_dict.update(custom)
        for key, value in attrs_dict.items():
            setattr(self, key, value)

    def get_attributes(self, key):
        print(getattr(self, key))

    def __str__(self):
        params = [
            (f"   out_dir = '{self.out_dir}'", self.out_dir),
            (f"   out_fn = '{self.out_fn}'", self.out_fn),
            (f"   nsave = {self.nsave}", self.nsave),
            (f"   csv_lake_fname = '{self.csv_lake_fname}'",
             self.csv_lake_fname),
            (f"   csv_point_nlevs = {self.csv_point_nlevs}",
             self.csv_point_nlevs),
            (f"   csv_point_fname = '{self.csv_point_fname}'",
             self.csv_point_fname),
            (f"   csv_point_at = {', '.join([str(num) for num in self.csv_point_at]) if self.csv_point_at else None}", self.csv_point_at),
            (f"   csv_point_nvars = {self.csv_point_nvars}",
             self.csv_point_nvars),
            (f"   csv_point_vars = {', '.join([repr(var) for var in self.csv_point_vars]) if self.csv_point_vars else None}", self.csv_point_vars),
            (f"   csv_outlet_allinone = {str(self.csv_outlet_allinone)}",
             self.csv_outlet_allinone),
            (f"   csv_outlet_fname = '{self.csv_outlet_fname}'",
             self.csv_outlet_fname),
            (f"   csv_outlet_nvars = {self.csv_outlet_nvars}",
             self.csv_outlet_nvars),
            (f"   csv_outlet_vars = {', '.join([repr(var) for var in self.csv_outlet_vars]) if self.csv_outlet_vars else None}", self.csv_outlet_vars),
            (f"   csv_ovrflw_fname = '{self.csv_ovrflw_fname}'",
             self.csv_ovrflw_fname),
        ]
        return "\n".join(param_str for param_str, param_val in params if param_val is not None)


class NMLInitProfiles:
    """"""

    def __init__(self):
        self.lake_depth = None
        self.num_depths = None
        self.the_depths = None
        self.the_temps = None
        self.the_sals = None

    def set_attributes(self, attrs_dict, custom: dict):
        if custom is not None:
            attrs_dict.update(custom)
        for key, value in attrs_dict.items():
            setattr(self, key, value)

    def get_attributes(self, key):
        print(getattr(self, key))

    def __str__(self):
        params = [
            (f"   lake_depth = {self.lake_depth}", self.lake_depth),
            (f"   num_depths = {self.num_depths}", self.num_depths),
            (f"   the_depths = {', '.join([str(num) for num in self.the_depths]) if self.the_depths else None}", self.the_depths),
            (f"   the_temps = {', '.join([str(num) for num in self.the_temps]) if self.the_temps else None}", self.the_temps),
            (f"   the_sals = {', '.join([str(num) for num in self.the_sals]) if self.the_sals else None}", self.the_sals),
        ]
        return "\n".join(param_str for param_str, param_val in params if param_val is not None)


class NMLMeteorology:
    """"""

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

    def set_attributes(self, attrs_dict, custom: dict):
        if custom is not None:
            attrs_dict.update(custom)
        for key, value in attrs_dict.items():
            setattr(self, key, value)

    def get_attributes(self, key):
        print(getattr(self, key))

    def __str__(self):
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
        return "\n".join(param_str for param_str, param_val in params if param_val is not None)


class NMLLight:
    """"""

    def __init__(self):
        self.light_mode = None
        self.Kw = None
        self.n_bands = None
        self.light_extc = None
        self.energy_frac = None
        self.Benthic_Imin = None

    def set_attributes(self, attrs_dict, custom: dict):
        if custom is not None:
            attrs_dict.update(custom)
        for key, value in attrs_dict.items():
            setattr(self, key, value)

    def get_attributes(self, key):
        print(getattr(self, key))

    def __str__(self):
        params = [
            (f"   light_mode = {self.light_mode}", self.light_mode),
            (f"   Kw = {self.Kw}", self.Kw),
            (f"   n_bands = {self.n_bands}", self.n_bands),
            (f"   light_extc = {', '.join([str(num) for num in self.light_extc]) if self.light_extc else None}", self.light_extc),
            (f"   energy_frac = {', '.join([str(num) for num in self.energy_frac]) if self.energy_frac else None}", self.energy_frac),
            (f"   Benthic_Imin = {self.Benthic_Imin}", self.Benthic_Imin),
        ]
        return "\n".join(param_str for param_str, param_val in params if param_val is not None)


class NMLBirdModel:
    """"""

    def __init__(self):
        self.AP = None
        self.Oz = None
        self.WatVap = None
        self.AOD500 = None
        self.AOD380 = None
        self.Albedo = None

    def set_attributes(self, attrs_dict, custom: dict):
        if custom is not None:
            attrs_dict.update(custom)
        for key, value in attrs_dict.items():
            setattr(self, key, value)

    def get_attributes(self, key):
        print(getattr(self, key))

    def __str__(self):
        params = [
            (f"   AP = {self.AP}", self.AP),
            (f"   Oz = {self.Oz}", self.Oz),
            (f"   WatVap = {self.WatVap}", self.WatVap),
            (f"   AOD500 = {self.AOD500}", self.AOD500),
            (f"   AOD380 = {self.AOD380}", self.AOD380),
            (f"   Albedo = {self.Albedo}", self.Albedo),
        ]
        return "\n".join(param_str for param_str, param_val in params if param_val is not None)


class NMLInflows:
    """"""

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

    def set_attributes(self, attrs_dict):
        for key, value in attrs_dict.items():
            setattr(self, key, value)

    def get_attributes(self, key):
        print(getattr(self, key))

    def __str__(self):
        params = [
            (f"   num_inflows = {self.num_inflows}", self.num_inflows),
            (f"   names_of_strms = {', '.join([repr(var) for var in self.names_of_strms]) if self.names_of_strms else None}", self.names_of_strms),
            (f"   subm_flag = {', '.join([str(num) for num in self.subm_flag]) if self.subm_flag else None}", self.subm_flag),
            (f"   strm_hf_angle = {', '.join([str(num) for num in self.strm_hf_angle]) if self.strm_hf_angle else None}", self.strm_hf_angle),
            (f"   strmbd_slope = {', '.join([str(num) for num in self.strmbd_slope]) if self.strmbd_slope else None}", self.strmbd_slope),
            (f"   strmbd_drag = {', '.join([str(num) for num in self.strmbd_drag]) if self.strmbd_drag else None}", self.strmbd_drag),
            (f"   inflow_factor = {', '.join([str(num) for num in self.inflow_factor]) if self.inflow_factor else None}", self.inflow_factor),
            (f"   inflow_fl = {', '.join([repr(num) for num in self.inflow_fl]) if self.inflow_fl else None}", self.inflow_fl),
            (f"   inflow_varnum = {self.inflow_varnum}", self.inflow_varnum),
            (f"   inflow_vars = {', '.join([repr(var) for var in self.inflow_vars]) if self.inflow_vars else None}", self.inflow_vars),
            (f"   coef_inf_entrain = {self.coef_inf_entrain}",
             self.coef_inf_entrain),
            (f"   time_fmt = '{self.time_fmt}'", self.time_fmt),
        ]
        return "\n".join(param_str for param_str, param_val in params if param_val is not None)


class NMLOutflows:
    """"""

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

    def set_attributes(self, attrs_dict):
        for key, value in attrs_dict.items():
            setattr(self, key, value)

    def get_attributes(self, key):
        print(getattr(self, key))

    def __str__(self):
        params = [
            (f"   num_outlet = {self.num_outlet}", self.num_outlet),
            (f"   flt_off_sw = {self.flt_off_sw}", self.flt_off_sw),
            (f"   outlet_type = {self.outlet_type}", self.outlet_type),
            (f"   outl_elvs = {self.outl_elvs}", self.outl_elvs),
            (f"   bsn_len_outl = {self.bsn_len_outl}", self.bsn_len_outl),
            (f"   bsn_wid_outl = {self.bsn_wid_outl}", self.bsn_wid_outl),
            (f"   outflow_fl = '{self.outflow_fl}'", self.outflow_fl),
            (f"   outflow_factor = {self.outflow_factor}",
             self.outflow_factor),
            (f"   outflow_thick_limit = {self.outflow_thick_limit}",
             self.outflow_thick_limit),
            (f"   seepage = {self.seepage}", self.seepage),
            (f"   seepage_rate = {self.seepage_rate}", self.seepage_rate),
        ]
        return "\n".join(param_str for param_str, param_val in params if param_val is not None)


class NMLSediment:
    """"""

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

    def set_attributes(self, attrs_dict):
        for key, value in attrs_dict.items():
            setattr(self, key, value)

    def get_attributes(self, key):
        print(getattr(self, key))

    def __str__(self):
        params = [
            (f"   sed_heat_Ksoil = {self.sed_heat_Ksoil}",
             self.sed_heat_Ksoil),
            (f"   sed_temp_depth = {self.sed_temp_depth}",
             self.sed_temp_depth),
            (f"   benthic_mode = {self.benthic_mode}", self.benthic_mode),
            (f"   n_zones = {self.n_zones}", self.n_zones),
            (f"   zone_heights = {', '.join([str(num) for num in self.zone_heights]) if self.zone_heights else None}", self.zone_heights),
            (f"   sed_temp_mean = {', '.join([str(num) for num in self.sed_temp_mean]) if self.sed_temp_mean else None}", self.sed_temp_mean),
            (f"   sed_temp_amplitude = {', '.join([str(num) for num in self.sed_temp_amplitude]) if self.sed_temp_amplitude else None}", self.sed_temp_amplitude),
            (f"   sed_temp_peak_doy = {', '.join([str(num) for num in self.sed_temp_peak_doy]) if self.sed_temp_peak_doy else None}", self.sed_temp_peak_doy),
            (f"   sed_reflectivity = {', '.join([str(num) for num in self.sed_reflectivity]) if self.sed_reflectivity else None}", self.sed_reflectivity),
            (f"   sed_roughness = {', '.join([str(num) for num in self.sed_roughness]) if self.sed_roughness else None}", self.sed_roughness),
        ]
        return "\n".join(param_str for param_str, param_val in params if param_val is not None)


class NMLIceSnow:
    """"""

    def __init__(self):
        self.snow_albedo_factor = None
        self.snow_rho_max = None,
        self.snow_rho_min = None

    def set_attributes(self, attrs_dict):
        for key, value in attrs_dict.items():
            setattr(self, key, value)

    def get_attributes(self, key):
        print(getattr(self, key))

    def __str__(self):
        params = [
            (f"   snow_albedo_factor = {self.snow_albedo_factor}",
             self.snow_albedo_factor),
            (f"   snow_rho_max = {self.snow_rho_max}", self.snow_rho_max),
            (f"   snow_rho_min = {self.snow_rho_min}", self.snow_rho_min)
        ]
        return "\n".join(param_str for param_str, param_val in params if param_val is not None)


class NMLWQSetup:
    """"""

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

    def set_attributes(self, attrs_dict):
        for key, value in attrs_dict.items():
            setattr(self, key, value)

    def get_attributes(self, key):
        print(getattr(self, key))

    def __str__(self):
        params = [
            (f"   wq_lib = '{self.wq_lib}'", self.wq_lib),
            (f"   wq_nml_file = '{self.wq_nml_file}'", self.wq_nml_file),
            (f"   ode_method = {self.ode_method}", self.ode_method),
            (f"   split_factor = {self.split_factor}", self.split_factor),
            (f"   bioshade_feedback = {self.bioshade_feedback}",
             self.bioshade_feedback),
            (f"   repair_state = {self.repair_state}", self.repair_state),
            (f"   mobility_off = {self.mobility_off}", self.mobility_off)
        ]
        return "\n".join(param_str for param_str, param_val in params if param_val is not None)

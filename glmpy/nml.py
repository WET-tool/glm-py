from typing import Union, List, Any, Callable

class NML:
    """Generate .nml files.

    The `.nml` file contains the model parameters needed to run the General Lake Model (GLM). 
    """
    def __init__(
        self,
        glm_setup: dict,
        morphometry: dict,
        time: dict,
        init_profiles: dict,
        mixing: Union[dict, None] = None,
        output: Union[dict, None] = None,
        meteorology: Union[dict, None] = None,
        light: Union[dict, None] = None,
        bird_model: Union[dict, None] = None,
        inflow: Union[dict, None] = None,
        outflow: Union[dict, None] = None,
        sediment: Union[dict, None] = None,
        snow_ice: Union[dict, None] = None,
        wq_setup: Union[dict, None] = None,  
        error_checking: bool = True      
    ):
        self.glm_setup = glm_setup
        self.mixing = mixing
        self.morphometry = morphometry
        self.time = time
        self.output = output
        self.init_profiles = init_profiles
        self.meteorology = meteorology
        self.light = light
        self.bird_model = bird_model
        self.inflow = inflow
        self.outflow = outflow
        self.sediment = sediment
        self.snow_ice = snow_ice
        self.wq_setup = wq_setup

        if error_checking:
            pass

    def write_nml(self, nml_file_path: str = "glm3.nml"):
        
        nml_string = ""

        if self.glm_setup is not None:
            nml_string += self._write_nml_glm_setup(self.glm_setup) + "\n"
        if self.mixing is not None:
            nml_string += self._write_nml_mixing(self.mixing) + "\n"
        if self.wq_setup is not None:
            nml_string += self._write_nml_wq_setup(self.wq_setup) + "\n"
        if self.morphometry is not None:
            nml_string += self._write_nml_morphometry(self.morphometry) + "\n"
        if self.time is not None:
            nml_string += self._write_nml_time(self.time) + "\n"
        if self.output is not None:
            nml_string += self._write_nml_output(self.output) + "\n"
        if self.init_profiles is not None:
            nml_string += self._write_nml_init_profiles(
                self.init_profiles
            ) + "\n"
        if self.light is not None:
            nml_string += self._write_nml_light(self.light) + "\n"
        if self.bird_model is not None:
            nml_string += self._write_nml_bird_model(self.bird_model) + "\n"
        if self.sediment is not None:
            nml_string += self._write_nml_sediment(self.sediment) + "\n"
        if self.snow_ice is not None:
            nml_string += self._write_nml_snow_ice(self.snow_ice) + "\n"
        if self.meteorology is not None:
            nml_string += self._write_nml_meteorology(self.meteorology) + "\n"
        if self.inflow is not None:
            nml_string += self._write_nml_inflow(self.inflow) + "\n"
        if self.outflow is not None:
            nml_string += self._write_nml_outflow(self.outflow) + "\n"
        
        with open(file=nml_file_path, mode="w") as file:
            file.write(nml_string)

    @staticmethod
    def _nml_bool(python_bool: bool) -> str:
        """Python boolean to Fortran boolean.

        Convert a Python boolean to a string representation of a Fortran 
        boolean. For internal `nml.NML` use in generating `.nml` files.

        Parameters
        ----------
        python_bool : bool
            A Python boolean
        """
        if python_bool is True:
            return '.true.'
        else:
            return '.false.'

    @staticmethod    
    def _nml_str(python_str: str) -> str:
        """Python string to Fortran string.

        Convert a Python string to a Fortran string by adding inverted commas.
        For internal `nml.NML` use in generating `.nml` files.

        Parameters
        ----------
        python_str : str
            A Python string
        """
        return f"'{python_str}'"

    @staticmethod
    def _nml_list(
            python_list: List[Any], 
            syntax_func: Union[Callable, None] = None
        ) -> str:
        if len(python_list) == 1:
            if syntax_func is not None:
                return syntax_func(python_list[0])
            else:
                return str(python_list[0])
        else:
            if syntax_func is not None:
                return ','.join(syntax_func(val) for val in python_list)
            else:
                return ','.join(str(val) for val in python_list)


    def _nml_list_wrapper(
        self,
        python_list: List[Any], 
        func: Union[Callable, None] = None
    ) -> str:
        """A wrapper function to process lists with a given nml syntax 
        conversion function.
        """
        return self._nml_list(python_list, syntax_func=func)

    @staticmethod
    def _nml_param_val(
        block: dict, 
        param:str, 
        syntax_func: Union[Callable, None] = None
    ) -> str:
        if block[param] is not None:
            if syntax_func is not None:
                return f"   {param} = {syntax_func(block[param])}\n"
            else:
                return f"   {param} = {block[param]}\n"
        else:
            return ""
    
    def _write_nml_glm_setup(self, glm_setup: dict) -> str:
        glm_setup_str = (
            "&glm_setup\n" +
            self._nml_param_val(glm_setup, "sim_name", self._nml_str) +
            self._nml_param_val(glm_setup, "max_layers") +
            self._nml_param_val(glm_setup, "min_layer_vol") +
            self._nml_param_val(glm_setup, "min_layer_thick") +
            self._nml_param_val(glm_setup, "max_layer_thick") +
            self._nml_param_val(glm_setup, "density_model") +
            self._nml_param_val(glm_setup, "non_avg", self._nml_bool) +
            "/"
        )

        return glm_setup_str
    
    def _write_nml_mixing(self, mixing: dict) -> str:
        mixing_str = (
            "&mixing\n" +
            self._nml_param_val(mixing, "surface_mixing") +
            self._nml_param_val(mixing, "coef_mix_conv") +
            self._nml_param_val(mixing, "coef_wind_stir") +
            self._nml_param_val(mixing, "coef_mix_shear") +
            self._nml_param_val(mixing, "coef_mix_turb") +
            self._nml_param_val(mixing, "coef_mix_KH") +
            self._nml_param_val(mixing, "deep_mixing") +
            self._nml_param_val(mixing, "coef_mix_hyp") +
            self._nml_param_val(mixing, "diff") +
            "/"
        )

        return mixing_str

    def _write_nml_wq_setup(self, wq_setup: dict) -> str:
        wq_setup_str = (
            "&wq_setup\n" +
            self._nml_param_val(wq_setup, "wq_lib", self._nml_str) +
            self._nml_param_val(wq_setup, "wq_nml_file", self._nml_str) +
            self._nml_param_val(
                wq_setup, "bioshade_feedback", self._nml_bool
            ) +
            self._nml_param_val(wq_setup, "mobility_off", self._nml_bool)+
            self._nml_param_val(wq_setup, "ode_method") +
            self._nml_param_val(wq_setup, "split_factor") +
            self._nml_param_val(wq_setup, "repair_state", self._nml_bool) +
            "/"
        )

        return wq_setup_str
    
    def _write_nml_morphometry(self, morphometry: dict) -> str:
        morphometry_str = (
            "&morphometry\n" +
            self._nml_param_val(morphometry, "lake_name", self._nml_str) +
            self._nml_param_val(morphometry, "latitude") +
            self._nml_param_val(morphometry, "longitude") +
            self._nml_param_val(morphometry, "base_elev") +
            self._nml_param_val(morphometry, "crest_elev") +
            self._nml_param_val(morphometry, "bsn_len") +
            self._nml_param_val(morphometry, "bsn_wid") +
            self._nml_param_val(morphometry, "bsn_vals") +
            self._nml_param_val(
                morphometry, "H", lambda x: self._nml_list_wrapper(x)
            ) +
            self._nml_param_val(
                morphometry, "A", lambda x: self._nml_list_wrapper(x)
            ) +
            "/"
        )

        return morphometry_str

    def _write_nml_time(self, time: dict) -> str:
        time_str = (
            "&time\n" +
            self._nml_param_val(time, "timefmt") +
            self._nml_param_val(time, "start", self._nml_str) +
            self._nml_param_val(time, "stop", self._nml_str) +
            self._nml_param_val(time, "dt") +
            self._nml_param_val(time, "num_days") +
            self._nml_param_val(time, "timezone") +
            "/"
        )

        return time_str

    def _write_nml_output(self, output: dict) -> str:
        output_str = (
            "&output\n" +
            self._nml_param_val(output, "out_dir", self._nml_str) +
            self._nml_param_val(output, "out_fn", self._nml_str) +
            self._nml_param_val(output, "nsave") +
            self._nml_param_val(output, "csv_lake_fname", self._nml_str) +
            self._nml_param_val(output, "csv_point_nlevs") +
            self._nml_param_val(output, "csv_point_fname", self._nml_str) +
            self._nml_param_val(
                output, 
                "csv_point_frombot", 
                lambda x: self._nml_list_wrapper(x)
            ) +
            self._nml_param_val(
                output, "csv_point_at",lambda x: self._nml_list_wrapper(x)
            ) +
            self._nml_param_val(output, "csv_point_nvars") +
            self._nml_param_val(
                output, 
                "csv_point_vars", 
                lambda x: self._nml_list_wrapper(x, self._nml_str)
            ) +
            self._nml_param_val(
                output, "csv_outlet_allinone", self._nml_bool
            ) +
            self._nml_param_val(output, "csv_outlet_fname", self._nml_str) +
            self._nml_param_val(output, "csv_outlet_nvars") +
            self._nml_param_val(
                output, 
                "csv_outlet_vars", 
                lambda x: self._nml_list_wrapper(x, self._nml_str)
            ) +
            self._nml_param_val(output, "csv_ovrflw_fname", self._nml_str) +
            "/"
        )

        return output_str

    def _write_nml_init_profiles(self, init_profiles: dict) -> str:
        init_profiles_str = (
            "&init_profiles\n" +
            self._nml_param_val(init_profiles, "lake_depth") +
            self._nml_param_val(init_profiles, "num_depths") +
            self._nml_param_val(
                init_profiles, 
                "the_depths", 
                lambda x: self._nml_list_wrapper(x)
            ) +
            self._nml_param_val(
                init_profiles, "the_temps", lambda x: self._nml_list_wrapper(x)
            ) +
            self._nml_param_val(
                init_profiles, 
                "the_sals", 
                lambda x: self._nml_list_wrapper(x)
            ) +
            self._nml_param_val(init_profiles, "num_wq_vars") +
            self._nml_param_val(
                init_profiles, 
                "wq_names", 
                lambda x: self._nml_list_wrapper(x, self._nml_str)
            ) +
            self._nml_param_val(
                init_profiles, 
                "wq_init_vals", 
                lambda x: self._nml_list_wrapper(x)
            ) +
            "/"
        )

        return init_profiles_str

    def _write_nml_light(self, light: dict) -> str:
        light_str = (
            "&light\n" +
            self._nml_param_val(light, "light_mode") +
            self._nml_param_val(light, "Kw") +
            self._nml_param_val(light, "Kw_file", self._nml_str) +
            self._nml_param_val(light, "n_bands") +
            self._nml_param_val(
                light, "light_extc", lambda x: self._nml_list_wrapper(x)
            ) +
            self._nml_param_val(
                light, "energy_frac", lambda x: self._nml_list_wrapper(x)
            ) +
            self._nml_param_val(light, "Benthic_Imin") +
            "/"
        )

        return light_str
    
    def _write_nml_bird_model(self, bird_model: dict) -> str:
        bird_model_str = (
            "&bird_model\n" +
            self._nml_param_val(bird_model, "AP") +
            self._nml_param_val(bird_model, "Oz") +
            self._nml_param_val(bird_model, "WatVap") +
            self._nml_param_val(bird_model, "AOD500") +
            self._nml_param_val(bird_model, "AOD380") +
            self._nml_param_val(bird_model, "Albedo") +
            "/"
        )

        return bird_model_str    
    
    def _write_nml_sediment(self, sediment: dict) -> str:
        sediment_str = (
            "&sediment\n" +
            self._nml_param_val(sediment, "sed_heat_Ksoil") +
            self._nml_param_val(sediment, "sed_temp_depth") +
            self._nml_param_val(
                sediment, "sed_temp_mean", lambda x: self._nml_list_wrapper(x)
            ) +
            self._nml_param_val(
                sediment, 
                "sed_temp_amplitude", 
                lambda x: self._nml_list_wrapper(x)
            ) +
            self._nml_param_val(
                sediment, 
                "sed_temp_peak_doy", 
                lambda x: self._nml_list_wrapper(x)
            ) +
            self._nml_param_val(sediment, "benthic_mode") +
            self._nml_param_val(sediment, "n_zones") +
            self._nml_param_val(
                sediment, 
                "zone_heights", 
                lambda x: self._nml_list_wrapper(x)
            ) +
            self._nml_param_val(
                sediment, 
                "sed_reflectivity", 
                lambda x: self._nml_list_wrapper(x)
            ) +
            self._nml_param_val(
                sediment, 
                "sed_roughness", 
                lambda x: self._nml_list_wrapper(x)
            ) +            
            "/"
        )

        return sediment_str

    def _write_nml_snow_ice(self, snow_ice: dict) -> str:
        snow_ice_str = (
            "&snowice\n" +
            self._nml_param_val(snow_ice, "snow_albedo_factor") +
            self._nml_param_val(snow_ice, "snow_rho_min") +
            self._nml_param_val(snow_ice, "snow_rho_max") +
            "/"
        )

        return snow_ice_str

    def _write_nml_meteorology(self, meteorology: dict) -> str:
        meteorology_str = (
            "&meteorology\n" +
            self._nml_param_val(meteorology, "met_sw", self._nml_bool) +
            self._nml_param_val(meteorology, "meteo_fl", self._nml_str) +
            self._nml_param_val(meteorology, "subdaily", self._nml_bool) +
            self._nml_param_val(meteorology, "time_fmt", self._nml_str) +
            self._nml_param_val(meteorology, "rad_mode") +
            self._nml_param_val(meteorology, "albedo_mode") +
            self._nml_param_val(meteorology, "sw_factor") +
            self._nml_param_val(meteorology, "lw_type", self._nml_str) +
            self._nml_param_val(meteorology, "cloud_mode") +
            self._nml_param_val(meteorology, "lw_factor") +
            self._nml_param_val(meteorology, "atm_stab") +
            self._nml_param_val(meteorology, "rh_factor") +
            self._nml_param_val(meteorology, "at_factor") +
            self._nml_param_val(meteorology, "ce") +
            self._nml_param_val(meteorology, "ch") +
            self._nml_param_val(meteorology, "rain_sw", self._nml_bool) +
            self._nml_param_val(meteorology, "rain_factor") +
            self._nml_param_val(meteorology, "catchrain", self._nml_bool) +
            self._nml_param_val(meteorology, "rain_threshold") +
            self._nml_param_val(meteorology, "runoff_coef") +
            self._nml_param_val(meteorology, "cd") +
            self._nml_param_val(meteorology, "wind_factor") +
            self._nml_param_val(meteorology, "fetch_mode") +
            self._nml_param_val(meteorology, "Aws") +
            self._nml_param_val(meteorology, "Xws") +
            self._nml_param_val(meteorology, "num_dir") +
            self._nml_param_val(meteorology, "wind_dir") +
            self._nml_param_val(meteorology, "fetch_scale") +
            "/"
        )

        return meteorology_str

    def _write_nml_inflow(self, inflow: dict) -> str:
        inflow_str = (
            "&inflow\n" +
            self._nml_param_val(inflow, "num_inflows") +
            self._nml_param_val(
                inflow, 
                "names_of_strms", 
                lambda x: self._nml_list_wrapper(x, self._nml_str)
            ) +
            self._nml_param_val(
                inflow, 
                "subm_flag", 
                lambda x: self._nml_list_wrapper(x, self._nml_bool)
            ) +
            self._nml_param_val(
                inflow, "strm_hf_angle", lambda x: self._nml_list_wrapper(x)
            ) +
            self._nml_param_val(
                inflow, "strmbd_slope", lambda x: self._nml_list_wrapper(x)
            ) +
            self._nml_param_val(
                inflow, "strmbd_drag", lambda x: self._nml_list_wrapper(x)
            ) +
            self._nml_param_val(
                inflow, "coef_inf_entrain", lambda x: self._nml_list_wrapper(x)
            ) +
            self._nml_param_val(
                inflow, "inflow_factor", lambda x: self._nml_list_wrapper(x)
            ) +
            self._nml_param_val(
                inflow, 
                "inflow_fl", 
                lambda x: self._nml_list_wrapper(x, self._nml_str)
            ) +
            self._nml_param_val(inflow, "inflow_varnum") +
            self._nml_param_val(
                inflow, 
                "inflow_vars", 
                lambda x: self._nml_list_wrapper(x, self._nml_str)
            ) +
            self._nml_param_val(inflow, "time_fmt", self._nml_str) +
            "/"
        )

        return inflow_str

    def _write_nml_outflow(self, outflow: dict) -> str:
        outflow_str = (
            "&outflow\n" +
            self._nml_param_val(outflow, "num_outlet")+
            self._nml_param_val(outflow, "outflow_fl", self._nml_str) +
            self._nml_param_val(outflow, "time_fmt", self._nml_str) +
            self._nml_param_val(
                outflow, "outflow_factor", lambda x: self._nml_list_wrapper(x)
            ) +
            self._nml_param_val(
                outflow, 
                "outflow_thick_limit", 
                lambda x: self._nml_list_wrapper(x)
            ) +
            self._nml_param_val(
                outflow, 
                "single_layer_draw", 
                lambda x: self._nml_list_wrapper(x, self._nml_bool)
            ) +
            self._nml_param_val(
                outflow, 
                "flt_off_sw", 
                lambda x: self._nml_list_wrapper(x, self._nml_bool)
            ) +
            self._nml_param_val(
                outflow, "outlet_type", lambda x: self._nml_list_wrapper(x)
            ) +
            self._nml_param_val(
                outflow, "outl_elvs", lambda x: self._nml_list_wrapper(x)
            ) +
            self._nml_param_val(
                outflow, "bsn_len_outl", lambda x: self._nml_list_wrapper(x)
            ) +
            self._nml_param_val(
                outflow, "bsn_wid_outl", lambda x: self._nml_list_wrapper(x)
            ) +
            self._nml_param_val(outflow, "crit_O2") +
            self._nml_param_val(outflow, "crit_O2_dep") +
            self._nml_param_val(outflow, "crit_O2_days") +
            self._nml_param_val(outflow, "outlet_crit") +
            self._nml_param_val(outflow, "O2name", self._nml_str) +
            self._nml_param_val(outflow, "O2idx", self._nml_str) +
            self._nml_param_val(outflow, "target_temp") +
            self._nml_param_val(outflow, "min_lake_temp") +
            self._nml_param_val(outflow, "fac_range_upper") +
            self._nml_param_val(outflow, "fac_range_lower") +
            self._nml_param_val(outflow, "mix_withdraw", self._nml_bool) +
            self._nml_param_val(outflow, "coupl_oxy_sw", self._nml_bool) +
            self._nml_param_val(outflow, "withdrTemp_fl", self._nml_str) +
            self._nml_param_val(outflow, "seepage", self._nml_bool) +
            self._nml_param_val(outflow, "seepage_rate") +
            self._nml_param_val(outflow, "crest_width") +
            self._nml_param_val(outflow, "crest_factor") +
            "/"
        )

        return outflow_str

class NMLBase:
    def set_attributes(self, attrs_dict: dict):
        for key, value in attrs_dict.items():
            setattr(self, key, value)

    def _single_value_to_list(
            self, 
            value: Any
        ) -> List[Any]:
        """Convert a single value to a list

        Many GLM parameters expect a comma separated list of values, e.g., a 
        list of floats, a list of integers, or a list of strings. Often this
        list may only contain a single value. Consider the `csv_point_vars` 
        attribute of `NMLOutput()`. Here GLM expects a comma separated list of 
        variable names. `glmpy` needs to convert lists such as 
        `['temp', 'salt']` and `['temp']` to `"'temp', 'salt'"` and `"'temp'"`,
        respectively. When setting attributes of `NMLOutput()`, 
        `csv_point_vars='temp'` is preferrable to `csv_point_vars=['temp']`. 
        The `_single_value_to_list` method will convert the value to a python 
        list providing it is not `None`. 
        """
        if not isinstance(value, list) and value is not None:
            list_value = [value]
        else:
            list_value = value
        return list_value
 

class NMLGLMSetup(NMLBase):
    def __init__(
        self,
        sim_name: Union[str, None] = None,
        max_layers: Union[int, None] = None,
        min_layer_vol: Union[float, None] = None,
        min_layer_thick: Union[float, None] = None,
        max_layer_thick: Union[float, None] = None,
        density_model: Union[int, None] = None,
        non_avg: Union[bool, None] = None,    
    ):
        self.sim_name = sim_name
        self.max_layers = max_layers
        self.min_layer_vol = min_layer_vol
        self.min_layer_thick = min_layer_thick
        self.max_layer_thick = max_layer_thick
        self.density_model = density_model
        self.non_avg = non_avg
    
    def __call__(
        self, 
        check_errors: bool = True
    ) -> dict[str, Union[float, int, str, bool, None]]:
        if check_errors:
            pass

        glm_setup_dict = {
            "sim_name": self.sim_name,
            "max_layers": self.max_layers,
            "min_layer_vol": self.min_layer_vol,
            "min_layer_thick": self.min_layer_thick,
            "max_layer_thick": self.max_layer_thick,
            "density_model": self.density_model,
            "non_avg": self.non_avg
        }

        return glm_setup_dict

class NMLMixing(NMLBase):
    def __init__(
        self,
        surface_mixing: Union[int, None] = None,
        coef_mix_conv: Union[float, None] = None,
        coef_wind_stir: Union[float, None] = None,
        coef_mix_shear: Union[float, None] = None,
        coef_mix_turb: Union[float, None] = None,
        coef_mix_KH: Union[float, None] = None,
        deep_mixing: Union[int, None] = None,
        coef_mix_hyp: Union[float, None] = None,
        diff: Union[float, None] = None,        
    ):
        self.surface_mixing = surface_mixing
        self.coef_mix_conv = coef_mix_conv
        self.coef_wind_stir = coef_wind_stir
        self.coef_mix_shear = coef_mix_shear
        self.coef_mix_turb = coef_mix_turb
        self.coef_mix_KH = coef_mix_KH
        self.deep_mixing = deep_mixing
        self.coef_mix_hyp = coef_mix_hyp
        self.diff = diff 
    
    def __call__(
        self, 
        check_errors: bool = True
    ) -> dict[str, Union[float, int, None]]:
        if check_errors:
            pass

        mixing_dict = {
            "surface_mixing": self.surface_mixing,
            "coef_mix_conv": self.coef_mix_conv,
            "coef_wind_stir": self.coef_wind_stir,
            "coef_mix_shear": self.coef_mix_shear,
            "coef_mix_turb": self.coef_mix_turb,
            "coef_mix_KH": self.coef_mix_KH,
            "deep_mixing": self.deep_mixing,
            "coef_mix_hyp": self.coef_mix_hyp,
            "diff": self.diff
        }

        return mixing_dict

class NMLWQSetup(NMLBase):
    def __init__(
        self,
        wq_lib: Union[str, None] = None,
        wq_nml_file: Union[str, None] = None,
        bioshade_feedback: Union[bool, None] = None,
        mobility_off: Union[bool, None] = None,
        ode_method: Union[int, None] = None,
        split_factor: Union[float, None] = None,
        repair_state: Union[bool, None] = None,
    ):
        self.wq_lib = wq_lib
        self.wq_nml_file = wq_nml_file
        self.bioshade_feedback = bioshade_feedback
        self.mobility_off = mobility_off
        self.ode_method = ode_method
        self.split_factor = split_factor
        self.repair_state = repair_state

    def __call__(
        self, 
        check_errors: bool = True
    ) -> dict[str, Union[float, int, str, bool, None]]:
        if check_errors:
            pass        

        wq_setup_dict = {
            "wq_lib": self.wq_lib,
            "wq_nml_file": self.wq_nml_file,
            "bioshade_feedback": self.bioshade_feedback,
            "mobility_off": self.mobility_off,
            "ode_method": self.ode_method,
            "split_factor": self.split_factor,
            "repair_state": self.repair_state
        }

        return wq_setup_dict

class NMLMorphometry(NMLBase):
    def __init__(
        self,
        lake_name: Union[str, None] = None,
        latitude: Union[float, None] = None,
        longitude: Union[float, None] = None,
        base_elev: Union[float, None] = None,
        crest_elev: Union[float, None] = None,
        bsn_len: Union[float, None] = None,
        bsn_wid: Union[float, None] = None,
        bsn_vals: Union[float, None] = None,
        H: Union[List[float], None] = None,
        A: Union[List[float], None] = None,
    ):
        self.lake_name = lake_name
        self.latitude = latitude
        self.longitude = longitude
        self.base_elev = base_elev
        self.crest_elev = crest_elev
        self.bsn_len = bsn_len
        self.bsn_wid = bsn_wid
        self.bsn_vals = bsn_vals
        self.H = H
        self.A = A
    
    def __call__(
        self, 
        check_errors: bool = True
    ) -> dict[str, Union[float, str, List[float], None]]:
        if check_errors:
            pass

        morphometry_dict = {
            "lake_name": self.lake_name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "base_elev": self.base_elev,
            "crest_elev": self.crest_elev,
            "bsn_len": self.bsn_len,
            "bsn_wid": self.bsn_wid,
            "bsn_vals": self.bsn_vals,
            "H": self.H,
            "A": self.A
        }

        return morphometry_dict

class NMLTime(NMLBase):
    def __init__(
        self,
        timefmt: Union[int, None] = None,
        start: Union[str, None] = None,
        stop: Union[str, None] = None,
        dt: Union[float, None] = None,
        num_days: Union[int, None] = None,
        timezone: Union[float, None] = None,
    ):
        self.timefmt = timefmt
        self.start = start
        self.stop = stop
        self.dt = dt
        self.num_days = num_days
        self.timezone = timezone       
    
    def __call__(
        self, 
        check_errors: bool = True
    ) -> dict[str, Union[float, int, str, None]]:
        if check_errors:
            pass

        time_dict = {
            "timefmt": self.timefmt,
            "start": self.start,
            "stop": self.stop,
            "dt": self.dt,
            "num_days": self.num_days,
            "timezone": self.timezone
        }

        return time_dict    
    
class NMLOutput(NMLBase):
    def __init__(
        self,
        out_dir: Union[str, None] = None,
        out_fn: Union[str, None] = None,
        nsave: Union[int, None] = None,
        csv_lake_fname: Union[str, None] = None,
        csv_point_nlevs: Union[float, None] = None,
        csv_point_fname: Union[str, None] = None,
        csv_point_frombot: Union[List[float], float, None] = None,
        csv_point_at: Union[List[float], float, None] = None,
        csv_point_nvars: Union[int, None] = None,
        csv_point_vars: Union[List[str], str, None] = None,
        csv_outlet_allinone: Union[bool, None] = None,
        csv_outlet_fname: Union[str, None] = None,
        csv_outlet_nvars: Union[int, None] = None,
        csv_outlet_vars: Union[List[str], str, None] = None,
        csv_ovrflw_fname: Union[str, None] = None,
    ):
        self.out_dir = out_dir
        self.out_fn = out_fn
        self.nsave = nsave
        self.csv_lake_fname = csv_lake_fname
        self.csv_point_nlevs = csv_point_nlevs
        self.csv_point_fname = csv_point_fname
        self.csv_point_frombot = csv_point_frombot
        self.csv_point_at = csv_point_at
        self.csv_point_nvars = csv_point_nvars
        self.csv_point_vars = csv_point_vars
        self.csv_outlet_allinone = csv_outlet_allinone
        self.csv_outlet_fname = csv_outlet_fname
        self.csv_outlet_nvars = csv_outlet_nvars
        self.csv_outlet_vars = csv_outlet_vars
        self.csv_ovrflw_fname = csv_ovrflw_fname

    def __call__(
        self, 
        check_errors: bool = True
    ) -> dict[
        str, Union[float, int, str, bool, List[float], List[str], None]
    ]:

        self.csv_point_frombot = self._single_value_to_list(
            self.csv_point_frombot
        )
        self.csv_point_at = self._single_value_to_list(self.csv_point_at)
        self.csv_point_vars = self._single_value_to_list(self.csv_point_vars)    
        self.csv_outlet_vars = self._single_value_to_list(self.csv_outlet_vars)       

        if check_errors:
            pass

        output_dict = {
            "out_dir": self.out_dir,
            "out_fn": self.out_fn,
            "nsave": self.nsave,
            "csv_lake_fname": self.csv_lake_fname,
            "csv_point_nlevs": self.csv_point_nlevs,
            "csv_point_fname": self.csv_point_fname,
            "csv_point_frombot": self.csv_point_frombot,
            "csv_point_at": self.csv_point_at,
            "csv_point_nvars": self.csv_point_nvars,
            "csv_point_vars": self.csv_point_vars,
            "csv_outlet_allinone": self.csv_outlet_allinone,
            "csv_outlet_fname": self.csv_outlet_fname,
            "csv_outlet_nvars": self.csv_outlet_nvars,
            "csv_outlet_vars": self.csv_outlet_vars,
            "csv_ovrflw_fname": self.csv_ovrflw_fname
        }

        return output_dict

class NMLInitProfiles(NMLBase):
    def __init__(
        self,
        lake_depth: Union[float, None] = None,
        num_depths: Union[int, None] = None,
        the_depths: Union[List[float], float, None] = None,
        the_temps: Union[List[float], float, None] = None,
        the_sals: Union[List[float], float, None] = None,
        num_wq_vars: Union[int, None] = None,
        wq_names: Union[List[str], str, None] = None,
        wq_init_vals: Union[List[float], float, None] = None,
    ):
        self.lake_depth = lake_depth
        self.num_depths = num_depths
        self.the_depths = the_depths
        self.the_temps = the_temps
        self.the_sals = the_sals
        self.num_wq_vars = num_wq_vars
        self.wq_names = wq_names
        self.wq_init_vals = wq_init_vals

    def __call__(
        self, 
        check_errors: bool = True
    ) -> dict[
        str, Union[float, int, str, List[float], List[str], None]
    ]:
        self.the_depths = self._single_value_to_list(self.the_depths)
        self.the_temps = self._single_value_to_list(self.the_temps)
        self.the_depths = self._single_value_to_list(self.the_depths)
        self.wq_names = self._single_value_to_list(self.wq_names)
        self.wq_init_vals = self._single_value_to_list(self.wq_init_vals)

        if check_errors:
            pass

        init_profiles_dict = {
            "lake_depth": self.lake_depth,
            "num_depths": self.num_depths,
            "the_depths": self.the_depths,
            "the_temps": self.the_temps,
            "the_sals": self.the_sals,
            "num_wq_vars": self.num_wq_vars,
            "wq_names": self.wq_names,
            "wq_init_vals": self.wq_init_vals
        }

        return init_profiles_dict
    
class NMLLight(NMLBase):
    def __init__(
        self,
        light_mode: Union[int, None] = None,
        Kw: Union[float, None] = None,
        Kw_file: Union[str, None] = None,
        n_bands: Union[int, None] = None,
        light_extc: Union[List[float], float, None] = None,
        energy_frac: Union[List[float], float, None] = None,
        Benthic_Imin: Union[float, None] = None,
    ):
        self.light_mode = light_mode
        self.Kw = Kw
        self.Kw_file = Kw_file
        self.n_bands = n_bands
        self.light_extc = light_extc
        self.energy_frac = energy_frac
        self.Benthic_Imin = Benthic_Imin   

    def __call__(
        self, 
        check_errors: bool = True
    ) -> dict[str, Union[float, int, str, List[float], None]]:
        self.light_extc = self._single_value_to_list(self.light_extc)   
        self.energy_frac = self._single_value_to_list(self.light_extc)

        if check_errors:
            pass

        light_dict = {
            "light_mode": self.light_mode,
            "Kw": self.Kw,
            "Kw_file": self.Kw_file,
            "n_bands": self.n_bands,
            "light_extc": self.light_extc,
            "energy_frac": self.energy_frac,
            "Benthic_Imin": self.Benthic_Imin
        }     

        return light_dict

class NMLBirdModel(NMLBase):
    def __init__(
        self,
        AP: Union[float, None] = None,
        Oz: Union[float, None] = None,
        WatVap: Union[float, None] = None,
        AOD500: Union[float, None] = None,
        AOD380: Union[float, None] = None,
        Albedo: Union[float, None] = None,
    ):
        self.AP = AP
        self.Oz = Oz
        self.WatVap = WatVap
        self.AOD500 = AOD500
        self.AOD380 = AOD380
        self.Albedo = Albedo
    
    def __call__(
        self, 
        check_errors: bool = True
    ) -> dict[str, Union[float, None]]:
        if check_errors:
            pass

        bird_model_dict = {
            "AP": self.AP,
            "Oz": self.Oz,
            "WatVap": self.WatVap,
            "AOD500": self.AOD500,
            "AOD380": self.AOD380,
            "Albedo": self.Albedo
        }

        return bird_model_dict
    
class NMLSediment(NMLBase):
    def __init__(
        self,
        sed_heat_Ksoil: Union[float, None] = None,
        sed_temp_depth: Union[float, None] = None,
        sed_temp_mean: Union[List[float], float, None] = None,
        sed_temp_amplitude: Union[List[float], float, None] = None,
        sed_temp_peak_doy: Union[List[int], int, None] = None,
        benthic_mode: Union[int, None] = None,
        n_zones: Union[int, None] = None,
        zone_heights: Union[List[float], float, None] = None,
        sed_reflectivity: Union[List[float], float, None] = None,
        sed_roughness: Union[List[float], float, None] = None,
    ):
        self.sed_heat_Ksoil = sed_heat_Ksoil
        self.sed_temp_depth = sed_temp_depth
        self.sed_temp_mean = sed_temp_mean
        self.sed_temp_amplitude = sed_temp_amplitude
        self.sed_temp_peak_doy = sed_temp_peak_doy
        self.benthic_mode = benthic_mode
        self.n_zones = n_zones
        self.zone_heights = zone_heights
        self.sed_reflectivity = sed_reflectivity
        self.sed_roughness = sed_roughness

    def __call__(
        self, 
        check_errors: bool = True
    ) -> dict[str, Union[float, int, List[float], List[int], None]]:
        self.sed_temp_mean = self._single_value_to_list(self.sed_temp_mean)
        self.sed_temp_amplitude = self._single_value_to_list(
            self.sed_temp_amplitude
        )
        self.sed_temp_peak_doy = self._single_value_to_list(
            self.sed_temp_peak_doy
        )
        self.zone_heights = self._single_value_to_list(self.zone_heights)
        self.sed_reflectivity = self._single_value_to_list(
            self.sed_reflectivity
        )
        self.sed_roughness = self._single_value_to_list(self.sed_roughness)

        if check_errors:
            pass

        sediment_dict = {
            "sed_heat_Ksoil": self.sed_heat_Ksoil,
            "sed_temp_depth": self.sed_temp_depth,
            "sed_temp_mean": self.sed_temp_mean,
            "sed_temp_amplitude": self.sed_temp_amplitude,
            "sed_temp_peak_doy": self.sed_temp_peak_doy,
            "benthic_mode": self.benthic_mode,
            "n_zones": self.n_zones,
            "zone_heights": self.zone_heights,
            "sed_reflectivity": self.sed_reflectivity,
            "sed_roughness": self.sed_roughness
        }

        return sediment_dict

class NMLSnowIce(NMLBase):
    def __init__(
        self,
        snow_albedo_factor: Union[float, None] = None,
        snow_rho_min: Union[float, None] = None,
        snow_rho_max: Union[float, None] = None,
    ):
        self.snow_albedo_factor = snow_albedo_factor
        self.snow_rho_max = snow_rho_max
        self.snow_rho_min = snow_rho_min
    
    def __call__(
        self, 
        check_errors: bool = True
    ) -> dict[str, Union[float, None]]:
        if check_errors:
            pass

        snowice_dict = {
            "snow_albedo_factor": self.snow_albedo_factor,
            "snow_rho_min": self.snow_rho_min,
            "snow_rho_max": self.snow_rho_max
        }

        return snowice_dict

class NMLMeteorology(NMLBase):
    def __init__(
        self,
        met_sw: Union[bool, None] = None,
        meteo_fl: Union[str, None] = None,
        subdaily: Union[bool, None] = None,
        time_fmt: Union[str, None] = None,
        rad_mode: Union[int, None] = None,
        albedo_mode: Union[int, None] = None,
        sw_factor: Union[float, None] = None,
        lw_type: Union[str, None] = None,
        cloud_mode: Union[int, None] = None,
        lw_factor: Union[float, None] = None,
        atm_stab: Union[int, None] = None,
        rh_factor: Union[float, None] = None,
        at_factor: Union[float, None] = None,
        ce: Union[float, None] = None,
        ch: Union[float, None] = None,
        rain_sw: Union[bool, None] = None,
        rain_factor: Union[float, None] = None,
        catchrain: Union[bool, None] = None,
        rain_threshold: Union[float, None] = None,
        runoff_coef: Union[float, None] = None,
        cd: Union[float, None] = None,
        wind_factor: Union[float, None] = None,
        fetch_mode: Union[int, None] = None,
        Aws: Union[float, None] = None,
        Xws: Union[float, None] = None,
        num_dir: Union[int, None] = None,
        wind_dir: Union[float, None] = None,
        fetch_scale: Union[float, None] = None,
    ):    
        self.met_sw = met_sw        
        self.meteo_fl = meteo_fl
        self.subdaily = subdaily
        self.time_fmt = time_fmt
        self.rad_mode = rad_mode
        self.albedo_mode = albedo_mode
        self.sw_factor = sw_factor
        self.lw_type = lw_type
        self.cloud_mode = cloud_mode
        self.lw_factor = lw_factor
        self.atm_stab = atm_stab
        self.rh_factor = rh_factor
        self.at_factor = at_factor
        self.ce = ce
        self.ch = ch
        self.rain_sw = rain_sw        
        self.rain_factor = rain_factor
        self.catchrain = catchrain
        self.rain_threshold = rain_threshold
        self.runoff_coef = runoff_coef
        self.cd = cd
        self.wind_factor = wind_factor
        self.fetch_mode = fetch_mode
        self.Aws = Aws
        self.Xws = Xws
        self.num_dir = num_dir
        self.wind_dir = wind_dir
        self.fetch_scale = fetch_scale

    def __call__(
        self, 
        check_errors: bool = True
    ) -> dict[str, Union[float, int, str, bool, None]]:
        if check_errors:
            pass

        meteorology_dict = {
            "met_sw": self.met_sw,
            "meteo_fl": self.meteo_fl,
            "subdaily": self.subdaily,
            "time_fmt": self.time_fmt,
            "rad_mode": self.rad_mode,
            "albedo_mode": self.albedo_mode,
            "sw_factor": self.sw_factor,
            "lw_type": self.lw_type,
            "cloud_mode": self.cloud_mode,
            "lw_factor": self.lw_factor,
            "atm_stab": self.atm_stab,
            "rh_factor": self.rh_factor,
            "at_factor": self.at_factor,
            "ce": self.ce,
            "ch": self.ch,
            "rain_sw": self.rain_sw,
            "rain_factor": self.rain_factor,
            "catchrain": self.catchrain,
            "rain_threshold": self.rain_threshold,
            "runoff_coef": self.runoff_coef,
            "cd": self.cd,
            "wind_factor": self.wind_factor,
            "fetch_mode": self.fetch_mode,
            "Aws": self.Aws,
            "Xws": self.Xws,
            "num_dir": self.num_dir,
            "wind_dir": self.wind_dir,
            "fetch_scale": self.fetch_scale
        }

        return meteorology_dict

class NMLInflow(NMLBase):
    def __init__(
        self,
        num_inflows: Union[int, None] = None,
        names_of_strms: Union[List[str], str, None] = None,
        subm_flag: Union[List[bool], bool, None] = None,
        strm_hf_angle: Union[List[float], float, None] = None,
        strmbd_slope: Union[List[float], float, None] = None,
        strmbd_drag: Union[List[float], float, None] = None,
        coef_inf_entrain: Union[List[float], float, None] = None,
        inflow_factor: Union[List[float], float, None] = None,
        inflow_fl: Union[List[str], str, None] = None,
        inflow_varnum: Union[int, None] = None,
        inflow_vars: Union[List[str], str, None] = None,
        time_fmt: Union[str, None] = None,
    ):
        self.num_inflows = num_inflows        
        self.names_of_strms = names_of_strms
        self.subm_flag = subm_flag
        self.strm_hf_angle = strm_hf_angle
        self.strmbd_slope = strmbd_slope
        self.strmbd_drag = strmbd_drag
        self.coef_inf_entrain = coef_inf_entrain
        self.inflow_factor = inflow_factor
        self.inflow_fl = inflow_fl
        self.inflow_varnum = inflow_varnum
        self.inflow_vars = inflow_vars
        self.time_fmt = time_fmt
    
    def __call__(
        self,
        check_errors: bool = True
    ) -> dict[
        str, Union[
            float, int, str, bool, List[float], List[str], List[bool], None
        ]
    ]:
        self.names_of_strms = self._single_value_to_list(self.names_of_strms)
        self.subm_flag = self._single_value_to_list(self.subm_flag)
        self.strm_hf_angle = self._single_value_to_list(self.strm_hf_angle)
        self.strmbd_slope = self._single_value_to_list(self.strmbd_slope)
        self.strmbd_drag = self._single_value_to_list(self.strmbd_drag)
        self.coef_inf_entrain = self._single_value_to_list(
            self.coef_inf_entrain
        )
        self.inflow_factor = self._single_value_to_list(self.inflow_factor)
        self.inflow_fl = self._single_value_to_list(self.inflow_fl)
        self.inflow_vars = self._single_value_to_list(self.inflow_vars)

        if check_errors:
            pass        

        inflow_dict = {
            "num_inflows": self.num_inflows,
            "names_of_strms": self.names_of_strms,
            "subm_flag": self.subm_flag,
            "strm_hf_angle": self.strm_hf_angle,
            "strmbd_slope": self.strmbd_slope,
            "strmbd_drag": self.strmbd_drag,
            "coef_inf_entrain": self.coef_inf_entrain,
            "inflow_factor": self.inflow_factor,
            "inflow_fl": self.inflow_fl,
            "inflow_varnum": self.inflow_varnum,
            "inflow_vars": self.inflow_vars,
            "time_fmt": self.time_fmt
        }

        return inflow_dict

class NMLOutflow(NMLBase):
    def __init__(
        self,
        num_outlet: Union[int, None] = None,
        outflow_fl: Union[str, None] = None,
        time_fmt: Union[str, None] = None,
        outflow_factor: Union[List[float], float, None] = None, 
        outflow_thick_limit: Union[List[float], float, None] = None, 
        single_layer_draw: Union[List[bool], bool, None] = None, 
        flt_off_sw: Union[List[bool], bool, None] = None, 
        outlet_type: Union[List[int], int, None] = None, 
        outl_elvs: Union[List[float], float, None] = None, 
        bsn_len_outl: Union[List[float], float, None] = None, 
        bsn_wid_outl: Union[List[float], float, None] = None, 
        crit_O2: Union[int, None] = None,
        crit_O2_dep: Union[int, None] = None,
        crit_O2_days: Union[int, None] = None,
        outlet_crit: Union[int, None] = None,
        O2name: Union[str, None] = None,
        O2idx: Union[str, None] = None,
        target_temp: Union[float, None] = None,
        min_lake_temp: Union[float, None] = None,
        fac_range_upper: Union[float, None] = None,
        fac_range_lower: Union[float, None] = None,
        mix_withdraw: Union[bool, None] = None,
        coupl_oxy_sw: Union[bool, None] = None,
        withdrTemp_fl: Union[str, None] = None,
        seepage: Union[bool, None] = None,
        seepage_rate: Union[float, None] = None,
        crest_width: Union[float, None] = None,
        crest_factor: Union[float, None] = None,
    ):

        self.num_outlet = num_outlet
        self.outflow_fl = outflow_fl
        self.time_fmt = time_fmt
        self.outflow_factor = outflow_factor
        self.outflow_thick_limit = outflow_thick_limit
        self.single_layer_draw = single_layer_draw
        self.flt_off_sw = flt_off_sw
        self.outlet_type = outlet_type
        self.outl_elvs = outl_elvs
        self.bsn_len_outl = bsn_len_outl
        self.bsn_wid_outl = bsn_wid_outl
        self.crit_O2 = crit_O2
        self.crit_O2_dep = crit_O2_dep
        self.crit_O2_days = crit_O2_days
        self.outlet_crit = outlet_crit
        self.O2name = O2name
        self.O2idx = O2idx
        self.target_temp = target_temp
        self.min_lake_temp = min_lake_temp
        self.fac_range_upper = fac_range_upper
        self.fac_range_lower = fac_range_lower
        self.mix_withdraw = mix_withdraw
        self.coupl_oxy_sw = coupl_oxy_sw
        self.withdrTemp_fl = withdrTemp_fl
        self.seepage = seepage
        self.seepage_rate = seepage_rate
        self.crest_width = crest_width
        self.crest_factor = crest_factor

    def __call__(
        self,
        check_errors: bool = True
    ) -> dict[str, Union[
                float, int, str, bool, List[float], List[int], List[bool], None
            ]
        ]:
        self.outflow_factor = self._single_value_to_list(self.outflow_factor)
        self.outflow_thick_limit = self._single_value_to_list(
            self.outflow_thick_limit
        )
        self.single_layer_draw = self._single_value_to_list(
            self.single_layer_draw
        )
        self.flt_off_sw = self._single_value_to_list(self.flt_off_sw)
        self.outlet_type = self._single_value_to_list(self.outlet_type)
        self.outl_elvs = self._single_value_to_list(self.outl_elvs)
        self.bsn_len_outl = self._single_value_to_list(self.bsn_len_outl)
        self.bsn_wid_outl = self._single_value_to_list(self.bsn_wid_outl)

        if check_errors:
            pass    

        outflow_dict = {
            "num_outlet": self.num_outlet,
            "outflow_fl": self.outflow_fl,
            "time_fmt": self.time_fmt,
            "outflow_factor": self.outflow_factor,
            "outflow_thick_limit": self.outflow_thick_limit,
            "single_layer_draw": self.single_layer_draw,
            "flt_off_sw": self.flt_off_sw,
            "outlet_type": self.outlet_type,
            "outl_elvs": self.outl_elvs,
            "bsn_len_outl": self.bsn_len_outl,
            "bsn_wid_outl": self.bsn_wid_outl,
            "crit_O2": self.crit_O2,
            "crit_O2_dep": self.crit_O2_dep,
            "crit_O2_days": self.crit_O2_days,
            "outlet_crit": self.outlet_crit,
            "O2name": self.O2name,
            "O2idx": self.O2idx,
            "target_temp": self.target_temp,
            "min_lake_temp": self.min_lake_temp,
            "fac_range_upper": self.fac_range_upper,
            "fac_range_lower": self.fac_range_lower,
            "mix_withdraw": self.mix_withdraw,
            "coupl_oxy_sw": self.coupl_oxy_sw,
            "withdrTemp_fl": self.withdrTemp_fl,
            "seepage": self.seepage,
            "seepage_rate": self.seepage_rate,
            "crest_width": self.crest_width,
            "crest_factor": self.crest_factor
        }

        return outflow_dict
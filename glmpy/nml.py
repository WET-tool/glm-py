from typing import Union, List

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
        setup: str,
        morphometry: str,
        time: str,
        init_profiles: str,
        mixing: Union[str, None] = None,
        output: Union[str, None] = None,
        meteorology: Union[str, None] = None,
        light: Union[str, None] = None,
        bird_model: Union[str, None] = None,
        inflows: Union[str, None] = None,
        outflows: Union[str, None] = None,
        sediment: Union[str, None] = None,
        ice_snow: Union[str, None] = None,
        wq_setup: Union[str, None] = None,
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

    def set_attributes(self, attrs_dict, update: Union[dict, None] = None):
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

    @staticmethod
    def fortran_bool_string(bool_input: Union[bool, List[bool], None]) -> Union[str, List[Union[str, None]], None]:
        """Python boolean to Fortran boolean string.

        Convert a Python boolean or a list of Python booleans to a Fortran
        boolean string or a list of Fortran boolean strings.

        Parameters
        ----------
        bool_input : Union[bool, List[bool], None]
            A Python boolean or a list of Python booleans.

        Returns
        -------
        Union[str, List[Union[str, None]], None]
            A Fortran boolean string or a list of Fortran boolean strings.

        Examples
        --------
        >>> fortran_bool_string(True)
        '.true.'
        >>> fortran_bool_string([True, False])
        ['.true.', '.false.']
        """
        if isinstance(bool_input, List):
            result: List[Union[str, None]] = []
            for item in bool_input:
                if item is True:
                    result.append(".true.")
                elif item is False:
                    result.append(".false.")
                else:
                    result.append(None)
            return result
        else:
            if bool_input is True:
                return ".true."
            elif bool_input is False:
                return ".false."
            else:
                return None

    @staticmethod
    def comma_sep_list(
        list_input: Union[List[int], List[float], List[str], List[bool], None],
        inverted_commas: bool = False
        ):
        """Convert a Python list to a NML formatted  comma separated string.

        If the list_input is None, None is returned. If inverted_commas is True,
        the list items are returned as strings with inverted commas.

        Parameters
        ----------
        list_input : list
            A list of values.
        inverted_commas : bool
            If True, the list items are returned as strings with inverted commas.

        Returns
        -------
        str
            A comma separated string for use in defining a NML block. Returns
            None if list_input is None.

        Examples
        --------
        >>> from glmpy import NMLBase
        >>> NMLBase.comma_sep_list([1, 2, 3], inverted_commas = False)
        '1, 2, 3'
        >>> NMLBase.comma_sep_list([1, 2, 3], inverted_commas=True)
        "'1', '2', '3'"
        >>> NMLBase.comma_sep_list(['a', 'b', 'c'], inverted_commas=True)
        "'a', 'b', 'c'"
        >>> comma_sep_list(['a', 'b', 'c'], inverted_commas=False)
        'a, b, c'
        """
        if inverted_commas:
            return ', '.join([repr(str(item)) for item in list_input]) if list_input else None
        else:
            return ', '.join([str(item) for item in list_input]) if list_input else None





class NMLSetup(NMLBase):
    """Define the glm_setup block of a GLM simulation configuration.

    The glm_setup component is used to define the simulations layer details.
    Attributes are set using the `set_attributes()` method and returned as a
    formatted string using the `__str__()` method.

    Attributes
    ----------
    sim_name : str
        Title of simulation. Default is 'lake'.
    max_layers : Union[int, None]
        Maximum number of layers. Default is 500.
    min_layer_vol : Union[float, None]
        Minimum layer volume. Default is None.
    min_layer_thick : Union[float, None]
        Minimum thickness of a layer (m). Default is None.
    max_layer_thick : Union[float, None]
        Maximum thickness of a layer (m). Default is None.
    density_model : Union[int, None]
        Switch to set the density equation. Default is 1.
    non_avg : bool
        Switch to configure flow boundary condition temporal interpolation.
        Default is True.

    Examples
    --------
    >>> from glmpy import NMLSetup
    >>> setup = NMLSetup()
    >>> my_setup = {
    ...     "sim_name": "Example Simulation #1",
    ...     "max_layers": 500,
    ...     "min_layer_vol": 0.15,
    ...     "min_layer_thick": 1.50,
    ...     "max_layer_thick": 0.025,
    ...     "density_model": 1,
    ...     "non_avg": True
    ... }
    >>> setup.set_attributes(my_setup)
    >>> print(setup)

    """

    def __init__(self):
        self.sim_name: str = 'lake'
        self.max_layers: Union[int, None] = 500
        self.min_layer_vol: Union[float, None] = None
        self.min_layer_thick: Union[float, None] = None
        self.max_layer_thick: Union[float, None] = None
        self.density_model: Union[int, None] = 1
        self.non_avg: bool = True

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
        >>> my_setup = {
        ...     "sim_name": "Example Simulation #1",
        ...     "max_layers": 500,
        ...     "min_layer_vol": 0.15,
        ...     "min_layer_thick": 1.50,
        ...     "max_layer_thick": 0.025,
        ...     "density_model": 1,
        ...     "non_avg": True
        ... }
        >>> setup.set_attributes(my_setup)
        >>> print(setup)
        """
        params = [
            (f"   sim_name = '{self.sim_name}'", self.sim_name),
            (f"   max_layers = {self.max_layers}", self.max_layers),
            (f"   min_layer_vol = {self.min_layer_vol}", self.min_layer_vol),
            (f"   min_layer_thick = {self.min_layer_thick}",
             self.min_layer_thick),
            (f"   max_layer_thick = {self.max_layer_thick}",
             self.max_layer_thick),
            (f"   density_model = {self.density_model}", self.density_model),
            (f"   non_avg = {self.fortran_bool_string(self.non_avg)}",
             self.non_avg),
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
    lake_name : Union[str, None]
        Site name. Default is None.
    latitude : float
        Latitude, positive North. Default is 0.0.
    longitude : float
        Longitude, positive East. Default is 0.0.
    base_elev: Union[float, None]
        Elevation of the bottom-most point of the lake (m above datum). Default
        is None.
    crest_elev : Union[float, None]
        Elevation of a weir crest, where overflow begins. Default is None.
    bsn_len : Union[float, None]
        Length of the lake basin, at crest height (m). Default is None.
    bsn_wid : Union[float, None]
        Width of the lake basin, at crest height (m). Default is None.
    bsn_vals : Union[float, None]
        Number of points being provided to described the hyposgraphic details.
        Default is None.
    H : Union[List[float], None]
        Comma-separated list of lake elevations (m above datum). Default is
        None.
    A : Union[List[float], None]
        Comma-separated list of lake areas (m^2). Default is None.

    Examples
    --------
    >>> from glmpy import NMLMorphometry
    >>> morphometry = NMLMorphometry()
    >>> my_morphometry = {
    ...     "lake_name": "Example Lake",
    ...     "latitude": 32,
    ...     "longitude": 35,
    ...     "base_elev": -252.9,
    ...     "crest_elev": -203.9,
    ...     "bsn_len": 21000,
    ...     "bsn_wid": 13000,
    ...     "bsn_vals": 45,
    ...     "H": [
    ...         -252.9, -251.9, -250.9, -249.9, -248.9, -247.9, -246.9,
    ...         -245.9, -244.9, -243.9, -242.9, -241.9, -240.9, -239.9,
    ...         -238.9, -237.9, -236.9, -235.9, -234.9, -233.9, -232.9,
    ...         -231.9, -230.9, -229.9, -228.9, -227.9, -226.9, -225.9,
    ...         -224.9, -223.9, -222.9, -221.9, -220.9, -219.9, -218.9,
    ...         -217.9, -216.9, -215.9, -214.9, -213.9, -212.9, -211.9,
    ...         -208.9, -207.9,  -203.9
    ...         ],
    ...     "A": [
    ...         0, 9250000, 15200000, 17875000, 21975000, 26625000,
    ...         31700000, 33950000, 38250000, 41100000, 46800000,
    ...         51675000, 55725000, 60200000, 64675000, 69600000, 74475000,
    ...         79850000, 85400000, 90975000, 96400000, 102000000,
    ...         107000000, 113000000, 118000000, 123000000, 128000000,
    ...         132000000, 136000000, 139000000, 143000000, 146000000,
    ...         148000000, 150000000, 151000000, 153000000, 155000000,
    ...         157000000, 158000000, 160000000, 161000000, 162000000,
    ...         167000000, 170000000, 173000000
    ...         ]
    ... }
    >>> morphometry.set_attributes(my_morphometry)
    >>> print(morphometry)
    """

    def __init__(self):
        self.lake_name: Union[str, None] = None
        self.latitude: float = 0.0
        self.longitude: float = 0.0
        self.base_elev: Union[float, None] = None
        self.crest_elev: Union[float, None] = None
        self.bsn_len: Union[float, None] = None
        self.bsn_wid: Union[float, None] = None
        self.bsn_vals: Union[float, None] = None
        self.H: Union[List[float], None] = None
        self.A: Union[List[float], None] = None

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
        >>> my_morphometry = {
        ...     "lake_name": "Example Lake",
        ...     "latitude": 32,
        ...     "longitude": 35,
        ...     "base_elev": -252.9,
        ...     "crest_elev": -203.9,
        ...     "bsn_len": 21000,
        ...     "bsn_wid": 13000,
        ...     "bsn_vals": 45,
        ...     "H": [
        ...         -252.9, -251.9, -250.9, -249.9, -248.9, -247.9, -246.9,
        ...         -245.9, -244.9, -243.9, -242.9, -241.9, -240.9, -239.9,
        ...         -238.9, -237.9, -236.9, -235.9, -234.9, -233.9, -232.9,
        ...         -231.9, -230.9, -229.9, -228.9, -227.9, -226.9, -225.9,
        ...         -224.9, -223.9, -222.9, -221.9, -220.9, -219.9, -218.9,
        ...         -217.9, -216.9, -215.9, -214.9, -213.9, -212.9, -211.9,
        ...         -208.9, -207.9,  -203.9
        ...         ],
        ...     "A": [
        ...         0, 9250000, 15200000, 17875000, 21975000, 26625000,
        ...         31700000, 33950000, 38250000, 41100000, 46800000,
        ...         51675000, 55725000, 60200000, 64675000, 69600000, 74475000,
        ...         79850000, 85400000, 90975000, 96400000, 102000000,
        ...         107000000, 113000000, 118000000, 123000000, 128000000,
        ...         132000000, 136000000, 139000000, 143000000, 146000000,
        ...         148000000, 150000000, 151000000, 153000000, 155000000,
        ...         157000000, 158000000, 160000000, 161000000, 162000000,
        ...         167000000, 170000000, 173000000
        ...         ]
        ... }
        >>> morphometry.set_attributes(my_morphometry)
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
            (f"   H = {self.comma_sep_list(self.H)}",self.H),
            (f"   A = {self.comma_sep_list(self.A)}",self.A),
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
        Switch to select the options of the surface mixing model. Default is 1.
    coef_mix_conv : Union[float, None]
        Mixing efficiency - convective overturn. Default is None.
    coef_wind_stir : Union[float, None]
        Mixing efficiency - wind stirring. Default is None.
    coef_mix_shear : Union[float, None]
        Mixing efficiency - shear production. Default is None.
    coef_mix_turb : Union[float, None]
        Mixing efficiency - unsteady turbulence effects. Default is None.
    coef_mix_KH : Union[float, None]
        Mixing efficiency - Kelvin-Helmholtz billowing. Default is None.
    deep_mixing : Union[int, None]
        Switch to select the options of the deep (hypolimnetic) mixing model
        (0 = no deep mixing, 1 = constant diffusivity, 2 = weinstock model).
        Default is None.
    coef_mix_hyp : Union[float, None]
        Mixing efficiency - hypolimnetic turbulence. Default is None.
    diff : Union[float, None]
        Background (molecular) diffusivity in the hypolimnion. Default is None.

    Examples
    --------
    >>> from glmpy import NMLMixing
    >>> mixing = NMLMixing()
    >>> my_mixing = {
    >>>     "surface_mixing": 1,
    >>>     "coef_mix_conv": 0.125,
    >>>     "coef_wind_stir": 0.23,
    >>>     "coef_mix_shear": 0.2,
    >>>     "coef_mix_turb": 0.51,
    >>>     "coef_mix_KH": 0.3,
    >>>     "deep_mixing": 0.2,
    >>>     "coef_mix_hyp": 0.5,
    >>>     "diff": 0.0,
    >>> }
    >>> mixing.set_attributes(my_mixing)
    >>> print(mixing)
    """

    def __init__(self):
        self.surface_mixing: int  = 1
        self.coef_mix_conv: Union[float, None] = None
        self.coef_wind_stir: Union[float, None] = None
        self.coef_mix_shear: Union[float, None] = None
        self.coef_mix_turb: Union[float, None] = None
        self.coef_mix_KH: Union[float, None] = None
        self.deep_mixing: Union[int, None] = None
        self.coef_mix_hyp: Union[float, None] = None
        self.diff: Union[float, None] = None

    def __str__(self):
        """Return the string representation of the NMLMixing object.

        Returns a formatted string of the NMLMixing configution options and
        values.

        Returns
        -------
        str
            String representation of the NMLMixing object.

        Examples
        --------
        >>> from glmpy import NMLMixing
        >>> mixing = NMLMixing()
        >>> my_mixing = {
        >>>     "surface_mixing": 1,
        >>>     "coef_mix_conv": 0.125,
        >>>     "coef_wind_stir": 0.23,
        >>>     "coef_mix_shear": 0.2,
        >>>     "coef_mix_turb": 0.51,
        >>>     "coef_mix_KH": 0.3,
        >>>     "deep_mixing": 0.2,
        >>>     "coef_mix_hyp": 0.5,
        >>>     "diff": 0.0,
        >>> }
        >>> mixing.set_attributes(my_mixing)
        >>> print(mixing)
        """
        params = [
            (f"   surface_mixing = {self.surface_mixing}",
             self.surface_mixing),
            (f"   coef_mix_conv = {self.coef_mix_conv}", self.coef_mix_conv),
            (f"   coef_wind_stir = {self.coef_wind_stir}",
             self.coef_wind_stir,),
            (f"   coef_mix_shear = {self.coef_mix_shear}",
             self.coef_mix_shear,),
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
    timefmt : Union[int, None]
        Time configuration switch. Default is None.
    start : Union[str, None]
        Start time/date of simulation in format 'yyyy-mm-dd hh:mm:ss'. Default
        is None.
    stop : Union[str, None]
        End time/date of simulation in format 'yyyy-mm-dd hh:mm:ss'. Default is
        None.
    dt : float
        Time step (seconds). Default is 3600.0.
    num_days : Union[int, None]
        Number of days to simulate. Default is None.
    timezone : float
        UTC time zone. Default is 0.0.

    Examples
    --------
    >>> from glmpy import NMLSetup
    >>> time = NMLTime()
    >>> my_time = {
    >>>     "timefmt": 3,
    >>>     "start": '1997-01-01 00:00:00',
    >>>     "stop": '1999-01-01 00:00:00',
    >>>     "dt": 3600.0,
    >>>     "num_days": 730,
    >>>     "timezone": 7.0
    >>> }
    >>> time.set_attributes(my_time)
    >>> print(time)
    """

    def __init__(self):
        self.timefmt: Union[int, None] = None
        self.start: Union[str, None] = None
        self.stop: Union[int, None] = None
        self.dt: float = 3600.0
        self.num_days: Union[int, None] = None
        self.timezone: float = 0.0

    def __str__(self):
        """Return the string representation of the NMLTime object.

        Returns a formatted string of the NMLTime configution options and
        values.

        Returns
        -------
        str
            String representation of the NMLTime object.

        Examples
        --------
        >>> from glmpy import NMLSetup
        >>> time = NMLTime()
        >>> my_time = {
        >>>     "timefmt": 3,
        >>>     "start": '1997-01-01 00:00:00',
        >>>     "stop": '1999-01-01 00:00:00',
        >>>     "dt": 3600.0,
        >>>     "num_days": 730,
        >>>     "timezone": 7.0
        >>> }
        >>> time.set_attributes(my_time)
        >>> print(time)
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
        Directory to write the output files. Default is './'.
    out_fn : str
        Filename of the main NetCDF output file. Default is 'output'.
    nsave : int
        Frequency to write to the NetCDF and CSV point files. Default is 1.
    csv_lake_fname : str
        Filename for the daily summary file. Default is 'lake'.
    csv_point_nlevs : float
        Number of specific level/depth csv files to be created. Default is 0.0.
    csv_point_fname : str
        Name to be appended to specified depth CSV files. Default is 'WQ_'.
    csv_point_frombot : Union[List[float], None]
        Comma separated list identify whether each output point listed in
        csv_point_at is relative to the bottom (ie heights) or the surface
        (ie depths). Default is None.
    csv_point_at : Union[List[float], None]
        Height or Depth of points to output at (comma separated list). Default
        is None.
    csv_point_nvars : Union[int, None]
        Number of variables to output into the csv files. Default is None.
    csv_point_vars : Union[List[str], None]
        Comma separated list of variable names. Default is None.
    csv_outlet_allinone : bool
        Switch to create an optional outlet file combining all outlets. Default
        is False.
    csv_outlet_fname : Union[str, None]
        Name to be appended to each of the outlet CSV files. Default is None.
    csv_outlet_nvars : int
        Number of variables to be written into the outlet file(s). Default is
        0.
    csv_outlet_vars : Union[str, None]
        Comma separated list of variable names to be included in the output
        file(s). Default is None.
    csv_ovrflw_fname : Union[str, None]
        Filename to be used for recording the overflow details. Default is
        None.

    Examples
    --------
    >>> from glmpy import NMLOutput
    >>> output = NMLOutput()
    >>> my_output = {
    >>>     'out_dir': 'output',
    >>>     'out_fn': 'output',
    >>>     'nsave': 6,
    >>>     'csv_lake_fname': 'lake',
    >>>     'csv_point_nlevs': 2.0,
    >>>     'csv_point_fname': 'WQ_',
    >>>     'csv_point_at': [5, 30],
    >>>     'csv_point_nvars': 7,
    >>>     'csv_point_vars': ['temp', 'salt', 'OXY_oxy', 'SIL_rsi', 'NIT_amm', 'NIT_nit', 'PHS_frp'],
    >>>     'csv_outlet_allinone': False,
    >>>     'csv_outlet_fname': 'outlet_',
    >>>     'csv_outlet_nvars': 4,
    >>>     'csv_outlet_vars': ['flow', 'temp', 'salt', 'OXY_oxy'],
    >>>     'csv_ovrflw_fname': 'overflow'
    >>> }
    >>> output.set_attributes(my_output)
    >>> print(output)
    """

    def __init__(self):
        self.out_dir: str = './'
        self.out_fn: str = 'output'
        self.nsave: int = 1
        self.csv_lake_fname: str = 'lake'
        self.csv_point_nlevs: float = 0.0
        self.csv_point_fname: str = 'WQ_'
        self.csv_point_frombot: Union[List[float], None] = None
        self.csv_point_at: Union[List[float], None] = None
        self.csv_point_nvars: Union[int, None] = None
        self.csv_point_vars: Union[List[str], None] = None
        self.csv_outlet_allinone: bool = False
        self.csv_outlet_fname: Union[str, None] = None
        self.csv_outlet_nvars: int = 0
        self.csv_outlet_vars: Union[List[str], None] = None
        self.csv_ovrflw_fname: Union[str, None] = None

    def __str__(self):
        """Return the string representation of the NMLOutput object.

        Returns a formatted string of the NMLOutput configution options and
        values.

        Returns
        -------
        str
            String representation of the NMLOutput object.

        Examples
        --------
        >>> from glmpy import NMLOutput
        >>> output = NMLOutput()
        >>> my_output = {
        >>>     'out_dir': 'output',
        >>>     'out_fn': 'output',
        >>>     'nsave': 6,
        >>>     'csv_lake_fname': 'lake',
        >>>     'csv_point_nlevs': 2.0,
        >>>     'csv_point_fname': 'WQ_',
        >>>     'csv_point_at': [5, 30],
        >>>     'csv_point_nvars': 7,
        >>>     'csv_point_vars': ['temp', 'salt', 'OXY_oxy', 'SIL_rsi', 'NIT_amm', 'NIT_nit', 'PHS_frp'],
        >>>     'csv_outlet_allinone': False,
        >>>     'csv_outlet_fname': 'outlet_',
        >>>     'csv_outlet_nvars': 4,
        >>>     'csv_outlet_vars': ['flow', 'temp', 'salt', 'OXY_oxy'],
        >>>     'csv_ovrflw_fname': 'overflow'
        >>> }
        >>> output.set_attributes(my_output)
        >>> print(output)
        """
        params = [
            (f"   out_dir = '{self.out_dir}'", self.out_dir),
            (f"   out_fn = '{self.out_fn}'", self.out_fn),
            (f"   nsave = {self.nsave}", self.nsave),
            (f"   csv_lake_fname = '{self.csv_lake_fname}'",
             self.csv_lake_fname,),
            (f"   csv_point_nlevs = {self.csv_point_nlevs}",
             self.csv_point_nlevs,),
            (f"   csv_point_fname = '{self.csv_point_fname}'",
             self.csv_point_fname),
            (f"   csv_point_frombot = {self.comma_sep_list(self.csv_point_frombot)}",
             self.csv_point_frombot),
            (f"   csv_point_at = {self.comma_sep_list(self.csv_point_at)}",
             self.csv_point_at),
            (f"   csv_point_nvars = {self.csv_point_nvars}",self.csv_point_nvars),
            (f"   csv_point_vars = {self.comma_sep_list(self.csv_point_vars, True)}",
             self.csv_point_vars),
            (f"   csv_outlet_allinone = {self.fortran_bool_string(self.csv_outlet_allinone)}",
             self.csv_outlet_allinone),
            (f"   csv_outlet_fname = '{self.csv_outlet_fname}'", self.csv_outlet_fname),
            (f"   csv_outlet_nvars = {self.csv_outlet_nvars}",self.csv_outlet_nvars),
            (f"   csv_outlet_vars = {self.comma_sep_list(self.csv_outlet_vars, True)}",
             self.csv_outlet_vars),
            (f"   csv_ovrflw_fname = '{self.csv_ovrflw_fname}'",
             self.csv_ovrflw_fname),
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
    lake_depth : Union[float, None]
        Initial lake height/depth (m). Default is NOne.
    num_depths : Union[int, None]
        Number of depths provided for initial profiles. Default is None.
    the_depths : Union[List[float], None]
        The depths of the initial profile points (m). Default is None.
    the_temps : Union[List[float], None]
        The temperature (C) at each of the initial profile points. Default is
        None.
    the_sals : Union[List[float], None]
        The salinity (ppt) at each of the initial profile points. Default is
        None.
    num_wq_vars : Union[int, None]
        Number of non GLM (ie FABM or AED2) variables to be initialised.
        Default is 0.
    wq_names : Union[List[str], None]
        Names of non GLM (ie FABM or AED2) variables to be initialised.
        Default is None.
    wq_init_vals : Union[List[str], None]
        Array of WQ variable initial data (rows = vars; cols = depths).
        Default is [0.0].

    Examples
    --------
    >>> from glmpy import NMLSetup
    >>> init_profiles = NMLInitProfiles()
    >>> my_init_profile = {
    >>>     "lake_depth": 43,
    >>>     "num_depths": 3,
    >>>     "the_depths": [1, 20, 40],
    >>>     "the_temps": [18.0, 18.0, 18.0],
    >>>     "the_sals": [0.5, 0.5, 0.5],
    >>>     "num_wq_vars": 6,
    >>>     "wq_names": ["OGM_don", "OGM_pon", "OGM_dop", "OGM_pop", "OGM_doc", "OGM_poc"],
    >>>     "wq_init_vals": [1.1, 1.2, 1.3, 1.2, 1.3,
    >>>                     2.1, 2.2, 2.3, 1.2, 1.3,
    >>>                     3.1, 3.2, 3.3, 1.2, 1.3,
    >>>                     4.1, 4.2, 4.3, 1.2, 1.3,
    >>>                     5.1, 5.2, 5.3, 1.2, 1.3,
    >>>                     6.1, 6.2, 6.3, 1.2, 1.3]
    >>> }
    >>> init_profile.set_attributes(my_init_profile)
    >>> print(init_profile)
    """

    def __init__(self):
        self.lake_depth: Union[float, None] = None
        self.num_depths: Union[int, None] = None
        self.the_depths: Union[List[float], None] = None
        self.the_temps: Union[List[float], None] = None
        self.the_sals: Union[List[float], None] = None
        self.num_wq_vars: Union[int, None] = 0
        self.wq_names: Union[List[str], None] = None
        self.wq_init_vals: Union[List[float], None] = [0.0]

    def __str__(self):
        """Return the string representation of the NMLInitProfiles object.

        Returns a formatted string of the NMLInitProfiles configution options
        and values.

        Returns
        -------
        str
            String representation of the NMLInitProfiles object.

        Examples
        --------
        >>> from glmpy import NMLSetup
        >>> init_profiles = NMLInitProfiles()
        >>> my_init_profile = {
        >>>     "lake_depth": 43,
        >>>     "num_depths": 3,
        >>>     "the_depths": [1, 20, 40],
        >>>     "the_temps": [18.0, 18.0, 18.0],
        >>>     "the_sals": [0.5, 0.5, 0.5],
        >>>     "num_wq_vars": 6,
        >>>     "wq_names": ["OGM_don", "OGM_pon", "OGM_dop", "OGM_pop", "OGM_doc", "OGM_poc"],
        >>>     "wq_init_vals": [1.1, 1.2, 1.3, 1.2, 1.3,
        >>>                     2.1, 2.2, 2.3, 1.2, 1.3,
        >>>                     3.1, 3.2, 3.3, 1.2, 1.3,
        >>>                     4.1, 4.2, 4.3, 1.2, 1.3,
        >>>                     5.1, 5.2, 5.3, 1.2, 1.3,
        >>>                     6.1, 6.2, 6.3, 1.2, 1.3]
        >>> }
        >>> init_profile.set_attributes(my_init_profile)
        >>> print(init_profile)
        """
        params = [
            (f"   lake_depth = {self.lake_depth}", self.lake_depth),
            (f"   num_depths = {self.num_depths}", self.num_depths),
            (f"   the_depths = {self.comma_sep_list(self.the_depths)}",
             self.the_depths),
            (f"   the_temps = {self.comma_sep_list(self.the_temps)}",
             self.the_temps),
            (f"   the_sals = {self.comma_sep_list(self.the_sals)}",
             self.the_sals),
            (f"   num_wq_vars = {self.num_wq_vars}", self.num_wq_vars),
            (f"   wq_names = {self.comma_sep_list(self.wq_names, True)}",
                self.wq_names),
            (f"   wq_init_vals = {self.comma_sep_list(self.wq_init_vals)}",
                self.wq_init_vals),
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
    met_sw : bool
        Switch to enable the surface heating module. Default is True.
    meteo_fl : Union[str, None]
        Filename of the meterological file. Default is None.
    subdaily : bool
        Switch to indicate the meteorological data is provided with sub-daily
        resolution, at an interval equivalent to Δt. Default is None.
    time_fmt : str
        Time format of the 1st column in the inflow_fl. For example,
        'YYYY-MM-DD hh:mm:ss'. Default is None.
    rad_mode : Union[int, None]
        Switch to configure which incoming radiation option to use. Default is
        None.
    albedo_mode : Union[int, None]
        Switch to configure which albedo calculation option is used. Default is
        None.
    sw_factor : Union[float, None]
        Scaling factor to adjust the shortwave radiation data provided
        in the meteo_fl. Default is None.
    lw_type : Union[str, None]
        Switch to configure which input approach is being used for
        longwave/cloud data in the meteo_fl. Default is None.
    cloud_mode : Union[int, None]
        Switch to configure which atmospheric emmissivity calculation
        option is used. Default is None.
    lw_factor : Union[float, None]
        Scaling factor to adjust the longwave (or cloud) data provided in the
        meteo_fl. Default is None.
    atm_stab : Union[int, None]
        Switch to configure which approach to atmospheric stability is used.
        Default is None.
    rh_factor : Union[float, None]
        Scaling factor to adjust the relative humidity data provided in the
        meteo_fl. Default is None.
    at_factor : Union[float, None]
        Scaling factor to adjust the air temperature data provided in the
        meteo_fl. Default is None.
    ce : Union[float, None]
        Bulk aerodynamic transfer coefficient for latent heat flux. Default is
        0.0013.
    ch : Union[float, None]
        Bulk aerodynamic transfer coefficient for sensible heat flux. Default
        is 0.0013.
    rain_sw : Union[bool, None]
        Switch to configure rainfall input concentrations. Default is None.
    rain_factor : Union[float, None]
        Scaling factor to adjust the rainfall data provided in the meteo_fl.
        Default is None.
    catchrain : Union[bool, None]
        Switch that configures runoff from exposed banks of lake area. Default
        is None.
    rain_threshold : Union[float, None]
        Daily rainfall amount (m) required before runoff from exposed banks
        occurs. Default is None.
    runoff_coef : Union[float, None]
        Conversion fraction of infiltration excess rainfall to runoff in
        exposed lake banks. Default is None.
    cd :
        Bulk aerodynamic transfer coefficient for momentum. Default is 0.0013.
    wind_factor : Union[float, None]
        Scaling factor to adjust the windspeed data provided in the meteo_fl.
        Default is None.
    fetch_mode : int
        Switch to configure which wind-sheltering/fetch option to use. Default
        is 0.
    num_dir : Union[int, None]
        Number of wind direction reference points being read in. Default is
        None.
    wind_dir : Union[float, None]
        Wind direction reference points (degrees) being read in. Default is
        None.
    fetch_scale : Union[float, None]
        Direction specific wind-sheltering scaling factors. Default is None.

    Examples
    --------
    >>> from glmpy import NMLMeteorology
    >>> meteorology = NMLMeteorology()
    >>> my_meteorology = {
    >>>     'met_sw': True,
    >>>     'lw_type': 'LW_IN',
    >>>     'rain_sw': False,
    >>>     'atm_stab': 0,
    >>>     'fetch_mode': 0,
    >>>     'rad_mode': 1,
    >>>     'albedo_mode': 1,
    >>>     'cloud_mode': 4,
    >>>     'subdaily': True,
    >>>     'meteo_fl': 'bcs/met_hourly.csv',
    >>>     'wind_factor': 0.9,
    >>>     'ce': 0.0013,
    >>>     'ch': 0.0013,
    >>>     'cd': 0.0013,
    >>>     'catchrain': True,
    >>>     'rain_threshold': 0.001,
    >>>     'runoff_coeff': 0.0,
    >>> }
    >>> meteorology.set_attributes(my_meteorology)
    >>> print(meteorology)
    """

    def __init__(self):
        self.met_sw: bool = True
        self.meteo_fl: Union[str, None] = None
        self.subdaily: Union[bool, None] = None
        self.time_fmt: Union[str, None] = None
        self.rad_mode: Union[int, None] = None
        self.albedo_mode: Union[int, None] = None
        self.sw_factor: Union[float, None] = None
        self.lw_type: Union[str, None] = None
        self.cloud_mode: Union[int, None] = None
        self.lw_factor: Union[float, None] = None
        self.atm_stab: Union[int, None] = None
        self.rh_factor: Union[float, None] = None
        self.at_factor: Union[float, None] = None
        self.ce: Union[float, None] = 0.0013
        self.ch: Union[float, None] = 0.0013
        self.rain_sw: Union[bool, None] = None
        self.rain_factor: Union[float, None] = None
        self.catchrain: Union[bool, None] = None
        self.rain_threshold: Union[float, None] = None
        self.runoff_coeff: Union[float, None] = None
        self.cd: Union[float, None] = 0.0013
        self.wind_factor: Union[float, None] = None
        self.fetch_mode: int = 0
        self.num_dir: Union[int, None] = None
        self.wind_dir: Union[float, None] = None
        self.fetch_scale: Union[float, None] = None

    def __str__(self):
        """Return the string representation of the NMLMeteorology object.

        Returns a formatted string of the NMLMeteorology configution options
        and values.

        Returns
        -------
        str
            String representation of the NMLMeteorology object.

        Examples
        --------
        >>> from glmpy import NMLMeteorology
        >>> meteorology = NMLMeteorology()
        >>> my_meteorology = {
        >>>     'met_sw': True,
        >>>     'lw_type': 'LW_IN',
        >>>     'rain_sw': False,
        >>>     'atm_stab': 0,
        >>>     'fetch_mode': 0,
        >>>     'rad_mode': 1,
        >>>     'albedo_mode': 1,
        >>>     'cloud_mode': 4,
        >>>     'subdaily': True,
        >>>     'meteo_fl': 'bcs/met_hourly.csv',
        >>>     'wind_factor': 0.9,
        >>>     'ce': 0.0013,
        >>>     'ch': 0.0013,
        >>>     'cd': 0.0013,
        >>>     'catchrain': True,
        >>>     'rain_threshold': 0.001,
        >>>     'runoff_coeff': 0.0,
        >>> }
        >>> meteorology.set_attributes(my_meteorology)
        >>> print(meteorology)
        """

        params = [
            (f"   met_sw = {self.fortran_bool_string(self.met_sw)}",
             self.met_sw),
            (f"   meteo_fl = '{self.meteo_fl}'", self.meteo_fl),
            (f"   subdaily = {self.fortran_bool_string(self.subdaily)}",
             self.subdaily),
            (f"   time_fmt = '{self.time_fmt}'", self.time_fmt),
            (f"   rad_mode = {self.rad_mode}", self.rad_mode),
            (f"   albedo_mode = {self.albedo_mode}", self.albedo_mode),
            (f"   sw_factor = {self.sw_factor}", self.sw_factor),
            (f"   lw_type = '{self.lw_type}'", self.lw_type),
            (f"   cloud_mode = {self.cloud_mode}", self.cloud_mode),
            (f"   lw_factor = {self.lw_factor}", self.lw_factor),
            (f"   atm_stab = {self.atm_stab}", self.atm_stab),
            (f"   rh_factor = {self.rh_factor}", self.rh_factor),
            (f"   at_factor = {self.at_factor}", self.at_factor),
            (f"   ce = {self.ce}", self.ce),
            (f"   ch = {self.ch}", self.ch),
            (f"   rain_sw = {self.fortran_bool_string(self.rain_sw)}",
             self.rain_sw),
            (f"   rain_factor = {self.rain_factor}", self.rain_factor),
            (f"   catchrain = {self.fortran_bool_string(self.catchrain)}",
                self.catchrain),
            (f"   rain_threshold = {self.rain_threshold}",
                self.rain_threshold),
            (f"   runoff_coeff = {self.runoff_coeff}", self.runoff_coeff),
            (f"   cd = {self.cd}", self.cd),
            (f"   wind_factor = {self.wind_factor}", self.wind_factor),
            (f"   fetch_mode = {self.fetch_mode}", self.fetch_mode),
            (f"   num_dir = {self.num_dir}", self.num_dir),
            (f"   wind_dir = {self.wind_dir}", self.wind_dir),
            (f"   fetch_scale = {self.fetch_scale}", self.fetch_scale),
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
        Switch to configure the approach to light penetration. Default is 1.
    Kw : Union[float, None]
        Light extinction coefficient. Default is None
    Kw_file : Union[str, None]
        Name of file with Kw time-series included. Default is None.
    n_bands : Union[int, None]
        Number of light bandwidths to simulate. Default is 4.
    light_extc : Union[List[float], None]
        Comma-separated list of light extinction coefficients for each
        waveband. Default is None.
    energy_frac : Union[List[float], None]
        Comma-separated list of energy fraction captured by each waveband.
        Default is None.
    Benthic_Imin : Union[float, None]
        Critical fraction of incident light reaching the benthos. Default is
        None.

    Examples
    --------
    >>> from glmpy import NMLLight
    >>> light = NMLLight()
    >>> my_light = {
    >>>     'light_mode': 0,
    >>>     'Kw': 0.57,
    >>>     'n_bands': 4,
    >>>     'light_extc': [1.0, 0.5, 2.0, 4.0],
    >>>     'energy_frac': [0.51, 0.45, 0.035, 0.005],
    >>>     'Benthic_Imin': 10
    >>> }
    >>> light.set_attributes(my_light)
    >>> print(light)
    """

    def __init__(self):
        self.light_mode: int = 1
        self.Kw: Union[float, None] = None
        self.Kw_file: Union[str, None] = None
        self.n_bands: Union[int, None] = 4
        self.light_extc: Union[List[float], None] = None
        self.energy_frac: Union[List[float], None] = None
        self.Benthic_Imin: Union[float, None] = None

    def __str__(self):
        """Return the string representation of the NMLLight object.

        Returns a formatted string of the NMLLight configution options
        and values.

        Returns
        -------
        str
            String representation of the NMLLight object.

        Examples
        --------
        >>> from glmpy import NMLLight
        >>> light = NMLLight()
        >>> my_light = {
        >>>     'light_mode': 0,
        >>>     'Kw': 0.57,
        >>>     'n_bands': 4,
        >>>     'light_extc': [1.0, 0.5, 2.0, 4.0],
        >>>     'energy_frac': [0.51, 0.45, 0.035, 0.005],
        >>>     'Benthic_Imin': 10
        >>> }
        >>> light.set_attributes(my_light)
        >>> print(light)
        """
        params = [
            (f"   light_mode = {self.light_mode}", self.light_mode),
            (f"   Kw = {self.Kw}", self.Kw),
            (f"   n_bands = {self.n_bands}", self.n_bands),
            (f"   light_extc = {self.comma_sep_list(self.light_extc)}",
             self.light_extc),
            (f"   energy_frac = {self.comma_sep_list(self.energy_frac)}",
             self.energy_frac,),
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
    AP : Union[float, None]
        Atmospheric pressure (hPa). Default is None.
    Oz : Union[float, None]
        Ozone concentration (atm-cm). Default is None.
    WatVap : Union[float, None]
        Total Precipitable water vapor (atm-cm). Default is None.
    AOD500 : Union[float, None]
        Dimensionless Aerosol Optical Depth at wavelength 500 nm. Default is
        None.
    AOD380 : Union[float, None]
        Dimensionless Aerosol Optical Depth at wavelength 380 nm. Default is
        None.
    Albedo : Union[float, None]
        Albedo of the surface used for Bird Model insolation calculation.
        Default is 0.2.

    Examples
    --------
    >>> from glmpy import NMLBirdModel
    >>> bird_model = NMLBirdModel()
    >>> my_bird_model = {
    >>>     'AP': 973,
    >>>     'Oz': 0.279,
    >>>     'WatVap': 1.1,
    >>>     'AOD500': 0.033,
    >>>     'AOD380': 0.038,
    >>>     'Albedo': 0.2
    >>> }
    >>> bird_model.set_attributes(my_bird_model)
    >>> print(bird_model)
    """

    def __init__(self):
        self.AP: Union[float, None]= None
        self.Oz: Union[float, None]= None
        self.WatVap: Union[float, None]= None
        self.AOD500: Union[float, None]= None
        self.AOD380: Union[float, None]= None
        self.Albedo: Union[float, None]= 0.2

    def __str__(self):
        """Return the string representation of the NMLBirdModel object.

        Returns a formatted string of the NMLBirdModel configution options
        and values.

        Returns
        -------
        str
            String representation of the NMLBirdModel object.

        Examples
        --------
        >>> from glmpy import NMLBirdModel
        >>> bird_model = NMLBirdModel()
        >>> my_bird_model = {
        >>>     'AP': 973,
        >>>     'Oz': 0.279,
        >>>     'WatVap': 1.1,
        >>>     'AOD500': 0.033,
        >>>     'AOD380': 0.038,
        >>>     'Albedo': 0.2
        >>> }
        >>> bird_model.set_attributes(my_bird_model)
        >>> print(bird_model)
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
        Number of inflows to be simulated in this simulation. Default is 0.
    names_of_strms : Union[List[str], None]
        Names of each inflow.
    subm_flag : Union[List[bool], None]
        Switch indicating if the inflow I is entering as a submerged input.
        Default is [False].
    strm_hf_angle : Union[List[float], None]
        Angle describing the width of an inflow river channel ("half angle").
        Default is None.
    strmbd_slope : Union[List[float], None]
        Slope of the streambed / river thalweg for each river (degrees).
        Default is None.
    strmbd_drag : Union[List[float], None]
        Drag coefficient of the river inflow thalweg, to calculate entrainment
        during insertion. Default is None.
    coef_inf_entrain : Union[List[float], None]
        Default is None.
    inflow_factor : Union[List[float], None]
        Scaling factor that can be applied to adjust the provided input data.
        Default is 1.0.
    inflow_fl : Union[List[str], None]
        Filename(s) of the inflow CSV boundary condition files. Default is None.
    inflow_varnum : int
        Number of variables being listed in the columns of inflow_fl
        (comma-separated list). Default is 0.
    inflow_vars : Union[List[str], None]
        Names of the variables in the inflow_fl. Default is None.
    time_fmt : Union[str, None]
        Time format of the 1st column in the inflow_fl. Default is
        'YYYY-MM-DD hh:mm:ss'.

    Examples
    --------
    >>> from glmpy import NMLInflows
    >>> inflows = NMLInflows()
    >>> my_inflows = {
    >>>     'num_inflows': 6,
    >>>     'names_of_strms': ['Inflow1','Inflow2','Inflow3','Inflow4','Inflow5','Inflow6'],
    >>>     'subm_flag': [False, False, False, True, False, False],
    >>>     'strm_hf_angle': [85.0, 85.0, 85.0, 85.0, 85.0, 85.0],
    >>>     'strmbd_slope': [4.0, 4.0, 4.0, 4.0, 4.0, 4.0],
    >>>     'strmbd_drag': [0.0160, 0.0160, 0.0160, 0.0160, 0.0160, 0.0160],
    >>>     'inflow_factor': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    >>>     'inflow_fl': ['bcs/inflow_1.csv', 'bcs/inflow_2.csv', 'bcs/inflow_3.csv', 'bcs/inflow_4.csv', 'bcs/inflow_5.csv', 'bcs/inflow_6.csv'],
    >>>     'inflow_varnum': 3,
    >>>     'inflow_vars': ['FLOW','TEMP','SALT'],
    >>>     'coef_inf_entrain': [0.0],
    >>>     'time_fmt': 'YYYY-MM-DD hh:mm:ss'
    >>> }
    >>> inflows.set_attributes(my_inflows)
    >>> print(inflows)
    """

    def __init__(self):
        self.num_inflows: int = 0
        self.names_of_strms: Union[List[str], None] = None
        self.subm_flag: Union[List[bool], None] = [False]
        self.strm_hf_angle: Union[List[float], None] = None
        self.strmbd_slope: Union[List[float], None] = None
        self.strmbd_drag: Union[List[float], None] = None
        self.coef_inf_entrain: Union[List[float], None] = None
        self.inflow_factor: Union[List[float], None] = 1.0
        self.inflow_fl: Union[List[str], None] = None
        self.inflow_varnum: int = 0
        self.inflow_vars: Union[List[str], None] = None
        self.time_fmt: Union[str, None] = 'YYYY-MM-DD hh:mm:ss'

    def __str__(self):
        """Return the string representation of the NMLInflows object.

        Returns a formatted string of the NMLInflows configution options
        and values.

        Returns
        -------
        str
            String representation of the NMLInflows object.

        Examples
        --------
        >>> from glmpy import NMLInflows
        >>> inflows = NMLInflows()
        >>> my_inflows = {
        >>>     'num_inflows': 6,
        >>>     'names_of_strms': ['Inflow1','Inflow2','Inflow3','Inflow4','Inflow5','Inflow6'],
        >>>     'subm_flag': [False, False, False, True, False, False],
        >>>     'strm_hf_angle': [85.0, 85.0, 85.0, 85.0, 85.0, 85.0],
        >>>     'strmbd_slope': [4.0, 4.0, 4.0, 4.0, 4.0, 4.0],
        >>>     'strmbd_drag': [0.0160, 0.0160, 0.0160, 0.0160, 0.0160, 0.0160],
        >>>     'inflow_factor': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        >>>     'inflow_fl': ['bcs/inflow_1.csv', 'bcs/inflow_2.csv', 'bcs/inflow_3.csv', 'bcs/inflow_4.csv', 'bcs/inflow_5.csv', 'bcs/inflow_6.csv'],
        >>>     'inflow_varnum': 3,
        >>>     'inflow_vars': ['FLOW','TEMP','SALT'],
        >>>     'coef_inf_entrain': [0.0],
        >>>     'time_fmt': 'YYYY-MM-DD hh:mm:ss'
        >>> }
        >>> inflows.set_attributes(my_inflows)
        >>> print(inflows)
        """
        params = [
            (f"   num_inflows = {self.num_inflows}", self.num_inflows),
            (f"   names_of_strms = {self.comma_sep_list(self.names_of_strms, True)}",
             self.names_of_strms),
            (f"   subm_flag = {self.comma_sep_list(self.fortran_bool_string(self.subm_flag))}",self.subm_flag),
            (f"   strm_hf_angle = {self.comma_sep_list(self.strm_hf_angle)}",
             self.strm_hf_angle),
            (f"   strmbd_slope = {self.comma_sep_list(self.strmbd_slope)}",
             self.strmbd_slope),
            (f"   strmbd_drag = {self.comma_sep_list(self.strmbd_drag)}",
             self.strmbd_drag),
            (f"   coef_inf_entrain = {self.comma_sep_list(self.coef_inf_entrain)}",
             self.coef_inf_entrain),
            (f"   inflow_factor = {self.comma_sep_list(self.inflow_factor)}",
             self.inflow_factor),
            (f"   inflow_fl = {self.comma_sep_list(self.inflow_fl, True)}",
             self.inflow_fl),
            (f"   inflow_varnum = {self.inflow_varnum}", self.inflow_varnum),
            (f"   inflow_vars = {self.comma_sep_list(self.inflow_vars, True)}",
             self.inflow_vars),
            (f"   time_fmt = '{self.time_fmt}'", self.time_fmt)
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
        included in this simulation. Default is 0.
    outflow_fl : Union[str, None]
        Filename of the file containing the outflow time-series.
    time_fmt : Union[str, None]
        Time format of the 1st column in the outflow_fl. Default is
        'YYYY-MM-DD hh:mm:ss'.
    outflow_factor : float
        Scaling factor used as a multiplier for outflows. Default is 1.0.
    outflow_thick_limit : Union[List[float], None]
        Maximum vertical limit of withdrawal entrainment. Default is None.
    single_layer_draw : Union[List[bool], None]
        Switch to only limit withdrawal entrainment and force outflows from
        layer at the outlet elevation height. Default is [False].
    flt_off_sw : Union[List[bool], None]
        Switch to indicate if the outflows are floating offtakes
        (taking water from near the surface). Default is None.
    outlet_type : int
        Switch to configure approach of each withdrawal. Default is 1.
    outl_elvs : Union[List[float], None]
        Outlet elevations (m). Default is [0].
    bsn_len_outl : Union[List[float], None]
        Basin length at the outlet height(s) (m). Default is None.
    bsn_wid_outl : Union[List[float], None]
        Basin width at the outlet heights (m). Default is None.
    seepage : Union[bool, None]
        Switch to enable the seepage of water from the lake bottom. Default is
        False.
    seepage_rate : Union[float, None]
        Seepage rate of water, or, soil hydraulic conductivity. Default is 0.0.
    crest_width : Union[float, None]
        Width of weir (at crest height) where lake overflows (m). Default is
        0.0.
    crest_factor : Union[float, None]
        Drag coefficient associated with the weir crest, used to compute the
        overflow discharge rate. Default is 0.0.

    Examples
    --------
    >>> from glmpy import NMLOutflows
    >>> outflows = NMLOutflows()
    >>> my_outflows = {
    >>>     'num_outlet': 1,
    >>>     'flt_off_sw': [False],
    >>>     'outlet_type': 1,
    >>>     'outl_elvs': [-215.5],
    >>>     'bsn_len_outl': [18000],
    >>>     'bsn_wid_outl': [11000],
    >>>     'outflow_fl': 'bcs/outflow.csv',
    >>>     'outflow_factor': [1.0],
    >>>     'seepage': True,
    >>>     'seepage_rate': 0.01
    >>> }
    >>> outflows.set_attributes(my_outflows)
    >>> print(outflows)
    """

    def __init__(self):
        self.num_outlet: int = 0
        self.outflow_fl: Union[str, None] = None
        self.flt_off_sw: Union[List[bool], None] = None
        self.time_fmt: Union[str, None] = 'YYYY-MM-DD hh:mm:ss'
        self.outflow_factor: List[float]  = [1.0]
        self.outflow_thick_limit: Union[List[float], None] = None
        self.single_layer_draw: Union[List[bool], None] = [False]
        self.flt_off_sw: Union[List[bool], None] = None
        self.outlet_type: int = 1
        self.outl_elvs: Union[List[float], None] = [0]
        self.bsn_len_outl: Union[List[float], None] = None
        self.bsn_wid_outl: Union[List[float], None] = None
        self.seepage: Union[bool, None] = False
        self.seepage_rate: Union[float, None] = 0.0
        self.crest_width: Union[float, None] = 0.0
        self.crest_factor: Union[float, None] = 0.0

    def __str__(self):
        """Return the string representation of the NMLOutflows object.

        Returns a formatted string of the NMLOutflows configution options
        and values.

        Returns
        -------
        str
            String representation of the NMLOutflows object.

        Examples
        --------
        >>> from glmpy import NMLOutflows
        >>> outflows = NMLOutflows()
        >>> my_outflows = {
        >>>     'num_outlet': 1,
        >>>     'flt_off_sw': [False],
        >>>     'outlet_type': 1,
        >>>     'outl_elvs': [-215.5],
        >>>     'bsn_len_outl': [18000],
        >>>     'bsn_wid_outl': [11000],
        >>>     'outflow_fl': 'bcs/outflow.csv',
        >>>     'outflow_factor': [1.0],
        >>>     'seepage': True,
        >>>     'seepage_rate': 0.01
        >>> }
        >>> outflows.set_attributes(my_outflows)
        >>> print(outflows)
        """
        params = [
            (f"   num_outlet = {self.num_outlet}", self.num_outlet),
            (f"   outflow_fl = '{self.outflow_fl}'", self.outflow_fl),
            (f"   time_fmt = '{self.time_fmt}'", self.time_fmt),
            (f"   outflow_factor = {self.comma_sep_list(self.outflow_factor)}",
             self.outflow_factor),
            (f"   outflow_thick_limit = {self.comma_sep_list(self.outflow_thick_limit)}",
             self.outflow_thick_limit),
            (f"   single_layer_draw = {self.comma_sep_list(self.fortran_bool_string(self.single_layer_draw))}",
             self.single_layer_draw),
             (f"   flt_off_sw = {self.comma_sep_list(self.fortran_bool_string(self.flt_off_sw))}",
             self.flt_off_sw),
            (f"   outlet_type = {self.outlet_type}", self.outlet_type),
            (f"   outl_elvs = {self.comma_sep_list(self.outl_elvs)}",
             self.outl_elvs),
            (f"   bsn_len_outl = {self.comma_sep_list(self.bsn_len_outl)}",
             self.bsn_len_outl),
            (f"   bsn_wid_outl = {self.comma_sep_list(self.bsn_wid_outl)}",
             self.bsn_wid_outl),
            (f"   seepage = {self.fortran_bool_string(self.seepage)}",
             self.seepage),
            (f"   seepage_rate = {self.seepage_rate}", self.seepage_rate),
            (f"   crest_width = {self.crest_width}", self.crest_width),
            (f"   crest_factor = {self.crest_factor}", self.crest_factor)
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

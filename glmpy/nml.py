from typing import List, Union


class NML:
    """Generate .nml files.

    `.nml` files contain the parameters required for running a simulation with
    the General Lake Model (GLM). The `NML` class combines string
    representations of each component of a `.nml` file, e.g., `&setup`, and
    `&morphometry`. The file can be saved to disk with the`write_nml()` method.

    Attributes
    ----------
    setup : str
        String representation of the `&glm_setup` component of the .nml file.
        See `NMLSetup`. Required for every GLM simulation.
    morphometry : str
        String representation of the `&morphometry` component of the .nml file.
        See `NMLMorphometry`. Required for every GLM simulation.
    time : str
        String representation of the `&time` component of the .nml file.
        See `NMLTime`. Required for every GLM simulation.
    init_profiles : str
        String representation of the `&init_profiles` component of the .nml
        file. See `NMLInitProfiles`. Required for every GLM simulation.
    mixing : Union[str, None]
        String representation of the `&mixing` component of the .nml file. See
        `NMLMixing`. Default is None.
    output : Union[str, None]
        String representation of the `&output` component of the .nml file. See
        `NMLOutput`. Default is None.
    meteorology : Union[str, None]
        String representation of the `&meteorology` component of the .nml file.
        See `NMLMeteorology`. Default is None.
    light : Union[str, None]
        String representation of the `&light` component of the .nml file.
        See `NMLLight`. Default is None.
    bird_model : Union[str, None]
        String representation of the `&bird_model` component of the .nml file.
        See `NMLBirdModel`. Default is None.
    inflows : Union[str, None]
        String representation of the `&inflows` component of the .nml file.
        See `NMLInflows`. Default is None.
    outflows : Union[str, None]
        String representation of the `&outflows` component of the .nml file.
        See `NMLOutflows`. Default is None.
    sediment : Union[str, None]
        String representation of the `&sediment` component of the .nml file.
        See `NMLSediment`. Default is None.
    ice_snow : Union[str, None]
        String representation of the `&ice_snow` component of the .nml file.
        See `NMLIceSnow`. Default is None.
    wq_setup : Union[str, None]
        String representation of the `&wq_setup` component of the .nml file.
        See `NMLWQSetup`. Default is None.

    Examples
    --------
    >>> from glmpy import nml
    >>> from glmpy import json
    Read a json file of GLM config data:
    >>> json = JSONToNML("sparkling_lake.json")
    For each NML block, get the attributes from the json file:
    >>> setup_dict = json.get_nml_attributes("&glm_setup")
    >>> morphometry_dict = json.get_nml_attributes("&morphometry")
    >>> time_dict = json.get_nml_attributes("&time")
    >>> init_profiles_dict = json.get_nml_attributes("&init_profiles")
    Initialise an instance of each NML block class and set the attributes:
    >>> setup = nml.NMLSetup()
    >>> setup.set_attributes(setup_dict)
    >>> morphometry=nml.NMLMorphometry()
    >>> morphometry.set_attributes(morphometry_dict)
    >>> time=nml.NMLTime()
    >>> time.set_attributes(time_dict)
    >>> init_profiles=nml.NMLInitProfiles()
    >>> init_profiles.set_attributes(init_profiles_dict)
    Initialise the NML class with the NML block instances:
    >>> nml = nml.NML(
    ...     setup=setup,
    ...     morphometry=morphometry,
    ...     time=time,
    ...     init_profiles=init_profiles
    ... )
    Write the .nml file:
    >>> nml.write_nml(nml_file_path="sparkling.nml")
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

    def write_nml(self, nml_file_path: str = "glm3.nml"):
        """Write a .nml file.

        Write the `NML` instance to file with the .nml extension.

        Parameters
        ----------
        nml_file_path : str
            File path to save .nml file, by default `glm3.nml`.

        Examples
        --------
        >>> nml.write_nml(nml_file_path="sparkling.nml")
        """

        def nml_output():
            """Returns a string representation of the .nml file.

            Constructs a string representation of the .nml file from
            `nml_block()`.

            Returns
            -------
            str
                the string representation of the .nml file

            Examples
            --------
            >>> nml_output()
            """

            config_string = ""

            if self.setup is not None:
                config_string += str(self.setup) + "\n"
            if self.mixing is not None:
                config_string += str(self.mixing) + "\n"
            if self.wq_setup is not None:
                config_string += str(self.wq_setup) + "\n"
            if self.morphometry is not None:
                config_string += str(self.morphometry) + "\n"
            if self.time is not None:
                config_string += str(self.time) + "\n"
            if self.output is not None:
                config_string += str(self.output) + "\n"
            if self.init_profiles is not None:
                config_string += str(self.init_profiles) + "\n"
            if self.light is not None:
                config_string += str(self.light) + "\n"
            if self.bird_model is not None:
                config_string += str(self.bird_model) + "\n"
            if self.sediment is not None:
                config_string += str(self.sediment) + "\n"
            if self.ice_snow is not None:
                config_string += str(self.ice_snow) + "\n"
            if self.meteorology is not None:
                config_string += str(self.meteorology) + "\n"
            if self.inflows is not None:
                config_string += str(self.inflows) + "\n"
            if self.outflows is not None:
                config_string += str(self.outflows) + "\n"
            return config_string

        with open(file=nml_file_path, mode="w") as file:
            file.write(nml_output())


class NMLBase:
    """Base class for each NML block class.

    Provides the `set_attributes()` method for assigning a dictionary of
    attributes to any NML block class.

    Attributes
    ----------
    attrs_dict : dict
        A dictionary containing the GLM configuration parameters as keys and the
        corresponding values to set.

    Examples
    --------
    >>> from glmpy import NMLBase
    >>> from glmpy import NMLMorphometry
    >>> morphometry_attrs={
    ...         "lake_name": "Example Lake'",
    ...         "latitude":  32,
    ...         "longitude": 35,
    ...         "crest_elev": -203.9,
    ...         "bsn_len": 21000,
    ...         "bsn_wid": 13000,
    ...         "max_layer_thick": 0.1,
    ...         "density_model": 1,
    ...         "bsn_vals": "3",
    ...         "H": [-252.9,  -251.9,  -250.9],
    ...         "A": [0,  9250000,  15200000,],
    ... }
    >>> morphometry = NMLMorphometry()
    >>> morphometry.set_attributes(attrs_dict=morphometry_attrs)
    """

    def set_attributes(self, attrs_dict: dict):
        """Set attributes for a NML block class.

        Set the attributes of any NML block class (e.g. `NMLSetup`, `NMLTime`)
        using a dictionary of attribute names and values.

        Parameters
        ----------
        attrs_dict : dict
            A dictionary containing the attribute names as keys and the
            corresponding values to set.

        Examples
        --------
        >>> from glmpy import NMLBase
        >>> from glmpy import NMLMorphometry
        >>> morphometry_attrs={
        ...         "lake_name": "Example Lake'",
        ...         "latitude":  32,
        ...         "longitude": 35,
        ...         "crest_elev": -203.9,
        ...         "bsn_len": 21000,
        ...         "bsn_wid": 13000,
        ...         "max_layer_thick": 0.1,
        ...         "density_model": 1,
        ...         "bsn_vals": "3",
        ...         "H": [-252.9,  -251.9,  -250.9],
        ...         "A": [0,  9250000,  15200000,],
        ... }
        >>> morphometry = NMLMorphometry()
        >>> morphometry.set_attributes(attrs_dict=morphometry_attrs)
        """

        for key, value in attrs_dict.items():
            setattr(self, key, value)

    @staticmethod
    def fortran_bool_string(
        bool_input: Union[bool, List[bool], None]
    ) -> Union[str, List[Union[str, None]], None]:
        """Python boolean to Fortran boolean string.

        Convert a Python boolean, or a list of Python booleans, to a Fortran
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
        inverted_commas: bool = False,
    ):
        """Convert a Python list to a NML formatted comma separated string.

        If the list_input is None, None is returned. If inverted_commas is
        True, the list items are returned as strings with inverted commas.

        Parameters
        ----------
        list_input : list
            A list of values.
        inverted_commas : bool
            If True, the list items are returned as strings with inverted
            commas.

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
            return (
                ", ".join([repr(str(item)) for item in list_input])
                if list_input
                else None
            )
        else:
            return (
                ", ".join([str(item) for item in list_input])
                if list_input
                else None
            )


class NMLSetup(NMLBase):
    """Define the `&glm_setup` block of a GLM model.

    The `&glm_setup` component is used to define properties of the vertical
    series of layers used by GLM to model a water body. Attributes are set
    using the `set_attributes()` method and returned as a formatted
    string using the `__str__()` method.

    Attributes
    ----------
    sim_name : Union[str, None]
        Title of simulation. Default is None.
    max_layers : Union[int, None]
        Maximum number of layers. Default is None.
    min_layer_vol : Union[float, None]
        Minimum layer volume. Default is None.
    min_layer_thick : Union[float, None]
        Minimum thickness of a layer (m). Default is None.
    max_layer_thick : Union[float, None]
        Maximum thickness of a layer (m). Default is None.
    density_model : Union[int, None]
        Switch to set the density equation. Default is None.
    non_avg : Union[bool, None]
        Switch to configure flow boundary condition temporal interpolation.
        Default is None.

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

    def __str__(self):
        """Return the string representation of the `NMLSetup` object.

        Returns a `.nml` formatted string of the `NMLSetup` attributes.

        Returns
        -------
        str
            String representation of the `NMLSetup` object.

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
            (
                f"   min_layer_thick = {self.min_layer_thick}",
                self.min_layer_thick,
            ),
            (
                f"   max_layer_thick = {self.max_layer_thick}",
                self.max_layer_thick,
            ),
            (f"   density_model = {self.density_model}", self.density_model),
            (
                f"   non_avg = {self.fortran_bool_string(self.non_avg)}",
                self.non_avg,
            ),
        ]
        return (
            "&glm_setup \n"
            + "\n".join(
                param_str
                for param_str, param_val in params
                if param_val is not None
            )
            + "\n/"
        )


class NMLMorphometry(NMLBase):
    """Define the `&morphometry` block of a GLM model.

    Used to configure the morphological parameters of the modelled water body.
    Attributes are set using the `set_attributes()` method and returned as a
    formatted string using the `__str__()` method.

    Attributes
    ----------
    lake_name : Union[str, None]
        Site name. Default is None.
    latitude : Union[float, None]
        Latitude, positive North. Default is None.
    longitude : Union[float, None]
        Longitude, positive East. Default is None.
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

    def __str__(self):
        """Return the string representation of the `NMLMorphometry` object.

        Returns a `.nml` formatted string of the `NMLMorphometry` attributes.

        Returns
        -------
        str
            String representation of the `NMLMorphometry` object.

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
            (f"   H = {self.comma_sep_list(self.H)}", self.H),
            (f"   A = {self.comma_sep_list(self.A)}", self.A),
        ]
        return (
            "&morphometry \n"
            + "\n".join(
                param_str
                for param_str, param_val in params
                if param_val is not None
            )
            + "\n/"
        )


class NMLMixing(NMLBase):
    """Define the `&mixing` block of a GLM model.

    Used to configure the mixing processes within the modelled water body.
    Attributes are set using the `set_attributes()` method and returned as a
    formatted string using the `__str__()` method.

    Attributes
    ----------
    surface_mixing : Union[int, None]
        Switch to select the options of the surface mixing model. Default is
        None.
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

    def __str__(self):
        """Return the string representation of the `NMLMixing` object.

        Returns a `.nml` formatted string of the `NMLMixing` attributes.

        Returns
        -------
        str
            String representation of the `NMLMixing` object.

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
        return (
            "&mixing \n"
            + "\n".join(
                param_str
                for param_str, param_val in params
                if param_val is not None
            )
            + "\n/"
        )


class NMLTime(NMLBase):
    """Define the `&time` block of a GLM model.

    Used to configure the temporal parameters of the model, e.g., simulation
    period, time step, and time zone. Attributes are set using the
    `set_attributes()` method and returned as a formatted string using the
    `__str__()` method.

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
    dt : Union[float, None]
        Time step (seconds). Default is None
    num_days : Union[int, None]
        Number of days to simulate. Default is None.
    timezone : Union[float, None]
        UTC time zone. Default is None.

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

    def __init__(
        self,
        timefmt: Union[int, None] = None,
        start: Union[str, None] = None,
        stop: Union[int, None] = None,
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

    def __str__(self):
        """Return the string representation of the `NMLTime` object.

        Returns a `.nml` formatted string of the `NMLTime` attributes.

        Returns
        -------
        str
            String representation of the `NMLTime` object.

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
        return (
            "&time \n"
            + "\n".join(
                param_str
                for param_str, param_val in params
                if param_val is not None
            )
            + "\n/"
        )


class NMLOutput(NMLBase):
    """Define the `&output` block of a GLM model.

    Used to configure how GLM saves the model outputs to file.  Attributes are
    set using the `set_attributes()` method and returned as a formatted string
    using the `__str__()` method.

    Attributes
    ----------
    out_dir : Union[str, None]
        Directory to write the output files. Default is None.
    out_fn : Union[str, None]
        Filename of the main NetCDF output file. Default is None.
    nsave : Union[int, None]
        Frequency to write to the NetCDF and CSV point files. Default is None.
    csv_lake_fname : Union[str, None]
        Filename for the daily summary file. Default is None
    csv_point_nlevs : Union[float, None]
        Number of specific level/depth csv files to be created. Default is
        None.
    csv_point_fname : Union[str, None]
        Name to be appended to specified depth CSV files. Default is None.
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
    csv_outlet_nvars : Union[int, None]
        Number of variables to be written into the outlet file(s). Default is
        None.
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

    def __init__(
        self,
        out_dir: Union[str, None] = None,
        out_fn: Union[str, None] = None,
        nsave: Union[int, None] = None,
        csv_lake_fname: Union[str, None] = None,
        csv_point_nlevs: Union[float, None] = None,
        csv_point_fname: Union[str, None] = None,
        csv_point_frombot: Union[List[float], None] = None,
        csv_point_at: Union[List[float], None] = None,
        csv_point_nvars: Union[int, None] = None,
        csv_point_vars: Union[List[str], None] = None,
        csv_outlet_allinone: bool = False,
        csv_outlet_fname: Union[str, None] = None,
        csv_outlet_nvars: Union[int, None] = None,
        csv_outlet_vars: Union[List[str], None] = None,
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

    def __str__(self):
        """Return the string representation of the `NMLOutput` object.

        Returns a `.nml` formatted string of the `NMLOutput` attributes.

        Returns
        -------
        str
            String representation of the `NMLOutput` object.

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
                f"   csv_point_frombot = {self.comma_sep_list(self.csv_point_frombot)}",
                self.csv_point_frombot,
            ),
            (
                f"   csv_point_at = {self.comma_sep_list(self.csv_point_at)}",
                self.csv_point_at,
            ),
            (
                f"   csv_point_nvars = {self.csv_point_nvars}",
                self.csv_point_nvars,
            ),
            (
                f"   csv_point_vars = {self.comma_sep_list(self.csv_point_vars, True)}",
                self.csv_point_vars,
            ),
            (
                f"   csv_outlet_allinone = {self.fortran_bool_string(self.csv_outlet_allinone)}",
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
                f"   csv_outlet_vars = {self.comma_sep_list(self.csv_outlet_vars, True)}",
                self.csv_outlet_vars,
            ),
            (
                f"   csv_ovrflw_fname = '{self.csv_ovrflw_fname}'",
                self.csv_ovrflw_fname,
            ),
        ]
        return (
            "&output \n"
            + "\n".join(
                param_str
                for param_str, param_val in params
                if param_val is not None
            )
            + "\n/"
        )


class NMLInitProfiles(NMLBase):
    """Define the `&init_profiles` block of a GLM model.

    Used to configure the initial state of various water quality variables at
    specific depths in the water body. Attributes are set using the
    `set_attributes()` method and returned as a formatted string using the
    `__str__()` method.

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
        Default is None.
    wq_names : Union[List[str], None]
        Names of non GLM (ie FABM or AED2) variables to be initialised.
        Default is None.
    wq_init_vals : Union[List[str], None]
        Array of WQ variable initial data (rows = vars; cols = depths).
        Default is None.

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

    def __init__(
        self,
        lake_depth: Union[float, None] = None,
        num_depths: Union[int, None] = None,
        the_depths: Union[List[float], None] = None,
        the_temps: Union[List[float], None] = None,
        the_sals: Union[List[float], None] = None,
        num_wq_vars: Union[int, None] = None,
        wq_names: Union[List[str], None] = None,
        wq_init_vals: Union[List[float], None] = None,
    ):
        self.lake_depth = lake_depth
        self.num_depths = num_depths
        self.the_depths = the_depths
        self.the_temps = the_temps
        self.the_sals = the_sals
        self.num_wq_vars = num_wq_vars
        self.wq_names = wq_names
        self.wq_init_vals = wq_init_vals

    def __str__(self):
        """Return the string representation of the `NMLInitProfiles` object.

        Returns a `.nml` formatted string of the `NMLInitProfiles` attributes.

        Returns
        -------
        str
            String representation of the `NMLInitProfiles` object.

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
            (
                f"   the_depths = {self.comma_sep_list(self.the_depths)}",
                self.the_depths,
            ),
            (
                f"   the_temps = {self.comma_sep_list(self.the_temps)}",
                self.the_temps,
            ),
            (
                f"   the_sals = {self.comma_sep_list(self.the_sals)}",
                self.the_sals,
            ),
            (f"   num_wq_vars = {self.num_wq_vars}", self.num_wq_vars),
            (
                f"   wq_names = {self.comma_sep_list(self.wq_names, True)}",
                self.wq_names,
            ),
            (
                f"   wq_init_vals = {self.comma_sep_list(self.wq_init_vals)}",
                self.wq_init_vals,
            ),
        ]
        return (
            "&init_profiles \n"
            + "\n".join(
                param_str
                for param_str, param_val in params
                if param_val is not None
            )
            + "\n/"
        )


class NMLMeteorology(NMLBase):
    """Define the `&meteorology` block of a GLM model.

    Used to configure the meteorological dynamics of the model, e.g., rainfall,
    air temperature, and incoming radiation. Attributes are set using  the
    `set_attributes()` method and returned as a formatted string using the
    `__str__()` method.

    Attributes
    ----------
    met_sw : Union[bool, None]
        Switch to enable the surface heating module. Default is None.
    meteo_fl : Union[str, None]
        Filename of the meterological file. Default is None.
    subdaily : Union[bool, None]
        Switch to indicate the meteorological data is provided with sub-daily
        resolution, at an interval equivalent to Δt. Default is None.
    time_fmt : Union[str, None]
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
        None.
    ch : Union[float, None]
        Bulk aerodynamic transfer coefficient for sensible heat flux. Default
        is None.
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
    cd : Union[float, None]
        Bulk aerodynamic transfer coefficient for momentum. Default is None.
    wind_factor : Union[float, None]
        Scaling factor to adjust the windspeed data provided in the meteo_fl.
        Default is None.
    fetch_mode : Union[int, None]
        Switch to configure which wind-sheltering/fetch option to use. Default
        is None.
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
    >>>     'runoff_coef': 0.0,
    >>> }
    >>> meteorology.set_attributes(my_meteorology)
    >>> print(meteorology)
    """

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
        self.num_dir = num_dir
        self.wind_dir = wind_dir
        self.fetch_scale = fetch_scale

    def __str__(self):
        """Return the string representation of the `NMLMeteorology` object.

        Returns a `.nml` formatted string of the `NMLMeteorology` attributes.

        Returns
        -------
        str
            String representation of the `NMLMeteorology` object.

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
        >>>     'runoff_coef': 0.0,
        >>> }
        >>> meteorology.set_attributes(my_meteorology)
        >>> print(meteorology)
        """

        params = [
            (
                f"   met_sw = {self.fortran_bool_string(self.met_sw)}",
                self.met_sw,
            ),
            (f"   meteo_fl = '{self.meteo_fl}'", self.meteo_fl),
            (
                f"   subdaily = {self.fortran_bool_string(self.subdaily)}",
                self.subdaily,
            ),
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
            (
                f"   rain_sw = {self.fortran_bool_string(self.rain_sw)}",
                self.rain_sw,
            ),
            (f"   rain_factor = {self.rain_factor}", self.rain_factor),
            (
                f"   catchrain = {self.fortran_bool_string(self.catchrain)}",
                self.catchrain,
            ),
            (
                f"   rain_threshold = {self.rain_threshold}",
                self.rain_threshold,
            ),
            (f"   runoff_coef = {self.runoff_coef}", self.runoff_coef),
            (f"   cd = {self.cd}", self.cd),
            (f"   wind_factor = {self.wind_factor}", self.wind_factor),
            (f"   fetch_mode = {self.fetch_mode}", self.fetch_mode),
            (f"   num_dir = {self.num_dir}", self.num_dir),
            (f"   wind_dir = {self.wind_dir}", self.wind_dir),
            (f"   fetch_scale = {self.fetch_scale}", self.fetch_scale),
        ]
        return (
            "&meteorology \n"
            + "\n".join(
                param_str
                for param_str, param_val in params
                if param_val is not None
            )
            + "\n/"
        )


class NMLLight(NMLBase):
    """Define the `&light` block of a GLM model.

    Used to configure the how light will penetrates the water body. Attributes
    are set using the `set_attributes()` method and returned as a formatted
    string using the `__str__()` method.

    Attributes
    ----------
    light_mode : Union[int, None]
        Switch to configure the approach to light penetration. Default is None.
    Kw : Union[float, None]
        Light extinction coefficient. Default is None
    Kw_file : Union[str, None]
        Name of file with Kw time-series included. Default is None.
    n_bands : Union[int, None]
        Number of light bandwidths to simulate. Default is None.
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

    def __init__(
        self,
        light_mode: Union[int, None] = None,
        Kw: Union[float, None] = None,
        Kw_file: Union[str, None] = None,
        n_bands: Union[int, None] = None,
        light_extc: Union[List[float], None] = None,
        energy_frac: Union[List[float], None] = None,
        Benthic_Imin: Union[float, None] = None,
    ):
        self.light_mode = light_mode
        self.Kw = Kw
        self.Kw_file = Kw_file
        self.n_bands = n_bands
        self.light_extc = light_extc
        self.energy_frac = energy_frac
        self.Benthic_Imin = Benthic_Imin

    def __str__(self):
        """Return the string representation of the `NMLLight` object.

        Returns a `.nml` formatted string of the `NMLLight` attributes.

        Returns
        -------
        str
            String representation of the `NMLLight` object.

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
            (
                f"   light_extc = {self.comma_sep_list(self.light_extc)}",
                self.light_extc,
            ),
            (
                f"   energy_frac = {self.comma_sep_list(self.energy_frac)}",
                self.energy_frac,
            ),
            (f"   Benthic_Imin = {self.Benthic_Imin}", self.Benthic_Imin),
        ]
        return (
            "&light \n"
            + "\n".join(
                param_str
                for param_str, param_val in params
                if param_val is not None
            )
            + "\n/"
        )


class NMLBirdModel(NMLBase):
    """Define the `&bird_model` block of a GLM simulation configuration.

    Used to configure surface irradiance based on the Bird Clear Sky Model
    (BCSM) (Bird, 1984). Attributes are set using the `set_attributes()` method
    and returned as a formatted string using the `__str__()` method.

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
        Default is None.

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

    def __str__(self):
        """Return the string representation of the `NMLBirdModel` object.

        Returns a `.nml` formatted string of the NMLBirdModel attributes.

        Returns
        -------
        str
            String representation of the `NMLBirdModel` object.

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
        return (
            "&bird_model \n"
            + "\n".join(
                param_str
                for param_str, param_val in params
                if param_val is not None
            )
            + "\n/"
        )


class NMLInflows(NMLBase):
    """Define the `&inflow` block of a GLM model.

    Used to configure the number/type of water inflows. Attributes are set
    using the `set_attributes()` method and returned as a formatted string
    using the `__str__()` method.

    Attributes
    ----------
    num_inflows : Union[int, None]
        Number of inflows to be simulated in this simulation. Default is None.
    names_of_strms : Union[List[str], None]
        Names of each inflow.
    subm_flag : Union[List[bool], None]
        Switch indicating if the inflow I is entering as a submerged input.
        Default is None.
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
        Default is None.
    inflow_fl : Union[List[str], None]
        Filename(s) of the inflow CSV boundary condition files. Default is None.
    inflow_varnum : Union[int, None]
        Number of variables being listed in the columns of inflow_fl
        (comma-separated list). Default is None.
    inflow_vars : Union[List[str], None]
        Names of the variables in the inflow_fl. Default is None.
    time_fmt : Union[str, None]
        Time format of the 1st column in the inflow_fl. Default is
        None.

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

    def __init__(
        self,
        num_inflows: Union[int, None] = None,
        names_of_strms: Union[List[str], None] = None,
        subm_flag: Union[List[bool], None] = None,
        strm_hf_angle: Union[List[float], None] = None,
        strmbd_slope: Union[List[float], None] = None,
        strmbd_drag: Union[List[float], None] = None,
        coef_inf_entrain: Union[List[float], None] = None,
        inflow_factor: Union[List[float], None] = None,
        inflow_fl: Union[List[str], None] = None,
        inflow_varnum: Union[int, None] = None,
        inflow_vars: Union[List[str], None] = None,
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

    def __str__(self):
        """Return the string representation of the `NMLInflows` object.

        Returns a `.nml` formatted string of the `NMLInflows` attributes.

        Returns
        -------
        str
            String representation of the `NMLInflows` object.

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
            (
                f"   names_of_strms = {self.comma_sep_list(self.names_of_strms, True)}",
                self.names_of_strms,
            ),
            (
                f"   subm_flag = {self.comma_sep_list(self.fortran_bool_string(self.subm_flag))}",
                self.subm_flag,
            ),
            (
                f"   strm_hf_angle = {self.comma_sep_list(self.strm_hf_angle)}",
                self.strm_hf_angle,
            ),
            (
                f"   strmbd_slope = {self.comma_sep_list(self.strmbd_slope)}",
                self.strmbd_slope,
            ),
            (
                f"   strmbd_drag = {self.comma_sep_list(self.strmbd_drag)}",
                self.strmbd_drag,
            ),
            (
                f"   coef_inf_entrain = {self.comma_sep_list(self.coef_inf_entrain)}",
                self.coef_inf_entrain,
            ),
            (
                f"   inflow_factor = {self.comma_sep_list(self.inflow_factor)}",
                self.inflow_factor,
            ),
            (
                f"   inflow_fl = {self.comma_sep_list(self.inflow_fl, True)}",
                self.inflow_fl,
            ),
            (f"   inflow_varnum = {self.inflow_varnum}", self.inflow_varnum),
            (
                f"   inflow_vars = {self.comma_sep_list(self.inflow_vars, True)}",
                self.inflow_vars,
            ),
            (f"   time_fmt = '{self.time_fmt}'", self.time_fmt),
        ]
        return (
            "&inflows \n"
            + "\n".join(
                param_str
                for param_str, param_val in params
                if param_val is not None
            )
            + "\n/"
        )


class NMLOutflows(NMLBase):
    """Define the `&outflow` block of a GLM model.

    Used to configure the number/type of water outflows. Attributes are set
    using the `set_attributes()` method and returned as a formatted string
    using the `__str__()` method.

    Attributes
    ----------
    num_outlet : Union[int, None]
        Number of outflows (including withdrawals, outlets or offtakes) to be
        included in this simulation. Default is None.
    outflow_fl : Union[str, None]
        Filename of the file containing the outflow time-series. Default is
        None.
    time_fmt : Union[str, None]
        Time format of the 1st column in the outflow_fl. Default is
        None.
    outflow_factor : Union[float, None]
        Scaling factor used as a multiplier for outflows. Default is None.
    outflow_thick_limit : Union[List[float], None]
        Maximum vertical limit of withdrawal entrainment. Default is None.
    single_layer_draw : Union[List[bool], None]
        Switch to only limit withdrawal entrainment and force outflows from
        layer at the outlet elevation height. Default is None.
    flt_off_sw : Union[List[bool], None]
        Switch to indicate if the outflows are floating offtakes
        (taking water from near the surface). Default is None.
    outlet_type : Union[List[int], None]
        Switch to configure approach of each withdrawal. Default is None.
    outl_elvs : Union[List[float], None]
        Outlet elevations (m). Default is [0].
    bsn_len_outl : Union[List[float], None]
        Basin length at the outlet height(s) (m). Default is None.
    bsn_wid_outl : Union[List[float], None]
        Basin width at the outlet heights (m). Default is None.
    seepage : Union[bool, None]
        Switch to enable the seepage of water from the lake bottom. Default is
        None.
    seepage_rate : Union[float, None]
        Seepage rate of water, or, soil hydraulic conductivity. Default is
        None.
    crest_width : Union[float, None]
        Width of weir (at crest height) where lake overflows (m). Default is
        None.
    crest_factor : Union[float, None]
        Drag coefficient associated with the weir crest, used to compute the
        overflow discharge rate. Default is None.

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

    def __init__(
        self,
        num_outlet: Union[int, None] = None,
        outflow_fl: Union[str, None] = None,
        time_fmt: Union[str, None] = None,
        outflow_factor: Union[List[float], None] = None,
        outflow_thick_limit: Union[List[float], None] = None,
        single_layer_draw: Union[List[bool], None] = None,
        flt_off_sw: Union[List[bool], None] = None,
        outlet_type: Union[List[int], None] = None,
        outl_elvs: Union[List[float], None] = None,
        bsn_len_outl: Union[List[float], None] = None,
        bsn_wid_outl: Union[List[float], None] = None,
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
        self.seepage = seepage
        self.seepage_rate = seepage_rate
        self.crest_width = crest_width
        self.crest_factor = crest_factor

    def __str__(self):
        """Return the string representation of the `NMLOutflows` object.

        Returns a `.nml` formatted string of the `NMLOutflows` attributes.

        Returns
        -------
        str
            String representation of the `NMLOutflows` object.

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
            (
                f"   outflow_factor = {self.comma_sep_list(self.outflow_factor)}",
                self.outflow_factor,
            ),
            (
                f"   outflow_thick_limit = {self.comma_sep_list(self.outflow_thick_limit)}",
                self.outflow_thick_limit,
            ),
            (
                f"   single_layer_draw = {self.comma_sep_list(self.fortran_bool_string(self.single_layer_draw))}",
                self.single_layer_draw,
            ),
            (
                f"   flt_off_sw = {self.comma_sep_list(self.fortran_bool_string(self.flt_off_sw))}",
                self.flt_off_sw,
            ),
            (f"   outlet_type = {self.outlet_type}", self.outlet_type),
            (
                f"   outl_elvs = {self.comma_sep_list(self.outl_elvs)}",
                self.outl_elvs,
            ),
            (
                f"   bsn_len_outl = {self.comma_sep_list(self.bsn_len_outl)}",
                self.bsn_len_outl,
            ),
            (
                f"   bsn_wid_outl = {self.comma_sep_list(self.bsn_wid_outl)}",
                self.bsn_wid_outl,
            ),
            (
                f"   seepage = {self.fortran_bool_string(self.seepage)}",
                self.seepage,
            ),
            (f"   seepage_rate = {self.seepage_rate}", self.seepage_rate),
            (f"   crest_width = {self.crest_width}", self.crest_width),
            (f"   crest_factor = {self.crest_factor}", self.crest_factor),
        ]
        return (
            "&outflows \n"
            + "\n".join(
                param_str
                for param_str, param_val in params
                if param_val is not None
            )
            + "\n/"
        )


class NMLSediment(NMLBase):
    """Define the `&sediment` block of a GLM model.

    Used to configure the thermal properties of the soil-sediment. Attributes
    are set using the `set_attributes()` method and returned as a formatted
    string using the `__str__()` method.

    Attributes
    ----------
    sed_heat_Ksoil : Union[float, None]
        Heat conductivity of soil/sediment. Default is None.
    sed_temp_depth : Union[float, None]
        Depth of soil/sediment layer below the lake bottom, used for heat flux
        calculation. Default is None.
    sed_temp_mean : Union[List[float], None]
        Annual mean sediment temperature. Default is None.
    sed_temp_amplitude : Union[List[float], None]
        Amplitude of temperature variation experienced in the sediment over one
        year. Default is None.
    sed_temp_peak_doy : Union[List[int], None]
        Day of the year where the sediment temperature peaks. Default is None.
    benthic_mode : Union[int, None]
        Switch to configure which mode of benthic interaction to apply. Default
        is None.
    n_zones : Union[int, None]
        Number of sediment zones to simulate. Default is None.
    zone_heights : Union[List[float], None]
        Upper height of zone boundary. Default is None.
    sed_reflectivity : Union[List[float], None]
        Sediment reflectivity. Default is None.
    sed_roughness : Union[List[float], None]
        Sediment roughness. Default is None.

    Examples
    --------
    >>> from glmpy import NMLSediment
    >>> sediment = NMLSediment()
    >>> my_sediment = {
    >>>     'sed_heat_Ksoil': 0.0,
    >>>     'sed_temp_depth': 0.2,
    >>>     'sed_temp_mean': [5,10,20],
    >>>     'sed_temp_amplitude': [6,8,10],
    >>>     'sed_temp_peak_doy': [80, 70, 60],
    >>>     'benthic_mode': 1,
    >>>     'n_zones': 3,
    >>>     'zone_heights': [10., 20., 50.],
    >>>     'sed_reflectivity': [0.1, 0.01, 0.01],
    >>>     'sed_roughness': [0.1, 0.01, 0.01]
    >>> }
    >>> sediment.set_attributes(my_sediment)
    >>> print(sediment)
    """

    def __init__(
        self,
        sed_heat_Ksoil: Union[float, None] = None,
        sed_temp_depth: Union[float, None] = None,
        sed_temp_mean: Union[List[float], None] = None,
        sed_temp_amplitude: Union[List[float], None] = None,
        sed_temp_peak_doy: Union[List[int], None] = None,
        benthic_mode: Union[int, None] = None,
        n_zones: Union[int, None] = None,
        zone_heights: Union[List[float], None] = None,
        sed_reflectivity: Union[List[float], None] = None,
        sed_roughness: Union[List[float], None] = None,
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

    def __str__(self):
        """Return the string representation of the `NMLSediment` object.

        Returns a `.nml` formatted string of the NMLSediment attributes.

        Returns
        -------
        str
            String representation of the `NMLSediment` object.

        Examples
        --------
        >>> from glmpy import NMLSediment
        >>> sediment = NMLSediment()
        >>> my_sediment = {
        >>>     'sed_heat_Ksoil': 0.0,
        >>>     'sed_temp_depth': 0.2,
        >>>     'sed_temp_mean': [5,10,20],
        >>>     'sed_temp_amplitude': [6,8,10],
        >>>     'sed_temp_peak_doy': [80, 70, 60],
        >>>     'benthic_mode': 1,
        >>>     'n_zones': 3,
        >>>     'zone_heights': [10., 20., 50.],
        >>>     'sed_reflectivity': [0.1, 0.01, 0.01],
        >>>     'sed_roughness': [0.1, 0.01, 0.01]
        >>> }
        >>> sediment.set_attributes(my_sediment)
        >>> print(sediment)
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
            (
                f"   sed_temp_mean = {self.comma_sep_list(self.sed_temp_mean)}",
                self.sed_temp_mean,
            ),
            (
                f"   sed_temp_amplitude = {self.comma_sep_list(self.sed_temp_amplitude)}",
                self.sed_temp_amplitude,
            ),
            (
                f"   sed_temp_peak_doy = {self.comma_sep_list(self.sed_temp_peak_doy)}",
                self.sed_temp_peak_doy,
            ),
            (f"   benthic_mode = {self.benthic_mode}", self.benthic_mode),
            (f"   n_zones = {self.n_zones}", self.n_zones),
            (
                f"   zone_heights = {self.comma_sep_list(self.zone_heights)}",
                self.zone_heights,
            ),
            (
                f"   sed_reflectivity = {self.comma_sep_list(self.sed_reflectivity)}",
                self.sed_reflectivity,
            ),
            (
                f"   sed_roughness = {self.comma_sep_list(self.sed_roughness)}",
                self.sed_roughness,
            ),
        ]
        return (
            "&sediment \n"
            + "\n".join(
                param_str
                for param_str, param_val in params
                if param_val is not None
            )
            + "\n/"
        )


class NMLSnowIce(NMLBase):
    """Define the `&snowice` block of a GLM model.

    Used to configure formation of snow and ice cover on the simulated water
    body. Attributes are set using the `set_attributes()` method and returned
    as a formatted string using the `__str__()` method.

    Attributes
    ----------
    snow_albedo_factor : Union[float, None]
        Scaling factor used to as a multiplier to scale the snow/ice albedo
        estimate. Default is None.
    snow_rho_max : Union[float, None]
        Minimum snow density allowable. Default is None.
    snow_rho_min : Union[float, None]
        Maximum snow density allowable. Default is None.

    Examples
    --------
    >>> from glmpy import NMLSnowIce
    >>> snow_ice = NMLSnowIce()
    >>> my_snow_ice = {
    >>>        'snow_albedo_factor': 0.0,
    >>>        'snow_rho_min': 50,
    >>>        'snow_rho_max': 300
    >>>    }
    >>> snow_ice.set_attributes(my_snow_ice)
    >>> print(snow_ice)
    """

    def __init__(
        self,
        snow_albedo_factor: Union[float, None] = None,
        snow_rho_max: Union[float, None] = None,
        snow_rho_min: Union[float, None] = None,
    ):
        self.snow_albedo_factor = snow_albedo_factor
        self.snow_rho_max = snow_rho_max
        self.snow_rho_min = snow_rho_min

    def __str__(self):
        """Return the string representation of the `NMLSnowIce` object.

        Returns a `.nml` formatted string of the `NMLSnowIce` attributes.

        Returns
        -------
        str
            String representation of the `NMLSnowIce` object.

        Examples
        --------
        >>> from glmpy import NMLSnowIce
        >>> snow_ice = NMLSnowIce()
        >>> my_snow_ice = {
        >>>        'snow_albedo_factor': 0.0,
        >>>        'snow_rho_min': 50,
        >>>        'snow_rho_max': 300
        >>>    }
        >>> snow_ice.set_attributes(my_snow_ice)
        >>> print(snow_ice)
        """
        params = [
            (
                f"   snow_albedo_factor = {self.snow_albedo_factor}",
                self.snow_albedo_factor,
            ),
            (f"   snow_rho_max = {self.snow_rho_max}", self.snow_rho_max),
            (f"   snow_rho_min = {self.snow_rho_min}", self.snow_rho_min),
        ]
        return (
            "&snowice \n"
            + "\n".join(
                param_str
                for param_str, param_val in params
                if param_val is not None
            )
            + "\n/"
        )


class NMLWQSetup(NMLBase):
    """Define the `&wq_setup`  block of a GLM simulation configuration.

    Used to configure the water quality library selection, solution options,
    and benthic coupling mode. Attributes are set using the `set_attributes()`
    method and returned as a formatted string using the `__str__()` method.

    Attributes
    ----------
    wq_lib : Union[bool, str]
        Water quality model selection. Default is None.
    wq_nml_file : Union[str, None]
        Filename of WQ configuration file. Default is None.
    bioshade_feedback : Union[bool, None]
        Switch to enable Kw to be updated by the WQ model. Default is None.
    mobility_off : Union[bool, None]
        Switch to enable settling within the WQ model. Default is None.
    ode_method : Union[int, None]
        Method to use for ODE solution of water quality module. Default is
        None.
    split_factor : Union[float, None]
        Factor weighting implicit vs explicit numerical solution of the WQ
        model. Default is None.
    repair_state : Union[bool, None]
        Switch to correct negative or out of range WQ variables. Default is
        None.

    Examples
    --------
    >>> from glmpy import NMLWQSetup
    >>> wq_setup = NMLWQSetup()
    >>> my_wq_setup = {
    >>>     'wq_lib': 'aed2',
    >>>     'wq_nml_file': 'aed2/aed2.nml',
    >>>     'ode_method': 1,
    >>>     'split_factor': 1,
    >>>     'bioshade_feedback': True,
    >>>     'repair_state': True,
    >>>     'mobility_off': False
    >>> }
    >>> wq_setup.set_attributes(my_wq_setup)
    >>> print(wq_setup)
    """

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

    def __str__(self):
        """Return the string representation of the `NMLWQSetup` object.

        Returns a `.nml` formatted string of the `NMLWQSetup` attributes.

        Returns
        -------
        str
            String representation of the `NMLWQSetup` object.

        Examples
        --------
        >>> from glmpy import NMLWQSetup
        >>> wq_setup = NMLWQSetup()
        >>> my_wq_setup = {
        >>>     'wq_lib': 'aed2',
        >>>     'wq_nml_file': 'aed2/aed2.nml',
        >>>     'ode_method': 1,
        >>>     'split_factor': 1,
        >>>     'bioshade_feedback': True,
        >>>     'repair_state': True,
        >>>     'mobility_off': False
        >>> }
        >>> wq_setup.set_attributes(my_wq_setup)
        >>> print(wq_setup)
        """
        params = [
            (f"   wq_lib = '{self.wq_lib}'", self.wq_lib),
            (f"   wq_nml_file = '{self.wq_nml_file}'", self.wq_nml_file),
            (
                f"   bioshade_feedback = {self.fortran_bool_string(self.bioshade_feedback)}",
                self.bioshade_feedback,
            ),
            (
                f"   mobility_off = {self.fortran_bool_string(self.mobility_off)}",
                self.mobility_off,
            ),
            (f"   ode_method = {self.ode_method}", self.ode_method),
            (f"   split_factor = {self.split_factor}", self.split_factor),
            (
                f"   repair_state = {self.fortran_bool_string(self.repair_state)}",
                self.repair_state,
            ),
        ]
        return (
            "&wq_setup \n"
            + "\n".join(
                param_str
                for param_str, param_val in params
                if param_val is not None
            )
            + "\n/"
        )

import json

from typing import Union


class JSONToNML:
    """Supports the reading and parsing of GLM configuration blocks in a json
    format.

    The json file is read and parsed into a dictionary, which is then
    used to set the attributes of the corresponding NML class. The NML class
    is then converted to a string and returned.

    Attributes
    ----------
    json_file : str
        The path to the json file to be read.
    nml_file : str
        The path to the nml file to be written.

    Examples
    --------
    >>> from glmpy import JSONToNML
    >>> json_to_nml = JSONToNML("config.json")
    >>> json_to_nml.get_nml_attributes("glm_setup")
    """

    def __init__(self, json_file: str, nml_file: str = "sim.nml"):
        self.json_file = json_file
        self.nml_file = nml_file

    def read_json(self):
        """Reads the json file and returns a dictionary.

        Reads a json file of GLM configuration blocks and returns a dictionary.

        Parameters
        ----------
        None

        Examples
        --------
        >>> from glmpy import JSONToNML
        >>> json_to_nml = JSONToNML("config.json")
        >>> json_to_nml.read_json()
        """
        with open(self.json_file) as file:
            json_data = json.load(file)
        return json_data

    # def get_custom_morphometry_attributes(self):
    #     json_data = self.read_json()
    #     morphometry = NMLMorphometry()
    #     morphometry.set_attributes(json_data["morphometry"])
    #     return(str(morphometry))

    def get_nml_attributes(
        self, nml_block, custom_attributes: Union[dict, None] = None
    ):
        """Reads a GLM configuration block from a json file and returns a
        string.

        Reads a json file and finds the specified GLM configuration block. The
        attributes of the NML class corresponding to the GLM configuration block
        are set using the dictionary from the json file. The NML class is then
        converted to a string and returned.

        Parameters
        ----------
        nml_block : str
            The GLM configuration block to read from the json file. Must be one
            of the following: "glm_setup", "mixing", "morphometry",
            "time", "output", "init_profiles", "meteorology", "light",
            "bird_model", "inflows", "outflows", "sediment", "ice_snow",
            "wq_setup"

        custom_attributes : Union[dict, None]
            A dictionary of custom attributes that will be used to either,
            overwrite attributes read from the json file, or add missing
            attributes. Useful for setting attributes that require a calculation
            e.g. the volume of a water body. Default is None.

        Examples
        --------
        >>> from glmpy import JSONToNML
        >>> json_sim_config = JSONToNML("config.json")
        >>> json_sim_config.get_nml_attributes("morphometry")

        Use of the `custom_attributes` parameter:

        >>> from glmpy import JSONToNML
        >>> from glmpy import SimpleTruncatedPyramidWaterBody
        >>> json_config = JSONToNML("config.json")
        >>> calc_morph_attrs = SimpleTruncatedPyramidWaterBody(
        ...    height=json_config["simple_inputs"]["height"],
        ...    surface_width=json_config["simple_inputs"]["surface_width"],
        ...    surface_length=json_config["simple_inputs"]["surface_length"],
        ...    side_slope=json_config["simple_inputs"]["side_slope"],
        ... )
        >>> custom_attrs = {
        ...    "crest_elev": calc_morph_attrs.get_heights().pop(),
        ...    "bsn_vals": len(calc_morph_attrs.get_heights()),
        ...    "H":calc_morph_attrs.get_heights(),
        ...    "A":calc_morph_attrs.get_surface_areas()
        ... }
        >>> json_config.get_nml_attributes("morphometry", custom_attrs)
        """
        json_data = self.read_json()
        if nml_block == "glm_setup":
            glm_setup = NMLSetup()
            glm_setup.set_attributes(
                json_data["glm_setup"], custom=custom_attributes
            )
            return str(glm_setup)
        elif nml_block == "mixing":
            mixing = NMLMixing()
            mixing.set_attributes(
                json_data["mixing"], custom=custom_attributes
            )
            return str(mixing)
        elif nml_block == "morphometry":
            morphometry = NMLMorphometry()
            morphometry.set_attributes(
                json_data["morphometry"], custom=custom_attributes
            )
            return str(morphometry)
        elif nml_block == "time":
            time = NMLTime()
            time.set_attributes(json_data["time"], custom=custom_attributes)
            return str(time)
        elif nml_block == "output":
            output = NMLOutput()
            output.set_attributes(
                json_data["output"], custom=custom_attributes
            )
            return str(output)
        elif nml_block == "init_profiles":
            init_profiles = NMLInitProfiles()
            init_profiles.set_attributes(
                json_data["init_profiles"], custom=custom_attributes
            )
            return str(init_profiles)
        elif nml_block == "meteorology":
            meteorology = NMLMeteorology()
            meteorology.set_attributes(
                json_data["meteorology"], custom=custom_attributes
            )
            return str(meteorology)
        elif nml_block == "light":
            light = NMLLight()
            light.set_attributes(json_data["light"], custom=custom_attributes)
            return str(light)
        elif nml_block == "bird_model":
            bird_model = NMLBirdModel()
            bird_model.set_attributes(
                json_data["bird_model"], custom=custom_attributes
            )
            return str(bird_model)
        elif nml_block == "inflows":
            inflows = NMLInflows()
            inflows.set_attributes(
                json_data["inflows"], custom=custom_attributes
            )
            return str(inflows)
        elif nml_block == "outflows":
            outflows = NMLOutflows()
            outflows.set_attributes(
                json_data["outflows"], custom=custom_attributes
            )
            return str(outflows)
        elif nml_block == "sediment":
            sediment = NMLSediment()
            sediment.set_attributes(
                json_data["sediment"], custom=custom_attributes
            )
            return str(sediment)
        elif nml_block == "ice_snow":
            ice_snow = NMLIceSnow()
            ice_snow.set_attributes(
                json_data["ice_snow"], custom=custom_attributes
            )
            return str(ice_snow)
        elif nml_block == "wq_setup":
            wq_setup = NMLWQSetup()
            wq_setup.set_attributes(
                json_data["wq_setup"], custom=custom_attributes
            )
            return str(wq_setup)

import json


class JSONToNML:
    """Supports the reading of GLM configuration blocks in a json format.

    Reads and parses a json file into a dictionary. Dictionaries can then be
    used to set the attributes of the corresponding NML class. Useful for
    converting a json file of GLM parameters from a web application.

    Attributes
    ----------
    json_file : str
        The path to the json file to be read.
    nml_file : str
        The path to the nml file to be written.

    Examples
    --------
    >>> from glmpy import JSONToNML
    >>> json_to_nml = JSONToNML("sparkling_lake.json")
    """

    def __init__(self, json_file: str, nml_file: str = "sim.nml"):
        if not isinstance(json_file, str):
            raise TypeError(
                f"Expected json_file to be a string, but got {type(json_file).__name__}."
            )
        if not isinstance(nml_file, str):
            raise TypeError(
                f"Expected nml_file to be a string, but got {type(nml_file).__name__}."
            )

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
        >>> json_to_nml = JSONToNML("sparkling_lake.json")
        >>> json_to_nml.read_json()
        """
        with open(self.json_file) as file:
            json_data = json.load(file)
        return json_data

    def get_nml_blocks(self):
        """Reads a json file of GLM configuration blocks and returns a list of
        the block names.

        Parameters
        ----------
        None

        Examples
        --------
        >>> from glmpy import JSONToNML
        >>> json_to_nml = JSONToNML("config.json")
        >>> json_to_nml.get_nml_blocks()
        """
        json_data = self.read_json()
        return list(json_data.keys())

    def get_nml_attributes(self, nml_block: str):
        """Get the attributes for a GLM configuration block.

        Returns the attributes of a specified GLM configuration block as a
        dictionary.

        Parameters
        ----------
        nml_block : str
            The name of the GLM configuration block

        Returns
        -------
        dict
            A dictionary of the attributes for a specified GLM configuration
            block.

        Examples
        --------
        >>> from glmpy import JSONToNML
        >>> json = JSONToNML("sparkling_lake.json")
        >>> setup_dict = json.get_nml_attributes("&glm_setup")
        >>> setup = nml.NMLSetup()
        >>> setup.set_attributes(setup_dict)
        """
        json_data = self.read_json()
        return json_data[nml_block]

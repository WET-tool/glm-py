import json

class JSONToNML:

    def __init__(self, json_file:str, nml_file:str = "sim.nml"):
        self.json_file = json_file
        self.nml_file = nml_file

    def read_json(self):
        with open(self.json_file) as file:
            json_data = json.load(file)
        return json_data

    def get_custom_morphometry_attributes(self):
        json_data = self.read_json()
        morphometry = NMLMorphometry()
        morphometry.set_attributes(json_data["morphometry"])
        return(str(morphometry))

    def get_nml_attributes(self, nml_block, custom_attributes:Union[dict, None]):
        json_data = self.read_json()
        if nml_block == "glm_setup":
            glm_setup = NMLGLMSetup()
            glm_setup.set_attributes(json_data["glm_setup"], custom=custom_attributes)
            return(str(glm_setup))
        elif nml_block == "mixing":
            mixing = NMLMixing()
            mixing.set_attributes(json_data["mixing"], custom=custom_attributes)
            return(str(mixing))
        elif nml_block == "morphometry":
            morphometry = NMLMorphometry()
            morphometry.set_attributes(json_data["morphometry"], custom=custom_attributes)
            return(str(morphometry))
        elif nml_block == "time":
            time = NMLTime()
            time.set_attributes(json_data["time"], custom=custom_attributes)
            return(str(time))
        elif nml_block == "output":
            output = NMLOutput()
            output.set_attributes(json_data["output"], custom=custom_attributes)
            return(str(output))
        elif nml_block == "init_profiles":
            init_profiles = NMLInitProfiles()
            init_profiles.set_attributes(json_data["init_profiles"], custom=custom_attributes)
            return(str(init_profiles))
        elif nml_block == "meteorology":
            meteorology = NMLMeteorology()
            meteorology.set_attributes(json_data["meteorology"], custom=custom_attributes)
            return(str(meteorology))
        elif nml_block == "light":
            light = NMLLight()
            light.set_attributes(json_data["light"], custom=custom_attributes)
            return(str(light))
        elif nml_block == "bird_model":
            bird_model = NMLBirdModel()
            bird_model.set_attributes(json_data["bird_model"], custom=custom_attributes)
            return(str(bird_model))
        elif nml_block == "inflows":
            inflows = NMLInflows()
            inflows.set_attributes(json_data["inflows"], custom=custom_attributes)
            return(str(inflows))
        elif nml_block == "outflows":
            outflows = NMLOutflows()
            outflows.set_attributes(json_data["outflows"], custom=custom_attributes)
            return(str(outflows))
        elif nml_block == "sediment":
            sediment = NMLSediment()
            sediment.set_attributes(json_data["sediment"], custom=custom_attributes)
            return(str(sediment))
        elif nml_block == "ice_snow":
            ice_snow = NMLIceSnow()
            ice_snow.set_attributes(json_data["ice_snow"], custom=custom_attributes)
            return(str(ice_snow))
        elif nml_block == "wq_setup":
            wq_setup = NMLWQSetup()
            wq_setup.set_attributes(json_data["wq_setup"], custom=custom_attributes)
            return(str(wq_setup))

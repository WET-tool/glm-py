import json
import os
import shutil
import zipfile

import pandas as pd


class GlmSim:
    """Prepare inputs and run a GLM simulation.

    Attributes
    ----------
    input_files : UploadFile
        FastAPI `UploadFile` object storing input files for a GLM simulation.
    api : bool
        If True, GLM is run using FastAPI engine. Otherwise, local GLM versions.
    inputs : str
        File path to directory to save input files for GLM simulation.

    Examples
    --------

    `files` is a FastAPI `UploadFile` object.

    >>> glm_sim = glmpy.GlmSim(files, True, "/inputs)
    >>> inputs_dir = glm_sim.prepare_inputs()
    >>> glm_sim.glm_run(inputs_dir, "/glm/glm")
    """

    def __init__(self, input_files, api: bool, inputs_dir: str):
        self.input_files = input_files
        self.fast_api = api
        self.inputs_dir = inputs_dir

    def prepare_inputs(self) -> str:
        """Prepare input files for a GLM simulation.

        Returns
        -------
        str     File path to directory with input files required for a GLM
            simulation.
        """
        if self.fast_api:
            if os.path.isdir(self.inputs_dir):
                shutil.rmtree(self.inputs_dir)
            os.mkdir(self.inputs_dir)

            for f in self.input_files:
                if f.filename == "glm3.nml":
                    nml_path = os.path.join(self.inputs_dir, f.filename)

                    with open(nml_path, "wb") as f_tmp:
                        f_tmp.write(f.file.read())
                else:
                    os.mkdir(os.path.join(self.inputs_dir, "bcs"))
                    bcs_path = os.path.join(self.inputs_dir, "bcs", f.filename)

                    with open(bcs_path, "wb") as f_tmp:
                        f_tmp.write(f.file.read())

        return self.inputs_dir

    def glm_run(self, inputs_dir: str, glm_dir: str) -> None:
        """Run a GLM simulation.

        Parameters
        ----------
        inputs_dir : str
            File path to directory with input files required for a GLM
            simulation.
        glm_dir : str
            Path to location of GLM binary.
        """
        if self.fast_api:
            nml_file = str(os.path.join(inputs_dir, "glm3.nml"))
            run_command = f'{glm_dir} --nml "{nml_file}"'
            os.system(run_command)


class GlmPostProcessor:
    def __init__(self, outputs_path):
        self.outputs_path = outputs_path

    def zip_outputs(self):
        outputs = os.listdir(self.outputs_path)

        with zipfile.ZipFile(
            os.path.join(self.outputs_path, "glm_outputs.zip"), "w"
        ) as z:
            for i in outputs:
                z.write(os.path.join(self.outputs_path, i))

        return os.path.join(self.outputs_path, "glm_outputs.zip")

    def zip_csvs(self):
        csvs = []
        outputs = os.listdir(self.outputs_path)
        for i in outputs:
            if i.endswith(".csv"):
                csvs.append(os.path.join(self.outputs_path, i))

        with zipfile.ZipFile(
            os.path.join(self.outputs_path, "glm_csvs.zip"), "w"
        ) as z:
            for i in csvs:
                z.write(i)

        return os.path.join(self.outputs_path, "glm_csvs.zip")

    def zip_json(self):
        jsons = []
        outputs = os.listdir(self.outputs_path)
        for i in outputs:
            if i.endswith(".json"):
                jsons.append(os.path.join(self.outputs_path, i))

        with zipfile.ZipFile(
            os.path.join(self.outputs_path, "glm_json.zip"), "w"
        ) as z:
            for i in jsons:
                z.write(i)

        return os.path.join(self.outputs_path, "glm_json.zip")

    def csv_to_json_files(self):
        csvs = []
        outputs = os.listdir(self.outputs_path)
        for i in outputs:
            if i.endswith(".csv"):
                csvs.append(os.path.join(self.outputs_path, i))

        tmp_dict = {}
        for i in csvs:
            prefix = str(i).split(".csv")[0]
            json_path = prefix + ".json"

            df = pd.read_csv(i)
            cols = df.columns

            for c in cols:
                tmp_dict[c] = df.loc[:, c].tolist()

            with open(json_path, "w") as dst:
                json.dump(tmp_dict, dst)

    def csv_to_json(self, csv_lake_fname, variables):
        df = pd.read_csv(os.path.join(self.outputs_path, csv_lake_fname))
        df = df.loc[:, variables]
        cols = df.columns

        tmp_dict = {}

        for c in cols:
            tmp_dict[c] = df.loc[:, c].tolist()

        return tmp_dict

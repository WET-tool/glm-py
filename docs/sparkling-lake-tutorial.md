# Tutorials

## Sparkling Lake

### Introduction

Sparkling Lake is an [oligotrophic, northern temperate lake](https://microbes.limnology.wisc.edu/sites/default/files/Modelling%20phytoplankton-zooplanktoninteractions%20in%20Sparkling%20Lake.pdf) (89.7 ºN, 46.3 ºW) in Winconsin, USA. The lake has a surface area of 0.638 km<sup>2</sup>, and is about 20 m deep. This tutorial will guide users through the process of setting up a model of Sparkling Lake using the `glmpy` package. The model will be configured to  simulate the hydrological domain of Sparkling Lake for 2 years, from 1980-04-15 to 1982-04-15, with water balance and heat fluxes [hypothetically calculated](http://aed.see.uwa.edu.au/research/models/GLM/downloads/AED_GLM_v2_0b0_20141025.pdf) based on the lake configuration and input data.

<div id="mapid" style="height: 400px;">
<script>
    var mymap = L.map('mapid').setView([46.008605420259336, -89.70028793742644], 14);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    }).addTo(mymap);
    L.marker([46.008605420259336, -89.70028793742644]).addTo(mymap)
        // .bindPopup("<b>Sparkling Lake!</b><br />Winconsin, USA.").openPopup();
</script>
</div>

### The GLM `.nml` file

To begin, start by importing the `nml` module from `glmpy`:

```python
from glmpy import nml
```

The `nml` module provides a set of methods and classes to work with namelist files (`.nml`), which are used to configure the model parameters of GLM. Each GLM simulation requires a namelist file containing a list of the model parameters and their values. The GLM namelist file is divided into multiple blocks that configure specific aspects of the simulation, e.g., the lake morphometry. The structure of a GLM namelist file is shown below for four of the required blocks (`...` indicates that the block contains more parameters than shown):

```
&glm_setup
  sim_name = 'GLMSimulation'
  ...
/
&morphometry
  lake_name = 'my_lake'
  ...
/
&time
  timefmt = 3
  ...
/
&init_profiles
  lake_depth = 10
  ...
/
```

The `nml` module provides a set of classes that are used to define each of these blocks.

### Model setup

As a 1-dimensional model, GLM simulates the dynamics of a water body by dividing it into a vertically stacked series of layers. The compulsory `&glm_setup` block defines the structure of these layers, e.g., the maximum number of layers, the minimum layer volume, and the minimum and maximum layer thicknesses. Let's configure the `&glm_setup` block using the `NMLSetup` class:

```python
setup = nml.NMLSetup(
    sim_name='Sparkling Lake',
    max_layers=500,
    min_layer_vol=0.5,
    min_layer_thick=0.15,
    max_layer_thick=0.5,
    density_model=1,
    non_avg=True
)
```

Alternatively, these attributes can also be passed to `NMLSetup` as a dictionary object:

```python
setup = nml.NMLSetup()

setup_attrs = {
    'sim_name': 'Sparkling Lake',
    'max_layers': 500,
    'min_layer_vol': 0.5,
    'min_layer_thick': 0.15,
    'max_layer_thick': 0.5,
    'density_model': 1,
    'non_avg': True
}

setup.set_attributes(setup_attrs)
```

Regardless of how you set the attributes, you can inspect the `.nml` formatted
`setup` object by printing it:

```python
print(setup)
```

```
&glm_setup
   sim_name = 'Sparkling Lake'
   max_layers = 500
   min_layer_vol = 0.5
   min_layer_thick = 0.15
   max_layer_thick = 0.5
   density_model = 1
   non_avg = .true.
/
```

### Mixing

Next, let's set the parameters that control the mixing processes between the simulated layers of Sparkling lake. Just as `NMLSetup` defines the `&glm_setup` block, we can configure the `&glm_mixing` block using the `NMLMixing` class:

```python
mixing = nml.NMLMixing(
    surface_mixing=1,
    coef_mix_conv=0.2,
    coef_wind_stir=0.402,
    coef_mix_shear=0.2,
    coef_mix_turb=0.51,
    coef_mix_KH=0.3,
    deep_mixing=2,
    coef_mix_hyp=0.5,
    diff=0.0
)
```

Let's take a look at the result:

```python
print(mixing)
```

```
&mixing
   surface_mixing = 1
   coef_mix_conv = 0.2
   coef_wind_stir = 0.402
   coef_mix_shear = 0.2
   coef_mix_turb = 0.51
   coef_mix_KH = 0.3
   deep_mixing = 2
   coef_mix_hyp = 0.5
   diff = 0.0
/
```



### Morphometry

The `&morphometry` block defines the physical measurements and structure of the lake. Comma-separated lists are used to detail the area at various elevations of the lake. These are listed from the lake bottom to the surface. Set the following attributes and inspect the result:

```python
morphometry = nml.NMLMorphometry(
    lake_name='Sparkling',
    latitude=46.00881,
    longitude=-89.69953,
    bsn_len=901.0385,
    bsn_wid=901.0385,
    crest_elev=320.0,
    bsn_vals=15,
    H=[301.712, 303.018285714286, 304.324571428571,
        305.630857142857, 306.937142857143, 308.243428571429,
        309.549714285714, 310.856, 312.162285714286,
        313.468571428571, 314.774857142857, 316.081142857143,
        317.387428571429, 318.693714285714, 320, 321],
    A=[0, 45545.8263571429, 91091.6527142857,
        136637.479071429, 182183.305428571, 227729.131785714,
        273274.958142857, 318820.7845, 364366.610857143,
        409912.437214286, 455458.263571429, 501004.089928571,
        546549.916285714, 592095.742642857, 637641.569, 687641.569]
)
```

```python
print(morphometry)
```

```
&morphometry
   lake_name = 'Sparkling'
   latitude = 46.00881
   longitude = -89.69953
   crest_elev = 320.0
   bsn_len = 901.0385
   bsn_wid = 901.0385
   bsn_vals = 15
   H = 301.712, 303.018285714286, 304.324571428571, 305.630857142857, 306.937142857143, 308.243428571429, 309.549714285714, 310.856, 312.162285714286, 313.468571428571, 314.774857142857, 316.081142857143, 317.387428571429, 318.693714285714, 320, 321
   A = 0, 45545.8263571429, 91091.6527142857, 136637.479071429, 182183.305428571, 227729.131785714, 273274.958142857, 318820.7845, 364366.610857143, 409912.437214286, 455458.263571429, 501004.089928571, 546549.916285714, 592095.742642857, 637641.569, 687641.569
/
```

### Setting the remaining blocks

There are up to 14 configurable blocks in the GLM namelist file - setting each will take some time! Let's speed up the process by importing a JSON file that contains the parameters for the remaining blocks. We'll use the `JSONToNML` class to extract the relevant attributes from each respective block. Download the JSON file [here](/data/sparkling_lake.json).

Import `JSONToNML` from `glmpy` and pass the JSON file to the class:

```python
from glmpy import glm_json

json_attributes = glm_json.JSONToNML("sparkling_lake.json")
```

Let's have a go at extracting attributes for the `&meteorology` block using the `get_nml_attributes()` method. This block defines the complex interactions that occur between the lake and the atmosphere, e.g., radiation, heat fluxes, rainfall, and wind. We'll pass in the name of the block as it appears in the JSON file:

```python
meteorology_attrs = json_attributes.get_nml_attributes("&meteorology")
```

Take a look at what `meteorology_attrs` contains:

```python
print(meteorology_attrs)
```

```
{'met_sw': True, 'lw_type': 'LW_IN', 'rain_sw': False, 'atm_stab': 0, 'catchrain': False, 'rad_mode': 1, 'albedo_mode': 1, 'cloud_mode': 4, 'fetch_mode': 0, 'subdaily': False, 'meteo_fl': 'bcs/nldas_driver.csv', 'wind_factor': 1, 'sw_factor': 1.08, 'lw_factor': 1, 'at_factor': 1, 'rh_factor': 1, 'rain_factor': 1, 'ce': 0.00132, 'ch': 0.0014, 'cd': 0.0013, 'rain_threshold': 0.01, 'runoff_coef': 0.3}
```

This is a dictionary containing all attributes for the `&meteorology` block. Let's
pass these to the `NMLMeteorology` class with the `set_attributes()` method:

```python
meteorology = nml.NMLMeteorology()
meteorology.set_attributes(meteorology_attrs)
print(meteorology)
```

```
&meteorology
   met_sw = .true.
   meteo_fl = 'bcs/nldas_driver.csv'
   subdaily = .false.
   rad_mode = 1
   albedo_mode = 1
   sw_factor = 1.08
   lw_type = 'LW_IN'
   cloud_mode = 4
   lw_factor = 1
   atm_stab = 0
   rh_factor = 1
   at_factor = 1
   ce = 0.00132
   ch = 0.0014
   rain_sw = .false.
   rain_factor = 1
   catchrain = .false.
   rain_threshold = 0.01
   runoff_coef = 0.3
   cd = 0.0013
   wind_factor = 1
   fetch_mode = 0
/
```

Easy! But before we go any futher, look closely at the `meteo_fl` attribute - what's `bcs/nldas_driver.csv`? This is a path to a CSV that contains boundary condition data for Sparkling Lake, e.g., daily rainfall, wind speed, and air temperature. You'll need this file to run the model. Download it [here](/data/nldas_driver.csv).

Now, let's do the same for the remaining blocks:  `&output`, `&init_profiles`, `&time`, `&bird_model`, `&light`, `&sediment`. There won't be any more boundary conidition files to include. If you're want to find out more about the attributes for each block, check out the [NML documentation]().

```python
output_attrs=glm_json_attributes.get_nml_attributes("&output")
init_profiles_attrs=glm_json_attributes.get_nml_attributes("&init_profiles")
time_attrs=glm_json_attributes.get_nml_attributes("&time")
light_attrs=glm_json_attributes.get_nml_attributes("&light")
bird_model_attrs=glm_json_attributes.get_nml_attributes("&bird_model")
sediment_attrs=glm_json_attributes.get_nml_attributes("&sediment")
wq_setup_attrs=glm_json_attributes.get_nml_attributes("&wq_setup")
```

Now initialise the respective classes:

```python
output = nml.NMLOutput()
init_profiles = nml.NMLInitProfiles()
time = nml.NMLTime()
light = nml.NMLLight()
bird_model = nml.NMLBirdModel()
sediment = nml.NMLSediment()
wq_setup = nml.NMLWQSetup()
```

And set the attributes:

```python
output.set_attributes(output_attrs)
init_profiles.set_attributes(init_profiles_attrs)
time.set_attributes(time_attrs)
light.set_attributes(light_attrs)
bird_model.set_attributes(bird_model_attrs)
sediment.set_attributes(sediment_attrs)
wq_setup.set_attributes(wq_setup_attrs)
```


### Writing the namelist file

Now that we have the attributes set for each block, the `.nml` file can be compiled and written to disk. First, create an instance of the `NML` class and pass in the configured blocks. Using the `write_nml()` method, the `.nml` can be saved to your directory.

```python
nml = nml.NML(
  setup=setup,
  mixing=mixing,
  morphometry=morphometry,
  time=time,
  output=output,
  init_profiles=init_profiles,
  meteorology=meteorology,
  bird_model=bird_model,
  light=light,
  sediment=sediment
)

nml.write_nml(nml_file_path='glm3.nml')
```

### Running the model

Model configuration is now complete! To run glm, first import the `simulation` module:

```python
import glmpy.simulation as sim
```

We now need to specify the location of any files we'll be using in the simulation. For Sparkling lake, that's just your newly created `glm3.nml` and the meterological boundary condition file `nldas_driver.csv`. These will be defined in a dictionary where the key is the file name and the value is the filepath:

```python
files = {
    "glm3.nml": "/path/to/glm3.nml",
    "nldas_driver.csv": "/path/to/nldas_driver.csv"
}
```

Pass this dictionary to a new instance of the `GlmSim` class. `GlmSim` will prepare a new directory called `inputs` that structures our files in a way that GLM expects. Set `api` to `False` to run the simulation locally:

```python
glm_sim = sim.GlmSim(
  input_files=files,
  api=False,
  inputs_dir="inputs"
)
```

Create the `inputs` directory by calling the `.prepare_inputs()` method:

```python
inputs_dir = glm_sim.prepare_inputs()
```

You should now have a new directory that looks like this:

```
├── bcs
│   └── nldas_driver.csv
├── glm3.nml
```

Finally, run the simulation with the `.glm_run()` method. Pass in the `inputs_dir` object and a string containing the path to the GLM binary:

```python
glm_sim.glm_run(inputs_dir=inputs_dir, glm_path="/path/to/glm/binary")
```

GLM will run the simulation. You should see a new directory called `outputs` that contains the model results.



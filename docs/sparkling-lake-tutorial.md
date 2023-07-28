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

setup_params = {
    'sim_name': 'Sparkling Lake',
    'max_layers': 500,
    'min_layer_vol': 0.5,
    'min_layer_thick': 0.15,
    'max_layer_thick': 0.5,
    'density_model': 1,
    'non_avg': True
}

setup.set_attributes(setup_params)
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

### Morphometry

The `&morphometry` block defines the physical measurements and structure of the lake. Comma-separated lists are used to detail the area at various elevations of the lake. These are listed from the lake bottom to the surface.

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

### Setting the remaining blocks

There are up to 14 configurable blocks in the GLM namelist file - setting each will take some time! Let's speed up the process by importing a JSON file that contains the parameters for the remaining blocks. We'll use the `JSONToNML` class to extract the relevant parameters from each respective block. Download the JSON file [here](/data/sparkling_lake.json).

Import `JSONToNML` from `glmpy` and pass the JSON file to the class:

```python
from glmpy import JSONToNML

json_parameters = JSONToNML("sparkling_lake.json")
```

Let's have a go at extracting parameters for the `&time` block using the `get_nml_attributes()`` method. Unsuprisingly, this block defines the temporal parameters of the simulation. We'll pass in the name of the block as a string as it appears in the JSON file:

```python
time=json_parameters.get_nml_attributes("time")
```

Now, print the contents of the `time` object and you'll see we now have the correct NML formmatting for the `&time` block:

```python
print(time)
```

```
timefmt = 3
start = '1980-04-15'
stop = '2012-12-10'
dt = 3600
num_days = 730
timezone = -6
```

Easy! Let's do the same for the remaining blocks:  `&output`, `&init_profiles`, `&meteorology`, `&bird_model`, `&light`, `&inflow`, `&outflow`, `&sediment`. If you're want to find out more about the parameters for each block, check out the [NML documentation]().

```python
output=json_parameters.get_nml_attributes("&output")
init_profiles=json_parameters.get_nml_attributes("&init_profiles")
meteorology=json_parameters.get_nml_attributes("&meteorology")
light=json_parameters.get_nml_attributes("&light")
bird_model=json_parameters.get_nml_attributes("&bird_model")
inflows=json_parameters.get_nml_attributes("&inflows")
outflows=json_parameters.get_nml_attributes("&outflows")
sediment=json_parameters.get_nml_attributes("&sediment")
wq_setup=json_parameters.get_nml_attributes("&wq_setup")
```

### Writing the namelist file

Now that we have the parameters for each block, the namelist file can be compiled and written to disk. First, create an instance of the `NML` class and pass in the configured blocks. Using the `write_nml()` method, the `.nml` can be saved to a specified path.

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
  inflows=inflows,
  outflows=outflows,
  sediment=sediment
)

nml.write_nml(nml_file_path='glm3.nml')
```




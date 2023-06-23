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

```fortran
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

There are up to 14 configurable blocks in the GLM namelist file. Dictionary objects have been provided below for the remaning blocks. Using the `set_attributes()` method for each respective class, configure the blocks for `&time`, `&output`, `&init_profiles`, `&meteorology`, `&bird_model`, `&light`, `&inflow`, `&outflow`, `&sediment`.

#### `&time`

```python
time = nml.NMLTime()

time_params = {
    'timefmt': 3,
    'start': '1980-04-15',
    'stop': '2012-12-10',
    'dt': 3600,
    'timezone': -6,
    'num_days': 730
}
```

#### `&output`

```python
output = nml.NMLOutput()

output_params = {
    'out_dir': 'output',
    'out_fn': 'output',
    'nsave': 24,
    'csv_lake_fname': 'lake',
    'csv_point_nlevs': 0,
    'csv_point_fname': 'WQ_',
    'csv_point_at': [17],
    'csv_point_nvars': 2,
    'csv_point_vars': ['temp', 'salt', 'OXY_oxy'],
    'csv_outlet_allinone': False,
    'csv_outlet_fname': 'outlet_',
    'csv_outlet_nvars': 3,
    'csv_outlet_vars': ['flow', 'temp', 'salt', 'OXY_oxy'],
    'csv_ovrflw_fname': 'overflow'
}
```

#### `&init_profiles`

```python
init_profiles = nml.NMLInitProfiles()

init_profiles_params = {
    'lake_depth': 18.288,
    'num_depths': 3,
    'the_depths': [0, 0.2, 18.288],
    'the_temps': [3, 4, 4],
    'the_sals': [0, 0, 0],
    'num_wq_vars': 6,
    'wq_names': ['OGM_don', 'OGM_pon', 'OGM_dop', 'OGM_pop', 'OGM_doc', 'OGM_poc'],
    'wq_init_vals': [1.1, 1.2, 1.3, 1.2, 1.3, 2.1, 2.2, 2.3, 1.2, 1.3, 3.1, 3.2, 3.3, 1.2, 1.3, 4.1, 4.2, 4.3, 1.2, 1.3, 5.1, 5.2, 5.3, 1.2, 1.3, 6.1, 6.2, 6.3, 1.2, 1.3]
}
```

#### `&meteorology`

```python
meteorology = nml.NMLMeteorology()

meteorology_params = {
    'met_sw': True,
    'lw_type': 'LW_IN',
    'rain_sw': False,
    'atm_stab': 0,
    'catchrain': False,
    'rad_mode': 1,
    'albedo_mode': 1,
    'cloud_mode': 4,
    'fetch_mode': 0,
    'subdaily': False,
    'meteo_fl': 'bcs/nldas_driver.csv',
    'wind_factor': 1,
    'sw_factor': 1.08,
    'lw_factor': 1,
    'at_factor': 1,
    'rh_factor': 1,
    'rain_factor': 1,
    'ce': 0.00132,
    'ch': 0.0014,
    'cd': 0.0013,
    'rain_threshold': 0.01,
    'runoff_coef': 0.3
}
```

#### `&bird_model`

```python
bird_model = nml.NMLBirdModel()

bird_model_params = {
    'AP': 973,
    'Oz': 0.279,
    'WatVap': 1.1,
    'AOD500': 0.033,
    'AOD380': 0.038,
    'Albedo': 0.2
}
```

#### `&light`

```python
light = nml.NMLLight()

light_params = {
    'light_mode': 0,
    'n_bands': 4,
    'light_extc': [1.0, 0.5, 2.0, 4.0],
    'energy_frac': [0.51, 0.45, 0.035, 0.005],
    'Benthic_Imin': 10,
    'Kw': 0.331
}
```

#### `&inflow`

```python
inflows = nml.NMLInflows()

inflows_params = {
    'num_inflows': 0,
    'names_of_strms': ['Riv1', 'Riv2'],
    'subm_flag': [False],
    'strm_hf_angle': [65, 65],
    'strmbd_slope': [2, 2],
    'strmbd_drag': [0.016, 0.016],
    'inflow_factor': [1, 1],
    'inflow_fl': ['bcs/inflow_1.csv', 'bcs/inflow_2.csv'],
    'inflow_varnum': 4,
    'inflow_vars': ['FLOW', 'TEMP', 'SALT', 'OXY_oxy', 'SIL_rsi', 'NIT_amm', 'NIT_nit', 'PHS_frp', 'OGM_don', 'OGM_pon', 'OGM_dop', 'OGM_pop', 'OGM_doc', 'OGM_poc', 'PHY_green', 'PHY_crypto', 'PHY_diatom']
}
```

#### `&outflow`

```python
outflows = nml.NMLOutflows()

outflows_params = {
    'num_outlet': 0,
    'flt_off_sw': [False],
    'outl_elvs': [1],
    'bsn_len_outl': [5],
    'bsn_wid_outl': [5],
    'outflow_fl': 'bcs/outflow.csv',
    'outflow_factor': [0.8],
    'crest_width': 100,
    'crest_factor': 0.61
}
```

#### `&sediment`

```python
sediment = nml.NMLSediment()

sediment_params = {
    'sed_heat_Ksoil': 2.0,
    'sed_temp_depth': 0.2,
    'sed_temp_mean': [4.5, 5, 6],
    'sed_temp_amplitude': [1, 1, 1],
    'sed_temp_peak_doy': [242, 242, 242],
    'benthic_mode': 2,
    'n_zones': 3,
    'zone_heights': [10.0, 20.0, 30.0],
    'sed_reflectivity': [0.1, 0.01, 0.01],
    'sed_roughness': [0.1, 0.01, 0.01]
}
```

### Writing the namelist file

Once all of the blocks have been configured, the namelist file can be compiled and written to disk. First, create an instance of the `NML` class and pass in the configured blocks. Using the `write_nml()` method, the `.nml` can be saved to a specified path.

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


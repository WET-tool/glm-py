# How-to

## NML

Begin by importing the `nml` module from `glmpy`:

```python
from glmpy import nml
```

### Setting paramters

Parameters for each block in a `.nml` file can either be passed to the respective class as keyword arguments or as a dictionary object. For example, the `setup` block can be configured with the [`NMLSetup`](nml.md#glmpy.nml.NMLSetup) class as follows:

```python
my_setup = nml.NMLSetup(
    sim_name='GLMSimulation',
    max_layers=500,
    min_layer_vol=0.5,
    min_layer_thick=0.15,
    max_layer_thick=0.5,
    density_model=1,
    non_avg=True
)
```

or as a dictionary object with the [`set_attributes()`](nml.md#glmpy.nml.NMLBase.set_attributes) method:

```python
my_setup = nml.NMLSetup()

setup_params = {
    'sim_name': 'GLMSimulation',
    'max_layers': 500,
    'min_layer_vol': 0.5,
    'min_layer_thick': 0.15,
    'max_layer_thick': 0.5,
    'density_model': 1,
    'non_avg': True
}

my_setup.set_attributes(setup_params)
```

Refer to the [API Reference](nml.md#glmpy.nml.NML) for detailed information about the parameters for each block.

### Writing the `.nml` file

At a minimum, the GLM namelist file (`.nml`) requires model parameters set for the following blocks:

- `setup` with the [`NMLSetup`](nml.md#glmpy.nml.NMLSetup) class
- `morphometry` with the [`NMLMorphometry`](nml.md#glmpy.nml.NMLMorphometry) class
- `time` with the [`NMLTime`](nml.md#glmpy.nml.NMLTime) class
- `init_profiles` with the [`NMLInitProfiles`](nml.md#glmpy.nml.NMLInitProfiles) class

The configured blocks can then be combined into a `.nml` file with the [`NML`](nml.md#glmpy.nml.NML) class:

```python
my_nml = nml.NML(
    setup=my_setup,
    morphometry=my_morphometry,
    time=my_time,
    init_profiles=my_init_profiles
)
```

To write the `.nml` file to disk, use the [`write_nml()`](nml.md#glmpy.nml.NML.write_nml) method:

```python
my_nml.write_nml(nml_file_path = 'my_nml.nml')
```

### Calculating the morphometry for simple water bodies

For simple water bodies, `glmpy` provides some classes to conveniently calculate the `H` and `A` (height and surface area) parameters for the `NMLMorphometry` class.

The [`SimpleTruncatedPyramidWaterBody`](dimensions.md#glmpy.dimensions.SimpleTruncatedPyramidWaterBody) class can be used for pyramidal water bodies with a rectangular base:

![Graphical representation of the SimpleTruncatedPyramidWaterBody](docs/../img/SimpleTruncatedPyramidWaterBody.png#only-light)
![Graphical representation of the SimpleTruncatedPyramidWaterBody](docs/../img/SimpleTruncatedPyramidWaterBody-dark.png#only-dark)

```python
from glmpy import dimensions

my_dimensions = SimpleTruncatedPyramidWaterBody(
    height = 3,
    surface_width = 5,
    surface_length =  5,
    side_slop = 3
)
```

Heights and surface areas can be then returned with the [`get_heights()`](dimensions.md#glmpy.dimensions.SimpleTruncatedPyramidWaterBody.get_heights) and [`get_surface_areas()`](dimensions.md#glmpy.dimensions.SimpleTruncatedPyramidWaterBody.get_surface_areas) methods:

```python
my_heights = my_dimensions.get_heights()
my_surface_areas = my_dimensions.get_surface_areas()
```
## JSON

### Converting JSON to `.nml`

GLM parameters stored in a JSON format can be converted to a `.nml` file with the `JSONToNML` class.

Consider the following JSON file:

```
{
  "&glm_setup": {
    "sim_name": "Sparkling Lake",
    "max_layers": 500,
    "min_layer_vol": 0.5,
    "min_layer_thick": 0.15,
    "max_layer_thick": 0.5,
    "density_model": 1,
    "non_avg": true
  },
  "&morphometry": {
    "lake_name": "Sparkling",
    "latitude": 46.00881,
    "longitude": -89.69953,
    "crest_elev": 320.0,
    "bsn_len": 901.0385,
    "bsn_wid": 901.0385,
    "bsn_vals": 15,
    "H": [301.712, 303.018285714286, 304.324571428571, 305.630857142857, 306.937142857143, 308.243428571429, 309.549714285714, 310.856, 312.162285714286, 313.468571428571, 314.774857142857, 316.081142857143, 317.387428571429, 318.693714285714, 320, 321],
    "A": [0, 45545.8263571429, 91091.6527142857, 136637.479071429, 182183.305428571, 227729.131785714, 273274.958142857, 318820.7845, 364366.610857143, 409912.437214286, 455458.263571429, 501004.089928571, 546549.916285714, 592095.742642857, 637641.569, 687641.569]
  },
  "&time": {
    "timefmt": 3,
    "start": "1980-04-15",
    "stop": "2012-12-10",
    "dt": 3600,
    "timezone": -6,
    "num_days": 730
  },
  "&init_profiles": {
    "lake_depth": 18.288,
    "num_depths": 3,
    "the_depths": [0, 0.2, 18.288],
    "the_temps": [3, 4, 4],
    "the_sals": [0, 0, 0],
    "num_wq_vars": 6,
    "wq_names": ["OGM_don", "OGM_pon", "OGM_dop", "OGM_pop", "OGM_doc", "OGM_poc"],
    "wq_init_vals": [1.1, 1.2, 1.3, 1.2, 1.3, 2.1, 2.2, 2.3, 1.2, 1.3, 3.1, 3.2, 3.3, 1.2, 1.3, 4.1, 4.2, 4.3, 1.2, 1.3, 5.1, 5.2, 5.3, 1.2, 1.3, 6.1, 6.2, 6.3, 1.2, 1.3]
  }
}
```

First, import the `JSONToNML` class:

```python
from glmpy import JSONToNML
```

Then, create an instance of the `JSONToNML` class with the path to the JSON file:

```python
json_file = JSONToNML('my_json_file.json')
```

Finally, use the `get_nml_attributes()` method to get the attributes for each block. This can be applied in the context of the `NML` class to create a `.nml` file:

```python
nml = nml.NML(
  setup=json_file.get_nml_attributes("&glm_setup"),
  morphometry=json_file.get_nml_attributes("&morphometry"),
  time=json_file.get_nml_attributes("&time"),
  init_profiles=json_file.get_nml_attributes("&init_profiles")
)

nml.write_nml(nml_file_path='glm3.nml')
```

## Outflows

The `Outflow` class provides functionality for creating and modifying the `outflows.csv`.

```python
from glmpy import outflows
```

### Setting up outflows

The duration of the `outflows.csv` is set with the `start_date` and `end_date` parameters. These must match the `start` and `stop` parameters used to configure `time` block with [`NMLTime`](nml.md#glmpy.nml.NMLTime).

An optional `base_flow` parameter can be set for constant outflows.

```python
my_outflows = Outflows(
    start_date = '1997-01-01',
    end_date = '1997-01-11',
    base_flow = 0.0
)
```

### Set outflows for specific dates

By default, the `Outflows` class sets outflows to zero for the enitre simulation period. To set outflows for specific dates, use the [`set_discrete_outflows()`](outflows.md#glmpy.outflows.Outflows.set_discrete_outflows) method:

```python
my_outflows.set_outflows(
    dates = ['1997-01-01', '1997-01-05', '1997-01-10'],
    outflows = [3.5, 1.2, 4.7]
)
```

### Set outflows for a date range

Constant outflows can be set for a date range with the [`set_continuous_outflows()`](outflows.md#glmpy.outflows.Outflows.set_continuous_outflows) method:

```python
my_outflows.set_continuous_outflows(
    start_date = '1997-01-06',
    end_date = '1997-01-09',
    outflow = 2.5
)
```

### Inspecting outflows

The [`get_outflows()`](outflows.md#glmpy.outflows.Outflows.get_outflows) method will return a `pandas.DataFrame` object with the outflows for the simulation period:

```python
my_outflows.get_outflows()
```

### Writing outflows to disk

Once the outflows have been defined, they can be saved to disk as a `.csv` with the [`write_outflows()`](outflows.md#glmpy.outflows.Outflows.write_outflows) method:

```python
my_outflows.write_outflows(outflow_file_path = 'my_outflows.csv')
```

## Inflows

Inflows define any additional inputs to the simulated water body.

```python
from glmpy import inflows
```

### Calculating inflows from catchment runoff

The [`CatchmentInflows`](inflows.md#glmpy.inflows.CatchmentInflows) class provides functionality for calculating inflows from catchment runoff. The amount of runoff is calculated as a product of the catchment area, precipitation, and a runoff coefficient/threshold.

First, an existing `.csv` file with precipitation data must be available on disk or loaded into a `pandas.DataFrame` object:

```python
met_data = pd.DataFrame({
    'Date': pd.date_range(
        start='1997-01-01',
        end='2004-12-31',
        freq='H'),
    'Rain': 10
})
met_data.to_csv('met_data.csv')
```

Next, the `CatchmentInflows` class can be instantiated with the path to the precipitation data. Provide the column names for the date and precipitation data (`date_time_col` and `precip_col` respectively). The `runoff_coeff` or `runoff_threshold` parameters can be used to set a constant runoff coefficient/threshold for the area of the catchment (`catchment_area`):

```python
my_inflows = CatchmentInflows(
    input_type = 'file',
    path_to_met_csv = 'met_data.csv',
    catchment_area = 1000,
    runoff_threshold = 10.0,
    precip_col = 'Rain',
    date_time_col = 'Date',
    date_time_format= '%Y-%m-%d %H:%M:%S'
)
```

### Writing catchment inflows to disk

GLM inflows must be recorded at daily timesteps. As catchment inflows are often calculated directly from high resolution precipitation data, the [`write_inflows`](inflows.md#glmpy.inflows.CatchmentInflows.write_inflows) method can be used resample the inflows to daily timesteps when writing them to disk:

```python
my_inflows.write_inflows(
    path_to_inflow_csv = "runoff.csv"
)
```

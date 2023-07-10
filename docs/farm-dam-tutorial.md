# Tutorials

## Farm Dam

### Introduction

In this tutorial, you will use `glmpy` to construct a simple model of a farm dam in the Western Australian (WA) Wheatbelt. The WA Wheatbelt is a semi-arid agricultural region dominated by rain-fed cropping and livestock production. Farm dams play a crucial role in storing fresh water for irrigation and animal consumption during the dry summer months. Climate change is warming the Wheatbelt and increasingly disrupting the winter rainfall patterns that fill farm dams. When dams dry out, the impact to farmers and animals can be servere. Modelling the water balance of these small water bodies is important to minimise their risk of failure under a drying climate.

In the map below, you can see the dam is connected to a large catchment area. These catchments are often constructed up-hill from the dam and consist of a compacted clay surface. This design increases runoff during rainfall events and channels the water into the dam. To accurately model the dam, we will need to incorporate the inflows from this catchment.

<div id="ridgefield-dam" style="height: 400px;">
<script>
    var mymap = L.map('ridgefield-dam').setView([-32.474573237844865, 116.98943188401849], 17);
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        maxZoom: 18,
        minZoom: 4,
        attribution: 'Tiles &copy; Esri'
    }).addTo(mymap);
    L.marker([-32.474420699229476, 116.98832692114296]).addTo(mymap).bindPopup("<b>Farm dam</b><br>Length: 62m Width: 40m Depth: 5m<br>Location: -32.474, 116.988", {autoClose: false}).openPopup();
    L.marker([-32.47557320681146, 116.99093865157606]).addTo(mymap).bindPopup("<b>Dam catchment</b><br>Area: 32,000m<sup>2</sup>", {autoClose: false}).openPopup();

</script>
</div>

### Model setup

Let's start building the model. `glmpy` provides a set of classes in the `nml` module that can be used to construct the GLM namelist file (`.nml`). The `.nml` file is simply a text file that contains a set of parameters which configure the model. These parameters are grouped into different components that each configure different aspects of the model. For every component, there is a corresponding class in the `nml` module that you can use to construct the namelist file, e.g., the `NMLMeteorology` class configures the `&meteorology` parameters. Go ahead and import the `nml` module:

```python
from glmpy import nml
```

The first component we will configure is the `&setup` component. These parameters control the model *layers*. GLM is a 1-D model that simulates a water body as a vertical series of layers. The number of layers, and their thickness, is dynamic. Layers will expand, contract, merge, and split in response to water and surface mass fluxes.  The `&setup` component defines the initial state of these layers. The `NMLSetup` class constructor takes the following arguments:

- `sim_name`: The name of your simulation
- `max_layers`: The maximum number of layers that can be created during the simulation
- `min_layer_vol`: The minimum volume of a layer in cubic metres
- `min_layer_thick`: The minimum thickness of a layer in metres
- `max_layer_thick`: The maximum thickness of a layer in metres
- `density_model`: The equation used to calculate the density of water in each layer
- `non_avg`: A flag to indicate whether the model should use non-averaged layers

Let's initialise our model with a maximum of 100 layers. Each layer must contain at least 0.1 m<sup>3</sup> of water and range in thickness from 0.01-1.0 m. By setting `density_model` to 1, we'll use a model from [TEOS-10](http://teos-10.org) that calculates the density as a function of local temperature and salinity. Finally, we'll set `non_avg` to `True` to indicate that we want to use non-averaged layers.

```python
setup = nml.NMLSetup(
    sim_name='farm_dam',
    max_layers=100,
    min_layer_vol=0.1,
    min_layer_thick=0.01,
    max_layer_thick=1.0,
    density_model=1,
    non_avg=True
)
```

### Model duration

Our model will run over a 10 year period from 2010 to 2020 at an hourly timestep. The `&time` component defines the start and stop time of the simulation, the time step, and the time zone. We can use `NMLTime` class constructor to configure these properties:

```python
time = nml.NMLTime(
    timefmt=2,
    start="2010-01-01 00:00:00",
    stop="2020-12-31 00:00:00",
    dt=3600,
    timezone=8
)
```

Here, we have specified the `timefmt` as `2` which configures GLM to accept `start` and `stop` times. Alternatively, a `timefmt=3` allows GLM to read the `num_days` parameter. The `start` and `stop` times are specified as strings in the format `YYYY-MM-DD HH:MM:SS`. The `dt` parameter is the time step in seconds (3600 seconds in an hour). The `timezone` parameter is the time zone offset from UTC in hours.

### Dam morphometry

Next, let's define the dam morphometry, i.e., the physical dimensions that capture the shape of the water body. GLM records the morphometry of a water body by a list of height and surface area pairs. The heights are vertical distances from the bottom of the water body to the surface. The surface areas are the horizontal area of the water body at the each height increment. The number of height/surface-area pairs largely depends on how complex the morphometry is. For dams, the morphometry is simple and often resembles an truncated pyramid that has been inverted. Conveniently, `glmpy` provides a `SimpleTruncatedPyramidWaterBody` class in the `dimensions` module to easily calculate the height/surface-area pairs!

```python
from gplmpy import dimensions
```
The `SimpleTruncatedPyramidWaterBody` constructor takes the following arguments:

- `height`: The height (i.e., the depth) of the dam in metres.
- `surface_width`: The width of the dam surface in metres.
- `surface_length`: The length of the dam surface in metres.
- `side_slope`: The rise over run of the dam side slopes

![Graphical representation of the SimpleTruncatedPyramidWaterBody](docs/../img/SimpleTruncatedPyramidWaterBody.png#only-light)
![Graphical representation of the SimpleTruncatedPyramidWaterBody](docs/../img/SimpleTruncatedPyramidWaterBody-dark.png#only-dark)

Three of these arguments are known from the information on our map. The `side_slope` is unknown so here we will make an assumption. Farm dams in the WA Wheatbelt are typically constructed with a side slope of 3:1. This means the dam slopes 3 metres vertically for every 1 metre horizontally. Based on this assumption we can now construct the `SimpleTruncatedPyramidWaterBody` object.

```python
dam_morphometry = dimensions.SimpleTruncatedPyramidWaterBody(
    height=5,
    surface_width=40,
    surface_length=62,
    side_slope=3
)
```

Calling the  `get_heights()` and `get_surface_areas()` method on the `dam_morphometry` object returns a list of height/surface-area pairs.

```python
dam_morphometry.get_heights()
```

```
[-5, -4, -3, -2, -1, 0]
```

```python
dam_morphometry.get_surface_areas()
```

```
[2151.111, 2215.111, 2280.0, 2345.774, 2412.444, 2480.0]
```

We can now plug this information into the `NMLMorphometry` constructor.

```python
morphometry = nml.NMLMorphometry(
    lake_name = "Farm dam",
    latitude = -32.474,
    longitude = 116.988,
    base_elev = dam_morphometry.get_heights()[0],
    crest_elev = dam_morphometry.get_heights()[-1],
    bsn_len = 62,
    bsn_wid = 40,
    H = dam_morphometry.get_heights(),
    A = dam_morphometry.get_surface_areas()
)
```

### Meteorology

Rainfall data from the Bureau of Meteorology (BoM) is available for the nearby Wheatbelt town of Pingelly is available from the [here](/docs/data/rainfall-farm-dam-tutorial.csv).

```python
meteorology = nml.NMLMeteorology(
    meteo_fl = 'path/to/rainfall-farm-dam-tutorial.csv',
    time_fmt = 'YYYY-MM-DD`
)
```

### Catchment inflows

```python
from glmpy import inflows
```

```python
inflows = inflows.CatchmentInflows(
    input_type = 'dataframe',
    met_data = met_data,
    catchment_area = 32000,
    runoff_threshold = 0.008,
    precip_col = 'rainfall',
    date_time_col = 'time'
)
```
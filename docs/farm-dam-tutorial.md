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

```python
from glmpy import nml
```

### Dam morphometry

Let's begin by defining the dam morphometry, i.e., the physical dimensions that capture the shape of the water body. GLM records the morphometry of a water body by a list of height and surface area pairs. The heights are vertical distances from the bottom of the water body to the surface. The surface areas are the horizontal area of the water body at the each height increment. The number of height/surface-area pairs largely depends on how complex the morphometry is. For dams, the morphometry is simple and often resembles an truncated pyramid that has been inverted. Conveniently, `glmpy` provides a `SimpleTruncatedPyramidWaterBody` class in the `dimensions` module to easily calculate the height/surface-area pairs!

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
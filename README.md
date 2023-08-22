# glm-py

<!-- badges: start -->
![Lifecycle: experimental](https://img.shields.io/badge/lifecycle-experimental-orange.svg)
<!-- badges: end -->

Python tools for running General Lake Model (GLM) simulations.

## GLM

GLM is a 1-dimensional lake water balance and stratification model. It is distributed coupled with a powerful ecological modelling library to also support simulations of lake water quality and ecosystems processes.

GLM is suitable for a wide range of natural and engineered lakes, including shallow (well-mixed) and deep (stratified) systems. The model has been successfully applied to systems from the scale of individual ponds and wetlands to the scale of Great Lakes.

For more information about running GLM please see the model website's <a href="https://aed.see.uwa.edu.au/research/models/glm/overview.html" target="_blank">scientific basis description</a> and the <a href="https://aquaticecodynamics.github.io/glm-workbook/" target="_blank">GLM workbook</a>. 

The <a href="https://github.com/AquaticEcoDynamics/glm-aed/tree/main/binaries" target="_blank">GLM model</a> is available as an executable for Linux (Ubuntu), MacOS, and Windows. It is actively developed by the 
Aquatic EcoDynamics research group at The University of Western Australia.

## Why GLM-py?

GLM-py provides a series of classes, functions, and data structures that to support running GLM simulations, preparing model input data and configurations, and processing model outputs. 

Its goal is to make running and deploying GLM in a range of environments easy such as building web APIs around GLM within web applications or cloud services, running batches of GLM simulations on HPCs, or running GLM simulations locally within Python environments such as JupyterLab or QGIS. 

### NML

Classes to store properties describing GLM simulation input data and configuration and methods that generate `.nml` config files required for running GLM. 

### Dimensions

Take simple user descriptions of lake geometry or dimensions and generate detailed representations of lake morphometry required for GLM simulations.

### JSON

Tools to convert JSON data to `.nml` format data. Useful for handling client requests if GLM is deployed within a web API / REST API.

### Simulations

Classes to handle running GLM simulations and processing output data into CSV, JSON, or NetCDF files or generating a JSON stream to pass onto clients. 

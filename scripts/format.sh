cd ..
black glmpy --line-length=79
docformatter glmpy/nml.py -i
docformatter glmpy/json.py -i
docformatter glmpy/dimensions.py -i
docformatter glmpy/simulation.py -i
flake8 glmpy

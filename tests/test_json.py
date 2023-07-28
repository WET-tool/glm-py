import pytest
from glmpy.json import JSONToNML


def test_json_to_nml_invalid_json_file():
    with pytest.raises(TypeError):
        JSONToNML(json_file=123, nml_file="sim.nml")

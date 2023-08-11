import pytest
from glmpy.nml import NML


def test_write_nml(tmp_path):
    nml = NML(
        setup="&glm_setup\n/",
        morphometry="&morphometry\n/",
        time="&time\n/",
        init_profiles="&init_profiles\n/",
    )
    file_path = tmp_path / "test.nml"
    nml.write_nml(file_path)

    with open(file_path, "r") as file:
        content = file.read()

    expected_content = (
        "&glm_setup\n/\n&morphometry\n/\n&time\n/\n&init_profiles\n/\n"
    )
    assert content == expected_content

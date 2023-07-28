import pytest
from glmpy.nml import NML


def test_write_nml(tmp_path):
    nml = NML(
        setup="setup",
        morphometry="morphometry",
        time="time",
        init_profiles="init_profiles",
    )
    file_path = tmp_path / "test.nml"
    nml.write_nml(file_path)

    with open(file_path, "r") as file:
        content = file.read()

    expected_content = (
        "&glm_setup\nsetup\n/\n&morphometry\nmorphometry\n/\n&time\ntime\n/\n&init_profiles\ninit_profiles\n/\n"
    )
    assert content == expected_content

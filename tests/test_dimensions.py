import pytest
import math
from glmpy.dimensions import SimpleTruncatedPyramidWaterBody


def test_non_numeric_height():
    with pytest.raises(ValueError) as dimensions_info:
        SimpleTruncatedPyramidWaterBody(
            height='foo',
            surface_width='foo',
            surface_length='foo'
        )
        assert str(
            dimensions_info.value) == "Height, surface width, surface length, and side slope must be numeric."


def test_SimpleTruncatedPyramidWaterBody_get_volumes():
    dam = SimpleTruncatedPyramidWaterBody(3, 5, 5)
    expected_volumes = [0.0, 11.148148148148149, 27.185185185185183, 49.0]
    assert dam.get_volumes() == pytest.approx(expected_volumes)


def test_SimpleTruncatedPyramidWaterBody_get_surface_areas():
    dam = SimpleTruncatedPyramidWaterBody(3, 5, 5)
    expected_surface_areas = [
        9.0, 13.444444444444443, 18.777777777777775, 25.0]
    assert dam.get_surface_areas() == pytest.approx(expected_surface_areas)


def test_SimpleTruncatedPyramidWaterBody_get_heights():
    dam = SimpleTruncatedPyramidWaterBody(3, 5, 5)
    expected_heights = [-3, -2, -1, 0]
    assert dam.get_heights() == expected_heights

import pytest
import math
from glmpy import dimensions


def test_non_numeric_height():
    with pytest.raises(ValueError) as exc_info:
        dimensions.SimpleTruncatedPyramidWaterBody(
            height='foo',
            surface_length=40,
            side_slope=1/3
        )
    assert str(
        exc_info.value) == (
            f"height must be a numeric value, but got {type(f'foo')}."
    )


def test_non_numeric_surface_length():
    with pytest.raises(ValueError) as exc_info:
        dimensions.SimpleTruncatedPyramidWaterBody(
            height=6,
            surface_length="foo",
            side_slope=1/3
        )
    assert str(
        exc_info.value) == (
            "surface_length must be a numeric value, but got "
            f"{type(f'foo')}."
    )


def test_non_numeric_side_slope():
    with pytest.raises(ValueError) as exc_info:
        dimensions.SimpleTruncatedPyramidWaterBody(
            height=6,
            surface_length=40,
            side_slope="foo"
        )
    assert str(
        exc_info.value) == (
            f"side_slope must be a numeric value, but got {type(f'foo')}."
    )


def test_negative_height():
    with pytest.raises(ValueError) as exc_info:
        dimensions.SimpleTruncatedPyramidWaterBody(
            height=-6,
            surface_length=40,
            side_slope=1/3
        )
    assert str(exc_info.value) == "height must be a positive value."


def test_negative_surface_length():
    with pytest.raises(ValueError) as exc_info:
        dimensions.SimpleTruncatedPyramidWaterBody(
            height=6,
            surface_length=-40,
            side_slope=1/3
        )
    assert str(exc_info.value) == (
        "surface_length must be a positive value."
    )


def test_negative_side_slope():
    with pytest.raises(ValueError) as exc_info:
        dimensions.SimpleTruncatedPyramidWaterBody(
            height=6,
            surface_length=40,
            side_slope=-1/3
        )
    assert str(exc_info.value) == "side_slope must be a positive value."


def test_negative_base_length():
    with pytest.raises(ValueError) as exc_info:
        dimensions.SimpleTruncatedPyramidWaterBody(
            height=6,
            surface_length=10,
            side_slope=1/3
        )
    assert str(exc_info.value) == (
        "Invalid combination of height, surface_length, and "
        "side_slope parameters. The calculated base_length of the "
        "polyhedron is currently <=0. base_width is calculated by "
        "(surface_length-(height/side_slope)*2). Adjust your input "
        "parameters to calculate a positive base_length value."
    )


def test_SimpleTruncatedPyramidWaterBody_get_volumes():
    dam = dimensions.SimpleTruncatedPyramidWaterBody(
        height=6,
        surface_length=40,
        side_slope=1/3
    )
    expected_volumes = [0.0, 52.0, 224.0, 588.0, 1216.0, 2180.0, 3552.0]
    assert dam.get_volumes() == pytest.approx(expected_volumes)


def test_SimpleTruncatedPyramidWaterBody_get_surface_areas():
    dam = dimensions.SimpleTruncatedPyramidWaterBody(
        height=6,
        surface_length=40,
        side_slope=1/3
    )
    expected_surface_areas = [16.0, 100.0, 256.0, 484.0, 784.0, 1156.0, 1600.0]
    assert dam.get_surface_areas() == pytest.approx(expected_surface_areas)


def test_SimpleTruncatedPyramidWaterBody_get_heights():
    dam = dimensions.SimpleTruncatedPyramidWaterBody(
        height=6,
        surface_length=40,
        side_slope=1/3
    )
    expected_heights = [-6, -5, -4, -3, -2, -1, 0]
    assert dam.get_heights() == expected_heights

import random
import pandas as pd
import pytest
from glmpy.inflows import CatchmentRunoffInflows


@pytest.fixture
def met_data():
    start_date = "2022-01-01"
    end_date = "2022-01-03"
    date_range = pd.date_range(start=start_date, end=end_date, freq="H")
    random.seed(42)
    met_data = pd.DataFrame(
        {
            "Date": date_range,
            "Rain": [
                random.uniform(0, 0.1) for i in range(0, len(date_range))
            ],
        }
    )
    return met_data

def test_met_data_type():
    with pytest.raises(ValueError) as excinfo:
        CatchmentRunoffInflows(
            met_data=None,
            catchment_area=1000,
            runoff_coef = 0.5,
            precip_col="Rain",
            date_time_col="Date"
        )
    assert (
        str(excinfo.value)
        == f"met_data must be a pandas DataFrame, but got {type(None)}."
    )



def test_catchment_area_type(met_data):
    with pytest.raises(ValueError) as excinfo:
        CatchmentRunoffInflows(
            met_data=met_data,
            catchment_area="foo",
            runoff_coef=0.5,
            precip_col="Rain",
            date_time_col="Date",
        )
    assert str(excinfo.value) == f"catchment_area must be a numeric value, but got {type('foo')}."

def test_runoff_coef_type(met_data):
    with pytest.raises(ValueError) as excinfo:
        CatchmentRunoffInflows(
            met_data=met_data,
            catchment_area=1000,
            runoff_coef='0.5',
            precip_col="Rain",
            date_time_col="Date",
        )
    assert str(excinfo.value) == f"runoff_coef must be a numeric value, but got {type('0.5')}."

def test_runoff_threshold_type(met_data):
    with pytest.raises(ValueError) as excinfo:
        CatchmentRunoffInflows(
            met_data=met_data,
            catchment_area=1000,
            runoff_threshold='10',
            precip_col="Rain",
            date_time_col="Date",
        )
    assert str(excinfo.value) == f"runoff_threshold must be a numeric value, but got {type('10')}."

def test_precip_col_type(met_data):
    with pytest.raises(ValueError) as excinfo:
        CatchmentRunoffInflows(
            met_data=met_data,
            catchment_area=1000,
            runoff_threshold=10,
            precip_col=1,
            date_time_col="Date",
        )
    assert str(excinfo.value) == f"precip_col must be a string, but got {type(1)}."

def test_date_time_col_type(met_data):
    with pytest.raises(ValueError) as excinfo:
        CatchmentRunoffInflows(
            met_data=met_data,
            catchment_area=1000,
            runoff_threshold=10,
            precip_col="Rain",
            date_time_col=1,
        )
    assert str(excinfo.value) == f"date_time_col must be a string, but got {type(1)}."

def test_negative_catchment_area(met_data):
    with pytest.raises(ValueError) as excinfo:
        CatchmentRunoffInflows(
            met_data=met_data,
            catchment_area=-1000.0,
            runoff_coef=0.5,
            precip_col="Rain",
            date_time_col="Date"
        )
    assert str(excinfo.value) == "catchment_area must be a positive value."


def test_invalid_precip_col(met_data):
    with pytest.raises(ValueError) as excinfo:
        CatchmentRunoffInflows(
            met_data=met_data,
            catchment_area=1000,
            runoff_coef=0.5,
            precip_col="NonExistentColumn",
            date_time_col="Date",
        )
    assert (
        str(excinfo.value) == f"{'NonExistentColumn'} not in {met_data} columns."
    )

def test_invalid_date_time_col(met_data):
    with pytest.raises(ValueError) as excinfo:
        CatchmentRunoffInflows(
            met_data=met_data,
            catchment_area=1000,
            runoff_coef=0.5,
            precip_col="Rain",
            date_time_col="NonExistentColumn",
        )
    assert (
        str(excinfo.value) == f"{'NonExistentColumn'} not in {met_data} columns."
    )


def test_missing_runoff_parameters(met_data):
    with pytest.raises(ValueError) as excinfo:
        CatchmentRunoffInflows(
            met_data=met_data,
            catchment_area=1000,
            precip_col="Rain",
            date_time_col="Date"
        )
    assert (
        str(excinfo.value)
        == "Either runoff_coef or runoff_threshold must be provided."
    )


def test_too_many_runoff_parameters(met_data):
    with pytest.raises(ValueError) as excinfo:
        CatchmentRunoffInflows(
            met_data=met_data,
            runoff_coef=0.5,
            runoff_threshold=10.0,
            catchment_area=1000,
            precip_col="Rain",
            date_time_col="Date"
        )
    assert (
        str(excinfo.value)
        == "Only one of runoff_coef or runoff_threshold can be provided."
    )



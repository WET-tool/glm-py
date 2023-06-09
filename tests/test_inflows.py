import random
import pandas as pd
import pytest
from glmpy.inflows import CatchmentInflows


@pytest.fixture
def met_data():
    start_date = '2022-01-01'
    end_date = '2022-01-03'
    date_range = pd.date_range(
        start=start_date, end=end_date, freq='H')
    random.seed(42)
    met_data = pd.DataFrame({
        'Date': date_range,
        'Rain': [random.uniform(0, 0.1) for i in range(0, len(date_range))]
    })
    return met_data


def test_missing_file_path():
    with pytest.raises(ValueError) as inflows_info:
        CatchmentInflows(
            input_type='file',
            catchment_area=1000,
            precip_col='Rain',
            date_time_col='Date',
            date_time_format='%Y-%m-%d %H:%M:%S'
        )
    assert str(
        inflows_info.value) == "path_to_met_csv cannot be None when input_type is 'file'."


def test_missing_data_frame():
    with pytest.raises(ValueError) as inflows_info:
        CatchmentInflows(
            input_type='dataframe',
            catchment_area=1000,
            precip_col='Rain',
            date_time_col='Date',
            date_time_format='%Y-%m-%d %H:%M:%S'
        )
    assert str(
        inflows_info.value) == "met_data cannot be None when input_type is 'dataframe'."


def test_invalid_input_type():
    with pytest.raises(ValueError) as inflows_info:
        CatchmentInflows(
            input_type='foo',
            catchment_area=1000,
            precip_col='Rain',
            date_time_col='Date',
            date_time_format='%Y-%m-%d %H:%M:%S'
        )
    assert str(
        inflows_info.value) == "Invalid input_type. Must be 'file' or 'dataframe'."


def test_non_numeric_catchment_area(met_data):
    with pytest.raises(ValueError) as inflows_info:
        CatchmentInflows(
            input_type='dataframe',
            met_data=met_data,
            catchment_area='foo',
            runoff_coef=0.5,
            precip_col='Rain',
            date_time_col='Date',
            date_time_format='%Y-%m-%d %H:%M:%S'
        )
    assert str(
        inflows_info.value) == "catchment_area must be numeric."


def test_negative_catchment_area(met_data):
    with pytest.raises(ValueError) as inflows_info:
        CatchmentInflows(
            input_type='dataframe',
            met_data=met_data,
            catchment_area=-1000.0,
            runoff_coef=0.5,
            precip_col='Rain',
            date_time_col='Date',
            date_time_format='%Y-%m-%d %H:%M:%S'
        )
    assert str(
        inflows_info.value) == "catchment_area must be positive."


def test_invalid_precip_col(met_data):
    with pytest.raises(ValueError) as inflows_info:
        CatchmentInflows(
            input_type='dataframe',
            met_data=met_data,
            catchment_area=1000,
            precip_col='NonExistentColumn',
            date_time_col='Date',
            date_time_format='%Y-%m-%d %H:%M:%S'
        )
    assert str(
        inflows_info.value) == "NonExistentColumn not in met_data columns."


def test_missing_runoff_parameters(met_data):
    with pytest.raises(ValueError) as inflows_info:
        CatchmentInflows(
            input_type='dataframe',
            met_data=met_data,
            catchment_area=1000,
            precip_col='Rain',
            date_time_col='Date',
            date_time_format='%Y-%m-%d %H:%M:%S'
        )
    assert str(
        inflows_info.value) == "Either runoff_coef or runoff_threshold must be provided."


def test_too_many_runoff_parameters(met_data):
    with pytest.raises(ValueError) as inflows_info:
        CatchmentInflows(
            input_type='dataframe',
            met_data=met_data,
            runoff_coef=0.5,
            runoff_threshold=10.0,
            catchment_area=1000,
            precip_col='Rain',
            date_time_col='Date',
            date_time_format='%Y-%m-%d %H:%M:%S'
        )
    assert str(
        inflows_info.value) == "Only one of runoff_coef or runoff_threshold can be provided."


def test_non_numeric_runoff_coef(met_data):
    with pytest.raises(ValueError) as inflows_info:
        CatchmentInflows(
            input_type='dataframe',
            met_data=met_data,
            runoff_coef='foo',
            catchment_area=1000,
            precip_col='Rain',
            date_time_col='Date',
            date_time_format='%Y-%m-%d %H:%M:%S'
        )
    assert str(
        inflows_info.value) == "runoff_coef must be numeric."


def test_non_numeric_runoff_threshold(met_data):
    with pytest.raises(ValueError) as inflows_info:
        CatchmentInflows(
            input_type='dataframe',
            met_data=met_data,
            runoff_threshold='foo',
            catchment_area=1000,
            precip_col='Rain',
            date_time_col='Date',
            date_time_format='%Y-%m-%d %H:%M:%S'
        )
    assert str(
        inflows_info.value) == "runoff_threshold must be numeric."


def test_date_time_parsing(met_data):
    inflows = CatchmentInflows(
        input_type='dataframe',
        met_data=met_data,
        catchment_area=1000,
        runoff_coef=0.5,
        precip_col='Rain',
        date_time_col='Date',
        date_time_format='%Y-%m-%d %H:%M:%S'
    )
    assert inflows.catchment_inflows.index.equals(
        pd.DatetimeIndex(met_data['Date']))


def test_inflow_calculation(met_data):
    inflows = CatchmentInflows(
        input_type='dataframe',
        met_data=met_data,
        catchment_area=1000,
        runoff_coef=0.5,
        precip_col='Rain',
        date_time_col='Date',
        date_time_format='%Y-%m-%d %H:%M:%S'
    )
    assert inflows.catchment_inflows['flow'].reset_index(drop=True).equals(
        (met_data['Rain'] * 1000 * 0.5 / 86400).reset_index(drop=True))


def test_file_io(met_data, tmp_path):
    met_data_path = tmp_path / "met_data.csv"
    met_data.to_csv(met_data_path)

    inflows = CatchmentInflows(
        input_type='file',
        path_to_met_csv=met_data_path,
        catchment_area=1000,
        runoff_coef=0.5,
        precip_col='Rain',
        date_time_col='Date',
        date_time_format='%Y-%m-%d %H:%M:%S'
    )
    assert isinstance(inflows.catchment_inflows, pd.DataFrame)

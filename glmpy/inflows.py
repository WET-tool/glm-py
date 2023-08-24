from typing import Union

import pandas as pd

class CatchmentRunoffInflows:
    """
    Calculate runoff inflows from a catchment.

    Generates an inflows timeseries by calculating catchment runoff from
    a pandas Dataframe of precipitation data. Requires a catchment area, a
    runoff coefficient or threshold, and a precipitation timeseries in either
    hourly or daily timesteps. Inflows are calculated at the same timestep as
    the precipitation data but in units of m^3/s. `CatchmentRunoffInflows`
    provides methods to return the calculated inflows timeseries as a pandas
    DataFrame or to write the timeseries to a CSV.

    Attributes
    ----------
    met_data : Union[pd.DataFrame, None]
        A pandas DataFrame of meteorological data.
    precip_col : str
        Name of the column in the DataFrame containing precipitation data in
        m/day or m/hour.
    date_time_col : str
        Name of the column in the DataFrame containing datetime data.
    catchment_area : float
        Area of the catchment in square meters.
    runoff_coef : Union[float, None]
        Runoff coefficient for the catchment. The fraction of rainfall that
        will result in runoff. Either `runoff_coef` or `runoff_threshold`
        must be provided.
    runoff_threshold : Union[float, None]
        Runoff threshold for the catchment. The amount of rainfall in mm to
        generate runoff. Either `runoff_coef` or `runoff_threshold` must be
        provided.


    Examples
    --------
    Generate a daily timeseries of rainfall:
    >>> daily_met_data = pd.DataFrame({
    ... 'Date': pd.date_range(
    ...     start='1997-01-01',
    ...     end='2004-12-31',
    ...     freq='24H'),
    ... 'Rain': 0.024 #m per day
    ... })

    Calculate inflows with a 50% runoff coefficient and a 1000 m^2 catchment
    area:
    >>> inflows_data = inflows.CatchmentRunoffInflows(
    ...     met_data = daily_met_data,
    ...     catchment_area = 1000,
    ...     runoff_coef = 0.5,
    ...     precip_col = 'Rain',
    ...     date_time_col = 'Date'
    ... )
    >>> inflows_data.get_inflows()

    Generate a hourly timeseries of rainfall:
    >>> hourly_met_data = pd.DataFrame({
    ... 'Date': pd.date_range(
    ...     start='1997-01-01',
    ...     end='2004-12-31',
    ...     freq='1H'),
    ... 'Rain': 0.001
    ... })

    Calculate inflows with a 50% runoff coefficient and a 1000 m^2 catchment
    area:
    >>> inflows_data = inflows.CatchmentRunoffInflows(
    ...     met_data = hourly_met_data,
    ...     catchment_area = 1000,
    ...     runoff_coef = 0.5,
    ...     precip_col = 'Rain',
    ...     date_time_col = 'Date'
    ... )
    >>> inflows_data.get_inflows()
    """

    def __init__(
        self,
        met_data: pd.DataFrame,
        precip_col: str,
        date_time_col: str,
        catchment_area: Union[float, int],
        runoff_coef: Union[float, int, None] = None,
        runoff_threshold: Union[float, None] = None,
    ):
        if not isinstance(met_data, pd.DataFrame):
            raise ValueError(
                f"met_data must be a pandas DataFrame, but got {type(met_data)}."
            )
        if not isinstance(catchment_area, (int, float)):
            raise ValueError(
                f"catchment_area must be a numeric value, but got {type(catchment_area)}."
            )
        if not isinstance(runoff_coef, (int, float, type(None))):
            raise ValueError(
                f"runoff_coef must be a numeric value, but got {type(runoff_coef)}."
            )
        if not isinstance(runoff_threshold, (int, float, type(None))):
            raise ValueError(
                f"runoff_threshold must be a numeric value, but got {type(runoff_threshold)}."
            )
        if not isinstance(precip_col, str):
            raise ValueError(
                f"precip_col must be a string, but got {type(precip_col)}."
            )
        if not isinstance(date_time_col, str):
            raise ValueError(
                f"date_time_col must be a string, but got {type(date_time_col)}."
            )

        if catchment_area < 0:
            raise ValueError("catchment_area must be a positive value.")
        if precip_col not in met_data.columns:
            raise ValueError(f"{precip_col} not in {met_data} columns.")
        if date_time_col not in met_data.columns:
            raise ValueError(f"{date_time_col} not in {met_data} columns.")
        if runoff_coef is None and runoff_threshold is None:
            raise ValueError("Either runoff_coef or runoff_threshold must be provided.")
        if runoff_coef is not None and runoff_threshold is not None:
            raise ValueError(
                "Only one of runoff_coef or runoff_threshold can be provided."
            )
        try:
            met_data[date_time_col] = pd.to_datetime(
                met_data[date_time_col], errors="raise"
            )
        except Exception as e:
            raise ValueError(
                f"{date_time_col} is not a valid datetime column. Error:{str(e)}"
            )

        time_diff = met_data[date_time_col][1] - met_data[date_time_col][0]
        if time_diff != pd.Timedelta(days=1) and time_diff != pd.Timedelta(hours=1):
            raise ValueError(
                "Precipitation data must be hourly or daily timesteps.vConsider resampling your data."
            )

        self.precip_col = precip_col
        self.catchment_area = catchment_area
        self.runoff_coef = runoff_coef
        self.runoff_threshold = runoff_threshold
        self.date_time_col = date_time_col
        self.met_data = met_data
        self.catchment_runoff_inflows = None

    def _calculate_inflows(self):
        """
        Calculates inflows from catchment runoff.
        """
        self.time_diff = (
            self.met_data[self.date_time_col][1] - self.met_data[self.date_time_col][0]
        )

        if self.time_diff == pd.Timedelta(hours=1):
            self.num_seconds = 3600
        elif self.time_diff == pd.Timedelta(days=1):
            self.num_seconds = 86400

        if self.runoff_coef is not None:
            self.inflow_data = (
                self.met_data[self.precip_col] * self.catchment_area * self.runoff_coef
            )
            self.inflow_data[self.inflow_data < 0] = 0
        else:
            self.runoff_threshold /= 1000
            self.inflow_data = (
                self.met_data[self.precip_col] - self.runoff_threshold
            ) * self.catchment_area
            self.inflow_data[self.inflow_data < 0] = 0

        self.inflow_data = self.inflow_data / self.num_seconds

        self.catchment_runoff_inflows = pd.DataFrame(
            {"time": self.met_data[self.date_time_col], "flow": self.inflow_data}
        )
        self.catchment_runoff_inflows.set_index("time", inplace=True)

    def get_inflows(self):
        """
        Get the inflows timeseries.

        Returns a pandas dataframe of the calculated catchment runoff inflows.

        Returns
        -------
        inflows : pd.DataFrame
            DataFrame of inflow data.

        Examples
        --------
        Generate a hourly timeseries of rainfall:
        >>> hourly_met_data = pd.DataFrame({
        ... 'Date': pd.date_range(
        ...     start='1997-01-01',
        ...     end='2004-12-31',
        ...     freq='1H'),
        ... 'Rain': 0.001
        ... })

        Calculate inflows with a 50% runoff coefficient and a 1000 m^2
        catchment area
        >>> inflows_data = inflows.CatchmentRunoffInflows(
        ...     met_data = hourly_met_data,
        ...     catchment_area = 1000,
        ...     runoff_coef = 0.5,
        ...     precip_col = 'Rain',
        ...     date_time_col = 'Date'
        ... )

        Call `get_inflows` to return the inflows timeseries:
        >>> inflows_data.get_inflows()
        """

        if self.catchment_runoff_inflows is None:
            self._calculate_inflows()
        return self.catchment_runoff_inflows

    def write_inflows(self, file_path: str):
        """
        Write the inflow timeseries to a CSV file.

        Calculates catchment runoff inflows and writes the timeseries to a CSV.

        Parameters
        ----------
        file_path : str
            Path to the output CSV file.

        Examples
        --------
        >>> from glmpy import inflows
        >>> daily_met_data = pd.DataFrame({
        ...     'Date': pd.date_range(
        ...         start='1997-01-01',
        ...         end='2004-12-31',
        ...         freq='24H'),
        ...     'Rain': 0.024
        ... })
        >>> inflows_data = inflows.CatchmentRunoffInflows(
        ...     met_data = daily_met_data,
        ...     catchment_area = 1000,
        ...     runoff_coef = 0.5,
        ...     precip_col = 'Rain',
        ...     date_time_col = 'Date'
        ... )

        Call `write_inflows` to write the inflows timeseries to a CSV:
        >>> inflows_data.write_inflows(file_path='runoff.csv')
        """

        if self.catchment_runoff_inflows is None:
            self._calculate_inflows()
        self.catchment_runoff_inflows.to_csv(file_path)

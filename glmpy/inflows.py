from typing import Union

import pandas as pd


class CatchmentRunoffInflows:
    """
    Calculate runoff inflows from a catchment.

    Generates an inflows timeseries by calculating catchment runoff from
    precipitation data. Requires a catchment area, a runoff coefficient or
    threshold, and a precipitation timeseries in either hourly or daily
    timesteps (the precipitation timeseries should be in units of m ).
    `CatchmentRunoffInflows` resamples the precipitation data to
    daily timesteps before calculating inflows. As per GLM requirements, the
    inflows timeseries is recorded at a daily timestep but in units of m^3/s.

    Attributes
    ----------
    input_type : str
        Type of input data. Must be 'file' or 'dataframe'. Defaults to
        'file'.
    path_to_met_csv : Union[str, None]
        Path to the CSV file containing the meteorological data. Required
        if `input_type` is 'file'.
    met_data : Union[pd.DataFrame, None]
        DataFrame of meteorological data. Required if `input_type` is
        'dataframe'.
    precip_col : str
        Name of the column in the CSV file containing precipitation data in
        m/day or m/hour.
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
    date_time_col : str
        Name of the column in the CSV file containing datetime data.
    date_time_format : str
        Format of the datetime data. Defaults to '%Y-%m-%d %H:%M'.

    Examples
    --------
    Daily precipitation with a runoff coefficient:
    >>> met_data_daily = pd.DataFrame({
    >>> 'Date': pd.date_range(
    ...     start='1997-01-01',
    ...     end='2004-12-31',
    ...     freq='D'),
    ... 'Rain': 0.024 #m per day
    ... })
    >>> inflows_data = CatchmentRunoffInflows(
    ...     input_type = 'dataframe',
    ...     met_data = met_data_daily,
    ...     catchment_area = 1000,
    ...     runoff_coef = 0.5,
    ...     precip_col = 'Rain',
    ...     date_time_col = 'Date',
    ...     date_time_format= '%Y-%m-%d'
    ... )
    >>> inflows_data.write_inflows('runoff.csv')

    Hourly precipitation with a runoff coefficient:
    >>> met_data_hourly = pd.DataFrame({
    >>> 'Date': pd.date_range(
    ...     start='1997-01-01',
    ...     end='2004-12-31',
    ...     freq='H'),
    ... 'Rain': 0.001 #m per hour
    ... })
    >>> met_data_hourly.to_csv('met_data_hourly.csv')
    >>> inflows_data = CatchmentRunoffInflows(
    ...     input_type = 'file',
    ...     path_to_met_csv = 'met_data_hourly.csv',
    ...     catchment_area = 1000,
    ...     runoff_threshold = 10,
    ...     precip_col = 'Rain',
    ...     date_time_col = 'Date',
    ...     date_time_format= '%Y-%m-%d %H:%M:%S'
    ... )
    >>> inflows_data.write_inflows('runoff.csv')

    Daily precipitation with a runoff threshold:
    >>> met_data_daily = pd.DataFrame({
    ...     'Date': pd.date_range(
    ...         start='1997-01-01',
    ...         end='2004-12-31',
    ...         freq='D'),
    ...     'Rain': 0.024 #m per day
    ... })
    >>> inflows_data = CatchmentRunoffInflows(
    ...     input_type = 'dataframe',
    ...     met_data = met_data_daily,
    ...     catchment_area = 1000,
    ...     runoff_threshold = 10,
    ...     precip_col = 'Rain',
    ...     date_time_col = 'Date',
    ...     date_time_format= '%Y-%m-%d'
    ... )
    >>> inflows_data.write_inflows('runoff.csv')

    Hourly precipitation with a runoff threshold:
    >>> met_data_hourly = pd.DataFrame({
    ...     'Date': pd.date_range(
    ...         start='1997-01-01',
    ...         end='2004-12-31',
    ...         freq='H'),
    ...     'Rain': 0.001 #m per hour
    ... })
    >>> met_data_hourly.to_csv('met_data_hourly.csv')
    >>> inflows_data = CatchmentRunoffInflows(
    ...     input_type = 'file',
    ...     path_to_met_csv = 'met_data_hourly.csv',
    ...     catchment_area = 1000,
    ...     runoff_threshold = 10,
    ...     precip_col = 'Rain',
    ...     date_time_col = 'Date',
    ...     date_time_format= '%Y-%m-%d %H:%M:%S'
    ... )
    >>> inflows_data.write_inflows('runoff.csv')
    """

    def __init__(
        self,
        precip_col: str,
        catchment_area: float,
        date_time_col: str,
        runoff_coef: Union[float, None] = None,
        runoff_threshold: Union[float, None] = None,
        input_type: str = "file",
        path_to_met_csv: Union[str, None] = None,
        met_data: Union[pd.DataFrame, None] = None,
        date_time_format: str = "%Y-%m-%d %H:%M",
    ):
        self.input_type = input_type
        self.path_to_met_csv = path_to_met_csv
        self.precip_col = precip_col
        self.catchment_area = catchment_area
        self.runoff_coef = runoff_coef
        self.runoff_threshold = runoff_threshold
        self.date_time_col = date_time_col
        self.date_time_format = date_time_format

        if self.input_type == "file":
            if path_to_met_csv is None:
                raise ValueError(
                    "path_to_met_csv cannot be None when input_type is 'file'."
                )
            self.met_data = pd.read_csv(path_to_met_csv)
        elif self.input_type == "dataframe":
            if met_data is None:
                raise ValueError(
                    "met_data cannot be None when input_type is 'dataframe'."
                )
            self.met_data = met_data
        else:
            raise ValueError(
                "Invalid input_type. Must be 'file' or 'dataframe'."
            )

        if not isinstance(self.catchment_area, (int, float)):
            raise ValueError("catchment_area must be numeric.")

        if self.catchment_area < 0:
            raise ValueError("catchment_area must be positive.")

        if self.precip_col not in self.met_data.columns:
            raise ValueError(f"{self.precip_col} not in met_data columns.")

        if self.date_time_col not in self.met_data.columns:
            raise ValueError(f"{self.date_time_col} not in met_data columns.")

        if self.runoff_coef is None and self.runoff_threshold is None:
            raise ValueError(
                "Either runoff_coef or runoff_threshold must be provided."
            )

        if self.runoff_coef is not None and self.runoff_threshold is not None:
            raise ValueError(
                "Only one of runoff_coef or runoff_threshold can be provided."
            )

        self.met_data[self.date_time_col] = pd.to_datetime(
            self.met_data[self.date_time_col], format=self.date_time_format
        )
        self.met_data.set_index(self.date_time_col, inplace=True)

        time_diff = self.met_data.index[1] - self.met_data.index[0]

        if time_diff == pd.Timedelta(hours=1):
            self.met_data = self.met_data.resample("D").sum()

        precip_data = self.met_data[self.precip_col].astype(float)

        if self.runoff_coef is not None:
            if not isinstance(self.runoff_coef, (int, float)):
                raise ValueError("runoff_coef must be numeric.")
            inflow_data = precip_data * self.catchment_area * self.runoff_coef
            inflow_data[inflow_data < 0] = 0
        else:
            if not isinstance(self.runoff_threshold, (int, float)):
                raise ValueError("runoff_threshold must be numeric.")
            self.runoff_threshold /= 1000
            inflow_data = (
                precip_data - self.runoff_threshold
            ) * self.catchment_area
            inflow_data[inflow_data < 0] = 0

        # note that inflow data in m is = to m^3
        inflow_data = inflow_data / 86400

        self.catchment_inflows = pd.DataFrame(
            {"time": self.met_data.index, "flow": inflow_data}
        )
        self.catchment_inflows.set_index("time", inplace=True)

    def get_inflows(self):
        """
        Get the inflows timeseries.

        Returns the inflows timeseries as a pandas dataframe.

        Returns
        -------
        inflows : pd.DataFrame
            DataFrame of inflow data.

        Examples
        --------
        >>> from glmpy import inflows
        >>> met_data = pd.DataFrame({
        ...     'Date': pd.date_range(
        ...         start='1997-01-01',
        ...         end='2004-12-31',
        ...         freq='H'),
        ...     'Rain': 10
        ... })
        >>> met_data.to_csv('met_data.csv', index=False)
        >>> inflows_data = inflows.CatchmentRunoffInflows(
        ...     input_type = 'file',
        ...     path_to_met_csv = 'met_data.csv',
        ...     catchment_area = 1000,
        ...     runoff_coef = 0.5,
        ...     precip_col = 'Rain',
        ...     date_time_col = 'Date',
        ...     date_time_format= '%Y-%m-%d %H:%M:%S'
        ... )
        >>> inflows_data.get_inflows()
        """
        return self.catchment_inflows

    def write_inflows(self, path_to_inflow_csv: str):
        """
        Writes the inflow timseries to a CSV file.

        The inflow data exported to a CSV file with two columns: 'time' and
        'flow'.

        Parameters
        ----------
        path_to_inflow_csv : str
            Path to the output CSV file.

        Examples
        --------
        >>> from glmpy import inflows
        >>> met_data = pd.DataFrame({
        ...     'Date': pd.date_range(
        ...         start='1997-01-01',
        ...         end='2004-12-31',
        ...         freq='H'),
        ...     'Rain': 10
        ... })
        >>> met_data.to_csv('met_data.csv', index=False)
        >>> inflows_data = inflows.CatchmentRunoffInflows(
        ...     input_type = 'file',
        ...     path_to_met_csv = 'met_data.csv',
        ...     catchment_area = 1000,
        ...     runoff_coef = 0.5,
        ...     precip_col = 'Rain',
        ...     date_time_col = 'Date',
        ...     date_time_format= '%Y-%m-%d %H:%M:%S'
        ... )
        >>> inflows_data.write_inflows('runoff.csv')
        """
        self.catchment_inflows.to_csv(path_to_inflow_csv)

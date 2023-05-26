import pandas as pd


class CatchmentInflows:
    """
    Calculates the catchment inflows for the GLM model.

    The `CatchmentInflows` class reads the GLM meteorological data from a CSV file, calculates inflows (m^3) using the provided catchment area and runoff coefficient,
    and writes the inflows to a CSV file. The data can be optionally resampled from hourly to daily timestep before writing.

    Attributes
    ----------
        path_to_met_csv : str
            Path to the CSV file containing the meteorological data.
        precip_col : str
            Name of the column in the CSV file containing precipitation data.
        catchment_area : float
            Area of the catchment in square meters.
        runoff_coef : float
            Runoff coefficient for the catchment. The fraction of rainfall that will result in runoff.
        date_time_col : str
            Name of the column in the CSV file containing datetime data.
        date_time_format : str
            Format of the datetime data. Defaults to '%Y-%m-%d %H:%M'.

    Examples
    --------
    >>> from glmpy import CatchmentInflows
    >>> met_data = pd.DataFrame({
    ...     'Date': pd.date_range(start='1997-01-01', end='2004-12-31', freq='H'),
    ...     'Rain': 0.1
    ... })
    >>> met_data.to_csv("met_data.csv")
    >>> inflows = CatchmentInflows(
    ...     path_to_met_csv = 'met_data.csv',
    ...     catchment_area = 1000,
    ...     runoff_coef = 1,
    ...     precip_col = 'Rain',
    ...     date_time_col = 'Date',
    ...     date_time_format= '%Y-%m-%d %H:%M:%S'
    ... )
    >>> inflows.write_inflows("runoff.csv", resample_daily = True)

    """

    def __init__(
            self,
            path_to_met_csv: str,
            precip_col: str,
            catchment_area: float,
            runoff_coef: float,
            date_time_col: str,
            date_time_format: str = '%Y-%m-%d %H:%M'
    ):
        self.path_to_met_csv = path_to_met_csv
        self.precip_col = precip_col
        self.catchment_area = catchment_area
        self.runoff_coef = runoff_coef
        self.date_time_col = date_time_col
        self.date_time_format = date_time_format

        met_data = pd.read_csv(path_to_met_csv)

        self.catchment_inflows = pd.DataFrame({
            'time': pd.to_datetime(met_data[self.date_time_col], format=self.date_time_format),
            'flow': met_data[self.precip_col] * self.catchment_area * self.runoff_coef
        })

        self.catchment_inflows.set_index('time', inplace=True)

    def write_inflows(
            self,
            path_to_inflow_csv: str,
            resample_daily: bool = False,
    ):
        """
        Writes the inflow data to a CSV file.

        The inflow data can be optionally resampled from hourly to daily timestep before writing.

        Parameters
        ----------
            path_to_inflow_csv : str
                Path to the output CSV file.
            resample_daily : bool
                If True, resample the inflow data from hourly to daily timestep. Defaults to False.

        Examples
        --------
        >>> from glmpy import CatchmentInflows
        >>> met_data = pd.DataFrame({
        ...     'Date': pd.date_range(start='1997-01-01', end='2004-12-31', freq='H'),
        ...     'Rain': 0.1
        ... })
        >>> met_data.to_csv("met_data.csv")
        >>> inflows = CatchmentInflows(
        ...     path_to_met_csv = 'met_data.csv',
        ...     catchment_area = 1000,
        ...     runoff_coef = 1,
        ...     precip_col = 'Rain',
        ...     date_time_col = 'Date',
        ...     date_time_format= '%Y-%m-%d %H:%M:%S'
        ... )
        >>> inflows.write_inflows("runoff.csv", resample_daily = True)
        """
        if resample_daily is False:
            self.catchment_inflows.to_csv(path_to_inflow_csv)
        else:
            self.catchment_inflows = self.catchment_inflows.resample('D').sum()
            self.catchment_inflows.to_csv(path_to_inflow_csv)

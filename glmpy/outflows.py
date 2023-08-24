from datetime import datetime

import pandas as pd

from typing import Dict, Union

class CustomOutflows:
    """
    Create a simple outflow timeseries for GLM.

    Generates a outflow timeseries between a given start and end date
    using a specified base flow (m^3). The timeseries can be updated in
    two ways:
    1. By providing a dictionary with specific dates and their corresponding
    outflows.
    2. By specifying a fixed outflow value between two dates.
    Once updated, the outflow data can be exported to a CSV file in units of
    m^3/second.

    Attributes
    ----------
    start_datetime : str
        Start datetime of the outflow timeseries. Must be in either
        'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS' format.
    end_datetime : str
        End datetime of the outflow timeseries. Must be in either 'YYYY-MM-DD'
        or 'YYYY-MM-DD HH:MM:SS' format.
    frequency : str
        Frequency of the outflow timeseries. Must be either 'daily' or
        'hourly'. Defaults to 'daily'.
    base_outflow : Union[int, float]
        Base flow of the outflow timeseries in m^3/day or m^3/hour depending on
        `frequency`. Defaults to 0.0.

    Examples
    --------
    >>> from glmpy import outflows

    Initialise a daily outflow timeseries with a base outflow of 0.0 m^3/day:
    >>> outflows = outflows.CustomOutflows(
    ...     start_datetime="2020-01-01",
    ...     end_datetime="2020-01-10",
    ...     frequency="daily",
    ...     base_outflow=0.0
    ... )

    Update the timeseries with a dictionary of specific dates and their
    corresponding outflows:
    >>> outflows_dict = {
    ...     "2020-01-01 00:00:00": 10,
    ...     "2020-01-02 00:00:00": 11,
    ...     "2020-01-03 00:00:00": 12
    ... }
    >>> outflows.set_discrete_outflows(outflows_dict)

    Return the outflows timeseries as a pandas DataFrame:
    >>> outflows.get_outflows()

    Update the timeseries with a fixed outflow between two dates:
    >>> outflows.set_continuous_outflows(
    ...     from_datetime="2020-01-05",
    ...     to_datetime = "2020-01-09",
    ...     continuous_outflow = 9
    ... )

    Return the updated timeseries:
    >>> outflows.get_outflows()
    """

    def __init__(self, start_datetime: str, end_datetime: str, frequency: str = "daily", base_outflow: Union[int, float] = 0.0):
        if not isinstance(start_datetime, str):
            raise ValueError(
                f"start_datetime must be a string, but got {type(start_datetime)}."
            )
        if not isinstance(end_datetime, str):
            raise ValueError(
                f"end_datetime must be a string, but got {type(end_datetime)}."
            )
        if not CustomOutflows.is_valid_datetime(start_datetime):
            raise ValueError(
                f"'{start_datetime}' is not a valid datetime string. Must be provided in the format '%Y-%m-%d %H:%M:%S' or '%Y-%m-%d'"
            )
        if not CustomOutflows.is_valid_datetime(end_datetime):
            raise ValueError(
                f"'{end_datetime}' is not a valid datetime string. Must be provided in the format '%Y-%m-%d %H:%M:%S' or '%Y-%m-%d'"
            )
        if not CustomOutflows.is_valid_datetime_order(start_dt_string=start_datetime, end_dt_string=end_datetime):
            raise ValueError(
                f"start_datetime must occur before end_datetime. Currently {start_datetime} >= {end_datetime}."
            )
        if not isinstance(frequency, str):
            raise ValueError(
                f"frequency must be a string, but got {type(frequency)}."
            )
        if frequency != "daily" and frequency != "hourly":
            raise ValueError(
                f"frequency must be either `daily` or `hourly, got {frequency}."
            )
        if not isinstance(base_outflow, (int, float)):
            raise ValueError(
                f"base_outflow must be numeric, but got {type(base_outflow)}."
            )
        if base_outflow < 0:
            raise ValueError(
                f"base_outflow must be a positive value, got {base_outflow}."
            )

        self.start_datetime = CustomOutflows.to_datetime_format(start_datetime)
        self.end_datetime = CustomOutflows.to_datetime_format(end_datetime)
        self.frequency = frequency
        self.base_outflow = base_outflow

        if self.frequency == "daily":
            freq = "24H"
            self.num_seconds = 86400
        elif self.frequency == "hourly":
            freq = "1H"
            self.num_seconds = 3600

        self.custom_outflows = pd.DataFrame({
            "time": pd.date_range(
                start=self.start_datetime,
                end=self.end_datetime,
                freq=freq
            ),
            "flow": self.base_outflow/self.num_seconds
        })

    def set_discrete_outflows(self, outflows_dict: Dict[str, Union[int, float]]):
        """
        Set the outflow volume for specific datetimes.

        The outflow volume for specific datetimes can be set by providing a
        dictionary with datetimes as keys and outflow volumes as values. The
        dictionary keys must be in 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS.
        Outflow volumes must be provided in the same units as the base outflow
        (m^3/day or m^3/hour).

        Parameters
        ----------
        outflows_dict : Dict[str, Union[int, float]]
            Dictionary with datetimes as keys and outflow volumes as values.

        Examples
        --------
        >>> from glmpy import outflows
        >>> outflows = outflows.CustomOutflows(
        ...     start_datetime="2020-01-01 00:00:00",
        ...     end_datetime="2020-01-01 23:00:00",
        ...     frequency="hourly",
        ...     base_outflow=0.0
        ... )
        >>> outflows_dict = {
        ...     "2020-01-01 01:00:00": 10,
        ...     "2020-01-01 02:00:00": 11,
        ...     "2020-01-01 03:00:00": 12
        ... }
        >>> outflows.set_discrete_outflows(outflows_dict)
        >>> outflows.get_outflows()
        """

        if not isinstance(outflows_dict, dict):
            raise ValueError(
                f"outflows_dict must be a dictionary, but got {type(outflows_dict)}."
                )
        if not all(isinstance(key, str) for key in outflows_dict.keys()):
            raise ValueError(
                f"outflows_dict.keys() must be strings, but got {type(outflows_dict.keys())}."
            )
        if not all(CustomOutflows.is_valid_datetime(dt_string=key) for key in outflows_dict.keys()):
            raise ValueError(
                 "outflows_dict keys must be in either '%Y-%m-%d' or '%Y-%m-%d %H:%M:%S' format."
            )
        if not all(CustomOutflows.is_within_date_range(dt_string=CustomOutflows.to_datetime_format(dt_string=key), start_dt_string=self.start_datetime, end_dt_string=self.end_datetime) for key in outflows_dict.keys()):
            raise ValueError(
                f"outflows_dict keys must be within start_datetime and end_datetime. Check {self.start_datetime} <= outflows_dict.keys() <= {self.end_datetime}."
            )
        if not all(pd.to_datetime(pd.Series(list(outflows_dict.keys()))).isin(self.custom_outflows["time"])):
            raise ValueError(
                f"One or more outflows_dict.keys() does not exist in the {self.frequency} timeseries between {self.start_datetime} and {self.end_datetime}."
            )
        if not all(isinstance(value, (int, float)) for value in outflows_dict.values()):
            raise ValueError(
                 f"outflows_dict.values() must be numeric, but got {type(outflows_dict.values())}."
            )
        if not all(value > 0 for value in outflows_dict.values()):
            raise ValueError(
                 f"outflows_dict.values() must be positive."
            )

        self.outflows_dict = outflows_dict

        self.custom_outflows.set_index("time", inplace=True)

        for key, value in outflows_dict.items():
            self.custom_outflows.at[pd.to_datetime(key), 'flow'] = value/self.num_seconds

        self.custom_outflows.reset_index(inplace=True)

    def set_continuous_outflows(self, from_datetime: str, to_datetime: str, continuous_outflow: Union[float, int]):
        """
        Set the outflow volume between two datetimes.

        Outflow volumes between two datetimes can be set by providing a start
        datetime, end datetime and an outflow volume.

        Parameters
        ----------
        from_datetime : str
            Update the outflow timeseries from this datetime. Must be in
            'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS' format.
        to_datetime : str
             Update the outflow timeseries to this datetime. Must be in
             'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS' format.
        continuous_outflow : float
            The outflow volume to set between the `from_datetime` and
            `to_datetime` in m^3/day or m^3/hour.

        Examples
        --------
        >>> from glmpy import outflows
        >>> outflows = outflows.CustomOutflows(
        ...     start_datetime="2020-01-01 00:00:00",
        ...     end_datetime="2020-01-01 23:00:00",
        ...     frequency="hourly",
        ...     base_outflow=0.0
        ... )
        >>> outflows.set_continuous_outflows(
        ...     from_datetime="2020-01-01 01:00:00",
        ...     to_datetime = "2020-01-01 10:00:00",
        ...     continuous_outflow = 9
        ... )
        >>> outflows.get_outflows()
        """
        if not isinstance(from_datetime, str):
            raise ValueError(
                f"from_datetime must be a string, but got {type(from_datetime)}."
            )
        if not isinstance(to_datetime, str):
            raise ValueError(
                f"to_datetime must be a string, but got {type(to_datetime)}."
            )
        if not CustomOutflows.is_valid_datetime(from_datetime):
            raise ValueError(
                f"'{from_datetime}' is not a valid datetime string. Must be provided in the format '%Y-%m-%d %H:%M:%S' or '%Y-%m-%d'"
            )
        if not CustomOutflows.is_valid_datetime(to_datetime):
            raise ValueError(
                f"'{to_datetime}' is not a valid datetime string. Must be provided in the format '%Y-%m-%d %H:%M:%S' or '%Y-%m-%d'"
            )
        if not isinstance(continuous_outflow, (int, float)):
            raise ValueError(
                f"continuous_outflow must be numeric, but got {type(continuous_outflow)}."
            )
        if continuous_outflow < 0:
            raise ValueError(
                f"continuous_outflow must be a positive value, got {continuous_outflow}."
            )

        self.from_datetime = from_datetime
        self.to_datetime = to_datetime
        self.continuous_outflow = continuous_outflow

        self.custom_outflows.set_index("time", inplace=True)

        self.custom_outflows.loc[
            pd.to_datetime(self.from_datetime) : pd.to_datetime(self.to_datetime)
        ] = self.continuous_outflow/self.num_seconds

        self.custom_outflows.reset_index(inplace=True)

    def get_outflows(self):
        """
        Get the outflow timeseries.

        Returns the outflow timeseries as a pandas DataFrame.

        Examples
        --------
        >>> from glmpy import outflows
        >>> outflows = outflows.CustomOutflows(
        ...     start_datetime="2020-01-01",
        ...     end_datetime="2020-01-10",
        ...     frequency="daily",
        ...     base_outflow=0.0
        ... )
        >>> outflows.get_outflows()
        """
        return self.custom_outflows

    def write_outflows(self, file_path: str,):
        """
        Write the outflow timeseries to a csv file.

        The outflow timeseries can be written to a csv file by providing a
        path to the csv file.

        Parameters
        ----------
        file_path : str
            Path to the csv file to which the outflow timeseries will be
            written.

        Examples
        --------
        >>> from glmpy import outflows
        >>> outflows = outflows.CustomOutflows(
        ...     start_datetime="2020-01-01",
        ...     end_datetime="2020-01-10",
        ...     frequency="daily",
        ...     base_outflow=10
        ... )
        >>> outflows.write_outflows(file_path="outflows.csv")
        """
        self.file_path = file_path
        self.custom_outflows.to_csv(self.file_path, index=False)

    @staticmethod
    def is_valid_datetime(dt_string: str, dt_formats: list[str] =["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]):
        for fmt in dt_formats:
            try:
                datetime.strptime(dt_string, fmt)
                return True
            except ValueError:
                continue
        return False

    @staticmethod
    def is_valid_datetime_order(start_dt_string: str, end_dt_string: str, dt_formats: list[str] =["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]):
        for fmt in dt_formats:
            try:
                if datetime.strptime(start_dt_string, fmt) < datetime.strptime(end_dt_string, fmt):
                    return True
            except ValueError:
                continue
        return False

    @staticmethod
    def is_within_date_range(dt_string: str, start_dt_string: str, end_dt_string: str, dt_formats: list[str] =["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]):
        for fmt in dt_formats:
            try:
                if datetime.strptime(start_dt_string, fmt) <= datetime.strptime(dt_string, fmt) <= datetime.strptime(end_dt_string, fmt):
                    return True
            except ValueError:
                continue
        return False

    @staticmethod
    def to_datetime_format(dt_string: str, to_format: str = "%Y-%m-%d %H:%M:%S"):
        for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
            try:
                return datetime.strptime(dt_string, fmt).strftime(to_format)
            except ValueError:
                continue
        return dt_string

    @staticmethod
    def to_datetime_format(dt_string: str, from_format: str = "%Y-%m-%d", to_format: str = "%Y-%m-%d %H:%M:%S") -> str:
        try:
            dt = datetime.strptime(dt_string, from_format)
            return dt.strftime(to_format)
        except ValueError:
            return dt_string



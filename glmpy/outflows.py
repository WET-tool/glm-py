from datetime import datetime
import pandas as pd


class Outflows:
    """
    Class for creating GLM outflow timeseries.

    The outflow timeseries is created by providing a start date, end date and
    base flow. The outflow timeseries can then be updated with a dictionary to
    specify outflows on specific dates. Alternatively, the outflow timeseries
    can be updated with a fixed outflow value between two dates. Outflows can
    then be written to a CSV file.

    Attributes
    ----------
    start_date : str
        Start date of the outflow timeseries. Must be in 'YYYY-MM-DD'
        format.
    end_date : str
        End date of the outflow timeseries. Must be in 'YYYY-MM-DD'
        format.
    base_flow : float
        Base flow of the outflow timeseries in ??? units. Defaults to 0.0.

    Examples
    --------
    >>> from glmpy import Outflows
    >>> my_outflows = Outflows(
    ...     start_date = '1997-01-01',
    ...     end_date = '1997-01-11',
    ...     base_flow = 0.0
    ... )
    >>> my_outflows.get_outflows()

    """

    def __init__(self, start_date: str, end_date: str, base_flow: float = 0.0):
        self.start_date = start_date
        self.end_date = end_date
        self.base_flow = base_flow

        if not Outflows.vali_date(self.start_date) or not Outflows.vali_date(
            self.end_date
        ):
            raise ValueError(
                "start_date and end_date must be in valid 'YYYY-MM-DD' format."
            )

        if datetime.strptime(self.start_date, "%Y-%m-%d") > datetime.strptime(
            self.end_date, "%Y-%m-%d"
        ):
            raise ValueError("start_date must be before end_date.")

        if self.base_flow < 0:
            raise ValueError("base_flow must be positive.")

        self.outflows = pd.DataFrame(
            {
                "time": pd.date_range(
                    start=start_date, end=end_date, freq="D"
                ),
                "flow": base_flow,
            }
        )

    @staticmethod
    def vali_date(date_text: str):
        try:
            if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime(
                "%Y-%m-%d"
            ):
                return False
            return True
        except ValueError:
            return False

    def set_discrete_outflows(self, outflows_dict: dict[str, float]):
        """
        Set the outflow volume for specific dates.

        The outflow volume for specific dates can be set by providing a
        dictionary with dates as keys and outflow volumes as values. The
        dictionary keys must be in 'YYYY-MM-DD' format and the dictionary
        values must be positive.

        Parameters
        ----------
        outflows_dict : dict[str, float]
            Dictionary with dates as keys and outflow volumes as values.

        Examples
        --------
        >>> from glmpy import Outflows
        >>> my_outflows = Outflows(
        ...     start_date = '1997-01-01',
        ...     end_date = '1997-01-11',
        ...     base_flow = 0.0
        ... )
        >>> specific_outflows = {
        ...     "1997-01-02": 1.5,
        ...     "1997-01-03": 0.5,
        ...     "1997-01-05": 0.5,
        ... }
        >>> my_outflows.set_discrete_outflows(outflows_dict = specific_outflows)
        >>> my_outflows.get_outflows()
        """

        if not outflows_dict:
            raise ValueError("outflows_dict cannot be empty.")

        if not all(Outflows.vali_date(key) for key in outflows_dict.keys()):
            raise ValueError(
                "outflows_dict keys must be in valid 'YYYY-MM-DD' format."
            )

        if not all(
            self.start_date <= key <= self.end_date
            for key in outflows_dict.keys()
        ):
            raise ValueError(
                f"outflows_dict keys must be between {self.start_date} and {self.end_date}."
            )

        if not all(value >= 0 for value in outflows_dict.values()):
            raise ValueError("outflows_dict values must be positive.")

        outflows_dict = {
            pd.to_datetime(time): flow for time, flow in outflows_dict.items()
        }

        outflows_dict_df = pd.DataFrame(
            list(outflows_dict.items()), columns=["time", "flow"]
        )

        outflows_dict_df["time"] = pd.to_datetime(outflows_dict_df["time"])

        self.outflows.set_index("time", inplace=True)

        outflows_dict_df.set_index("time", inplace=True)

        self.outflows.update(outflows_dict_df)

        self.outflows.reset_index(inplace=True)

    def set_continuous_outflows(
        self,
        outflow_start_date: str,
        outflow_end_date: str,
        outflow_volume: float,
    ):
        """
        Set the outflow volume between two dates.

        All outflow volumes between two dates can be set by providing a start
        date, end date and outflow volume. The start date and end date must be
        in 'YYYY-MM-DD' format and the outflow volume must be positive.

        Parameters
        ----------
        outflow_start_date : str
            Start date of the outflow timeseries. Must be in 'YYYY-MM-DD'
            format.
        outflow_end_date : str
            End date of the outflow timeseries. Must be in 'YYYY-MM-DD'
            format.
        outflow_volume : float
            Outflow volume between the start date and end date in ??? units.

        Examples
        --------
        >>> from glmpy import Outflows
        >>> my_outflows = Outflows(
        ...     start_date = '1997-01-01',
        ...     end_date = '1997-01-11',
        ...     base_flow = 0.0
        ... )
        >>> my_outflows.set_continuous_outflows(
        ...     outflow_start_date='1997-01-07',
        ...     outflow_end_date='1997-01-11',
        ...     outflow_volume= 1.5
        ... )
        >>> my_outflows.get_outflows()
        """

        self.outflow_start_date = outflow_start_date
        self.outflow_end_date = outflow_end_date
        self.outflow_volume = outflow_volume

        if not Outflows.vali_date(
            self.outflow_start_date
        ) or not Outflows.vali_date(self.outflow_end_date):
            raise ValueError(
                "outflow_start_date and outflow_end_date must be in valid 'YYYY-MM-DD' format."
            )

        if self.outflow_volume < 0:
            raise ValueError("outflow_volume must be positive.")

        if datetime.strptime(
            self.outflow_start_date, "%Y-%m-%d"
        ) > datetime.strptime(self.outflow_end_date, "%Y-%m-%d"):
            raise ValueError(
                "outflow_start_date must be before outflow_end_date."
            )

        if not (
            self.start_date
            <= self.outflow_start_date
            <= self.outflow_end_date
            <= self.end_date
        ):
            raise ValueError(
                f"outflow_start_date and outflow_end_date must be within {self.start_date} and {self.end_date}."
            )

        self.outflows.set_index("time", inplace=True)

        self.outflows.loc[
            self.outflow_start_date : self.outflow_end_date
        ] = self.outflow_volume

        self.outflows.reset_index(inplace=True)

    def get_outflows(self):
        """
        Get the outflow timeseries.

        Returns the outflow timeseries as a pandas dataframe.

        Examples
        --------
        >>> from glmpy import Outflows
        >>> my_outflows = Outflows(
        ...     start_date = '1997-01-01',
        ...     end_date = '1997-01-11',
        ...     base_flow = 0.0
        ... )
        >>> my_outflows.get_outflows()
        """
        return self.outflows

    def write_outflows(
        self,
        path_to_outflows_csv: str,
    ):
        """
        Write the outflow timeseries to a csv file.

        The outflow timeseries can be written to a csv file by providing a
        path to the csv file.

        Parameters
        ----------
        path_to_outflows_csv : str
            Path to the csv file to which the outflow timeseries will be
            written.

        Examples
        --------
        >>> from glmpy import Outflows
        >>> my_outflows = Outflows(
        ...     start_date = '1997-01-01',
        ...     end_date = '1997-01-11',
        ...     base_flow = 0.0
        ... )
        >>> my_outflows.write_outflows(
        ...     path_to_outflows_csv = 'outflows.csv'
        ... )
        """
        if not isinstance(path_to_outflows_csv, str):
            raise ValueError("path_to_outflows_csv must be a string.")
        self.outflows.to_csv(path_to_outflows_csv)

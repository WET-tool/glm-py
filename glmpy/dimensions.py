import math


class SimpleTruncatedPyramidWaterBody:
    """Calculates the volume and surface area of a truncated pyramid water
    body.

    Assumes only the height, slope, and surface dimensions of a truncated
    pyramid water body are known. Enables calculation of the volume and
    surface area of the water body at each height increment.

    Attributes
    ----------
    height : float
        Height of dam, metres.
    surface_width : float
        Width of dam, metres.
    surface_length : float
        Length of dam, metres.
    side_slope : float
        Side slope of dam - the rise over run, metres/metre. By default, 3.

    Examples
    --------
    >>> my_dam = SimpleTruncatedPyramidWaterBody(3, 5, 5)
    >>> my_dam.get_volumes()
    [0.0, 11.148148148148149, 27.185185185185183, 49.0]
    >>> my_dam.get_surface_areas()
    [9.0, 13.444444444444443, 18.777777777777775, 25.0]
    """

    def __init__(
        self,
        height: float,
        surface_width: float,
        surface_length: float,
        side_slope: float = 3,
    ):
        try:
            self.height = float(height)
            self.surface_width = float(surface_width)
            self.surface_length = float(surface_length)
            self.side_slope = float(side_slope)
        except:
            raise ValueError(
                "Height, surface width, surface length, and side slope must be numeric"
            )
        try:
            assert (
                self.surface_length > (self.height / self.side_slope) * 2
            ), "Invalid length"
            assert (
                self.surface_width > (self.height / self.side_slope) * 2
            ), "Invalid width"
        except AssertionError as error:
            if str(error) == "Invalid length":
                print(
                    f"The surface length must be greater than {2*(self.height/self.side_slope)}m"
                )
            if str(error) == "Invalid width":
                print(
                    f"The surface width must be greater than {2*(self.height/self.side_slope)}m"
                )
        else:
            self.base_length = (
                self.surface_length - (self.height / self.side_slope) * 2
            )
            self.base_width = (
                self.surface_width - (self.height / self.side_slope) * 2
            )

    def get_volumes(self):
        """Calculates volumes.

        Returns the volume of the water body at each height increment.

        Parameters
        ----------
        None

        Returns
        -------
        volume : list
            The volume of water body (m^3) at each metre height increment.
        """

        return [
            (
                (self.base_length * self.base_width * i)
                + (
                    (i**2)
                    * ((self.base_length + self.base_width) / self.side_slope)
                )
                + ((4 * (i**3)) / (3 * (self.side_slope**2)))
            )
            for i in range(0, int(self.height) + 1)
        ]

    def get_surface_areas(self):
        """Calculates surface areas.

        Returns the surface area of the water body at each height increment.

        Parameters
        ----------
        None

        Returns
        -------
        surface_areas : list
            Surface area of water body (m^3) at each metre height increment.
        """

        return [
            (self.base_width + ((2 * i) / (self.side_slope)))
            * (self.base_length + (2 * i) / (self.side_slope))
            for i in range(0, int(self.height) + 1)
        ]

    def get_heights(self):
        """Calculates heights.

        Returns a list of heights from base to surface.

        Parameters
        ----------
        None

        Returns
        -------
        heights : list
            Heights (m) from base to surface.
        """

        return list(range(0, -abs(int(self.height) + 1), -1))[::-1]


class SimpleCircularWaterBody:
    """Calculates the volume and surface area of a circular water body.

    Assumes only the height, radius, and surface radius are known. Enables
    calculation of the volume and surface area of the water body at each
    height increment.

    Attributes
    ----------
    height : float
        height of dam, metres
    surface_radius : float
        surface radius of dam, metres
    side_slope : float
        side slope of dam, by default 3

    Examples
    --------
    >>> my_dam = SimpleCircularWaterBody(3, 5)
    >>> my_dam.get_volumes()
    [0.0, 11.148148148148149, 27.185185185185183, 49.0]
    >>> my_dam.get_surface_areas()
    [9.0, 13.444444444444443, 18.777777777777775, 25.0]
    """

    def __init__(
        self, height: float, surface_radius: float, side_slope: float = 3.0
    ):
        try:
            self.height = float(height)
            self.surface_radius = float(surface_radius)
            self.side_slope = float(side_slope)
        except:
            raise ValueError("Height, radius, and side slope must be numeric")

        self.surface_diameter = self.surface_radius * 2
        self.base_diameter = (
            self.surface_diameter - (self.height / self.side_slope) * 2
        )
        self.base_radius = self.base_diameter / 2

    def get_volumes(self):
        """Calculates volumes.

        Returns the volume of the water body at each height increment.

        Parameters
        ----------
        None

        Returns
        -------
        volume : list
            The volume of water body (m^3) at each metre height increment.
        """

        return [
            (1 / 3)
            * math.pi
            * i
            * (
                (self.base_radius**2)
                + (self.base_radius * self.surface_radius)
                + (self.surface_radius**2)
            )
            for i in range(0, int(self.height) + 1)
        ]

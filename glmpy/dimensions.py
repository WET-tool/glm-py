import math
from typing import Union


class SimpleTruncatedPyramidWaterBody:
    """Calculates the volume and surface area of a truncated square pyramid.

    Assumes only the height (i.e., depth), slope, and surface length of a 
    square truncated pyramidal water body are known. Enables calculation of the 
    volume and surface area of the water body at each height increment. Useful 
    for constructing the `A` and `H` parameters of the `&morphometry` block 
    with `nml.NMLMorphometry()`.

    Attributes
    ----------
    height : float
        Height of water body from the base to surface in metres.
    surface_length : float
        Surface length of the water body in metres.
    side_slope : float
        Side slope of water body - the rise over run (metres/metre). By 
        default, 1/3.

    Examples
    --------
    Import the `dimensions` and `nml` modules:
    >>> from glmpy import dimensions, nml

    Consider a square on-farm reservoir that is 40m long, 40m wide, 5m deep, 
    and has a side slope of 1/3:
    >>> ofr = dimensions.SimpleTruncatedPyramidWaterBody(
    ...     height=6,
    ...     surface_length=40,
    ...     side_slope=1/3
    ... )

    Get the total volume at each metre increment of the reservoir profile:
    >>> ofr.get_volumes()
    [0.0, 52.0, 224.0, 588.0, 1216.0, 2180.0, 3552.0]

    Get the surface water area at each metre increment of the reservoir
    profile:
    >>> ofr.get_surface_areas()
    [16.0, 100.0, 256.0, 484.0, 784.0, 1156.0, 1600.0]

    Get the each metre increment of the reservoirs profile formatted as per GLM
    requirements:
    >>> ofr.get_heights()
    [-6, -5, -4, -3, -2, -1, 0]

    Combine the surface area and height values into a dictionary for setting
    the `A` and `H` attributes of `NMLMorphometry()`:
    >>> dimensions_dict = {
    ...     "A": ofr.get_surface_areas(),
    ...     "H": ofr.get_heights(),
    ... }
    >>> morphometry = nml.NMLMorphometry()
    >>> morphometry.set_attributes(dimensions_dict)

    Print the &morphometry block:
    >>> print(morphometry)

    """

    def __init__(
        self,
        height: Union[float, int],
        surface_length: Union[float, int],
        side_slope: Union[float, int] = 3,
    ):

        if not isinstance(height, (float, int)):
            raise ValueError(
                f"height must be a numeric value, but got {type(height)}."
            )
        if not isinstance(surface_length, (float, int)):
            raise ValueError(
                "surface_length must be a numeric value, but got "
                f"{type(surface_length)}."
            )
        if not isinstance(side_slope, (float, int)):
            raise ValueError(
                "side_slope must be a numeric value, but got "
                f"{type(side_slope)}."
            )
        if height < 0:
            raise ValueError(
                "height must be a positive value."
            )
        if surface_length < 0:
            raise ValueError(
                "surface_length must be a positive value."
            )
        if side_slope < 0:
            raise ValueError(
                "side_slope must be a positive value."
            )

        base_length = (
            surface_length - (height / side_slope) * 2
        )

        if base_length <= 0:
            raise ValueError(
                "Invalid combination of height, surface_length, and "
                "side_slope parameters. The calculated base_length of the "
                "polyhedron is currently <=0. base_width is calculated by "
                "(surface_length-(height/side_slope)*2). Adjust your input "
                "parameters to calculate a positive base_length value."
            )

        self.height = height
        self.surface_length = surface_length
        self.side_slope = side_slope
        self.base_length = base_length

    def get_volumes(self):
        """Calculates volumes.

        Calculates the total volume of the water body at each metre increment
        of its profile. Volumes are returned as a list of floats where the
        first item is the volume at the bottom of the water body and the last 
        is the volume at the surface.

        Parameters
        ----------
        None

        Returns
        -------
        volume : list
            The volume of water body (m^3) at each metre height increment.

        Examples
        --------
        Import the `dimensions` module:
        >>> from glmpy import dimensions

        Consider a square on-farm reservoir that is 40m long, 40m wide, 5m 
        deep, and has a side slope of 1/3:
        >>> ofr = dimensions.SimpleTruncatedPyramidWaterBody(
        ...     height=6,
        ...     surface_length=40,
        ...     side_slope=1/3
        ... )

        Get the total volume at each metre increment of the reservoir profile:
        >>> ofr.get_volumes()
        [0.0, 52.0, 224.0, 588.0, 1216.0, 2180.0, 3552.0]

        Get the total volume of the reservoir at 1m from the bottom:
        >>> ofr.get_volumes()[1]
        52.0

        Get the total volume of the entire reservoir, i.e., from the top of the
        water body:
        >>> ofr.get_volumes()[-1]
        3552.0
        """

        return [
            (
                ((self.base_length**2)*i) +
                (2*(i**2)*((self.base_length)/(self.side_slope))) +
                ((4*(i**3))/(3*(self.side_slope**2)))
            )
            for i in range(0, int(self.height) + 1)
        ]

    def get_surface_areas(self):
        """Calculates surface areas.

        Returns the surface area of the water body at each metre increment of
        its profile. Surfacea are returned as a list of floats where the
        first item is the area at the bottom of the water body
        and the last is the area at the top.


        Parameters
        ----------
        None

        Returns
        -------
        surface_areas : list
            Surface area of water body (m^2) at each metre height increment.

        Examples
        --------
        Import the `dimensions` module:
        >>> from glmpy import dimensions

        Consider a square on-farm reservoir that is 40m long, 40m wide, 5m 
        deep, and has a side slope of 1/3:
        >>> ofr = dimensions.SimpleTruncatedPyramidWaterBody(
        ...     height=6,
        ...     surface_length=40,
        ...     side_slope=1/3
        ... )

        Get the surface water area at each metre increment of the reservoir
        profile:
        >>> ofr.get_surface_areas()
        [16.0, 100.0, 256.0, 484.0, 784.0, 1156.0, 1600.0]

        Get the surface area of the reservoir at 1m from the bottom:
        >>> ofr.get_surface_areas()[1]
        100.0

        Get the surface area at the surface of the reservoir:
        >>> ofr.get_surface_areas()[-1]
        1600.0
        """

        return [
            ((self.base_length + ((2*i)/(self.side_slope)))**2)
            for i in range(0, int(self.height) + 1)
        ]

    def get_heights(self,):
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

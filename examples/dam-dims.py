import math

class Dam:

    def __init__(self):
        raise NotImplementedError

    def get_volumes(self):
        raise NotImplementedError("Dam subclasses must implement a get_volumes() method")

    def get_surface_areas(self):
        raise NotImplementedError("Dam subclasses must implement a get_surface_areas() method")

class RectangularDam(Dam):

    """Class for rectangular dam

    Attributes
    ----------
    height : float
        height of dam, metres
    surface_width : float
        width of dam, metres
    surface_length : float
        length of dam, metres
    side_slope : float
        side slope of dam, by default 3

    Methods
    -------
    get_volumes()
        returns volume of dam at each height increment
    get_surface_areas()
        returns surface area of dam at each height increment
    get_heights()
        return heights

    Raises
    ------
    ValueError
        if height, surface width, surface length, or side slope are not numeric
    AssertionError
        if surface length is less than 2 times the height divided by the side slope
        if surface width is less than 2 times the height divided by the side slope

    Examples
    --------
    >>> dam = RectangularDam(3, 5, 5)
    >>> dam.get_volumes()
    [0.0, 11.148148148148149, 27.185185185185183, 49.0]
    >>> dam.get_surface_areas()
    [9.0, 13.444444444444443, 18.777777777777775, 25.0]
    """

    def __init__(self, height:float, surface_width, surface_length, side_slope=3):

        try:
            self.height = float(height)
            self.surface_width = float(surface_width)
            self.surface_length = float(surface_length)
            self.side_slope = float(side_slope)
        except:
            raise ValueError('Height, surface width, surface length, and side slope must be numeric')

        try:
            assert self.surface_length > (self.height/self.side_slope)*2, "Invalid dam length"
            assert self.surface_width > (self.height/self.side_slope)*2, "Invalid dam width"
        except AssertionError as error:
            if str(error) == "Invalid dam length":
                print(f"The surface length must be greater than {2*(self.height/self.side_slope)}m")
            if str(error) == "Invalid dam width":
                print(f"The surface width must be greater than {2*(self.height/self.side_slope)}m")
        else:
            self.base_length = self.surface_length - (self.height/self.side_slope)*2
            self.base_width = self.surface_width - (self.height/self.side_slope)*2

    def get_volumes(self):

        """Returns volume of dam at each metre height increment

        Parameters
        ----------
        None

        Returns
        -------
        volume : list
            volume of dam at each metre height increment
        """

        return(
            [
            ((self.base_length*self.base_width*i)+
             ((i**2)*((self.base_length+self.base_width)/self.side_slope))+
             ((4*(i**3))/(3*(self.side_slope**2))))
            for i in range(0, int(self.height)+1)
            ]
        )

    def get_surface_areas(self):

        """Returns surface area of dam at each metre height increment

        Parameters
        ----------
        None

        Returns
        -------
        surface_areas : list
            surface area of dam at each metre height increment
        """

        return(
            [(self.base_width + ((2*i)/(self.side_slope)))*(self.base_length + (2*i)/(self.side_slope))
             for i in range(0, int(self.height)+1)]
             )

    def get_heights(self):

        return(
            list(range(0,-abs(int(self.height)+1),-1))[::-1]
        )

class CircularDam(Dam):

    """Class for circular dam

    Attributes
    ----------
    height : float
        height of dam, metres
    surface_radius : float
        surface radius of dam, metres
    side_slope : float
        side slope of dam, by default 3

    Methods
    -------
    get_volumes()
        returns volume of dam at each height increment
    get_surface_areas()
        returns surface area of dam at each height increment

    Raises
    ------
    ValueError
        if height, radius, or side slope are not numeric
    AssertionError
        if radius is less than 2 times the height divided by the side slope

    Examples
    --------
    """

    def __init__(self, height: float, surface_radius: float, side_slope:float = 3.):

        try:
            self.height = float(height)
            self.surface_radius = float(surface_radius)
            self.side_slope = float(side_slope)
        except:
            raise ValueError('Height, radius, and side slope must be numeric')

        self.surface_diameter = self.surface_radius*2
        self.base_diameter = self.surface_diameter - (self.height/self.side_slope)*2
        self.base_radius = self.base_diameter/2

    def get_volumes(self):

        """Returns volume of dam at each metre height increment

        Parameters
        ----------
        None

        Returns
        -------
        volume : list
            volume of dam at each metre height increment
        """

        return(
            [
             (1/3)*math.pi*i*((self.base_radius**2) + (self.base_radius*self.surface_radius) + (self.surface_radius**2))
             for i in range(0, int(self.height)+1)
            ]
        )

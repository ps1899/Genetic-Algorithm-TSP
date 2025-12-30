"""
City Module
-----------
Defines the City class representing a location in the TSP problem.
"""

import numpy as np


class City:
    """
    Represents a city with coordinates (x, y) and provides methods to calculate 
    the distance to another city.
    """

    def __init__(self, x, y):
        """
        Initialize a city with the given x and y coordinates.
        
        :param x: The x-coordinate of the city.
        :param y: The y-coordinate of the city.
        """
        self.x = x
        self.y = y
    
    def distance(self, city):
        """
        Calculate the Euclidean distance between this city and another city.

        :param city: The other city.
        :return: The distance between the two cities.
        """
        xDistance = abs(self.x - city.x)
        yDistance = abs(self.y - city.y)
        distance = np.sqrt(xDistance ** 2 + yDistance ** 2)
        return distance
    
    def __repr__(self):
        """
        Return a string representation of the city in the format (x, y).

        :return: The string representation of the city.
        """
        return "(" + str(self.x) + "," + str(self.y) + ")"

"""
Fitness Module
-------------
Provides fitness evaluation for routes with parallel processing capabilities.
"""

from multiprocessing import Pool, cpu_count
from functools import partial


class Fitness:
    """
    Represents the fitness of a route, including its distance and fitness value.
    """
    
    def __init__(self, route):
        """
        Initialize the Fitness object with the given route.
        
        :param route: The route to evaluate the fitness for.
        """
        self.route = route
        self.distance = 0
        self.fitness = 0.0

    def routeDistance(self):
        """
        Calculate the total distance of the route by summing the distances 
        between consecutive cities.

        :return: The total distance of the route.
        """
        if self.distance == 0:
            pathDistance = 0
            for i in range(0, len(self.route)):
                fromCity = self.route[i]
                toCity = None
                if i + 1 < len(self.route):
                    toCity = self.route[i + 1]
                else:
                    toCity = self.route[0]
                pathDistance += fromCity.distance(toCity)
            self.distance = pathDistance
        return self.distance
    
    def routeFitness(self):
        """
        Calculate the fitness value of the route as the reciprocal of the route distance.
        We maximize fitness by minimizing distance. This is why we use the reciprocal 
        of the distance.

        :return: The fitness value of the route.
        """
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
        return self.fitness


def evaluate_route_fitness(route):
    """
    Helper function to evaluate fitness of a single route.
    Used for parallel processing.
    
    :param route: The route to evaluate.
    :return: The fitness value of the route.
    """
    return Fitness(route).routeFitness()


def parallel_fitness_evaluation(population, num_processes=None):
    """
    Evaluate fitness of all routes in population using parallel processing 
    across CPU cores.
    
    :param population: List of routes to evaluate.
    :param num_processes: Number of processes to use. If None, uses all available CPU cores.
    :return: Dictionary mapping route index to fitness value.
    """
    if num_processes is None:
        num_processes = cpu_count()
    
    fitness_results = {}
    
    # Use multiprocessing Pool for parallel fitness evaluation
    with Pool(processes=num_processes) as pool:
        fitness_values = pool.map(evaluate_route_fitness, population)
    
    # Map results back to indices
    for i, fitness_value in enumerate(fitness_values):
        fitness_results[i] = fitness_value
    
    return fitness_results

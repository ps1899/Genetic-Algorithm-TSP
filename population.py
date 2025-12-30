"""
Population Module
----------------
Handles population initialization and management for the genetic algorithm.
"""

import random
import numpy as np
import pandas as pd
import operator
from fitness import Fitness, parallel_fitness_evaluation


def createRoute(cityList):
    """
    Creates a random route by shuffling the given city list.
    
    :param cityList: The list of cities to create the route from.
    :return: A randomly generated route.
    """
    route = random.sample(cityList, len(cityList))
    return route


def initialPopulation(popSize, cityList):
    """
    Initializes the population with a specified size by generating random routes.
    
    :param popSize: The desired size of the population.
    :param cityList: The list of cities to create the routes from.
    :return: The initial population consisting of randomly generated routes.
    """
    population = []
    
    for i in range(0, popSize):
        population.append(createRoute(cityList))
    return population


def rankRoutes(population, use_parallel=True):
    """
    Ranks the routes in the population based on their fitness values.
    Uses parallel fitness evaluation for improved performance.
    
    :param population: The population of routes to be ranked.
    :param use_parallel: Whether to use parallel fitness evaluation (default: True).
    :return: A sorted list of tuples containing the route indices and their 
             corresponding fitness values, sorted in descending order of fitness.
    """
    if use_parallel:
        # Use parallel fitness evaluation across CPU cores
        fitnessResults = parallel_fitness_evaluation(population)
    else:
        # Sequential fitness evaluation
        fitnessResults = {}
        for i in range(0, len(population)):
            fitnessResults[i] = Fitness(population[i]).routeFitness()
    
    return sorted(fitnessResults.items(), key=operator.itemgetter(1), reverse=True)


def selection(popRanked, eliteSize):
    """
    Performs selection of individuals from the ranked population for the next generation.
    Uses fitness-proportionate selection (roulette wheel selection).
    
    :param popRanked: The ranked population, a list of tuples containing the 
                      individual indices and their fitness values.
    :param eliteSize: The number of top-ranked individuals to include in the selection.
    :return: A list of selected individual indices for the next generation.
    """
    selectionResults = []
    df = pd.DataFrame(np.array(popRanked), columns=["Index", "Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_prec'] = 100 * df.cum_sum / df.Fitness.sum()
    
    # Elite selection - preserve best individuals
    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
    
    # Fitness-proportionate selection for remaining slots
    for i in range(0, len(popRanked) - eliteSize):
        pick = 100 * random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i, 3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults


def matingPool(population, selectionResults):
    """
    Creates a mating pool by selecting individuals from the population based on 
    the selection results.
    
    :param population: The population of individuals.
    :param selectionResults: The selected individual indices from the selection process.
    :return: The mating pool containing the selected individuals.
    """
    matingpool = []
    
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool

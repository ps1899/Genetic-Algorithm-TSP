"""
Genetic Operators Module
-----------------------
Implements crossover and mutation operations for the genetic algorithm.
"""

import random


def breed(parent1, parent2):
    """
    Performs ordered crossover between two parents to create a child individual.
    This ensures that each city appears exactly once in the child route.
    
    :param parent1: The first parent individual.
    :param parent2: The second parent individual.
    :return: The child individual created through crossover.
    """
    child = []
    childP1 = []
    childP2 = []
    
    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))
    
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)
    
    # Copy a segment from parent1
    for i in range(startGene, endGene):
        childP1.append(parent1[i])
    
    # Fill remaining positions with cities from parent2 (maintaining order)
    childP2 = [item for item in parent2 if item not in childP1]
    child = childP1 + childP2
    return child


def breedPopulation(matingpool, eliteSize):
    """
    Performs breeding (crossover) among individuals in the mating pool to create 
    a new generation.
    
    :param matingpool: The pool of individuals selected for breeding.
    :param eliteSize: The number of top individuals to preserve as elites.
    :return: The new generation of individuals created through breeding.
    """
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))
    
    # Preserve elite individuals
    for i in range(0, eliteSize):
        children.append(matingpool[i])
    
    # Create offspring through crossover
    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool) - i - 1])
        children.append(child)
    return children


def mutate(individual, mutationRate):
    """
    Applies swap mutation to an individual by swapping cities with a certain probability.
    This introduces genetic diversity and helps avoid local optima.
    
    :param individual: The individual (route) to be mutated.
    :param mutationRate: The probability of mutation for each city in the individual.
    :return: The mutated individual.
    """
    for swapped in range(len(individual)):
        if random.random() < mutationRate:
            swapWith = int(random.random() * len(individual))
            
            city1 = individual[swapped]
            city2 = individual[swapWith]
            
            individual[swapped] = city2
            individual[swapWith] = city1
    return individual


def mutatePopulation(population, mutationRate):
    """
    Applies mutation to a population by mutating each individual in the population.
    
    :param population: The population of individuals (routes) to be mutated.
    :param mutationRate: The probability of mutation for each city in an individual.
    :return: The mutated population.
    """
    mutatedPopulation = []
    
    for i in range(0, len(population)):
        mutatedIndividual = mutate(population[i], mutationRate)
        mutatedPopulation.append(mutatedIndividual)
    return mutatedPopulation

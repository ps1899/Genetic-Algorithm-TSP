"""
Genetic Algorithm Core Module
-----------------------------
Implements the main genetic algorithm for solving the TSP with parallel fitness evaluation.
Includes adaptive mutation rate, early stopping, and enhanced logging.
"""

import time
from population import initialPopulation, rankRoutes, selection, matingPool
from genetic_operators import breedPopulation, mutatePopulation
from fitness import Fitness
from utils import calculate_adaptive_mutation_rate, calculate_population_statistics, check_early_stopping


def nextGeneration(currentGeneration, eliteSize, mutationRate, use_parallel=True):
    """
    Generates the next generation of the population by performing selection, 
    mating, breeding, and mutation with parallel fitness evaluation.
    
    :param currentGeneration: The current generation of the population.
    :param eliteSize: The number of top individuals to be preserved as elite.
    :param mutationRate: The probability of mutation for each city in an individual.
    :param use_parallel: Whether to use parallel fitness evaluation (default: True).
    :return: The next generation of the population.
    """
    # Rank routes using parallel fitness evaluation
    populationRanked = rankRoutes(currentGeneration, use_parallel=use_parallel)
    
    # Select individuals for mating
    selectionResults = selection(populationRanked, eliteSize)
    
    # Create mating pool
    matingpool = matingPool(currentGeneration, selectionResults)
    
    # Breed new generation
    children = breedPopulation(matingpool, eliteSize)
    
    # Apply mutation
    nextGen = mutatePopulation(children, mutationRate)
    
    return nextGen


def geneticAlgorithm(cityList, populationSize, eliteSize, mutationRate, generations, 
                     use_parallel=True, verbose=True, detailed_stats=False, 
                     log_interval=50, adaptive_mutation=False, mutation_rate_initial=None,
                     mutation_rate_final=None, mutation_decay="linear",
                     early_stopping=False, patience=50, min_improvement=0.01):
    """
    Implements a genetic algorithm to solve the Traveling Salesman Problem (TSP)
    using a heuristic, concurrent population-based approach with parallel fitness 
    evaluation across CPU cores.
    
    :param cityList: The list of cities representing the problem.
    :param populationSize: The size of the population.
    :param eliteSize: The number of top individuals to be preserved as elite in each generation.
    :param mutationRate: The probability of mutation (used if adaptive_mutation=False).
    :param generations: The number of generations to run the algorithm.
    :param use_parallel: Whether to use parallel fitness evaluation (default: True).
    :param verbose: Whether to print progress information (default: True).
    :param detailed_stats: Whether to print detailed statistics (default: False).
    :param log_interval: Print stats every N generations (default: 50).
    :param adaptive_mutation: Whether to use adaptive mutation rate (default: False).
    :param mutation_rate_initial: Initial mutation rate for adaptive mutation.
    :param mutation_rate_final: Final mutation rate for adaptive mutation.
    :param mutation_decay: Type of decay for adaptive mutation ('linear' or 'exponential').
    :param early_stopping: Whether to enable early stopping (default: False).
    :param patience: Number of generations to wait for improvement (default: 50).
    :param min_improvement: Minimum improvement threshold in % (default: 0.01).
    :return: Tuple of (best route, progress list, statistics dict).
    """
    start_time = time.time()
    
    # Initialize population
    pop = initialPopulation(populationSize, cityList)
    
    # Track progress and statistics
    progress = []
    all_stats = []
    initial_distance = 1 / rankRoutes(pop, use_parallel=use_parallel)[0][1]
    progress.append(initial_distance)
    
    if verbose:
        print(f"Initial Distance: {initial_distance:.2f}")
        if use_parallel:
            print("Using parallel fitness evaluation across CPU cores")
        if adaptive_mutation:
            print(f"Adaptive mutation: {mutation_rate_initial:.4f} → {mutation_rate_final:.4f}")
        if early_stopping:
            print(f"Early stopping enabled (patience={patience}, min_improvement={min_improvement}%)")
        print()
    
    # Evolve population over generations
    stopped_early = False
    for i in range(0, generations):
        # Calculate adaptive mutation rate if enabled
        current_mutation_rate = mutationRate
        if adaptive_mutation and mutation_rate_initial and mutation_rate_final:
            current_mutation_rate = calculate_adaptive_mutation_rate(
                i, generations, mutation_rate_initial, mutation_rate_final, mutation_decay
            )
        
        # Generate next generation
        pop = nextGeneration(pop, eliteSize, current_mutation_rate, use_parallel=use_parallel)
        
        # Track best distance in this generation
        current_best = 1 / rankRoutes(pop, use_parallel=use_parallel)[0][1]
        progress.append(current_best)
        
        # Calculate detailed statistics if requested
        if detailed_stats:
            stats = calculate_population_statistics(pop, Fitness)
            stats['generation'] = i + 1
            stats['mutation_rate'] = current_mutation_rate
            all_stats.append(stats)
        
        # Print progress
        if verbose and (i + 1) % log_interval == 0:
            if detailed_stats:
                stats = all_stats[-1]
                print(f"Generation {i + 1}:")
                print(f"  Best: {stats['best_distance']:.2f} | "
                      f"Avg: {stats['average_distance']:.2f} | "
                      f"Worst: {stats['worst_distance']:.2f} | "
                      f"Std: {stats['std_dev']:.2f}")
                if adaptive_mutation:
                    print(f"  Mutation Rate: {current_mutation_rate:.4f}")
            else:
                print(f"Generation {i + 1}: Best Distance = {current_best:.2f}")
        
        # Check early stopping
        if early_stopping and i >= patience:
            should_stop, gens_without_improvement = check_early_stopping(
                progress, patience, min_improvement
            )
            if should_stop:
                stopped_early = True
                if verbose:
                    print(f"\nEarly stopping triggered at generation {i + 1}")
                    print(f"No significant improvement for {gens_without_improvement} generations")
                break
    
    # Get final best route
    final_distance = 1 / rankRoutes(pop, use_parallel=use_parallel)[0][1]
    bestRouteIndex = rankRoutes(pop, use_parallel=use_parallel)[0][0]
    bestRoute = pop[bestRouteIndex]
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    if verbose:
        print(f"\n{'='*70}")
        print(f"Final Distance: {final_distance:.2f}")
        improvement = ((initial_distance - final_distance) / initial_distance) * 100
        print(f"Improvement: {improvement:.2f}%")
        print(f"Time Elapsed: {elapsed_time:.2f} seconds")
        if stopped_early:
            print(f"Stopped at generation {i + 1} (early stopping)")
        print(f"{'='*70}")
    
    # Compile results
    results = {
        'initial_distance': initial_distance,
        'final_distance': final_distance,
        'improvement_percent': ((initial_distance - final_distance) / initial_distance) * 100,
        'generations_run': i + 1 if stopped_early else generations,
        'stopped_early': stopped_early,
        'elapsed_time': elapsed_time,
        'progress': progress,
        'detailed_stats': all_stats if detailed_stats else None
    }
    
    return bestRoute, progress, results


def geneticAlgorithmWithTracking(cityList, populationSize, eliteSize, mutationRate, 
                                 generations, use_parallel=True):
    """
    Runs the genetic algorithm and returns both the best route and progress tracking data.
    Useful for visualization and analysis.
    
    :param cityList: The list of cities representing the problem.
    :param populationSize: The size of the population.
    :param eliteSize: The number of top individuals to be preserved as elite.
    :param mutationRate: The probability of mutation for each city in an individual.
    :param generations: The number of generations to run the algorithm.
    :param use_parallel: Whether to use parallel fitness evaluation (default: True).
    :return: Tuple of (best route, progress list).
    """
    return geneticAlgorithm(cityList, populationSize, eliteSize, mutationRate, 
                           generations, use_parallel=use_parallel, verbose=True)

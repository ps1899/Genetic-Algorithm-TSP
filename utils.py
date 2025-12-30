"""
Utility Module
-------------
Helper functions for configuration loading and statistics calculation.
"""

import yaml
import json
import os
from pathlib import Path


def load_config(config_path="config.yaml"):
    """
    Load configuration from YAML file.
    
    :param config_path: Path to the configuration file.
    :return: Dictionary containing configuration parameters.
    """
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def calculate_adaptive_mutation_rate(generation, total_generations, initial_rate, final_rate, decay_type="linear"):
    """
    Calculate adaptive mutation rate based on current generation.
    
    :param generation: Current generation number.
    :param total_generations: Total number of generations.
    :param initial_rate: Starting mutation rate.
    :param final_rate: Ending mutation rate.
    :param decay_type: Type of decay ('linear' or 'exponential').
    :return: Mutation rate for current generation.
    """
    progress = generation / total_generations
    
    if decay_type == "linear":
        # Linear decay from initial to final rate
        mutation_rate = initial_rate - (initial_rate - final_rate) * progress
    elif decay_type == "exponential":
        # Exponential decay
        import math
        decay_factor = math.log(final_rate / initial_rate)
        mutation_rate = initial_rate * math.exp(decay_factor * progress)
    else:
        mutation_rate = initial_rate
    
    return mutation_rate


def calculate_population_statistics(population, fitness_func):
    """
    Calculate statistics for the current population.
    
    :param population: List of routes in the population.
    :param fitness_func: Function to calculate fitness for a route.
    :return: Dictionary with statistics (best, worst, average, std_dev).
    """
    import numpy as np
    
    # Calculate fitness for all routes
    fitness_values = [fitness_func(route).routeFitness() for route in population]
    
    # Convert fitness to distances (inverse of fitness)
    distances = [1 / f for f in fitness_values]
    
    stats = {
        'best_distance': min(distances),
        'worst_distance': max(distances),
        'average_distance': np.mean(distances),
        'std_dev': np.std(distances),
        'best_fitness': max(fitness_values),
        'worst_fitness': min(fitness_values),
        'average_fitness': np.mean(fitness_values)
    }
    
    return stats


def save_results(results, filepath):
    """
    Save results to JSON file.
    
    :param results: Dictionary containing results.
    :param filepath: Path to save the results.
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to {filepath}")


def save_route(route, filepath):
    """
    Save best route to JSON file.
    
    :param route: List of City objects representing the route.
    :param filepath: Path to save the route.
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Convert route to serializable format
    route_data = {
        'cities': [{'x': city.x, 'y': city.y} for city in route],
        'num_cities': len(route)
    }
    
    with open(filepath, 'w') as f:
        json.dump(route_data, f, indent=2)
    
    print(f"Route saved to {filepath}")


def check_early_stopping(progress, patience, min_improvement):
    """
    Check if early stopping criteria is met.
    
    :param progress: List of best distances per generation.
    :param patience: Number of generations to wait for improvement.
    :param min_improvement: Minimum improvement threshold (percentage).
    :return: Tuple (should_stop, generations_without_improvement).
    """
    if len(progress) < patience + 1:
        return False, 0
    
    # Get recent history
    recent_best = progress[-patience-1]
    current_best = progress[-1]
    
    # Calculate improvement percentage
    improvement = ((recent_best - current_best) / recent_best) * 100
    
    # Count generations without significant improvement
    generations_without_improvement = 0
    for i in range(len(progress) - patience, len(progress)):
        if i > 0:
            gen_improvement = ((progress[i-1] - progress[i]) / progress[i-1]) * 100
            if gen_improvement < min_improvement:
                generations_without_improvement += 1
    
    should_stop = generations_without_improvement >= patience
    
    return should_stop, generations_without_improvement

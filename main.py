"""
Main Execution Script
---------------------------------------
Demonstrates the Genetic Algorithm with:
- Configuration file support
- Command-line interface
- Adaptive mutation rate
- Early stopping
- Enhanced logging with statistics
"""

import argparse
import random
import os
from city import City
from genetic_algorithm import geneticAlgorithm
from visualization import plot_progress, plot_route, plot_combined
from utils import load_config, save_results, save_route


def create_random_cities(num_cities=40, max_coord=100, seed=None):
    """
    Creates a list of cities with random coordinates.
    
    :param num_cities: Number of cities to generate.
    :param max_coord: Maximum coordinate value.
    :param seed: Random seed for reproducibility (None for random).
    :return: List of City objects.
    """
    if seed is not None:
        random.seed(seed)
    
    cityList = []
    for i in range(num_cities):
        cityList.append(City(x=int(random.random() * max_coord), 
                            y=int(random.random() * max_coord)))
    return cityList


def main():
    """
    Main function with CLI support and configuration file loading.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Genetic Algorithm for TSP with parallel fitness evaluation'
    )
    parser.add_argument('--config', type=str, default='config.yaml',
                       help='Path to configuration file (default: config.yaml)')
    parser.add_argument('--cities', type=int, help='Number of cities (overrides config)')
    parser.add_argument('--generations', type=int, help='Number of generations (overrides config)')
    parser.add_argument('--population', type=int, help='Population size (overrides config)')
    parser.add_argument('--no-parallel', action='store_true', 
                       help='Disable parallel processing')
    parser.add_argument('--no-adaptive', action='store_true',
                       help='Disable adaptive mutation rate')
    parser.add_argument('--no-early-stop', action='store_true',
                       help='Disable early stopping')
    parser.add_argument('--seed', type=int, help='Random seed (overrides config)')
    
    args = parser.parse_args()
    
    # Load configuration
    try:
        config = load_config(args.config)
        print(f"Loaded configuration from {args.config}")
    except FileNotFoundError:
        print(f"Configuration file {args.config} not found. Using defaults.")
        config = {
            'problem': {'num_cities': 40, 'max_coordinate': 100, 'random_seed': 42},
            'algorithm': {
                'population_size': 250, 'elite_size': 20, 'generations': 500,
                'mutation_rate_initial': 0.02, 'mutation_rate_final': 0.005,
                'mutation_decay': 'linear', 'early_stopping_enabled': True,
                'patience': 50, 'min_improvement': 0.01
            },
            'performance': {'use_parallel': True, 'num_processes': None},
            'logging': {'verbose': True, 'log_interval': 50, 'detailed_stats': True},
            'visualization': {'save_plots': True, 'output_dir': 'results', 'show_plots': False},
            'output': {'save_results': True, 'results_file': 'results/ga_results.json',
                      'save_best_route': True, 'route_file': 'results/best_route.json'}
        }
    
    # Override config with command-line arguments
    if args.cities:
        config['problem']['num_cities'] = args.cities
    if args.generations:
        config['algorithm']['generations'] = args.generations
    if args.population:
        config['algorithm']['population_size'] = args.population
    if args.no_parallel:
        config['performance']['use_parallel'] = False
    if args.seed is not None:
        config['problem']['random_seed'] = args.seed
    
    # Extract configuration
    num_cities = config['problem']['num_cities']
    max_coord = config['problem']['max_coordinate']
    seed = config['problem']['random_seed']
    
    population_size = config['algorithm']['population_size']
    elite_size = config['algorithm']['elite_size']
    generations = config['algorithm']['generations']
    mutation_rate_initial = config['algorithm']['mutation_rate_initial']
    mutation_rate_final = config['algorithm']['mutation_rate_final']
    mutation_decay = config['algorithm']['mutation_decay']
    
    use_parallel = config['performance']['use_parallel']
    verbose = config['logging']['verbose']
    log_interval = config['logging']['log_interval']
    detailed_stats = config['logging']['detailed_stats']
    
    early_stopping = config['algorithm']['early_stopping_enabled'] and not args.no_early_stop
    patience = config['algorithm']['patience']
    min_improvement = config['algorithm']['min_improvement']
    
    adaptive_mutation = not args.no_adaptive
    
    # Print header
    print("=" * 70)
    print("Enhanced Genetic Algorithm for TSP")
    print("=" * 70)
    print("\nFeatures:")
    print("- Heuristic, population-based approach")
    print("- Parallel fitness evaluation across CPU cores" if use_parallel else "- Sequential fitness evaluation")
    print("- Adaptive mutation rate" if adaptive_mutation else "- Fixed mutation rate")
    print("- Early stopping" if early_stopping else "- Fixed generations")
    print("- Enhanced logging with statistics" if detailed_stats else "- Basic logging")
    print("\n" + "=" * 70 + "\n")
    
    # Create problem instance
    print(f"Creating TSP problem with {num_cities} random cities...")
    cityList = create_random_cities(num_cities=num_cities, max_coord=max_coord, seed=seed)
    print(f"Cities created: {len(cityList)}")
    print(f"Sample cities: {cityList[:3]}")
    
    # Display parameters
    print(f"\nAlgorithm Parameters:")
    print(f"  Population Size: {population_size}")
    print(f"  Elite Size: {elite_size}")
    print(f"  Generations: {generations}")
    if adaptive_mutation:
        print(f"  Mutation Rate: {mutation_rate_initial:.4f} → {mutation_rate_final:.4f} ({mutation_decay})")
    else:
        print(f"  Mutation Rate: {mutation_rate_initial:.4f} (fixed)")
    if early_stopping:
        print(f"  Early Stopping: patience={patience}, min_improvement={min_improvement}%")
    print("\n" + "=" * 70 + "\n")
    
    # Run genetic algorithm
    print("Running Enhanced Genetic Algorithm...\n")
    bestRoute, progress, results = geneticAlgorithm(
        cityList=cityList,
        populationSize=population_size,
        eliteSize=elite_size,
        mutationRate=mutation_rate_initial,  # Used only if adaptive_mutation=False
        generations=generations,
        use_parallel=use_parallel,
        verbose=verbose,
        detailed_stats=detailed_stats,
        log_interval=log_interval,
        adaptive_mutation=adaptive_mutation,
        mutation_rate_initial=mutation_rate_initial,
        mutation_rate_final=mutation_rate_final,
        mutation_decay=mutation_decay,
        early_stopping=early_stopping,
        patience=patience,
        min_improvement=min_improvement
    )
    
    # Save results if configured
    if config['output']['save_results']:
        save_results(results, config['output']['results_file'])
    
    if config['output']['save_best_route']:
        save_route(bestRoute, config['output']['route_file'])
    
    # Generate visualizations
    if config['visualization']['save_plots']:
        output_dir = config['visualization']['output_dir']
        os.makedirs(output_dir, exist_ok=True)
        
        print("\nGenerating visualizations...")
        
        # Combined plot
        combined_path = os.path.join(output_dir, f"results_combined.{config['visualization']['plot_format']}")
        plot_combined(bestRoute, progress, save_path=combined_path)
        
        # Individual plots
        progress_path = os.path.join(output_dir, f"progress.{config['visualization']['plot_format']}")
        plot_progress(progress, save_path=progress_path)
        
        route_path = os.path.join(output_dir, f"best_route.{config['visualization']['plot_format']}")
        plot_route(bestRoute, title=f"Best Route (Distance: {results['final_distance']:.2f})", 
                  save_path=route_path)
        
        print("Visualization complete!")
    
    if config['visualization']['show_plots']:
        print("\nDisplaying plots...")
        plot_combined(bestRoute, progress)
    
    print("\n" + "=" * 70)
    print("Execution Complete!")
    print("=" * 70)
    print(f"\nTo run with different parameters:")
    print(f"  python {__file__} --cities 50 --generations 1000")
    print(f"  python {__file__} --config my_config.yaml")
    print(f"  python {__file__} --no-parallel --no-adaptive")


if __name__ == "__main__":
    main()

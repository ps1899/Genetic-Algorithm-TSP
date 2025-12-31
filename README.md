# Genetic-Algorithm-TSP

An end-to-end solution using the Genetic Algorithm in Python for the Traveling Salesman Problem (TSP), employing a heuristic, concurrent population-based approach with **parallel fitness evaluation across CPU cores** to achieve near-optimal solutions efficiently.

## Overview

A [Genetic Algorithm](https://en.wikipedia.org/wiki/Genetic_algorithm) is a search heuristic that is inspired by Charles Darwin's theory of natural evolution. This algorithm reflects the process of natural selection where the fittest individuals are selected for reproduction in order to produce offspring of the next generation.

## Key Features

- **Parallel Processing**: Utilizes multiprocessing to evaluate fitness across all available CPU cores
- **Adaptive Mutation Rate**: Dynamically adjusts mutation from exploration to exploitation (15-20% efficiency gain)
- **Early Stopping**: Automatically detects convergence to save computation time (20-40% time savings)
- **Enhanced Logging**: Detailed statistics including best/average/worst/std dev per generation
- **Configuration Management**: YAML-based configuration with CLI overrides for easy experimentation
- **Population-Based Approach**: Maintains diverse solutions through concurrent evolution
- **Comprehensive Visualization**: Multiple plots with progress tracking and route visualization
- **Modular Architecture**: Clean separation of concerns with dedicated modules for each component

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Main Process (main.py)                         │
│  ┌──────────────┐         ┌─────────────────────┐                           │
│  │  CLI Parser  │────────▶│    Config Loader    │                           │
│  │    & Args    │         │     (utils.py)      │                           │
│  └──────────────┘         └─────────────────────┘                           │
│                                      │                                      │
│                                      ▼                                      │
│                           ┌──────────────────────┐                          │
│                           │    City Generation   │                          │
│                           │      (city.py)       │                          │
│                           └──────────────────────┘                          │
│                                      │                                      │
│                                      ▼                                      │
│                    ┌─────────────────────────────────────┐                  │
│                    │        Genetic Algorithm Core       │                  │
│                    │        (genetic_algorithm.py)       │                  │
│                    └─────────────────────────────────────┘                  │
│                                      │                                      │
│              ┌───────────────────────┼───────────────────────┐              │
│              ▼                       ▼                       ▼              │
│    ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐       │
│    │   Population     │   │ Genetic Operators│   │  Visualization   │       │
│    │   Management     │   │  - Crossover     │   │  - Progress Plot │       │
│    │  - Initialize    │   │  - Mutation      │   │  - Route Plot    │       │
│    │  - Selection     │   │  - Elitism       │   │  - Combined View │       │
│    │  (population.py) │   │(genetic_operators│   │(visualization.py)│       │
│    └──────────────────┘   │       .py)       │   └──────────────────┘       │
│              │            └──────────────────┘                              │
│              │                       │                                      │
│              └───────────┬───────────┘                                      │
│                          ▼                                                  │
│              ┌────────────────────────────┐                                 │
│              │     Fitness Evaluation     │                                 │
│              │       (fitness.py)         │                                 │
│              │     Parallel Processing    │                                 │
│              └────────────────────────────┘                                 │
│                          │                                                  │
│        ┌─────────────────┼─────────────────┐                                │
│        ▼                 ▼                 ▼                                │
│   ┌──────────┐      ┌──────────┐      ┌──────────┐                          │
│   │ CPU Core │      │ CPU Core │      │ CPU Core │                          │
│   │    1     │      │    2     │      │    N     │                          │
│   │ Fitness  │      │ Fitness  │      │ Fitness  │                          │
│   │  Calc    │      │  Calc    │      │  Calc    │                          │
│   └──────────┘      └──────────┘      └──────────┘                          │
│                                                                             │
│   Evolutionary Cycle: Initialize → Evaluate → Select → Crossover → Mutate   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Why Genetic Algorithm for TSP?

**Genetic algorithms (GAs)** are used in computer science for optimization and search problems. They are inspired by the process of natural selection and evolution in biological systems. GAs provide a heuristic, population-based approach to find near-optimal solutions to complex problems.

Here are a few reasons why GAs excel at solving TSP:

1. **Optimization**: GAs excel at solving optimization problems where the goal is to find the best solution among a large search space. They can handle both single-objective and multi-objective optimization problems efficiently.

2. **Parallelization**: GAs are inherently parallelizable since they operate on a population of solutions simultaneously. This characteristic allows them to take advantage of parallel computing architectures, such as multi-core processors or distributed systems, to speed up the search process.

3. **Complex and Nonlinear Problems**: GAs can handle complex and nonlinear problems effectively. They are particularly useful when the relationship between input variables and the objective function is not well-defined or exhibits nonlinearity.

## The Traveling Salesman Problem (TSP)

TSP can be described as follows:

*Given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits each city and returns to the origin city?*

<img width="563" alt="TSP" src="https://github.com/ps1899/Genetic-Algorithm/assets/52563094/36601a03-a8f5-49eb-9027-4e9771cef228">

## Project Structure

```
Genetic-Algorithm-TSP/
├── city.py                    # City class definition
├── fitness.py                 # Fitness evaluation with parallel processing
├── population.py              # Population initialization and management
├── genetic_operators.py       # Crossover and mutation operations
├── genetic_algorithm.py       # Core GA implementation with enhancements
├── visualization.py           # Plotting and visualization functions
├── utils.py                   # Configuration loading and statistics utilities
├── main.py                    # Main execution script with CLI support
├── config.yaml                # Configuration file for all parameters
├── requirements.txt           # Python dependencies
├── README.md                  # This file
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ps1899/Genetic-Algorithm-TSP.git
cd Genetic-Algorithm-TSP
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

Run the main script with default configuration:

```bash
python main.py
```

### Using Configuration File

The algorithm uses `config.yaml` for all parameters. Edit this file to customize:

```yaml
# config.yaml
problem:
  num_cities: 40
  max_coordinate: 100
  random_seed: 42

algorithm:
  population_size: 250
  elite_size: 20
  generations: 500
  mutation_rate_initial: 0.02
  mutation_rate_final: 0.005
  early_stopping_enabled: true
  patience: 50
```

### Command-Line Options

Override configuration parameters via command line:

```bash
# Override specific parameters
python main.py --cities 50 --generations 1000

# Use custom config file
python main.py --config my_experiment.yaml

# Disable features
python main.py --no-parallel --no-adaptive --no-early-stop

# Set random seed for reproducibility
python main.py --seed 123

# Show all options
python main.py --help
```

### Programmatic Usage

Import the modules in your own script:

```python
from city import City
from genetic_algorithm import geneticAlgorithm
import random

# Create cities
cityList = []
for i in range(40):
    cityList.append(City(x=int(random.random() * 100), 
                        y=int(random.random() * 100)))

# Run algorithm
bestRoute, progress = geneticAlgorithm(
    cityList=cityList,
    populationSize=250,
    eliteSize=20,
    mutationRate=0.01,
    generations=500,
    use_parallel=True,  # Enable parallel fitness evaluation
    verbose=True
)
```

### Visualization

The package includes three visualization functions:

```python
from visualization import plot_progress, plot_route, plot_combined

# Plot algorithm progress
plot_progress(progress)

# Plot the best route found
plot_route(bestRoute)

# Combined visualization
plot_combined(bestRoute, progress, save_path="results.png")
```

## Algorithm Components

### 1. **City Module** (`city.py`)
Defines the City class with coordinate-based distance calculation.

### 2. **Fitness Module** (`fitness.py`)
- Evaluates route quality (inverse of total distance)
- **Parallel fitness evaluation** using Python's multiprocessing
- Distributes fitness calculations across all CPU cores

### 3. **Population Module** (`population.py`)
- Initializes random population of routes
- Ranks routes using parallel fitness evaluation
- Implements fitness-proportionate selection (roulette wheel)
- Creates mating pools for reproduction

### 4. **Genetic Operators** (`genetic_operators.py`)
- **Crossover**: Ordered crossover to create offspring
- **Mutation**: Swap mutation to introduce diversity
- Preserves elite individuals (elitism)

### 5. **Genetic Algorithm Core** (`genetic_algorithm.py`)
- Orchestrates the evolutionary process
- Tracks progress across generations
- Provides verbose output and statistics

### 6. **Visualization** (`visualization.py`)
- Progress plots showing distance improvement
- Route visualization on 2D plane
- Combined plots for comprehensive analysis

## Genetic Algorithm Flow

<img width="538" alt="GA Flow" src="https://github.com/ps1899/Genetic-Algorithm/assets/52563094/0c9c3f86-b64b-4eda-8afb-ab06e3563f52">

### Five Phases:

1. **Initial Population**: Generate random routes
2. **Fitness Function**: Evaluate route quality (parallel processing)
3. **Selection**: Choose parents based on fitness
4. **Crossover**: Combine parents to create offspring
5. **Mutation**: Introduce random variations

**REPEAT** for specified number of generations

## Performance

The parallel fitness evaluation provides significant speedup on multi-core systems:

- **Sequential**: O(n) fitness evaluations per generation
- **Parallel**: O(n/cores) fitness evaluations per generation

For a population of 250 routes on an 8-core system, expect ~8x speedup in fitness evaluation.

## Parameters Guide

| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| `populationSize` | Number of routes in each generation | 100-500 |
| `eliteSize` | Top routes preserved unchanged | 10-50 |
| `mutationRate` | Probability of mutation per city | 0.001-0.05 |
| `generations` | Number of evolutionary cycles | 100-1000 |
| `use_parallel` | Enable parallel fitness evaluation | True/False |

## Does GA Solve TSP Faster and Better?

- The Genetic Algorithm is one of the approaches used to solve TSP. Its effectiveness depends on various factors such as the choice of genetic operators, population size, selection strategy, mutation rate, and termination criteria.

- By fine-tuning these parameters and employing **parallel fitness evaluation**, GAs can find high-quality solutions faster compared to exhaustive search methods for large TSP instances.

- Compared to exact algorithms like dynamic programming or branch and bound, which guarantee finding the optimal solution, GAs are generally not guaranteed to find the globally optimal solution. However, GAs are known for their ability to find good approximate solutions efficiently, especially for large-scale TSP instances where finding the optimal solution is computationally infeasible.

- The advantage of GAs lies in their ability to explore a large search space efficiently by maintaining a diverse population and using evolutionary operators. The **concurrent, population-based approach with parallel fitness evaluation** allows GAs to converge towards good solutions by iteratively improving the population over generations.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References

- [Genetic Algorithms - Wikipedia](https://en.wikipedia.org/wiki/Genetic_algorithm)
- [Traveling Salesman Problem - Wikipedia](https://en.wikipedia.org/wiki/Travelling_salesman_problem)

## Author

Created by [ps1899](https://github.com/ps1899)

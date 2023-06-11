# Genetic-Algorithm-TSP
A [Genetic Algorithm](https://en.wikipedia.org/wiki/Genetic_algorithm) is a search heuristic that is inspired by Charles Darwin’s theory of natural 
evolution. This algorithm reflects the process of natural selection where the fittest individuals are selected for reproduction in order to produce 
offspring of the next generation.

</br>

**Why Genetic Algorithm is used in Computer Science?**

Genetic algorithms (GAs) are used in computer science for optimization and search problems. They are inspired by the process of natural selection 
and evolution in biological systems. GAs provide a heuristic, population-based approach to find near-optimal solutions to complex problems.  
Here are a few reasons why GAs can be used in computer science:  
1. *Optimization*: GAs excel at solving optimization problems where the goal is to find the best solution among a large search space. They can handle both single-objective and multi-objective optimization problems efficiently.
2. *Parallelization*: GAs are inherently parallelizable since they operate on a population of solutions simultaneously. This characteristic allows them to take advantage of parallel computing architectures, such as multi-core processors or distributed systems, to speed up the search process.
3. *Complex and Nonlinear Problems*: GAs can handle complex and nonlinear problems effectively. They are particularly useful when the relationship between input variables and the objective function is not well-defined or exhibits nonlinearity.

</br>

Genetic Algorithm can be explained by the following steps:  

<img width="538" alt="Screenshot 2023-06-11 at 1 43 46 AM" src="https://github.com/ps1899/Genetic-Algorithm/assets/52563094/0c9c3f86-b64b-4eda-8afb-ab06e3563f52">

</br>
</br>

Here in this repository, I have demonstrated an end-to-end code of each and every step of Genetic Algorithm which is used to solve the Traveling 
Salesman Problem (TSP). In the '*geneticAlgorithm.ipynb*', I have critically explained all the steps coded in Python in a similar manner as flow 
diagram above.

TSP can be described as follows:  
*Given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits each city and returns to the 
origin city?*  

<img width="563" alt="TSP" src="https://github.com/ps1899/Genetic-Algorithm/assets/52563094/36601a03-a8f5-49eb-9027-4e9771cef228">

</br>
</br>

**Does Genetic algorithm helps solving Travelling Salesman Problem (TSP) faster and better?** 

The Genetic Algorithm (GA) is one of the approaches used to solve the traveling salesman problem (TSP), but its effectiveness in terms of speed 
depends on various factors such as the choice of genetic operators, population size, selection strategy, mutation rate, and termination criteria. By 
fine-tuning these parameters and employing effective heuristics, GAs can find high-quality solutions faster compared to exhaustive search methods 
for large TSP instances.

Compared to exact algorithms like dynamic programming or branch and bound, which guarantee finding the optimal solution, GAs are generally not guaranteed to find the globally optimal solution. However, GAs are known for their ability to find good approximate solutions efficiently, especially for large-scale TSP instances where finding the optimal solution is computationally infeasible.

The advantage of GAs lies in their ability to explore a large search space efficiently by maintaining a diverse population and using evolutionary operators such as selection, crossover, and mutation. GAs can converge towards good solutions by iteratively improving the population over generations.

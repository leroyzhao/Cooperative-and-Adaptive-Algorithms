
This repository contains various algorithms coded while taking ECE 457A (Cooperative and Adaptive Algorithms) at the University of Waterloo.
Note that some of these algorithms were created for specific problems and may not be particularly adaptable for different applications.

## Course Description
The following course description is provided by the university:

> The course starts by addressing the ill-structured problems and need for computational intelligence methods. It introduces the concepts of heuristics and their use in conjunction with search methods, solving problems using heuristics and metaheuristics, constraints satisfaction. The course also introduces the concepts of cooperation and adaptations and how they are influencing new methods for solving complex problems. The course starts by illustrating how the concepts of cooperation and adaptation are manifested in nature and how such models are inspiring new types of solutions methods. Topics to be covered include: search algorithms, game playing, constraints satisfaction, meta-heuristics, evolutionary computing methods, swarm intelligence, ant-colony algorithms, particle swarm methods, adaptive and learning algorithms and the use of these algorithms in solving continuous and discrete problems that arise in engineering applications.

## Algorithms Included

#### Basic Graph Search Methods
- Blind Search
    - **Breadth-First Search**
    - **Depth-First Search**
- Informed Search
    - A*

#### Heuristic Methods
- Trajectory Methods
    - **Simulated Annealing**
- Population-based Methods
    - Swarm Intelligence
        - **Particle Swarm Optimization**
        - **Ant Colony Optimization**
    - Evolutionary Computing
        - **Genetic Algorithms**
        - **Evolutionary Programming** (using [DEAP](https://github.com/deap/deap) framework)

## Implementation Details

- [A*](A_star.py) and [BFS and DFS](BFS_DFS.py) implementations are for a navigating a 2D maze.
- [Simulated Annealing](SA_TRP.py) was used to solve the Vehicle Routing Problem (VRP), which is a generalized version of the common Travelling Salesman Problem (TSP). Data for the VRP was taken from instance A-n39-k6.vrp found at [NEO](http://neo.lcc.uma.es/vrp/vrp-instances/capacitated-vrp-instances/).
- An object-oriented implementation of [Particle Swarm Optimization](PSO.py) was used to find the global minima of the 6-hump camelback function. Variations of the algorithm include Simple PSO, Inertia Weight, Constriction Coefficient, and Guaranteed Convergence (GCPSO).
- Two versions of Ant Colony Optimization (Ant Colony System (ACS) with [offline](ACS_offline_TSP.py) and [online-delayed](ACS_online_delayed_TSP.py) pheromone update methods) were used to solve the Travelling Salesman Problem. The target problem is the Bays29, whose data is stored in [cities.csv](cities.csv).
- The [Genetic Algorithm](GA.py) was used to optimize the Integral Squared Error (ISE) of the step response calculated for a sample PID Controller.
- The DEAP framework was used to apply [Genetic Programming](GP_using_deap.py) to create a program that simulates a multiplexer. 
import csv
import numpy as np
import random

data = []
with open('cities.csv') as f:
    reader = csv.reader(f)
    data = [row for row in reader]

# pick next city for ant based on pheromones
def get_next_city(current_city, ant_path):
    q = random.random()
    cities_left = list(set([i for i in range(29)]) - set(ant_path))
    remaining_city_pheromones = [pheromone_trail[current_city][i] for i in cities_left]
    if q<=q0:
        max_pheromone = max(remaining_city_pheromones)
        result = np.where(remaining_city_pheromones == max_pheromone)
        if result[0].size == 1:
            return cities_left[result[0][0]]
        else:
            chosen_index = result[0][int(round(random.uniform(0,result[0].size-1), 0))] # index of cities_remaining to be chosen
            return cities_left[chosen_index]
    else:
        total = sum(remaining_city_pheromones)
        pick = random.uniform(0, total)
        current = 0
        for i in range(len(remaining_city_pheromones)):
            current += remaining_city_pheromones[i]
            if current > pick:
                return cities_left[i]

# Parameters
iterations = 1000
q_pheromone = 1500
q0 = 0.5
p = 0.5
p_max_val = 30
p_min_val = 1
p_initial = 10

# initialize distance and pheromone arrays, etc
distances = np.zeros((29,29))
for i in range(29):
    distances[i][i] = np.inf
    for j in range(i+1, 29):
        distance = ((float(data[i][1])-float(data[j][1]))**2 + (float(data[i][2])-float(data[j][2]))**2)**0.5
        distances[i][j] = distance
        distances[j][i] = distance
distances = np.array(distances)
pheromone_trail = np.full(distances.shape, p_initial)
np.fill_diagonal(pheromone_trail, 0)
p_max = np.full(distances.shape, p_max_val)
p_min = np.full(distances.shape, p_min_val)
np.fill_diagonal(p_max, 0)
np.fill_diagonal(p_min, 0)

best_path_global = []
best_distance_global = 100000

# ACO
for i in range(iterations):
    # set up population (currently 3 ants per city)
    ant_paths = [[0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],[21],[22],[23],[24],[25],[26],[27],[28],
                [0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],[21],[22],[23],[24],[25],[26],[27],[28],
                [0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],[21],[22],[23],[24],[25],[26],[27],[28],
                [0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],[21],[22],[23],[24],[25],[26],[27],[28],
                [0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],[21],[22],[23],[24],[25],[26],[27],[28]]

    # evaporation: t = (1-p)*t
    pheromone_trail = np.multiply(pheromone_trail, 1-p)
    np.fill_diagonal(pheromone_trail, 0)

    path_distances = []
    for edge in range(29-1):
        # each ant moves to new city
        for ant in range(len(ant_paths)):
            ant_path = ant_paths[ant]
            current_city = ant_path[-1]
            next_city = get_next_city(current_city, ant_path)
            ant_path.append(next_city)
            ant_paths[ant] = ant_path
    
    for ant in range(len(ant_paths)):
        ant_paths[ant].append(ant_paths[ant][0]) # complete loop
        distance_list = []

        # intensification
        for city in range(1,len(ant_paths[ant])):
            distance = distances[ant_paths[ant][city-1]][ant_paths[ant][city]]
            distance_list.append(distance)
            update = q_pheromone/distance
            pheromone_trail[ant_paths[ant][city-1]][ant_paths[ant][city]] += update
            pheromone_trail[ant_paths[ant][city]][ant_paths[ant][city-1]] += update

        # set max and min pheromone limits
        pheromone_trail = np.maximum(pheromone_trail, p_min)
        pheromone_trail = np.minimum(pheromone_trail, p_max)

        path_distances.append(distance_list)

    # find best path of current population
    best_distance = 100000
    best_path = []
    for path in range(len(path_distances)):
        if sum(path_distances[path]) < best_distance:
            best_distance = sum(path_distances[path])
            best_path = ant_paths[path]

    # update global best
    if best_distance < best_distance_global:
        best_distance_global = best_distance
        best_path_global = best_path
    
    print(best_distance_global)
    # print(best_distance, best_path)

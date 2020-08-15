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
ant_population = 145
q0 = 0.5
p = 0.5 #0.9,0.2 got low 9000
q_pheromone = 1500
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

for i in range(iterations):
    path_distances = []
    # # if all ants start from same city
    # ant_paths = []
    # for ant in range(ant_population):
    #     ant_path = [0]
    #     current_city = 0
    #     for edge in range(29-1):
    #         next_city = get_next_city(current_city, ant_path)
    #         ant_path.append(next_city)
    #         current_city = next_city
    #     ant_path.append(0)
    #     ant_paths.append(ant_path)
    #     distance_list = [distances[ant_path[i-1]][ant_path[i]] for i in range(1,len(ant_path))]
    #     path_distances.append(sum(distance_list))

    ant_paths = [[0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],[21],[22],[23],[24],[25],[26],[27],[28],
            [0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],[21],[22],[23],[24],[25],[26],[27],[28]]
            # ,
            # [0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],[21],[22],[23],[24],[25],[26],[27],[28],
            # [0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],[21],[22],[23],[24],[25],[26],[27],[28],
            # [0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],[21],[22],[23],[24],[25],[26],[27],[28]]
    for ant in range(len(ant_paths)):
        ant_path = ant_paths[ant]
        for edge in range(29-1):
            current_city = ant_path[-1]
            next_city = get_next_city(current_city, ant_path)
            ant_path.append(next_city)
        ant_paths[ant] = ant_path
        ant_paths[ant].append(ant_path[0])
        distance_list = [distances[ant_path[i-1]][ant_path[i]] for i in range(1,len(ant_path))]
        path_distances.append(sum(distance_list))
        
    best_distance = min(path_distances)
    best_path = ant_paths[path_distances.index(best_distance)]

    # update global best
    if best_distance < best_distance_global:
        best_distance_global = best_distance
        best_path_global = best_path
    
    print(best_distance_global)
    # print(best_path, best_distance)
    
    # evaporation: t = (1-p)*t
    pheromone_trail = np.multiply(pheromone_trail, 1-p)
    np.fill_diagonal(pheromone_trail, 0)

    # intensification
    for i in range(1,len(best_path)):
        #how to calculate length?
        length = distances[best_path[i-1]][best_path[i]]
        update = q_pheromone/length
        pheromone_trail[best_path[i-1]][best_path[i]] += update
        pheromone_trail[best_path[i]][best_path[i-1]] += update

    # set max and min pheromone limits
    pheromone_trail = np.maximum(pheromone_trail, p_min)
    pheromone_trail = np.minimum(pheromone_trail, p_max)

# print(best_path, best_distance)
# for i in range(29):
#     print(max(pheromone_trail[i].tolist()))
# print(pheromone_trail.tolist())
#############################################################################
#FIND TYPICAL VALUES? VARIATION IN ONLINE/OFFLINE, GETNEXTCITY BASED ON DISTANCE, alpha, beta, mu??????
###### ANT POPULATION 1000 ###############################
# results:
# initial_pheromone = 70
# q_pheromone = 7000
# q0 = 0.2
# p = 0.2
# pheromone_max = 100
# pheromone_min = 3
# bad: 8800

# initial_pheromone = 3
# q_pheromone = 50
# q0 = 0.2
# p = 0.2
# pheromone_max = 100
# pheromone_min = 0
# meh: 8600

# initial_pheromone = 30
# q_pheromone = 500
# q0 = 0.2
# p = 0.2
# pheromone_max = 100
# pheromone_min = 0
# meh: 8800
####################################
# number of ants = 5000
# initial_pheromone = 30
# q_pheromone = 500
# q0 = 0.5
# p_max_val = 100
# p_min_val = 0
# best so far, <8600

# number of ants = 5000
# initial_pheromone = 30
# q_pheromone = 500
# q0 = 0.2
# p_max_val = 100
# p_min_val = 0
# meh: got stuck at 8600

# number of ants = 5000
# initial_pheromone = 30
# q_pheromone = 500
# q0 = 0.2
# p_max_val = 100
# p_min_val = 1
# terrible


# iterations = 60
# ant_population = 5000
# q_pheromone = 800
# p_max_val = 100
# p_min_val = 1
# q0 = 0.7
# p = 0.2
# [0, 27, 5, 11, 8, 25, 2, 28, 4, 20, 1, 19, 9, 12, 15, 18, 3, 14, 17, 13, 16, 21, 10, 24, 6, 22, 26, 7, 23, 0] 9105.876005990172


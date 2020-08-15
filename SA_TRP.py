import time
import random
import math

# (node #, x, y, demand)
cities = [
  (1, 39, 19, 0),
  (2, 79, 19, 18),
  (3, 41, 79, 16),
  (4, 25, 31, 22),
  (5, 63, 93, 24),
  (6, 33, 5, 3),
  (7, 69, 17, 19),
  (8, 57, 73, 6),
  (9, 53, 75, 6),
  (10, 1, 1, 6),
  (11, 79, 73, 12),
  (12, 59, 5, 18),
  (13, 1, 37, 16),
  (14, 41, 31, 72),
  (15, 23, 73, 7),
  (16, 37, 27, 16),
  (17, 85, 93, 23),
  (18, 93, 13, 4),
  (19, 85, 45, 22),
  (20, 49, 91, 23),
  (21, 55, 43, 7),
  (22, 83, 29, 11),
  (23, 93, 49, 11),
  (24, 87, 23, 1),
  (25, 31, 23, 22),
  (26, 19, 97, 16),
  (27, 41, 9, 15),
  (28, 83, 61, 7),
  (29, 9, 7, 5),
  (30, 13, 13, 22),
  (31, 43, 37, 9),
  (32, 13, 61, 10),
  (33, 71, 51, 11),
  (34, 45, 93, 9),
  (35, 93, 55, 3),
  (36, 5, 97, 7),
  (37, 81, 11, 15),
  (38, 7, 53, 10),
  (39, 7, 41, 2)
]
# first city is depot
depot = cities[0]
no_cars = 6

def distance_calc(a, b):
  return round(((a[1]-b[1])**2 + (a[2]-b[2])**2)**0.5)
 
def objective_function(X):
  route_costs = []
  for car in X:
    distance = 0
    route = car
    route.append(depot)
    for city in range(len(route)):
      distance += distance_calc(route[city], route[city-1])
      distance += route[city][3] # demand
    route_costs.append(distance)
    del route[-1]
  return sum(route_costs)

def neighbourhood(X):
  # swap order of cities for each car
  # route = X[random.sample(range(len(X)),1)[0]]
  # if len(route) >= 2:
  #   i1, i2 = random.sample(range(len(route)), 2)
  #   route[i1], route[i2] = route[i2], route[i1]
  for route in X:
    if len(route) >= 2:
      i1, i2 = random.sample(range(len(route)), 2)
      route[i1], route[i2] = route[i2], route[i1]
#------------------------------------------------------
  # switch city to another route
  if len(X) >= 2:
    [r1, r2] = random.sample(range(len(X)), 2) # take from r1, add to r2
    if len(X[r1]) > 1:
      X[r2].insert(random.sample(range(len(X[r2])),1)[0], X[r1][-1])
      del X[r1][-1]
    else:
      #swap cities between routes
      for route_index in range(-1, len(X)-1):
        # pop city
        route = X[route_index]
        idx = range(len(route))
        [i] = random.sample(idx, 1)
        city = route.pop(i)

        #put city
        route = X[route_index+1]
        idx = range(len(route))
        if len(route) == 0:
          route.append(city)
        else:
          [i] = random.sample(idx, 1)
          route.insert(i, city)
  #-------------------------------------------------
  # # swap cities between routes
  # for route_index in range(-1, len(X)-1):
  #   # pop city
  #   car = X[route_index]
  #   idx = range(len(car))
  #   [i] = random.sample(idx, 1)
  #   city = car.pop(i)

  #   #put city
  #   car = X[route_index+1]
  #   idx = range(len(car))
  #   [i] = random.sample(idx, 1)
  #   car.insert(i, city)
  #-----------------------------------------------------
  return X

# initial_solution spreads cities amongst given cars
cities_per_car = math.ceil((len(cities)-1)/no_cars)
initial_solution = [cities[x:x+int(cities_per_car)] for x in range(1, len(cities), int(cities_per_car))]

print(objective_function(initial_solution))

computing_time = 60 # second(s)
initial_temperature = 30
cooling_constant = 0.0001  # cooling coefficient
attempts = 1000 # number of attempts in each level of temperature

current_solution = initial_solution
best_solution = initial_solution
best_fitness = objective_function(best_solution)
best_global_solution = best_solution
best_global_fitness = best_fitness
current_temperature = initial_temperature # current temperature

start = time.time()
for i in range(2000):
  if i % 200==0:
    attempts = round(attempts*1.2)
    print(attempts)
  for j in range(int(attempts)):

    # generate neighbourhood
    current_solution = neighbourhood(best_solution)
    current_fitness = objective_function(current_solution)
    E = abs(current_fitness - best_fitness)
          
    if current_fitness > best_fitness:
      p = math.exp(-E/(current_temperature))
      if random.random()<p:
        accept = True
      else:
        accept = False
    else:
      accept = True

    if accept == True:
      best_solution = current_solution
      best_fitness = objective_function(best_solution)
      

      if best_fitness < best_global_fitness:
        best_global_fitness = best_fitness
        best_global_solution = best_solution
        print("new cost:", best_fitness)
      else:
        print("new cost:", best_fitness, "(bad move")
      current_temperature = current_temperature/(1+current_temperature*cooling_constant)
      break

  # Cooling the temperature
  current_temperature = current_temperature/(1+current_temperature*cooling_constant)
  
  # Stop if optimal solution is achieved
  if best_global_fitness == 831:
    print("Optimal solution achieved")
    break

  # Stop by computing time
    #   end = time.time()
    #   if end-start >= computing_time:
    #     print("stopped due to time")
    #     break

# Print best solution
print("Best Solution:")
for car in range(len(best_global_solution)):
  route = []
  for city in best_global_solution[car]:
    route.append(city[0]-1) # match dataset's optimal route node convention
  print("Route #{}: {}".format(car+1, route))

# best fitness (excluding demand to match dataset's optimal route node convention 
print("Best Fitness: ", best_global_fitness)

# compare to supposed optimal solution
print(
  "Optimal solution including demand is: ",
  objective_function([
    [cities[i] for i in [37,31,14,35,25,33,19,2]],
    [cities[i] for i in [26,11]],
    [cities[i] for i in [24,3,38,12,9,28,29,5]],
    [cities[i] for i in [15,30,13]],
    [cities[i] for i in [18,27,10,16,4,8,7]],
    [cities[i] for i in [6,1,36,17,23,21,22,34,32,20]],
  ])
)
from control import TransferFunction, feedback, step_info, step_response, series
import random

def q1_perfFNC(Kp, Ti, Td):
  G = Kp * TransferFunction([Ti * Td, Ti, 1], [Ti, 0])
  F = TransferFunction(1, [1, 6, 11, 6, 0])
  sys = feedback(series(G, F), 1)
  sysinf = step_info(sys)
  
  t = []
  i = 0
  while i < 100:
      t.append(i)
      i += 0.01
  
  T, y = step_response(sys, T=t)
  ISE = sum((y - 1) ** 2)
  t_r = sysinf['RiseTime']
  t_s = sysinf['SettlingTime']
  M_p = sysinf['Overshoot']

  return ISE, t_r, t_s, M_p

def apply_performance(generation):
  # only use ISE
  for i in range(len(generation)):
    try:
      ise = q1_perfFNC(generation[i][0], generation[i][1], generation[i][2])
      generation[i].append(10000/ise[0])
      # generation[i].append(100/(ise[0]-72.5))
    except:
      ise = None
      generation[i].append(0.0)

# returns index of FPS pick
def FPS_selection(population):
  total = sum(individual[-1] for individual in population)
  pick = random.uniform(0, total)
  current = 0
  for i in range(len(population)):
      current += population[i][-1]
      if current > pick:
          return i

# take 2 genes, apply crossover given alpha and crossover probability
def whole_arithmetic_crossover(g1, g2, p, a):
  if random.random() < p:
    c1 = a*g2 + (1-a)*g1
    c2 = a*g1 + (1-a)*g2
    return round(c1,2), round(c2,2)
  else:
    return g1, g2

def runGA(generations, population, crossover_probability, mutation_probability):
  evolution = []
  initial_population = []

  # create initial generation
  for i in range(population):
    K_p = round(random.uniform(2.01, 17.99), 2)
    T_i = round(random.uniform(1.06, 9.41), 2)
    T_d = round(random.uniform(0.27, 2.36), 2)
    evolution.append([K_p, T_i, T_d])
    initial_population.append([K_p, T_i, T_d])

  # GA
  for i in range(generations):
    apply_performance(evolution)  # calculate performance
    children = []                 # initialize children

    perf_vals = [individual[-1] for individual in evolution]
    print(max(perf_vals))

    # elitism
    for i in range(2):
      perf_vals = [individual[-1] for individual in evolution]
      children.append(evolution[perf_vals.index(max(perf_vals))][:-1]) # remove performance value and add to children

    # mating
    for mating in range(int((population-2)/2)):
      # select parents
      [i1,i2] = [FPS_selection(evolution), FPS_selection(evolution)]

      child_1 = []
      child_2 = []

      for gene in range(3):

        g1, g2 = whole_arithmetic_crossover(evolution[i1][gene], evolution[i2][gene], crossover_probability, 0.5)
        child_1.append(g1)
        child_2.append(g2)
        
      # Random Noise Mutation
      if random.random() < mutation_probability:
        child_1[0] += round(random.gauss(0,2))
        if child_1[0]>17.99:
          child_1[0]=17.99
        elif child_1[0]<2.01:
          child_1[0]=2.01
      if random.random() < mutation_probability:
        child_1[1] += round(random.gauss(0,1.5))
        if child_1[1]>9.41:
          child_1[1]=9.41
        elif child_1[1]<1.06:
          child_1[1]=1.06
      if random.random() < mutation_probability:
        child_1[2] += round(random.gauss(0,1))
        if child_1[2]>2.36:
          child_1[2]=2.36
        elif child_1[2]<0.27:
          child_1[2]=0.27
      if random.random() < mutation_probability:
        child_2[0] += round(random.gauss(0,2))
        if child_2[0]>17.99:
          child_2[0]=17.99
        elif child_2[0]<2.01:
          child_2[0]=2.01
      if random.random() < mutation_probability:
        child_2[1] += round(random.gauss(0,1.5))
        if child_2[1]>9.41:
          child_2[1]=9.41
        elif child_2[1]<1.06:
          child_2[1]=1.06
      if random.random() < mutation_probability:
        child_2[2] += round(random.gauss(0,1))
        if child_2[2]>2.36:
          child_2[2]=2.36
        elif child_2[2]<0.27:
          child_2[2]=0.27

      # Uniform Mutation
      # if random.random() < mutation_probability:
      #   child_1[0] = round(random.uniform(2, 18), 2)
      # if random.random() < mutation_probability:
      #   child_1[1] = round(random.uniform(1.05, 9.42), 2)
      # if random.random() < mutation_probability:
      #   child_1[2] = round(random.uniform(0.26, 2.37), 2)
      # if random.random() < mutation_probability:
      #   child_2[0] = round(random.uniform(2, 18), 2)
      # if random.random() < mutation_probability:
      #   child_2[1] = round(random.uniform(1.05, 9.42), 2)
      # if random.random() < mutation_probability:
      #   child_2[2] = round(random.uniform(0.26, 2.37), 2)
      # print(evolution[i1], evolution[i2], child_1, child_2)

      children.append(child_1)
      children.append(child_2)

    evolution = children

  # compare 
  apply_performance(initial_population)
  perf_vals = [individual[-1] for individual in initial_population]
  best_individual = initial_population[perf_vals.index(max(perf_vals))][:-1]
  ISE, t_r, t_s, M_p = q1_perfFNC(best_individual[0], best_individual[1], best_individual[2])
  print("Initial performance: ", ISE, t_r, t_s, M_p, " with parameters: ", best_individual)

  apply_performance(evolution)
  perf_vals = [individual[-1] for individual in evolution]
  best_individual = evolution[perf_vals.index(max(perf_vals))][:-1]
  ISE, t_r, t_s, M_p = q1_perfFNC(best_individual[0], best_individual[1], best_individual[2])
  print("Final performance: ", ISE, t_r, t_s, M_p, " with parameters: ", best_individual)


# algorithm parameters: generations, population, crossover_probability, mutation_probability
runGA(150,50,0.6,0.25)
runGA(60,50,0.6,0.25)
runGA(120,50,0.6,0.25)
runGA(180,50,0.6,0.25)
runGA(60,20,0.6,0.25)
# runGA(60,50,0.6,0.25) # duplicate
runGA(60,80,0.6,0.25)
runGA(60,50,0.9,0.25)
runGA(60,50,0.6,0.05)
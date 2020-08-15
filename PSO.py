import random
import math
from copy import copy

def camelback_function(position):
    x = position[0]
    y = position[1]
    return (4-2.1*x**2+(x**4)/3)*x**2 + x*y + (-4+4*y**2)*y**2

# def testing_function(position):
#     x = position[0]
#     y = position[1]
#     return x**2+y**2
       
def inertia_weight_update(v, x, parameters, p_best, n_best):
    w = parameters[0]
    c1 = parameters[1]
    c2 = parameters[2]
    r1 = random.random()
    r2 = random.random()
    return w*v + c1*r1*(p_best-x) + c2*r2*(n_best-x)
    
def constriction_factor_update(v, x, parameters, p_best, n_best):
    w = parameters[0]
    c1 = parameters[1]
    c2 = parameters[2]
    r1 = random.random()
    r2 = random.random()
    phi = c1+c2
    k = 2/abs(2-phi-math.sqrt(phi**2-4*phi))
    return k*(w*v + c1*r1*(p_best-x) + c2*r2*(n_best-x))
    
def guaranteed_convergence_update(v, x, parameters, p_best, n_best):
    return -x+n_best+w*v+p*(1-2*r)

class Particle:
    def __init__(self, position, fitness_function):
        self.position = position
        self.best_position = copy(position)
        self.num_dimensions = len(position)
        self.velocity = [0]*self.num_dimensions
        self.fitness_function = fitness_function
        self.best_fitness = None
        self.evaluate_fitness()

    def update_velocity(self, update_function, parameters, g_best_position, gcpso=False, p_t=None, r=None):
        if gcpso:
            w = parameters[0]
            for dim in range(self.num_dimensions):
                self.velocity[dim] = -self.position[dim] + g_best_position[dim] + w*self.velocity[dim] + p_t*(1-2*r[dim])
        else:
            for dim in range(self.num_dimensions):
                self.velocity[dim] = update_function(self.velocity[dim], self.position[dim], parameters, self.best_position[dim], g_best_position[dim])
            
    def update_position(self, bounds, gcpso=False, w=None, p_t=None, r=None, g_best_position=None):
        if gcpso:
            for dim in range(self.num_dimensions):
                self.position[dim] = g_best_position[dim] + w*self.velocity[dim] + p_t*(1-2*r[dim])
        else:
            for dim in range(self.num_dimensions):
                self.position[dim] += self.velocity[dim]
                
        for dim in range(self.num_dimensions):
            if self.position[dim] < bounds[dim][0]:
                self.position[dim] = bounds[dim][0]
                self.velocity[dim] = 0
            elif self.position[dim] > bounds[dim][1]:
                self.position[dim] = bounds[dim][1]
                self.velocity[dim] = 0

    def evaluate_fitness(self):
        fitness = self.fitness_function(self.position)
        if self.best_fitness == None:
            self.best_fitness = fitness
            self.best_position = copy(self.position)
        elif fitness < self.best_fitness:
            self.best_fitness = fitness
            self.best_position = copy(self.position)
            # print("p_best fitness: ", self.best_fitness, self.best_position)
        # return self.best_fitness, self.best_position
        return fitness, copy(self.position)

class Swarm:
    def __init__(self, particle_num, iterations, fitness_function, update_function, update_parameters, bounds, gcpso=False):
        self.swarm = []
        self.g_best_position = None
        self.g_best_fitness = None
        self.bounds_x = bounds[0]
        self.bounds_y = bounds[1]
        self.average_fitness_history = []
        self.g_best_history = []

        # GCPSO
        self.gcpso = gcpso
        self.g_successes = 0
        self.g_failures = 0
        self.g_best_particle = None
        self.e_s = 15
        self.e_f = 5
        self.p_t = 1

        # INITIALIZE
        fitness_counter = 0
        for i in range(particle_num):
            position = [random.uniform(self.bounds_x[0], self.bounds_x[1]), random.uniform(self.bounds_y[0], self.bounds_y[1])]
            self.swarm.append(Particle(position, fitness_function))
            p_result = self.swarm[-1].evaluate_fitness()
            # print(p_result)
            self.update_global(p_result)
            fitness_counter += p_result[0]
        self.g_best_history.append(self.g_best_fitness)
        self.average_fitness_history.append(fitness_counter/particle_num)
        # print("initial global best: ", self.g_best_fitness, self.g_best_position)

        for move in range(iterations):
            fitness_counter = 0
            for particle in self.swarm:
                is_best_particle = (particle==self.g_best_particle)
                if self.gcpso and is_best_particle:
                    r = [random.random() for dim in range(2)] # different for each dimension
                    if self.g_successes > self.e_s:
                        # print("increasing pt")
                        self.p_t *= 2
                    elif self.g_failures < self.e_f:
                        # print("decreasing pt")
                        self.p_t /= 2
                    w = update_parameters[0]
                    particle.update_velocity(update_function, update_parameters, self.g_best_position, is_best_particle, self.p_t, r)
                    particle.update_position(bounds, is_best_particle, w, self.p_t, r, self.g_best_position)
                else:
                    particle.update_velocity(update_function, update_parameters, self.g_best_position)
                    particle.update_position(bounds)

                p_result = particle.evaluate_fitness()
                fitness_counter += p_result[0]

                if self.gcpso:
                    # print(self.update_global(p_result))
                    self.update_gcpso_epsilon(self.update_global(p_result), particle)
                else:
                    self.update_global(p_result)

            self.g_best_history.append(self.g_best_fitness)
            self.average_fitness_history.append(fitness_counter/particle_num)

        print("best result: ", self.g_best_fitness, self.g_best_position)
        # print(self.g_best_history)
        # print(self.average_fitness_history)
        # for i in self.g_best_history:
        #     print(i)
        # for i in self.average_fitness_history:
        #     print(i)

        # # print particle end positions to check convergence
        # for particle in self.swarm:
        #     print(particle.position)

    def update_global(self, result):
        if self.g_best_fitness == None:
            self.g_best_fitness = result[0]
            self.g_best_position = result[1]
        else:
            if result[0] < self.g_best_fitness:
                self.g_best_fitness = result[0]
                self.g_best_position = result[1]
                # print("new global best!", result)
                return True
        return False

    def update_gcpso_epsilon(self, success, particle):
        if success:
            # GCPSO success
            # print("success")
            self.g_successes += 1
            self.g_failures = 0
            self.g_best_particle = particle
        else:
            # GCPSO failure
            self.g_failures += 1
            self.g_successes = 0

if __name__ == '__main__':
    bounds = [[-5,5], [-5,5]]

    # # update_parameters = [w, c1, c2]

    # # Simple PSO
    # update_parameters = [1, 1.4944, 1.4944]
    # update_parameters = [1, 0.1, 0.1]
    # Swarm(100, 500, camelback_function, inertia_weight_update, update_parameters, bounds)

    # # # Inertia weight PSO
    # update_parameters = [0.792, 1.4944, 1.4944]
    # Swarm(100, 500, camelback_function, inertia_weight_update, update_parameters, bounds)

    # # # Constriction Coefficient PSO
    update_parameters = [1, 2.05, 2.05]
    Swarm(100, 500, camelback_function, constriction_factor_update, update_parameters, bounds)

    # # # Inertia weight with Guaranteed Convergence PSO
    # update_parameters = [0.79, 1.4944, 1.4944]
    # Swarm(100, 500, camelback_function, inertia_weight_update, update_parameters, bounds, True)

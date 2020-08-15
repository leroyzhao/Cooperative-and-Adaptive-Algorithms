import random, math, numpy, operator
from deap import algorithms, base, creator, tools, gp

# define functions
def if_(a,b,c):
    if a:
        return b
    else:
        return c

def and_(a,b):
    return (a and b)

def or_(a,b):
    return (a or b)

def not_(a):
    return (not a)

"""
    6 terminal mux:
    mux terminals: [a0 a1 d0 d1 d2 d3]
    64 possible combinations (6 terminals, 2 values => 2**6 possibilities)
    create parallel arrays for input (all mux terminal combinations) and output (if arrangement is valid)
"""

num_address = 3
num_data = 2 ** num_address
num_terminals = num_address + num_data

# input : [A0 A1 A2 D0 D1 D2 D3 D4 D5 D6 D7] for a 8-3 mux
inputs = [[0] * num_terminals for i in range(2 ** num_terminals)]
outputs = [None] * (2 ** num_terminals)

for i in range(2 ** num_terminals):
    value = i
    divisor = 2 ** num_terminals
    # Fill the input bits
    for j in range(num_terminals):
        divisor /= 2
        if value >= divisor:
            inputs[i][j] = 1
            value -= divisor
    
    # Determine the corresponding output
    indexOutput = num_address
    for j, k in enumerate(inputs[i][:num_address]):
        indexOutput += k * 2**j
    outputs[i] = inputs[i][indexOutput]
# counter = 0
# for i, input_ in enumerate(inputs):
#     if (or_(and_(if_(input_[2], and_(if_(input_[2], input_[9], input_[2]), and_(input_[3], input_[7])), and_(input_[5], input_[1])), input_[1]), if_(input_[1], if_(input_[1], and_(input_[9], input_[2]), if_(if_(input_[1], input_[9], and_(if_(input_[8], input_[9], input_[2]), input_[1])), if_(input_[2], input_[9], and_(and_(input_[10], input_[2]), if_(input_[9], input_[1], if_(input_[2], input_[7], input_[3])))), if_(input_[2], and_(if_(input_[1], and_(input_[3], if_(input_[2], input_[8], input_[3])), input_[7]), input_[2]), input_[9]))), if_(input_[4], if_(input_[2], input_[7], input_[3]), and_(if_(and_(input_[5], input_[1]), input_[2], input_[8]), input_[2]))))==outputs[i]):
#         counter+=1
# print(counter/(2**num_terminals))
# asdf

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

pset = gp.PrimitiveSet(name="MAIN", arity=num_terminals, prefix="ARG")
pset.addPrimitive(and_, arity=2)
pset.addPrimitive(or_, arity=2)
pset.addPrimitive(not_, arity=1)
pset.addPrimitive(if_, arity=3)
# pset.renameArguments(ARG0="a0", ARG1="a1", ARG2="d0", ARG3="d1", ARG4="d3", ARG5="d4")
# pset.renameArguments(ARG0="a0", ARG1="a1", ARG2="a2", ARG3="d0", ARG4="d1", ARG5="d2", ARG6="d3", ARG7="d4", ARG8="d5", ARG9="d6", ARG10="d7", ARG11="d8")
pset.addTerminal(1)
pset.addTerminal(0)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genGrow, pset=pset, min_=2, max_=5) # enable generation a full expression tree with min and max depth
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr) # enable individual solution generator
toolbox.register("population", tools.initRepeat, list, toolbox.individual) # enable population generator
toolbox.register("compile", gp.compile, pset=pset) # enable compilation of expression

# evaluation of multiplexer
def evalMultiplexer(individual):
    func = toolbox.compile(expr=individual)
    return sum(func(*input_) == out for input_, out in zip(inputs, outputs))/(2 ** num_terminals),

toolbox.register("evaluate", evalMultiplexer)
toolbox.register("select", tools.selTournament, tournsize=7) # "Select the best individual among tournsize randomly chosen individuals, k times. The list returned contains references to the input individuals."
toolbox.register("mate", gp.cxOnePoint) # "Randomly select crossover point in each individual and exchange each subtree with the point as root between each individual."
toolbox.register("expr_mut", gp.genGrow, min_=0, max_=2) # "Generate an expression where each leaf might have a different depth between min and max."
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset) # "Mutate an individual by replacing attributes, with probability indpb, by a integer uniformly drawn between low and up inclusively."
toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=10)) # control bloat during crossover
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=10)) # control bloat during mutation

if __name__ == "__main__":
    pop = toolbox.population(n=200)

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    # stats.register("std", numpy.std)
    # stats.register("min", numpy.min)
    stats.register("max", numpy.max)    

    algorithms.eaSimple(pop, toolbox, cxpb=0.80, mutpb=0.01, ngen=100, stats=stats, halloffame=hof, verbose=True)

    bests = tools.selBest(pop, k=1)
    print(bests[0])
    print(bests[0].fitness)
    # print(pop, stats, hof)
    print(evalMultiplexer(bests[0]))

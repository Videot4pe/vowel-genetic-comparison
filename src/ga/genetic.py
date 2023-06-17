import random
from deap import base, creator, tools, algorithms
import numpy as np
import random
from analysis.distance import getDistance

def genetic(xTrain, yTrain):
  
  # Определение функции оценки приспособленности
  def fitness_function(individual):
    success = 0
    counter = 0
    
    for i in range (0, len(xTrain)):
      source = xTrain[i]
      sourceLabel = yTrain[i]
      
      distances = []
      labels = []
      
      min = float('inf')
      minIndex = -1
      for j in range (0, len(xTrain)):
        if i != j:
          target = xTrain[j]
          targetLabel = yTrain[j]
          
          distance = getDistance(individual, source, target)
          distances.append(distance)
          
          labels.append(targetLabel)
          
          if distance < min:
            min = distance
            minIndex = j
      
      # minIndex = distances.index(min(distances))
      
      counter += 1
      if sourceLabel == yTrain[minIndex]:
        success += 1
          
    return success/counter,

  creator.create("FitnessMax", base.Fitness, weights=(1.0,))
  creator.create("Individual", list, fitness=creator.FitnessMax)

  toolbox = base.Toolbox()
  toolbox.register("attr_float", random.uniform, 0, 1)
  toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=5)
  toolbox.register("population", tools.initRepeat, list, toolbox.individual)
  toolbox.register("evaluate", fitness_function)

  population_size = 100
  num_generations = 1
  cxpb = 0.8
  mutpb = 0.2

  population = toolbox.population(n=population_size)

  toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=0, up=1, eta=1.0)
  toolbox.register("mutate", tools.mutPolynomialBounded, eta=4.0, low=0, up=1, indpb=0.2)
  toolbox.register("select", tools.selTournament, tournsize=3)

  stats = tools.Statistics(lambda ind: ind.fitness.values)
  stats.register("max", np.max)

  result, log = algorithms.eaSimple(population, toolbox, cxpb=cxpb, mutpb=mutpb, ngen=num_generations, stats=stats, verbose=True)

  best_ind = tools.selBest(population, k=1)[0]
  print("Best individual: x1={}, x2={}, x3={}, x4={}, x5={}".format(best_ind[0], best_ind[1], best_ind[2], best_ind[3], best_ind[4]))
  print("Fitness: {}".format(best_ind.fitness.values[0]))
  return best_ind
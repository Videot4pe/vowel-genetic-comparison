import random
from deap import base, creator, tools, algorithms
import numpy as np
import random
from analysis.distance import getDistance
import matplotlib.pyplot as plt

def genetic(xTrain, yTrain):
  
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
      
      if sourceLabel == yTrain[minIndex]:
        success += 1
          
    return success/len(xTrain),

  creator.create("FitnessMax", base.Fitness, weights=(1.0,))
  creator.create("Individual", list, fitness=creator.FitnessMax)

  toolbox = base.Toolbox()
  toolbox.register("attr_float", random.uniform, 0, 1)
  toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=6)
  toolbox.register("population", tools.initRepeat, list, toolbox.individual)
  toolbox.register("evaluate", fitness_function)

  population_size = 80
  num_generations = 80
  cxpb = 0.8
  mutpb = 0.2

  population = toolbox.population(n=population_size)

  toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=0, up=1, eta=.5)
  # toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.5, indpb=0.2)
  toolbox.register("mutate", tools.mutPolynomialBounded, eta=4.0, low=0, up=1, indpb=0.1)
  toolbox.register("select", tools.selTournament, tournsize=3)

  stats = tools.Statistics(lambda ind: ind.fitness.values)
  stats.register("avg", np.mean, axis=0)
  stats.register("std", np.std, axis=0)
  stats.register("min", np.min, axis=0)
  stats.register("max", np.max, axis=0)

  hof = tools.ParetoFront()
  result, logbook = algorithms.eaMuPlusLambda(population, toolbox, mu=population_size, lambda_=population_size, cxpb=0.7, mutpb=0.3, ngen=num_generations, stats=stats, halloffame=hof)
  best_ind = tools.selBest(population, k=1)[0]
  print("Best individual: x1={}, x2={}, x3={}, x4={}, x5={}, x6={}".format(best_ind[0], best_ind[1], best_ind[2], best_ind[3], best_ind[4], best_ind[5]))
  print("Fitness: {}".format(best_ind.fitness.values[0]))
  
  
  plt.figure(figsize=(10,8))
  front = np.array([(c['gen'], c['avg'][0]) for c in logbook])
  plt.plot(front[:,0][1:-1], front[:,1][1:-1], "-bo", c="b")
  plt.axis("tight")
  plt.show()
  
  return best_ind
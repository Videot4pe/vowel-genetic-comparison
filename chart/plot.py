import matplotlib.pyplot as plt
import numpy as np
import random

def plotData(data):
  keys = data.keys()
  items = data.items()

  
  fig = plt.figure()
  ax = fig.add_subplot(projection='3d')
  ax.set_xlabel('tongue')
  ax.set_ylabel('throat')
  ax.set_zlabel('jaw')

  x = []
  y = []
  z = []
  c = []
  for key in keys:
    for tract in data[key]:
      x.append(tract[0])
      y.append(tract[1])
      z.append(tract[2])
      c.append(tract[3])
      
  img = ax.scatter(x, y, z, c=c, cmap=plt.hot())
  fig.colorbar(img)
  
  # for i, key in enumerate(keys):
  #   ax.annotate(key, (x[i], y[i], z[i]))
    
  plt.show()
import math
import numpy as np

def getDistance(coeffs, sound1, sound2):
  if len(sound1) == 0 or len(sound2) == 0 or len(coeffs) == 0:
    raise Exception("Can't be empty")
  
  if len(sound1) != len(sound2) or len(sound1) != len(coeffs) or len(sound2) != len(coeffs):
    raise Exception("Must be same len")
  
  sound1 = np.array(sound1)
  sound2 = np.array(sound2)
  weights = np.array(coeffs)
  
  sound1 = sound1 * weights
  sound2 = sound2 * weights
  
  return np.sum(abs(sound1 - sound2))
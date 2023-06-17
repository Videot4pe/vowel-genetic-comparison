from dtw import dtw
from fastdtw import fastdtw
import numpy as np

def getDtw(mfcc1, mfcc2):
  distance, path = fastdtw(mfcc1.T, mfcc2.T)
  pathLength = len(path)
  quality = np.exp(-distance/pathLength)
  return distance
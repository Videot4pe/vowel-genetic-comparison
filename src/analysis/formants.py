import glob
import numpy as np
import pandas as pd
import parselmouth 
import statistics

from parselmouth.praat import call
from scipy.stats.mstats import zscore
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def measureFormants(sound, wave_file, f0min,f0max):
  sound = parselmouth.Sound(sound) # read the sound
  pitch = call(sound, "To Pitch (cc)", 0, f0min, 15, 'no', 0.03, 0.45, 0.01, 0.35, 0.14, f0max)
  pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
  
  formants = call(sound, "To Formant (burg)", 0.0025, 5, 5000, 0.025, 50)
  numPoints = call(pointProcess, "Get number of points")

  f1_list = []
  f2_list = []
  f3_list = []
  f4_list = []
  
  # Measure formants only at glottal pulses
  for point in range(0, numPoints):
    point += 1
    t = call(pointProcess, "Get time from index", point)
    f1 = call(formants, "Get value at time", 1, t, 'Hertz', 'Linear')
    f2 = call(formants, "Get value at time", 2, t, 'Hertz', 'Linear')
    f1_list.append(f1)
    f2_list.append(f2)
  
  f1_list = [f1 for f1 in f1_list if str(f1) != 'nan']
  f2_list = [f2 for f2 in f2_list if str(f2) != 'nan']
  
  # calculate mean formants across pulses
  if len(f1_list) == 0 or len(f2_list) == 0:
    return 0, 0, 0, 0, 0, 0, 0, 0
  
  f1_mean = statistics.mean(f1_list)
  f2_mean = statistics.mean(f2_list)
  
  # calculate median formants across pulses, this is what is used in all subsequent calcualtions
  # you can use mean if you want, just edit the code in the boxes below to replace median with mean
  f1_median = statistics.median(f1_list)
  f2_median = statistics.median(f2_list)
  
  return f1_mean, f2_mean, f1_median, f2_median
  
def measurePitch(voiceID, f0min, f0max, unit):
  sound = parselmouth.Sound(voiceID)
  duration = call(sound, "Get total duration")
  pitch = call(sound, "To Pitch", 0.0, f0min, f0max) # create a praat pitch object
  meanF0 = call(pitch, "Get mean", 0, 0, unit) # get mean pitch
  return duration, meanF0

def extractFormants(path):
  sound = parselmouth.Sound(path)
  duration, meanF0 = measurePitch(sound, 75, 300, "Hertz")
  f1_mean, f2_mean, f1_median, f2_median = measureFormants(sound, path, 75, 300)
  
  return meanF0, f1_mean, f2_mean
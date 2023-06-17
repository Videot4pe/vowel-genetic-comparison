import numpy as np
import librosa
import scipy.signal as signal
import matplotlib.pyplot as plt
import scipy.fft as fft
from analysis.formants import extractFormants

def getTongue(meanF0, meanF1, meanF2):
  meanF1F2 = (meanF1 + meanF2) / 2
  
  # return (meanF1 / (2 * meanF0)) - 0.5
  # return (meanF1F2 / (2 * meanF0)) - 0.5
  return ((meanF2 - meanF1) / meanF0) * 100

def getThroat(meanF0, meanF1, meanF2):
  # return (meanF2 / (2 * meanF0)) - 0.5
  return ((meanF1 - meanF0) / meanF0) * 100

def getJaw(meanF0, meanF1, meanF2):
  # return (formants[2] / (2 * mean_f0)) - 0.5
  # return (meanF1 / (2 * meanF0)) - 0.5
  return ((meanF1 - meanF2) / meanF0) * 100

def getLips(meanF0, meanF1, meanF2):
  # return (formants[2] / (2 * mean_f0)) - 0.5
  # return (meanF1 / (2 * meanF0)) - 0.5
  return meanF0 - ((meanF1 + meanF2) / 2)

# def getVocalTractParams(y, sr):
#   f0, _ = librosa.core.piptrack(y=y, sr=sr)
#   mean_f0 = np.mean(f0[f0 > 0])
#   formants = extractFormants(y, sr)
  
#   tongue = getTongue(formants, mean_f0)
#   throat = getThroat(formants, mean_f0)
#   jaw = getJaw(formants, mean_f0)
#   return tongue, throat, jaw

def getVocalTractParams(formants):
  meanF0 = formants[0]
  meanF1 = formants[1]
  meanF2 = formants[2]
  meanF3 = formants[3]
  
  tongue = getTongue(meanF0, meanF1, meanF2)
  throat = getThroat(meanF0, meanF1, meanF2)
  jaw = getJaw(meanF0, meanF1, meanF2)
  lips = getLips(meanF0, meanF1, meanF2)
  return tongue, throat, jaw, lips
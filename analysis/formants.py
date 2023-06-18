import parselmouth 
import statistics
from parselmouth.praat import call

def measureFormants(sound, wave_file, f0min,f0max):
  sound = parselmouth.Sound(sound)
  pitch = call(sound, "To Pitch (cc)", 0, f0min, 15, 'no', 0.03, 0.45, 0.01, 0.35, 0.14, f0max)
  pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
  
  formants = call(sound, "To Formant (burg)", 0.0025, 5, 5000, 0.025, 50)
  numPoints = call(pointProcess, "Get number of points")

  f1_list = []
  f2_list = []
  
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
  
  if len(f1_list) == 0 or len(f2_list) == 0:
    return 0, 0
  
  f1_mean = statistics.mean(f1_list)
  f2_mean = statistics.mean(f2_list)
  
  return f1_mean, f2_mean
  
def measurePitch(voiceID, f0min, f0max, unit):
  sound = parselmouth.Sound(voiceID)
  duration = call(sound, "Get total duration")
  pitch = call(sound, "To Pitch", 0.0, f0min, f0max)
  meanF0 = call(pitch, "Get mean", 0, 0, unit)
  return duration, meanF0

def extractFormants(path):
  sound = parselmouth.Sound(path)
  duration, meanF0 = measurePitch(sound, 75, 300, "Hertz")
  f1_mean, f2_mean = measureFormants(sound, path, 75, 300)
  
  return meanF0, f1_mean, f2_mean
import math

def getDistance(coeffs, sound1, sound2):
  sound1Metric = coeffs[0] * (
    sound1[0] * coeffs[1] + 
    sound1[1] * coeffs[2] + 
    sound1[2] * coeffs[3] + 
    sound1[3] * coeffs[4]
  )
  sound2Metric = coeffs[0] * (
    sound2[0] * coeffs[1] + 
    sound2[1] * coeffs[2] + 
    sound2[2] * coeffs[3] + 
    sound2[3] * coeffs[4]
  )
  return abs(sound2Metric - sound1Metric)
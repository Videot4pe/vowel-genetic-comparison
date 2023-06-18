from analysis.distance import getDistance
from utils.files import loadFormantsFolder, loadFormantsPath
from analysis.tract import getVocalTractParams
import numpy as np
from collections import Counter

def recognize(xData, yData, label):
  with open('config.txt', 'r') as file:
    data = file.read().replace('\n', '')
    
  coeffs = np.asarray(data.split(' '), dtype=float)
  print(coeffs)
  
  print(label)
  
  meanParams = {}
  meanCounter = {}
  
  for i in range(0, len(yData)):
    if meanParams.get(yData[i]) is None:
      meanParams[yData[i]] = xData[i]
      meanCounter[yData[i]] = 1
    else:
      meanCounter[yData[i]] += 1
      meanParams[yData[i]] = np.add(meanParams[yData[i]], xData[i])
  
  for key in meanParams:
    meanParams[key] = np.multiply(np.divide(meanParams[key], meanCounter[key]), coeffs)
  
  print(meanParams)
  statistics = {}
  mean = {}
  allCount = 0
  tp = 0
  fp = 0
  np.set_printoptions(suppress=True)
  for i, test1 in enumerate(xData):
    minDistance = float('inf')
    minDistanceIndex = -1
    for j, test2 in enumerate(xData):
      if i != j:
        distance = getDistance(coeffs, test1, test2)
        # print('Distance: ', distance, yData[i], yData[j])
        if (distance < minDistance):
          minDistance = distance
          minDistanceIndex = j
        if mean.get(yData[i]) is None:
          mean[yData[i]] = {}
          mean[yData[i]][yData[j]] = [1, distance]
        elif mean.get(yData[i]).get(yData[j]) is None:
          mean[yData[i]][yData[j]] = [1, distance]
        else:
          mean[yData[i]][yData[j]][0] += 1
          mean[yData[i]][yData[j]][1] += distance
    allCount += 1
    
    if statistics.get(yData[i]) is None:
      statistics[yData[i]] = [0, 0, 1]
    else:
      statistics[yData[i]][2] += 1
    
    if yData[i] == yData[minDistanceIndex]:
      tp += 1
      statistics[yData[i]][0] += 1
    else:
      fp += 1
      statistics[yData[i]][1] += 1
      # print('Params of ', yData[i], ' and ', yData[minDistanceIndex], ': ', np.around(np.asarray(xData[i]), 2), np.around(np.asarray(xData[minDistanceIndex]), 2))
  
  for key in statistics.keys():
    print(key, ': ', round((statistics[key][0] / statistics[key][2]) * 100, 2), '%')
  
  for key in mean.keys():
    for key2 in mean[key].keys():
      print(key, ' mean with ', key2, ': ', round((mean[key][key2][1] / mean[key][key2][0]), 2))
  
  print('All: ', round((tp/allCount) * 100, 2), '%')
  
def compare(sound1, sound2):
  with open('config.txt', 'r') as file:
    data = file.read().replace('\n', '')
  
  coeffs = np.asarray(data.split(' '), dtype=float)
  
  formants = loadFormantsPath()
  vocalTract1 = getVocalTractParams(formants[0])
  vocalTract2 = getVocalTractParams(formants[1])
  
  print('Distance: ', getDistance(coeffs, vocalTract1, vocalTract2))
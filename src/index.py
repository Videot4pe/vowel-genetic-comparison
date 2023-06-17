from utils.files import loadFormantsFolder, preprocessFiles, loadFormantsPath
from chart.plot import plotData
from analysis.tract import getVocalTractParams
from analysis.distance import getDistance
from ga.genetic import genetic
import constants
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from sklearn.model_selection import train_test_split
import numpy as np

def preprocess():
  preprocessFiles('../resources')
  
def recognize(sound1, sound2):
  with open('config.txt', 'r') as file:
    data = file.read().replace('\n', '')
  
  coeffs = np.asarray(data.split(' '), dtype=float)
  print('Coeffs: ', coeffs)
  
  formants = loadFormantsPath(sound1, sound2)
  vocalTract1 = getVocalTractParams(formants[0])
  vocalTract2 = getVocalTractParams(formants[1])
  
  print('Distance: ', getDistance(coeffs, vocalTract1, vocalTract2))
  
def train():
  formants = loadFormantsFolder('../resources')

  params = {}
  xSet = []
  ySet = []

  for key in formants:
    params[key] = []
    for file in formants[key]:
      vocalTract = getVocalTractParams(file)
      params[key].append(vocalTract)
      xSet.append(vocalTract)
      ySet.append(key)

  xTrain, xTest, yTrain, yTest = train_test_split(xSet, ySet, train_size=0.9, random_state=42)

  phonemes = {}

  for y in yTrain:
    if phonemes.get(y) is None:
      phonemes[y] = 1
    else:
      phonemes[y] += 1

  coeffs = genetic(xTrain, yTrain)
  
  with open("config.txt", "w") as txt_file:
    txt_file.write(' '.join(str(c) for c in coeffs) + '\n')
  
def fullCycle():
  formants = loadFormantsFolder('../resources')

  params = {}
  xSet = []
  ySet = []

  for key in formants:
    params[key] = []
    for file in formants[key]:
      vocalTract = getVocalTractParams(file)
      params[key].append(vocalTract)
      xSet.append(vocalTract)
      ySet.append(key)

  xTrain, xTest, yTrain, yTest = train_test_split(xSet, ySet, train_size=0.6, random_state=42)

  phonemes = {}

  coeffs = genetic(xTrain, yTrain)
  print('Coeffs: ', coeffs)

  allCount = 0
  successCount = 0
  for i, test1 in enumerate(xTest):
    minDistance = float('inf')
    minDistanceIndex = -1
    for j, test2 in enumerate(xTest):
      if i != j:
        distance = getDistance(coeffs, test1, test2)
        if (distance < minDistance):
          minDistance = distance
          minDistanceIndex = j
    allCount += 1
    if yTest[i] == yTest[minDistanceIndex]:
      successCount += 1
      print('True for ', yTest[i])
    else:
      print('False for ', yTest[i], yTest[minDistanceIndex])
      
  print('Result: ', successCount/allCount)

  allCount = 0
  successCount = 0
  for i, test1 in enumerate(xTrain):
    minDistance = 999999
    minDistanceIndex = -1
    for j, test2 in enumerate(xTrain):
      if i != j:
        distance = getDistance(coeffs, test1, test2)
        if (distance < minDistance):
          minDistance = distance
          minDistanceIndex = j
    allCount += 1
    if yTrain[i] == yTrain[minDistanceIndex]:
      successCount += 1
      print('True for ', yTrain[i])
    else:
      print('False for ', yTrain[i], yTrain[minDistanceIndex])
      
  print(successCount/allCount)

if len(sys.argv) > 1 and 'preprocess' in str(sys.argv):
  preprocess()

elif len(sys.argv) > 1 and 'train' in str(sys.argv):
  train()
  
elif len(sys.argv) > 2:
  recognize(sys.argv[1], sys.argv[2])
  
else:
  fullCycle()
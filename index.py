from utils.files import loadFormantsFolder, preprocessFiles, loadFormantsPath
from analysis.tract import getVocalTractParams
from analysis.distance import getDistance
from train import train
from recognize import recognize, compare
import sys
from sklearn.model_selection import train_test_split
from collections import Counter
import random

if len(sys.argv) > 1 and 'preprocess' in str(sys.argv):
  preprocessFiles('resources')

elif len(sys.argv) > 1 and 'train' in str(sys.argv):
  train()
  
elif len(sys.argv) > 2:
  compare(sys.argv[1], sys.argv[2])
  
else:
  formants = loadFormantsFolder('resources')

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

  xTrain, xTest, yTrain, yTest = train_test_split(xSet, ySet, train_size=0.8, random_state=42)
  
  print('Train len: ', Counter(yTrain))
  print('Test len: ', Counter(yTest))
  print('All len: ', Counter(ySet))
  print(len(xTrain), len(xTest), len(xSet))
  
  recognize(xTest, yTest, 'Test data: ')
  recognize(xTrain, yTrain, 'Train data: ')
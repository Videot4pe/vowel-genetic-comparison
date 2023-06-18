from utils.files import loadFormantsFolder
from analysis.tract import getVocalTractParams
from ga.genetic import genetic
import sys
from sklearn.model_selection import train_test_split

def train():
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

  phonemes = {}

  for y in yTrain:
    if phonemes.get(y) is None:
      phonemes[y] = 1
    else:
      phonemes[y] += 1

  coeffs = genetic(xTrain, yTrain)
  
  with open("config.txt", "w") as txt_file:
    txt_file.write(' '.join(str(c) for c in coeffs) + '\n')
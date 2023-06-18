def getF1(meanF0, meanF1):
  if meanF0 == 0:
    raise Exception("F0 can't be zero")
  return meanF1 / meanF0

def getF2(meanF0, meanF2):
  if meanF0 == 0:
    raise Exception("F0 can't be zero")
  return meanF2 / meanF0

def getF1F0(meanF0, meanF1):
  return meanF1 - meanF0

def getF2F0(meanF0, meanF2):
  return meanF2 - meanF0

def getF1F2(meanF1, meanF2):
  return meanF1 - meanF2

def getDF1F2(meanF1, meanF2):
  if meanF2 == 0:
    raise Exception("F2 can't be zero")
  return meanF1 / meanF2


def getVocalTractParams(formants):
  if formants[0] == None or formants[1] == None or formants[2] == None:
    raise Exception("All formants must exist")
    
  meanF0 = formants[0]
  meanF1 = formants[1]
  meanF2 = formants[2]
  
  f1 = getF1(meanF0, meanF1)
  f2 = getF2(meanF0, meanF2)
  f1f0 = getF1F0(meanF0, meanF1)
  f2f0 = getF2F0(meanF0, meanF2)
  df1f2 = getDF1F2(meanF1, meanF2)
  f1f2 = getF1F2(meanF1, meanF2)
  return f1, f2, f1f0, f2f0, df1f2, f1f2
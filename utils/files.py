import os
import librosa
from utils.preprocess import preprocess
from analysis.formants import extractFormants
import soundfile as sf

actualEntities = ['а', 'е', 'ё', 'и', 'о', 'у', 'э', 'ю', 'ы', 'я']

def loadFormantsFolder(path):
  entityFiles = {}

  recordsFolders = [f.path for f in os.scandir(path) if f.is_dir()]
  for recordFolder in recordsFolders:
    entityFolders = [f for f in os.scandir(recordFolder) if f.is_dir()]
    for entityFolder in entityFolders:
      entityRecordsFolder = entityFolder.path
      entityName = entityFolder.name
      
      if entityName in actualEntities: 
        entityRecordsPaths = [f.path for f in os.scandir(entityRecordsFolder)]
        entityRecords = []
        for path in entityRecordsPaths:
          if ".wav" in path:
            file, sr = librosa.load(path, sr=None, mono=True, offset=0.0, duration=None)
            if len(file) > 1500:
              formants = extractFormants(path)
              if formants[0] != 0 and formants[1] != 0 and formants[2] != 0:
                entityRecords.append(formants)
          
        if entityFiles.get(entityName) is None:
          entityFiles[entityName] = entityRecords
        else:
          entityFiles[entityName] += entityRecords
  return entityFiles

def loadFormantsPath(path1, path2):
  
  entityRecords = []

  formants1 = extractFormants(path1)
  entityRecords.append(formants1)
  
  formants2 = extractFormants(path2)
  entityRecords.append(formants2)
    
  return entityRecords

def preprocessFiles(path):
  entityFiles = {}

  recordsFolders = [f.path for f in os.scandir(path) if f.is_dir()]
  for recordFolder in recordsFolders:
    entityFolders = [f for f in os.scandir(recordFolder) if f.is_dir()]
    for entityFolder in entityFolders:
      entityRecordsFolder = entityFolder.path
      entityName = entityFolder.name
      
      if entityName in actualEntities:
        entityRecordsPaths = [f.path for f in os.scandir(entityRecordsFolder)]
        entityRecords = []
        for path in entityRecordsPaths:
          if ".wav" in path:
            file, sr = librosa.load(path, sr=None, mono=True, offset=0.0, duration=None)
            if len(file) > 50:
              file, sr = preprocess(file, sr)
              sf.write(path, file, sr, 'PCM_24')
          
  return entityFiles
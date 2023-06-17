import librosa

def saveFile(name, file, sr):
  librosa.output.write_wav(name, file, sr)
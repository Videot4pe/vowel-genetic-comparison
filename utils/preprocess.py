import numpy as np
from scipy.signal import resample
import noisereduce as nr
import librosa

def highFilter(sound):
  return librosa.effects.preemphasis(sound)

def normalize(sound):
  normalizedSound = librosa.util.normalize(sound)
  return normalizedSound

def reduceNoise(sound, sr):
  reducedNoise = nr.reduce_noise(sound, sr, prop_decrease=1.0)
  trimmedAudio, _ = librosa.effects.trim(reducedNoise)
  return trimmedAudio

def trim(sound):
  sound, _ = librosa.effects.trim(sound)
  return sound

def preprocess(sound, sr):
  # Удаление тишины из начала и конца записи
  # sound = trim(sound)
  # Усилить высокочастотные компоненты семпла и уменьшить низкочастотные.
  # sound = highFilter(sound)
  # sound = reduceNoise(sound, sr)
  # Нормализация амплитуды звукового сигнала после изменения высоты тона
  sound = normalize(sound)
  return sound, sr
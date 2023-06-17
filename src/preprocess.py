import numpy as np
from scipy.signal import resample
import noisereduce as nr
import constants
import librosa

def highFilter(sound):
  return librosa.effects.preemphasis(sound)

def normalize(sound):
  normalizedSound = librosa.util.normalize(sound)
  return normalizedSound

def pitch(y, sr):
  y_pitch = librosa.effects.pitch_shift(y=y, sr=sr, n_steps=int(librosa.core.hz_to_midi(constants.HZ_TO_MIDI)), bins_per_octave=12)
  return y_pitch

def reduceNoise(sound, sr):
  reducedNoise = nr.reduce_noise(sound, sr, prop_decrease=constants.PROP_DECREASE)
  trimmedAudio, _ = librosa.effects.trim(reducedNoise)
  return trimmedAudio

def toSampleRate(sound, sr):
  resampled_y = librosa.resample(y=sound, orig_sr=sr, target_sr=constants.BASE_SR)
  return resampled_y, constants.BASE_SR

def trim(sound):
  sound, _ = librosa.effects.trim(sound)
  return sound

def preprocess(sound, sr):
  # Удаление тишины из начала и конца записи
  sound = trim(sound)
  # Приведение звуковых файлов к одному sample rate
  sound, sr = toSampleRate(sound, sr)
  # Усилить высокочастотные компоненты семпла и уменьшить низкочастотные.
  sound = highFilter(sound)
  sound = reduceNoise(sound, sr)
  # Изменение высоты тона
  sound = pitch(sound, sr)
  # Нормализация амплитуды звукового сигнала после изменения высоты тона
  sound = normalize(sound)
  return sound, sr
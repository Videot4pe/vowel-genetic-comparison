import librosa
import constants

def getSpectre(sound):
  spectre = librosa.stft(sound, n_fft=constants.N_FFT, hop_length=constants.HOP_LENGTH)
  return spectre

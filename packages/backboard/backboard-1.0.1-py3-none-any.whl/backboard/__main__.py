from scipy.io import wavfile
import numpy as np
import os
import keyboard
from backboard import keys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT']='1'
import pygame
def speedx(snd_array, factor):
    indices = np.round(np.arange(0, len(snd_array), factor))
    indices = indices[indices < len(snd_array)].astype(int)
    return snd_array[indices]
def stretch(snd_array, factor, window_size, h):
    phase = np.zeros(window_size)
    hanning_window = np.hanning(window_size)
    result = np.zeros(int(len(snd_array) / factor + window_size))
    for i in np.arange(0, len(snd_array) - (window_size + h), h * factor):
        i = int(i)
        a1 = snd_array[i: i + window_size]
        a2 = snd_array[i + h: i + window_size + h]
        s1 = np.fft.fft(hanning_window * a1)
        s2 = np.fft.fft(hanning_window * a2)
        phase = (phase + np.angle(s2 / s1)) % 2 * np.pi
        a2_rephased = np.fft.ifft(np.abs(s2) * np.exp(1j * phase))
        i2 = int(i / factor)
        result[i2: i2 + window_size] += hanning_window * a2_rephased.real
    result = ((2 ** (16 - 4)) * result / result.max())
    return result.astype('int16')
def pitchshift(snd_array, n, window_size = 2 ** 13, h = 2 ** 11):
    factor = 2 ** (1.0 * n / 12.0)
    stretched = stretch(snd_array, 1.0 / factor, window_size, h)
    return speedx(stretched[window_size:], factor)
fps, sound = wavfile.read(__file__.replace('__main__','temp'))
tones = range(-len(keys) // 2, len(keys) // 2)
transposed_sounds = [pitchshift(sound, n) for n in tones]
pygame.mixer.init(fps, -16, 1, 2048)
sounds = map(pygame.sndarray.make_sound, transposed_sounds)
key_sound = dict(zip(keys, sounds))
if __name__ =='__main__':
    while True:
        key = keyboard.read_key()
        if keyboard.KEY_DOWN and key in key_sound.keys(): key_sound[key].play(fade_ms=50)
        if key in key_sound.keys(): key_sound[key].fadeout(50)

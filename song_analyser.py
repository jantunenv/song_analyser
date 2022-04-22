# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 2022
@author: Ville Jantunen
"""
import numpy as np
import pydub
import pandas
import matplotlib.pyplot as plt

def band_bass_filter(fft_freqs, low_limit, high_limit):
    #Return lowest and highest index of fft_freqs array that matches the condition
    indmax = 0
    indmin = -1
    
    for i in range(len(fft_freqs)):
       if(fft_freqs[i] >= low_limit):
           indmin = i
           break
       
    for i in range(len(fft_freqs)):
       if(fft_freqs[i] > high_limit):
           indmax = i - 1
           break

    if(indmin > indmax):
        indmin = indmax
    
    return(indmin, indmax)

def read_mp3(fname):
    audio_data = pydub.AudioSegment.from_mp3(fname)
    audio_as_array = np.array(audio_data.get_array_of_samples())

    #just use left channel
    if(audio_data.channels == 2):
        left_channel = audio_as_array[0::2]
        audio_as_array = left_channel  


    return(audio_as_array, audio_data.frame_rate)


def volume_curve(song_array, f_rate):
    time_array = [i/f_rate for i in range(len(song_array))]
    
    #Rolling average is required
    plt.plot(time_array, pandas.DataFrame(np.abs(song_array)).rolling(f_rate, center=True, min_periods=1).mean().to_numpy())
    plt.show()
    
def fourier_test(song_array, f_rate, sample_position = 20.0, sample_length = 0.1):
    sample = song_array[int(sample_position*f_rate):int(sample_position*f_rate) + int(f_rate*sample_length)]

    fft_data = np.fft.fft(sample)
    fft_freqs = np.fft.fftfreq(len(sample), d=1/f_rate)

    #Remove negative frequencies
    freqs = fft_freqs[:int(len(fft_freqs)/2)]
    amplitudes = np.abs(fft_data)[:int(len(fft_freqs)/2)]
    amplitudes = amplitudes/np.max(amplitudes)

    min_ind, max_ind = band_bass_filter(freqs, 30.0, 1000.0)

    plt.plot(freqs[min_ind:max_ind], amplitudes[min_ind:max_ind])
    plt.xscale('log')
    plt.show()
    
def main():
    fname = "mountain_king.mp3"
    song_array, f_rate = read_mp3(fname)
    #fourier_test(song_array, f_rate, sample_position=20.0, sample_length=0.1)    
    volume_curve(song_array, f_rate)
    

if __name__ == "__main__":
    main()

import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import soundfile as sf
import time
from scipy.io import wavfile
from scipy import signal
from scipy.io.wavfile import write

def delay_effect(x_norm,delay,amplitude,fs):
    delay_samples = round(fs*delay)
    y = np.zeros(len(x_norm))
    zero_padding = np.zeros(delay_samples)
    x_delayed= np.concatenate((zero_padding, x_norm))
    y = x_norm + amplitude * x_delayed[:len(x_norm)]
    return y
    # return amplitude*x_delayed

def echo_effect(x_norm, stages, delay_step, amplitude, fs):
    y = np.zeros(len(x_norm))
    y += x_norm
    delay = round(delay_step*fs)
    zero_padding=np.zeros(delay)
    for stage in range(1, stages+1):
        gain = round(amplitude/stage)   
        # y += delay_effect(x_norm, delay, gain, fs)
        x_delayed = np.concatenate((zero_padding, x_norm))
        y += gain*x_delayed[:len(x_norm)]
    return y

def tremolo_effect(x_norm, depth, rate, sample_rate):
    y = np.zeros(len(x_norm))
    for i in range (len(x_norm)):
        y[i]= x_norm[i]*(1+depth*np.sin(2*np.pi*i*rate/sample_rate))
    return y

def flanger_effect(x_norm, depth, rate, sample_rate, delay_length):
    y = np.zeros(len(x_norm))
    delay_samples = round(delay_length * fs)   
    for i in range(len(x_norm)):
        d = int(delay_samples*(1+np.sin(2*np.pi*i*rate/sample_rate)))
        if d<i:
            y[i]= x_norm[i]+ depth*x_norm[i-d]
        else:
            y[i]=x_norm[i]
    return y

def bit_crusher_effect(x_norm, downsampling, bit_depth):
    # principal controls 1 and 2
    y = np.zeros(round(len(x_norm)/downsampling))
    j = 0
    # 1 downsampling - decimation 
    for i in range (0,len(x_norm),downsampling):
        y[j] = x_norm[i]
        j+=1
    # 2 resolution - quantizer
    max_value = 2**bit_depth
    for j in range (len(y)):
        y[j] = y[j]/max_value  
    return y


def mono_plot(audio_data, fs, title):
    plt.figure()
    t = np.arange(len(audio_data)) / fs
    plt.plot(t, audio_data)
    plt.title(title)
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.show()

def play_sound(signal, sample_rate):
    sd.play(signal, sample_rate)
    sd.wait()


if __name__ == "__main__":
    
    sound_file = 'guitar-clean.wav'
    fs, guitar_audio = wavfile.read(sound_file)
    number_of_samples = len(guitar_audio)
    #print(number_of_samples)

    source_audio_L = guitar_audio[:,0]
    source_audio_R = guitar_audio[:,1]
   
    source_audio_mono = np.array([(ch[0]+ch[1])//2 for ch in guitar_audio], dtype=np.int16)
    #source_audio_mono = np.mean(guitar_audio, axis=0, dtype=np.float32)
    #play_sound(source_audio_mono, fs)
    
    # # Generate .wav file for audio with effect
    # wavfile.write("audio-w-effect.wav", fs, guitar_effect)


#DECIMATION
#FIR filter, Hamming, order 30
#guitar_norm = source_audio_mono.astype(float)/2**15
    play_sound(source_audio_mono,44100)
    decimated_audio = signal.decimate(source_audio_mono, 4, 30, 'fir')
    num_newsamples = len(decimated_audio)
    print(num_newsamples)
    #play_sound(decimated_audio,11025)
    guitar_effect = delay_effect(decimated_audio, 2, 2.0, 11025)
    #guitar_effect = echo_effect(decimated_audio, 3, 0.2 , 1.0, 11025)
    #guitar_effect = tremolo_effect(decimated_audio, 0.5, 0.5, 11025)
    #guitar_effect = flanger_effect(decimated_audio, 0.5, 1.0, 11025, 0.001)
    #guitar_effect = bit_crusher_effect(decimated_audio, 3, 3)
    #guitar_effect = wah_effect(decimated_audio, 11025, 0.01, 2000, 3000, 500)
    #play_sound(guitar_effect,11025)
    guitar_norm = guitar_effect.astype(float)/2**15
    #guitar_norm = guitar_effect/np.max(np.abs(guitar_effect))
    #guitar_norm = decimated_audio.astype(float)/2**15
    # bit crusher has new frequency
    play_sound(guitar_norm, 11025)
    #play_sound(guitar_norm, 3675)
    
# Writing to header file
    f = open("audio_data.txt", "w")
    # f.write("#define NUM_SAMPLES 43155\n\n")
    # f.write("float audio_data[NUM_SAMPLES] = {\n\t")
    for i in range(num_newsamples):
    #          f.write(f"{guitar_norm[i]:.6f},")
    #          if (i + 1) % 5 == 0:
    #              f.write("\n\t")
                 f.write(f"{guitar_norm[i]:.6f}")
                 f.write("\n")
    # f.write("\n};")
    # f.write("\n\n")

# Export samples from CrossCore
    with open("./workspace1/project/Debug/audio_output.txt", "r") as file:
        samples = [float(line.strip()) for line in file]
        cross_audio = np.array(samples)
    play_sound(cross_audio, 11025)

# # Plot Python and CCE version
    plt.figure()
    plt.title("Signali sa efektima")
    plt.plot(guitar_norm)
    plt.plot(cross_audio)
    plt.show()

# # Error signal

    signal_error = np.abs(guitar_norm-cross_audio)
    plt.figure()
    plt.title("Error signal")
    plt.plot(signal_error)
    plt.show()



import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import soundfile as sf
import time
from scipy.io import wavfile
from scipy import signal
from scipy.io.wavfile import write

def delay_effect(x,delay_s,amplitude,sample_rate):
    delay_samples = round(sample_rate*delay_s)
    y = np.zeros(len(x))
    zero_padding = np.zeros(delay_samples)
    x_delayed= np.concatenate((zero_padding, x))
    y = x + amplitude * x_delayed[:len(x)]
    return y


def echo_effect(x, stages, delay_s, amplitude, sample_rate):
    y = np.zeros(len(x))
    y += x
    delay_samples = round(delay_s*sample_rate)
    zero_padding=np.zeros(delay_samples)
    for stage in range(1, stages+1):
        gain = amplitude/stage   
        x_delayed = np.concatenate((zero_padding, x))
        y += gain*x_delayed[:len(x)]
    return y


def tremolo_effect(x, depth, rate, sample_rate):
    y = np.zeros(len(x))
    for i in range (len(x)):
        y[i]= x[i]*(1+depth*np.sin(2*np.pi*i*rate/sample_rate))
    return y


def flanger_effect(x, amplitude, rate, delay_s, sample_rate):
    y = np.zeros(len(x))
    delay_samples = round(delay_s * fs)   
    for i in range(len(x)):
        d = int(delay_samples*(1+np.sin(2*np.pi*i*rate/sample_rate)))
        if d<i:
            y[i]= x[i]+ amplitude*x[i-d]
        else:
            y[i]=x[i]
    return y


# def bitcrusher_effect(x, d_fac, bit_depth):
#     # basic controls 1 and 2
#     y = np.zeros(round(len(x)/d_fac))
#     j = 0
#     # 1 - downsampling 
#     for i in range (0,len(x),d_fac):
#         y[j] = x[i]
#         j+=1
#     # 2 - quantizer
#     max_value = 2**bit_depth
#     for j in range (len(y)):
#         y[j] = np.ceil(max_value* y[j]) * (1/max_value)
#     return y

# # Example of Bit Crusher with LPF
# def bit_crusher_effect2(x_norm, downsampling, bit_depth):
#     niq_rate = 11025/2.0
#     cut_off = 1000
#     coeffs = signal.firwin(100, cut_off/niq_rate, window='hann')
    
#     f = open("./filter.h", "w")
#     f.write("#define NUM_TAPS 200\n\n")
#     f.write("float32_t pm LP_FILTER[NUM_TAPS] = {\n\t")
#     for i in range(coeffs.size):
#         f.write(f"{coeffs[i]:.6f},")
#         if (i+1) % 5 == 0:
#             f.write("\n\t")
#     f.write("\n};")
#     f.write("\n\n")

#     x_filtered = np.zeros(len(x_norm))
#     plt.figure()
#     plt.title("BEFORE LPF")
#     plt.plot(x_norm)
#     plt.show()
#     y = np.zeros(round(len(x_norm)/downsampling))
#     x_filtered = signal.lfilter(coeffs, 1.0, x_norm)
#     plt.figure()
#     plt.title("AFTER LPF")
#     plt.plot(x_filtered)
#     plt.show()
#     # principal controls 1 and 2
#     # y = np.zeros(round(len(x_norm)/downsampling))
#     j = 0
#     # 1 downsampling - decimation 
#     for i in range (0,len(x_norm),downsampling):
#         y[j] = x_filtered[i]
#         j+=1
#     # 2 resolution - quantizer
#     max_value = 2**bit_depth
#     for j in range (len(y)):
#        #y[j] = y[j]/max_value  
#        y[j] = np.ceil(max_value* y[j]) * (1/max_value)
#     return y

def read_from_file(path):
    with open(path, "r") as file:
        samples = [float(line.strip()) for line in file]
    cross_audio = np.array(samples)
    return cross_audio


def write_to_file(norm_audio, length):
    f = open("audio_data.h", "w")
    f.write("#define NUM_SAMPLES 41567\n\n")
    f.write("const float32_t audio_data[NUM_SAMPLES] = {\n\t")
    for i in range(length):
             f.write(f"{norm_audio[i]:.6f},")
             if (i + 1) % 5 == 0:
                 f.write("\n\t")
    f.write("\n};")
    f.write("\n\n")


def mono_plot(audio_data, fs, title):
    plt.figure()
    # for Bit Crusher, divide by 3675
    t = np.arange(len(audio_data)) / 11025
    plt.plot(t, audio_data)
    plt.title(title)
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.show()
    

def error_signal(diff, title):
    # for Bit Crusher, divide by 3675
    t = np.arange(len(diff)) / 11025
    plt.plot(t, diff)
    plt.title(title)
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.show()

def mono_decimated_plot(mono_norm, decimated_mono_norm):
    plt.figure()
    plt.title("Mono signal before and after decimation (normalized amplitude)")
    plt.xlabel("Samples")
    plt.subplot(2, 1, 1)
    plt.plot(mono_norm)
    plt.subplot(2, 1, 2)
    plt.ylim(-0.75, 0.75) 
    plt.yticks(np.arange(-0.90, 0.75, 0.55))
    plt.plot(decimated_mono_norm)
    plt.show()
    

def play_sound(signal, sample_rate):
    sd.play(signal, sample_rate)
    sd.wait()


if __name__ == "__main__":

    # Import stereo signal
    sound_file = 'guitar-clean.wav'
    fs, guitar_audio = wavfile.read(sound_file)
    number_of_samples = len(guitar_audio)
    # duration = guitar_audio.shape[0] / fs
    # print(number_of_samples)
    
    # Check if channels look the same
    
    t = np.arange(len(guitar_audio)) / fs
    plt.figure()
    plt.title("Stereo signal")
    plt.xlabel("Time [s]")
    plt.subplot(2, 1, 1)
    plt.ylim(-19000, 19000)
    plt.plot(t, guitar_audio[:,1])
    plt.ylabel("Right Channel")
    plt.subplot(2, 1, 2)
    plt.ylim(-19000, 19000)
    plt.plot(t, guitar_audio[:,0])
    plt.ylabel("Left Channel")
    plt.show()
    
    # Divide channels and get mono signal
    source_audio_L = guitar_audio[:,0]
    source_audio_R = guitar_audio[:,1]
    source_audio_mono = np.array(source_audio_L+source_audio_R//2, dtype=np.int16)
    #wavfile.write("guitar-mono.wav", fs, source_audio_mono)
    source_mono_norm = source_audio_mono.astype(float)/2**15
    ########################################################################
    # DECIMATION for factor 4, new frequency is 11 025 Hz
    # FIR filter, Hann window
    ########################################################################
    # plt.figure()
    # plt.title("BEFORE LPF")
    # plt.plot(source_audio_mono)
    # plt.show()
    niq_rate = fs/2.0
    cut_off = 2000
    coeffs = signal.firwin(500, cut_off/niq_rate, window='hann')
    x_filtered = np.zeros(len(source_audio_mono))
    x_filtered = signal.lfilter(coeffs, 1.0, source_audio_mono)
    decimated_audio = np.zeros(round(len(x_filtered)/4))
    decimated_audio = signal.decimate(x_filtered,4)
    norm_dec= decimated_audio.astype(float)/2**15 
    # plt.title("AFTER LPF and DECIMATION")
    # plt.plot(norm_dec)
    # plt.show()
    #######################################################################
    # Write decimated and normalized samples of mono signal to file
    ########################################################################
    new_len = len(norm_dec)
    print(new_len)
    write_to_file(norm_dec, new_len)
    mono_decimated_plot(source_mono_norm, norm_dec)
    ########################################################################
    #EFFECTS
    #########################################################################
     ## DELAY
  
    guitar_w_delay = delay_effect(norm_dec, 0.5, 0.5, 11025)
    wavfile.write("audio-py-delay.wav", 11025, guitar_w_delay)
    mono_plot(guitar_w_delay, "Delay in Python")
    guitar_w_delay_c= read_from_file("./audio_w_delay.txt")
    mono_plot(guitar_w_delay, "Delay in C")
    wavfile.write("audio-c-delay.wav", 11025, guitar_w_delay_c)
    # play_sound(guitar_w_delay, 11025)
    # time.sleep(2)
    # play_sound(guitar_w_delay_c, 11025)
    difference = np.abs(guitar_w_delay- guitar_w_delay_c)
    error_signal(difference, "Delay error signal")
    
    ## ECHO
    
    guitar_w_echo = echo_effect(norm_dec, 3, 0.5 , 1.0, 11025)
    wavfile.write("audio-py-echo.wav", 11025, guitar_w_echo)
    mono_plot(guitar_w_echo, "Echo in Python")
    guitar_w_echo_c= read_from_file("./audio_w_echo.txt")
    mono_plot(guitar_w_echo_c, "Echo in C")
    wavfile.write("audio-c-echo.wav", 11025, guitar_w_echo_c)
    # play_sound(guitar_w_echo, 11025)
    # time.sleep(2)
    # play_sound(guitar_w_echo_c, 11025)
    difference = np.abs(guitar_w_echo - guitar_w_echo_c)
    error_signal(difference, "Echo error signal")
    

    ## TREMOLO
    
    guitar_w_tremolo = tremolo_effect(norm_dec, 0.7, 5.0, 11025)
    wavfile.write("audio-py-tremolo.wav", 11025, guitar_w_tremolo)
    mono_plot(guitar_w_tremolo, "Tremolo in Python")
    t = np.arange(len(norm_dec)) / 11025
    plt.figure()
    plt.title("Mono before vs. mono with tremolo effect")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.plot(t, norm_dec)
    plt.plot(t, guitar_w_tremolo)
    plt.show()
    guitar_w_tremolo_c= read_from_file("./audio_w_tremolo.txt")
    mono_plot(guitar_w_tremolo, "Tremolo in C")
    wavfile.write("audio-c-tremolo.wav", 11025, guitar_w_tremolo_c)
    # play_sound(guitar_w_tremolo, 11025)
    # time.sleep(2)
    # play_sound(guitar_w_tremolo_c, 11025)
    difference = np.abs(guitar_w_tremolo - guitar_w_tremolo_c)
    error_signal(difference, "Tremolo error signal")

    
   ## FLANGER
   
    guitar_w_flanger = flanger_effect(norm_dec, 0.8, 2.0, 11025, 0.001)
    wavfile.write("audio-py-flanger.wav", 11025, guitar_w_flanger)
    mono_plot(guitar_w_flanger, "Flanger in Python")
    t = np.arange(len(norm_dec)) / 11025
    plt.figure()
    plt.title("Mono before vs. mono with flanger effect")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.plot(t, norm_dec)
    plt.plot(t, guitar_w_flanger)
    plt.show()
    guitar_w_flanger_c= read_from_file("./audio_w_flanger.txt")
    wavfile.write("audio-c-flanger.wav", 11025, guitar_w_flanger_c)
    mono_plot(guitar_w_flanger_c, "Flanger in C")
    wavfile.write("audio-c-flanger.wav", 11025, guitar_w_flanger_c)
    # play_sound(guitar_w_tremolo, 11025)
    # time.sleep(2)
    # play_sound(guitar_w_tremolo_c, 11025)
    difference = np.abs(guitar_w_flanger - guitar_w_flanger_c)
    error_signal(difference, "Flanger error signal")
    
    # BITCRUSHER
    
    guitar_w_bitcrusher = bit_crusher_effect(norm_dec, 3, 3)
    wavfile.write("audio-py-bitcrusher.wav", 3675, guitar_w_bitcrusher)
    mono_plot(guitar_w_bitcrusher, "Bitcrusher in Python")
    guitar_w_bitcrusher_c= read_from_file("./audio_w_bitcrusher.txt")
    mono_plot(guitar_w_bitcrusher_c, "Bitcrusher in C")
    wavfile.write("audio-c-bitcrusher.wav", 3675, guitar_w_bitcrusher_c)
    # play_sound(guitar_w_bitcrusher, 3675)
    # time.sleep(2)
    # play_sound(guitar_w_bitcrusher_c, 3675)
    t = np.arange(len(guitar_w_bitcrusher)) / 3675
    plt.figure()
    plt.title("Bitcrusher Python vs C")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.plot(t, guitar_w_bitcrusher)
    plt.plot(t, guitar_w_bitcrusher_c)
    plt.show()
    difference = np.abs(guitar_w_bitcrusher - guitar_w_bitcrusher_c)
    error_signal(difference, "Bitcrusher error signal")
    #########################################################################
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
   # y_norm = y.astype(float)/2**15
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
    #y_norm = y.astype(float)/2**15
    return y


def tremolo_effect(x, depth, rate, sample_rate):
    y = np.zeros(len(x))
    for i in range (len(x)):
        y[i]= x[i]*(1+depth*np.sin(2*np.pi*i*rate/sample_rate))
    #y_norm = y.astype(float)/2**15 
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
    #y_norm = y.astype(float)/2**15 
    return y


def bitcrusher_effect(x, d_fac, bit_depth):
    # basic controls 1 and 2
    y = np.zeros(round(len(x)/d_fac))
    j = 0
    # 1 - downsampling 
    for i in range (0,len(x),d_fac):
        y[j] = x[i]
        j+=1
    # 2 - quantizer
    max_value = 2**bit_depth
    for j in range (len(y)):
        y[j] = np.ceil(max_value* y[j]) * (1/max_value)
    #y_norm = y.astype(float)/2**15 
    return y

def read_from_file(path):
    with open(path, "r") as file:
        samples = [float(line.strip()) for line in file]
    cross_audio = np.array(samples)
    return cross_audio


def write_to_file(norm_audio, length):
    f = open("audio_data.h", "w")
    f.write("#define NUM_SAMPLES 41567\n\n")
    f.write("float audio_data[NUM_SAMPLES] = {\n\t")
    for i in range(length):
             f.write(f"{norm_audio[i]:.6f},")
             if (i + 1) % 5 == 0:
                 f.write("\n\t")
    f.write("\n};")
    f.write("\n\n")


def mono_plot(audio_data, fs, title):
    plt.figure()
    t = np.arange(len(audio_data)) / fs
    plt.plot(t, audio_data)
    plt.title(title)
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.show()


def error_signal(py_output, cce_output):
    plt.figure()
    plt.title("Error signal")
    signal_error = np.abs(py_output-cce_output)
    # manipulate with x-axis
    plt.plot(signal_error)
    plt.show()


def py_c_plot(py_output, cce_output):
    plt.figure()
    plt.title("Signals with effect")
    plt.plot(py_output)
    plt.plot(cce_output)
    plt.show()


def play_sound(signal, sample_rate):
    sd.play(signal, sample_rate)
    sd.wait()


if __name__ == "__main__":

    # Import stereo signal
    sound_file = 'guitar-clean.wav'
    fs, guitar_audio = wavfile.read(sound_file)
    number_of_samples = len(guitar_audio)
    # print(number_of_samples)
    # Divide channels and get mono signal
    source_audio_L = guitar_audio[:,0]
    source_audio_R = guitar_audio[:,1]
    source_audio_mono = np.array(source_audio_L+source_audio_R//2, dtype=np.int16)
    # Plot and play mono signal
    mono_plot(source_audio_mono, fs, "Original signal")
    play_sound(source_audio_mono, fs)
    ########################################################################
    # DECIMATION for factor 4, new frequency is 11 025 Hz
    # FIR filter, Hamming in 30 points
    ########################################################################
    decimated_audio = signal.decimate(source_audio_mono, 4, None, ftype='fir')
    num_newsamples = len(decimated_audio)
    # Write normalized samples to file
    guitar_norm = decimated_audio.astype(float)/2**15
    write_to_file(decimated_audio, num_newsamples)
    #print(num_newsamples)
    #play_sound(decimated_audio,11025)
    ########################################################################
    #EFFECTS
    #########################################################################
    py_delay = delay_effect(decimated_audio, 2, 2.0, 11025)
    c_delay = read_from_file("./workspace/project/Debug/audio_w_delay.txt")
    wavfile.write("audio-w-bitcrusher.wav", fs, py_delay)
    play_sound(py_delay, 11025)
    time.sleep(2)
    play_sound(c_delay, 11025)
    py_c_plot(py_delay,c_delay)
    error_signal(py_delay, c_delay)
    ##########################################################################
    py_echo = echo_effect(decimated_audio, 3, 0.2 , 1.0, 11025)
    c_echo = read_from_file("./workspace/project/Debug/audio_w_echo.txt")
    wavfile.write("audio-w-echo.wav", fs, py_echo)
    play_sound(py_echo, 11025)
    time.sleep(2)
    play_sound(c_echo, 11025)
    py_c_plot(py_echo, c_echo)
    error_signal(py_echo, c_echo)
    #########################################################################
    py_tremolo = tremolo_effect(decimated_audio, 0.7, 5.0, 11025)
    c_tremolo = read_from_file("./workspace/project/Debug/audio_w_tremolo.txt")
    wavfile.write("audio-w-tremolo.wav", fs, py_tremolo)
    play_sound(py_tremolo, 11025)
    time.sleep(2)
    play_sound(c_tremolo, 11025)
    py_c_plot(py_tremolo, c_tremolo)
    error_signal(py_tremolo, c_tremolo)
    #########################################################################
    py_flanger = flanger_effect(decimated_audio, 0.9, 1.0, 0.001, 11025)
    c_flanger = read_from_file("./workspace/project/Debug/audio_w_flanger.txt")
    wavfile.write("audio-w-flanger.wav", fs, py_flanger)
    play_sound(py_flanger, 11025)
    time.sleep(2)
    play_sound(c_flanger, 11025)
    py_c_plot(py_flanger,c_flanger)
    error_signal(py_flanger, c_flanger)
    #########################################################################
    py_bitcrusher = bitcrusher_effect(decimated_audio, 3, 3, 11025)
    c_bitcrusher = read_from_file("./workspace/project/Debug/audio_w_bitcrusher.txt")
    wavfile.write("audio-w-bitcrusher.wav", fs, py_bitcrusher)
    play_sound(py_bitcrusher, 3675)
    time.sleep(2)
    play_sound(c_bitcrusher, 3675)
    py_c_plot(py_bitcrusher, c_bitcrusher)
    error_signal(py_bitcrusher, c_bitcrusher)
    #########################################################################
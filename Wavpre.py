import numpy as np
import librosa, os, os.path
from glob import glob
import scipy.io as sio
import matplotlib.pyplot as plt
import sounddevice as sd
import noisereduce as nr
import soundfile as sf
import wave, math, array

## 음원 모음 결로 
## au_dir = /home/data/user
def Audio_add(au_dir):
    audio_dir = glob(au_dir+'/*.wav')
    for i in audio_dir:
        name = os.path.basename(i)
        with open(au_dir+'/au_list.txt','a', encoding='utf-8') as f:
            f.write("file '"+name+"'\n")
    os.system('ffmpeg -f concat i '+au_dir+'/au_list.txt -c copy '+au_dir+'/add_audio.wav')


def Band_gap_filter(audio, highpass, lowpass):
    os.system('ffmpeg -i %s -af "highpass=%s, lowpass=%s" ./ft_output.wav'%(audio, highpass, lowpass))


def Denoiser_filter(audio, sr, out_dir):
    rate, data = sio.wavefile.read(audio)
    data = data / int(sr)
    noisy_part2 = data[10000:15000]
    reduced_noise = nr.reduce_noise(audio_clip=data, noise_clip=noisy_part2,verbose=True)
    ## 그림 그려지는 것 지우기 필요
    name = os.path.basename(audio)
    sf.write(out_dir+'/de_'+name+'.wav',reduced_noise, rate, format='WAV', endian='LITTLE', subtype='PCM_16')


def cal_adjusted_rms(clean_rms, snr):
    a = float(snr) / 20
    noise_rms = clean_rms / (10**a)
    return noise_rms

def cal_amp(wf):
    buffer = wf.readframs(wf.getframes())
    amptitude = (np.frombuffer(buffer, dtype='int16')).astype(np.float64)
    return amptitude

def cal_rms(amp):
    return np.sqrt(np.mean(np.square(amp), axis=-1))

## 음원 데시벨 맞추기 
def audio_amp_change(stand_file, input_file, export_dir):
    stand_file = stand_file
    input_file = input_file
    export_dir = export_dir
    f_name = os.path.basename(input_file)
    name = f_name.split('.')[0]
    try:
        name = name.split('c')[1]
    except:
        name = name.split('d')[1]
    name = name.zfill(4)
    export_file='%s/m_%s.wav'%(export_dir, name)
    framerate = 44100
    stand_amp = librosa.load(stand_file, sr=framerate)
    input_amp = librosa.load(input_file, sr=framerate)
    stand_rms = cal_rms(stand_amp[0])
    input_rms = cal_rms(input_amp[0])
    snr = 0
    adjusted_input_rms = cal_adjusted_rms(stand_rms, snr)
    adjusted_input_amp = input_amp[0] * (adjusted_input_rms / input_rms)
    sf.write(export_file, adjusted_input_amp, samplerate=framerate, format='wav')

def save_waveform(output_path, params, amp):
    output_file = wave.Wave_write(output_path)
    output_file.setparams(params) #nchannels, sampwidth, framerate, nframes, comptype, compname
    output_file.writeframes(array.array('h', amp.astype(np.int16)).tobytes() )
    output_file.close()

##
def Audio_mixed(audio,path,mixed_audio):
    #ori_file = 'C:/Users/dataedu09/Documents/이동진/과제/데이터바우처/이코노아이/남자/taco_result/bn_output.wav'
    #path = 'C:/Users/dataedu09/Documents/이동진'
    #mixed_file = '%s/bensound.wav'%path
    ori_file = audio
    path = path
    mixed_file = mixed_audio
    ori_wav = wave.open(ori_file, "r")
    mixed_wav = wave.open(mixed_file, "r")
    ori_amp = cal_amp(ori_wav)
    mixed_amp = cal_amp(mixed_wav)
    for i in range(math.ceil(len(ori_amp)/len(mixed_amp))):
        mixed_amp = np.append(mixed_amp,mixed_amp, axis=0)
    ori_rms = cal_rms(ori_amp)
    start= 0
    divided_noise_amp = mixed_amp[start: start + len(ori_amp)]
    noise_rms = cal_rms(divided_noise_amp)
    snr = 20
    adjusted_noise_rms = cal_adjusted_rms(ori_rms, snr)
    adjusted_noise_amp = divided_noise_amp * (adjusted_noise_rms / noise_rms)
    mixed_amp = (ori_amp + adjusted_noise_amp)
    max_int16 = np.iinfo(np.int16).max
    min_int16 = np.iinfo(np.int16).min
    if mixed_amp.max(axis=0) > max_int16 or mixed_amp.min(axis=0) < min_int16:
        if mixed_amp.max(axis=0) >= abs(mixed_amp.min(axis=0)): 
            reduction_rate = max_int16 / mixed_amp.max(axis=0)
        else :
            reduction_rate = min_int16 / mixed_amp.min(axis=0)
        mixed_amp = mixed_amp * (reduction_rate)
        clean_amp = ori_amp * (reduction_rate)

    save_waveform(path+'/mixed_output.wav', clean_wav.getparams(), mixed_amp)



import os, glob, os.path, shutil
import librosa, wave
import scipy.io as sio
import scipy.io.wavfile
import re, copy, math, array
import pandas as pd
import soundfile as sf
from synthesizer import Synthesizer
import pymysql
from word_nomalize import  korean_count
import numpy as np
import tensorflow as tf
import nltk
#nltk.download('punkt')
synthesizer = Synthesizer()

def cal_adjusted_rms(clean_rms, snr):
    a = float(snr) / 20
    noise_rms = clean_rms / (10**a)
    return noise_rms

def cal_amp(wf):
    buffer = wf.readframes(wf.getnframes())
    # The dtype depends on the value of pulse-code modulation. The int16 is set for 16-bit PCM.
    amptitude = (np.frombuffer(buffer, dtype="int16")).astype(np.float64)
    return amptitude

def cal_rms(amp):
    return np.sqrt(np.mean(np.square(amp), axis=-1))

def save_waveform(output_path, params, amp):
    output_file = wave.Wave_write(output_path)
    output_file.setparams(params) #nchannels, sampwidth, framerate, nframes, comptype, compname
    output_file.writeframes(array.array('h', amp.astype(np.int16)).tobytes() )
    output_file.close()


def mix_audio(audio,num_op, path):
    bgm = '/data/training_model/Tacotron2-Wavenet-Korean-TTS/bgm/%s.wav'%num_op
    name = os.path.basename(audio)
    au_wav = wave.open(audio,'r')
    bgm_wav = wave.open(bgm,'r')
    au_amp = cal_amp(au_wav)
    bgm_amp = cal_amp(bgm_wav)
    for i in range(math.ceil(len(au_amp)/len(bgm_amp))):
        bgm_amp = np.append(bgm_amp, bgm_amp, axis=0)
    au_rms = cal_rms(au_amp)
    mix_bgm = bgm_amp[0:len(au_amp)]
    bgm_rms = cal_rms(mix_bgm)

    snr = 20
    adj_bgm_rms = cal_adjusted_rms(au_rms, snr)
    adj_bgm_amp = mix_bgm * (adj_bgm_rms/bgm_rms)
    mixed_amp = (au_amp + adj_bgm_amp)

    max_int16 = np.iinfo(np.int16).max
    min_int16 = np.iinfo(np.int16).min
    if mixed_amp.max(axis=0) > max_int16 or mixed_amp.min(axis=0) < min_int16:
        if mixed_amp.max(axis=0) >= abs(mixed_amp.min(axis=0)):
            reduction_rate = max_int16 / mixed_amp.max(axis=0)
        else :
            reduction_rate = min_int16 / mixed_amp.min(axis=0)
        mixed_amp = mixed_amp * (reduction_rate)
        au_amp = au_amp * (reduction_rate)
    
    save_waveform('%s/%s'%(path, name), au_wav.getparams(), mixed_amp)
    print(path)
    print(name)
    return '%s/%s'%(path, name)

def silence_detect(audio):
    from pydub import AudioSegment,silence
    sil = silence.detect_silence(AudioSegment.from_wav(audio), min_silence_len=1000, silence_thresh =-50)
    if not sil:
        sil = silence.detect_silence(AudioSegment.from_wav(audio), min_silence_len=700, silence_thresh =-50)
    if not sil:
        sil = silence.detect_silence(AudioSegment.from_wav(audio), min_silence_len=700, silence_thresh =-30)
    if not sil:
        sil = silence.detect_silence(AudioSegment.from_wav(audio), min_silence_len=400, silence_thresh =-40)
    print(sil)
    return sil[0][0]*0.001 +0.15

def tts_process(idx, texts, speaker,synthesizer):
    tf.reset_default_graph() 
    
    output='/data/training_model/Tacotron2-Wavenet-Korean-TTS/logdir-tacotron2/%s'%idx
    os.makedirs(output,exist_ok=True)
    if speaker == '1' :
        ## 남자
        synthesizer.load(checkpoint_path='logdir-tacotron2/lee_2020-10-30',num_speakers=1, inference_prenet_dropout=False)
    if speaker == '2':
        ## 여자
        synthesizer.load(checkpoint_path='logdir-tacotron2/kss_2020-09-16_13-55-59',num_speakers=1, inference_prenet_dropout=False)

    texts = texts.split('\n')
    for i in texts:
        count = korean_count(i)
        pad = 110 - count -2
        pad = pad*'-'
        print(i)
        if count <100:
            i = i.split('-')[0]
            p_i ='%s%s%s\n'%(i,pad,i[:2])
            audio = synthesizer.synthesize(texts=[p_i],base_path=output, speaker_ids=[0],attention_trim=True)[0]
            tmp = silence_detect(audio)
            n_name = os.path.basename(audio)
            print(n_name)
            os.system('ffmpeg -y -i %s -ss 0 -t %s %s/%s'%(audio, tmp, output,n_name))

        else:
            audio = synthesizer.synthesize(texts=[i],base_path=output,speaker_ids=[0],attention_trim=True)[0]

    #os.remove(text_file)
    audio_dir = glob.glob(output+'/*.wav')
    audio_dir.sort()
    for j,audio in enumerate(audio_dir):
        name = os.path.basename(audio)
        with open(output+'/file_list.txt','a',encoding='utf-8') as f:
            f.write("file '"+name+"'\n")
            f.write("file 'sil.wav'\n")
    shutil.copy('/data/training_model/Tacotron2-Wavenet-Korean-TTS/sil.wav', '/%s/'%output)
    num_op='1'
    os.system('ffmpeg -f concat -i %s/file_list.txt -c copy %s/%s.wav'%(output, output, idx))
    fin_output='/data/training_model/Tacotron2-Wavenet-Korean-TTS/logdir-tacotron2/output'
    os.makedirs(fin_output, exist_ok=True)
    print('------start mix----------')
    audio_dir = mix_audio(audio='%s/%s.wav'%(output, idx), num_op=num_op, path= fin_output)
    print(audio_dir)
    print('-----------out mix----------')
    #shutil.rmtree(r'%s'%output)

#############  DB   ##############

con = pymysql.connect(host='220.119.175.200', user='dataedu', password='dataedu!1', db='econoi')
curs = con.cursor()
curs.execute("SELECT n_idx, split_contents, TTS_YN  FROM news_title WHERE TTS_YN = 'N' and split_contents <> '' ORDER BY n_idx DESC")
row = curs.fetchall()
data=pd.DataFrame(data=row)
data = data.rename({0:'n_idx',1:'split_contents',2:'TTS'},axis='columns')

curs.close()
con = pymysql.connect(host='220.119.175.200', user='dataedu', password='dataedu!1', db='econoi')
for j,i in enumerate(data['split_contents']):
    tts_process(data['n_idx'][j],i,"2",synthesizer)
    curs = con.cursor()
    audio_list = glob.glob('/data/training_model/Tacotron2-Wavenet-Korean-TTS/logdir-tacotron2/output/*.wav')
    a_tmp=[]
    for a in audio_list:
        name = os.path.basename(a)
        name = name.split('.')[0]
        a_tmp.append(name)
    if str(data['n_idx'][j]) in a_tmp:
        tts='Y'
        state='A'
        audio=str(data['n_idx'][j])+'.wav'
    else:
        tts='N'
        state='R'
        audio='Null'
    curs.execute("UPDATE news_title SET TTS_YN=%s, state=%s,  audio=%s WHERE n_idx=%s",(tts, state, audio, str(data['n_idx'][j])))
    con.commit()    
curs.close()
con.cloes()


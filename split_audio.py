## import 
import librosa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import torch
import torchaudio
import os, os.path, glob

import IPython.display as ipd
import librosa.display
import soundfile as sf
import pymysql

#경로
stdir1 = '/data'
stdir2 = '/data'
audio_dir = glob.glob('%s/*.'%stdir1)
text_dir = glob.glob('%s/*.ctm'%stdir2)

# database connet
con = pymysql.connect(host='127.0.0.1',user='dataedu',password='dataedu!1', db='mysql',charset='utf8')
cursor = con.cursor()

# cursor.execute("select       from       ")
# row = cursor.fetchall()


# 음성파일 일기
for i in audio_dir:
    fname = os.path.basename(i)
    name = re.sub('.wav','',fname)
    wav_dir = './%s/youtube%s.wav'%(stdir1,name)
    # mp4일 경우 비트수 변경
    os.system('ffmpeg -i %s -acodec flac -bits_per_raw_sample 8 -ar 16000 %s'%(i, wav_dir))
    y, sr = librosa.load('%s'%wav_dir, sr = 16000)
#   대본 찾기
    df = pd.read_csv(str(stdir2)+'%s.ctm'%name, encoding='utf-8', header=None)
    df['sec'] = df[0].apply(lambda x : x.split(' ')[2])
    df['plus'] = df[0].apply(lambda x : x.split(' ')[3])
    df['plus'] = df['plus'].astype(float)
    df['sec'] = df['sec'].astype(float)
    df['time'] = df['sec']+df['plus']
    df['index'] = df['time'].apply(lambda x : int(x * 16000))
    df['text'] = df[0].apply(lambda x : x.split(' ')[4])
    num = df.loc[df['text'].apply(lambda x : x.startswith('니다',x.find('니다')))]
    # 저장
    a = num.index
    for j,k in enumerate (a):
        if j+1 == num['index'].shape[0]:
            pass
        else:
            #  음성파일 
            first=int(num['index'].iloc[j])
            end = int(num['index'].iloc[j+1])
            # 텍스트
            s=(j+1)
            e=a[i+1]
            words = []
            if j == 0:
                # 음원
                save_dir = ['']
                data = y[0:first]
                librosa.output.write_wav(str(save_dir)+'./%s.wav'%j+1, data, sr)
                # 텍스트
                t_save_dir =['']
                tmp = df['text'].iloc[0:s+1]
                for word in tmp:
                    words.append(word)
                tmp_2 = ' '.join(words)
                with open(str(t_save_dir)+'./%s.text'%j+1,'w') as f:
                    f.write(tmp_2)
            else:
                # 음원
                data = y[first:end]
                librosa.output.write_wav(str(save_dir)+'./%s.wav'%j+1, data, sr)
                # 텍스트
                tmp = df['text'].iloc[s:e+1]
                for word in tmp:
                    words.append(word)
                tmp_2 = ' '.join(words)
                with open(str(t_save_dir)'./%s.text'%j+1,'w') as f:
                    f.write(tmp_2)
    # 대본파일 저장

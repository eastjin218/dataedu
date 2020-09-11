import webvtt, sys, re, glob, os, os.path
import pandas as pd
import soundfile as sf
import librosa
import numpy as np


vtt_file_fold = sys.argv[1]
audio_file_fold = sys.argv[2]
vtt_file_name = glob.glob('%s/*.vtt'%vtt_file_fold)

for num,vtt in enumerate(vtt_file_name):
    print(vtt)
    fname = os.path.basename(vtt)
    name = re.sub('.vtt','',fname)
    df = pd.read_csv('%s'%vtt, encoding = 'utf-8',sep='delimiter',header=None)
    df.drop([0,1,2],inplace = True)
    df = df.reset_index()
    count = 0
    drop = 0
    for j,i in enumerate(df[0]):
        if i.startswith('00:'):
            drop +=1
            if drop ==2:
                df.drop(j-1, inplace =True)
                drop=0
            count=0
        else:
            count +=1
            if count ==2:
                df[0].loc[j-1] = df[0].loc[j-1] +' '+ df[0].loc[j]
                df.drop(j, inplace =True)
                count=0
            drop =0
    tmp = df[0].reset_index()
    df2 = tmp.reset_index()
    df2['clf'] = df2['level_0'].apply(lambda x :x%2)
    df3 = pd.DataFrame(data =df2.loc[df2['clf'] == 1])
    df3.rename(columns={0:"text", 'level_0':'num'}, inplace = True)
    df3.reset_index(inplace = True)
    df4 = pd.DataFrame(data =df2.loc[df2['clf'] == 0])
    df4.rename(columns={0:"time", 'level_0':'num'}, inplace = True)
    df4.reset_index(inplace = True)
    df5= pd.concat([df3, df4], axis =1)
    df6 = df5[['time', 'text']]
    df6['time_f'] = df6['time'].apply(lambda x  : x.split('-->')[0])
    df6['time_e'] = df6['time'].apply(lambda x  : x.split('-->')[1])
    df6['sec_f'] = df6['time_f'].apply(lambda x  :float(x.split(':')[2]))
    df6['min_f'] = df6['time_f'].apply(lambda x  :float(x.split(':')[1])*60)
    df6['time_f_t'] = ((df6['sec_f'] + df6['min_f'])*16000).astype(int)
    df6['sec_e'] = df6['time_e'].apply(lambda x  :float(x.split(':')[2]))
    df6['min_e'] = df6['time_e'].apply(lambda x  :float(x.split(':')[1])*60)
    df6['time_e_t'] = ((df6['sec_e'] + df6['min_e'])*16000).astype(int)
    df= df6[['text','time_f_t','time_e_t','time_f','time_e']]
    
    audio = '%s%s.mp4'%(audio_file_fold,name)
    if os.path.isdir(audio_file_fold+"excel_flac"):
        pass
    else:
        os.mkdir(audio_file_fold +"excel_flac")
    flac_dir='%sexcel_flac'%audio_file_fold
    os.system("ffmpeg -i " + audio + " -acodec pcm_s16le -ac 1 -ar 16000 " + name+".wav")
    os.system("ffmpeg -i " + name +".wav -c:a flac "+flac_dir+"/"+name+".flac")
    os.remove(name+".wav")
    y, sr = librosa.load(flac_dir+"/"+name+".flac", sr = 16000)
  
    for i in df.index:
        count = str(0+num)
        if os.path.isdir(audio_file_fold + count):
            pass
        else:
            os.mkdir(audio_file_fold + count)
        data = y[df['time_f_t'].iloc[i]:df['time_e_t'].iloc[i]]
        tmp = str(i)
        split_name = tmp.zfill(4) 
        sf.write(audio_file_fold + count+"/"+count+"_003_"+split_name+".flac", data, samplerate=sr, format='flac')
        with open(audio_file_fold + count+"/"+count+"_003.trans.txt" ,'a', encoding ='utf-8') as f:
            tmp = re.sub("/|o/|b/|n/|u/|[-=+,#/\?;:^$.@*\"※~&%ㆍ!』\\‘|\[\]\<\>`\'…》]",'',df['text'].iloc[i])
            text = re.sub('\)|\(', '', tmp)
            f.write(count+"_003_"+split_name+" "+text+"\n")

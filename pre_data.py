import os.path, glob, os
import re 
import wave
import subprocess
import random

start_point = 'utube_excel'
dir1 = glob.glob('./%s/*'%start_point)
dir2 =[]
for i in dir1:
    dir2.extend(glob.glob('%s/*'%i)) 


# AUDIO_INFO 만들기
name_list= ['Aaron', 'Abel', 'Abigail', 'Abraham', 'Ace', 'Ada', 'Adam', 'Adela', 'Adelio', 'Adolph', 'Adonis', 'Adora', 'Agatha', 'Aggie']
with open( './AUDIO_INFO', 'w', encoding='utf-8') as f:
    f.write('SPEAKERID|NAME|SEX|SCRIPTID|DATASET\n')
for i in dir2:
    tmp_i = re.sub('\./','',i)
#     tmp = tmp_i.split('/')
    tmp = tmp_i.split('\\')
    choice_name = random.choice(name_list)
#     print('%s|%s|f|%s|%s\n'%(tmp[2],choice_name,tmp[1],tmp[0]))
    with open('./AUDIO_INFO','a',encoding='utf-8') as f:
        f.write('%s|%s|f|%s|%s\n'%(tmp[2],choice_name,tmp[1],tmp[0]))

# text 파일 합치기 
text_list=[]

for k,i in enumerate (dir2):
    tmp_i = re.sub('\./','',i)
#     tmp = tmp_i.split('/')
    tmp = tmp_i.split('\\')
    dir3 = '%s/%s_%s.trans.txt'%(i, tmp[2], tmp[1])
#     with open(dir3,'w',encoding='utf-8') as f:
#             f.write('')
    tmp_text = glob.glob('%s/*.txt'%i)
    for n,j in enumerate (tmp_text):
        name = os.path.basename(j)
        name_d = re.sub('.txt','',name)
        names = name_d.split("_")
#         print(names)
        with open(j,'r',encoding='utf-8') as f:
            try:
                text = f.read()
                tmp_1 = re.sub("39;|quot;|lt;|gt;|\||/|o/|b/|n/|u/|[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\[\]\<\>`\'…》]",'',text)
                tmp_2 = re.sub(r'\([^\d)]*\)', '', tmp_1)
                re_text = re.sub('\)|\(', '', tmp_2)
            except:
                pass
        with open('%s'%dir3,'a',encoding='utf-8') as f:
            f.write('%s_%s_%s %s'%(tmp[2], tmp[1], names[0], re_text))
        os.remove(j)
    # print(k)


# 음성 확장자 변경 pcm ->flac
for script in dir2:
    tmp_utt = glob.glob('%s/*.wav'%script)
    for i in tmp_utt:
        names = i.split(".")
        name = names[1].split("_")
#         name_2 = names[1].split('/')
        name_2 = names[1].split('\\')
        pcm_dir = '%s'%i
#         wav_dir = '%s\%s_%s_%s.wav'%(script, name_2[2], name_2[1],name_2[3])
        wav_dir = '%s'%i
        flac_dir = '%s\%s_%s_%s.flac'%(script, name_2[2], name_2[1],name_2[3])

        if os.path.isfile('%s'%flac_dir):
            pass
        else:
#             pcm2wav( pcm_dir, wav_dir, 1, 16, 16000 )
            subprocess.run('ffmpeg -i %s -c:a flac %s'%(wav_dir, flac_dir))
#         os.remove(pcm_dir)
        os.remove(wav_dir)
    
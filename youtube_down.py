from pytube import YouTube
import subprocess
import os.path, glob
import re
from bs4 import BeautifulSoup
name = "Et8QeSmr8qc"
list_excel =['https://www.youtube.com/watch?v=%s'%name]
            #  'https://www.youtube.com/watch?v=JwyvEpKMwCc&t=34s',
            #  'https://www.youtube.com/watch?v=NB3T8e3cPyk&t=3s',
            #  'https://www.youtube.com/watch?v=PadWI1zfHw4',
            #  'https://www.youtube.com/watch?v=xYsupuA5AC8',
            #  'https://www.youtube.com/watch?v=BgV2dKvla4k',
            #  'https://www.youtube.com/watch?v=PRZYyhAdil8',
            #  'https://www.youtube.com/watch?v=WbHtn6ORsa4&t=62s',
            #  'https://www.youtube.com/watch?v=-e3cSTsiwuk',
            #  'https://www.youtube.com/watch?v=hLRrfuYUsL4',
            #  'https://www.youtube.com/watch?v=PmD4FpW4ptw',
            #  'https://www.youtube.com/watch?v=9X_g4b9dBWM']
            #  'https://www.youtube.com/watch?v=6heMauzTa7g',
            #  'https://www.youtube.com/watch?v=I-OiwOabXTk',
            #  'https://www.youtube.com/watch?v=qbmzx7TABnw',
            #  'https://www.youtube.com/watch?v=uxUsg5Av4Hw']

# list_excel = []
# with open ('./tube_excel.txt','r',encoding='utf-8') as f:
#     tmp = f.readlines()
#     for i in tmp:
#         tmp2 = i.split(' ')
#         try:
#             list_excel.append('https://www.youtube.com/watch?v=%s'%tmp2[1])
#         except:
#             pass
#유튜브 전용 인스턴스 생성
for j,i in enumerate (list_excel):
    yt = YouTube(i)
    
    # # 특정영상 다운로드
    # os.makedirs('./%s'%k)
    tmp=yt.streams.filter(only_audio=True).first()
    tmp=tmp.download(output_path= './kids', filename='%s'%name)
    os.system('ffmpeg -i ./kids/'+name+'.mp4 -acodec pcm_s16le -ac 1 -ar 16000 ./kids/'+name+'.wav')
    os.remove('./kids/'+name+'.mp4')
    # # convert mp4 to flac 
    # mp4_dir = tmp
    # wav_dir = './%s/youtube%s.wav'%(k,k)
    # subprocess.run('ffmpeg -i %s -acodec flac -bits_per_raw_sample 8 -ar 16000 %s'%(mp4_dir, wav_dir))
    # os.remove(mp4_dir)
    
    # 대본파일 들고오기
    # yt.captions.all()
    # caption = yt.captions.get_by_language_code('ko')

    # # 발화 내용과 태크표시됨
    # if caption is None:
    #     print(k)
    #     pass
    # else:
    #     text = caption.xml_captions
    #     soup = BeautifulSoup(text, "html.parser")
    #     tmp=soup.find_all("text")
    #     for i in tmp:
    #         sent = i.get_text()
    #         try:
    #             tmp_1 = re.sub("/|o/|b/|n/|u/|[-=+,#/\?;:^$.@*\"※~&%ㆍ!』\\‘|\[\]\<\>`\'…》]",'',sent)
    #             tmp_2 = re.sub(r'\([^\d)]*\)', '', tmp_1)
    #             re_text = re.sub('\)|\(', '', tmp_2)
    #         except:
    #             pass
    #         with open('./tube_excel/%s.txt'%k,'a',encoding ='utf-8') as f:
    #             f.write(re_text)

# print('완료')
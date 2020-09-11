import os.path, glob, os
import re 
import wave


start_point = 'KsponSpeech'
dir1 = glob.glob('./%s/*'%start_point)
dir2 =[]
for i in dir1:
    dir2.extend(glob.glob('%s/*'%i))

# AUDIO_INFO 만들기
# with open( './AUDIO_INFO', 'w', encoding='utf-8') as f:
#     f.write('SPEAKERID|NAME|SEX|SCRIPTID|DATASET\n')
# for i in dir2:
#     tmp_i = re.sub('\./','',i)
#     # tmp = tmp_i.split('/')
#     tmp = tmp_i.split('\\')
#     with open('./AUDIO_INFO','a',encoding='utf-8') as f:
#         f.write('%s|x|f|%s|%s\n'%(tmp[2],tmp[1],tmp[0]))

# text 파일 합치기 
text_datas = []
for k,i in enumerate (dir2):
    tmp_i = re.sub('\./','',i)
    # tmp = tmp_i.split('/')
    tmp = tmp_i.split('\\')
    dir3 = '%s/%s_%s.trans.txt'%(i, tmp[2], tmp[1])
    with open(dir3,'w',encoding='utf-8') as f:
            f.write('')
    tmp_text = glob.glob('%s/*.txt'%i)
    for j in tmp_text:
        name = os.path.basename(j)
        name_d = re.sub('.txt','',name)
        with open(j,'r',encoding= 'CP949') as f:
            try:
                text = f.read()
                tmp_1 = re.sub("/|o/|b/|n/|u/|[-=+,#/\?;:^$.@*\"※~&%ㆍ!』\\‘|\[\]\<\>`\'…》]",'',text)
                tmp_2 = re.sub(r'\([^\d)]*\)', '', tmp_1)
                re_text = re.sub('\)|\(', '', tmp_2)
            except:
                pass
        with open('%s'%dir3,'a',encoding='utf-8') as f:
            f.write('%s %s'%(name_d,re_text))
#        os.remove(j)
    print(k)
print("텍스트병합 완료")



cursor.execute('INSERT INTO youtube_data(uid, keyword, subject, content, date, hate_cnt, like_cnt, comment_cnt, subscribers, hit_cnt, channel, ch_id, tag, video_len, crawl_date, use) VALUES(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16)'
, [r.uid, r.키워드, r.제목, r.내용, r.영상 등록일, r.싫어요, r.좋아요, r.댓글 수, r.구독자 수, r.조회수, r.채널명, r.채널id, r.태그, r.영상 길이, r.정보수집일, r.사용여부])
# 음성 확장자 변경 pcm ->flac
# for script in dir2[:3]:
#     tmp_utt = glob.glob('%s/*.pcm'%script)
#     for i in tmp_utt:
#         names = i.split(".")
#         name = names[1].split("_")
#         name_2 = names[1].split('/')
#         print(name_2)
#         pcm_dir = '%s'%i
#         wav_dir = '%s/%s_%s_%s.wav'%(script, name_2[3], name_2[2],name[4])
#         flac_dir = '%s/%s_%s_%s.flac'%(script, name_2[3], name_2[2],name[4])
# #        pcm2wav( pcm_dir, wav_dir, 1, 16, 16000 )
# #        subprocess.run('ffmpeg -i %s -acodec pcm_s16le -ac 1 -ar 16000 %s'%(pcm_dir, wav_dir))
#         os.system('ffmpeg -ar 16000 -ac 1 -f s16le -i %s %s'%(pcm_dir, wav_dir))
#         os.system('ffmpeg -i %s -c:a flac %s'%(wav_dir, flac_dir))
#         os.remove(pcm_dir)
#         os.remove(wav_dir)
# print('음원 변환 완료')  

# wav -> flac
# for script in data_script:
#     tmp_utt = glob.glob('%s/*.wav'%script)
#     for i in tmp_utt:
#         names = i.split(".")
#         name = names[1].split("_")
#         name_2 = names[1].split('/')
#         wav_dir = i
#         flac_dir = '%s\%s_%s_%s.flac'%(script, name_2[2], name_2[1],name_2[3])
#         subprocess.run('ffmpeg -i %s -c:a flac %s'%(wav_dir, flac_dir))
#         os.remove(wav_dir)

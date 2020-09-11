import sys, os, glob, os.path, re

train_data_dir = sys.argv[1]

medium_category_dir = glob.glob(train_data_dir+"/*")
medium_category_dir.sort()

for i in medium_category_dir:
    tmp_name = os.path.basename(i)
    md_name = tmp_name.split('_')[1]
    os.makedirs(train_data_dir+"/"+md_name, exist_ok=True)
    small_category_dir = glob.glob(i+"/*")
    small_category_dir.sort()
    for j in small_category_dir:
        tmp_name = os.path.basename(j)
        small_name = tmp_name.split('_')[1] 
        os.makedirs(train_data_dir+"/"+md_name+"/"+small_name, exist_ok=True)
        pcm_dir = glob.glob(j+"/*.pcm")
        pcm_dir.sort()
        for k in pcm_dir:
            tmp_n = os.path.basename(k)
            tmp_name = tmp_n.split('.')[0]
            pcm_name = tmp_name.split('_')[1]
            wav_dir = '%s%s.wav'%(train_data_dir, pcm_name)
            flac_dir = '%s/%s_%s_%s.flac'%(train_data_dir+"/"+md_name+"/"+small_name, small_name, md_name,pcm_name)
#            os.system("ffmpeg -i " + k + " -acodec pcm_s16le -ac 1 -ar 16000 " + wav_dir)
            os.system("ffmpeg -f s16le -ar 16000 -ac 1 -i "+k+" "+wav_dir)
            os.system("ffmpeg -i " + wav_dir + " -c:a flac "+flac_dir)
            os.remove(wav_dir)
            os.remove(k)

print('완료')
            

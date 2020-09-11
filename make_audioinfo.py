import sys, os, glob, os.path


train_data_dir = sys.argv[1]
export_dir = sys.argv[2]

medium_category_dir = glob.glob(train_data_dir+"/*")
medium_category_dir.sort()

with open(export_dir+"/AUDIO_INFO", 'w', encoding='utf-8') as f:
    f.write('SPEAKERID|NAME|SEX|SCRIPTID|DATASET\n')

for i in medium_category_dir:
    md_name = os.path.basename(i)
    small_category_dir = glob.glob(i+"/*")
    small_category_dir.sort()
    for j in small_category_dir:
        small_name = os.path.basename(j)
        with open(export_dir+"/AUDIO_INFO",'a',encoding='utf-8') as f:
            f.write(small_name+"|jennie|f|"+md_name+"|train_data_01\n")


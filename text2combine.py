import sys, os, glob, os.path, re

train_data_dir = sys.argv[1]

medium_category_dir = glob.glob(train_data_dir+"/*")
medium_category_dir.sort()
print(medium_category_dir)
for i in medium_category_dir:
    print(i)
    tmp_name = os.path.basename(i)
    md_name = tmp_name.split('_')[1]
    small_category_dir = glob.glob(i+"/*")
    small_category_dir.sort()
    for j in small_category_dir:
        tmp_name = os.path.basename(j)
        small_name = tmp_name.split('_')[1]
        text_dir = glob.glob(j+"/*.txt")
        text_dir.sort()
        for k in text_dir:
            tmp_n = os.path.basename(k)
            tmp_name = tmp_n.split('.')[0]
            text_name = tmp_name.split('_')[1]
            export_dir = '/data/send_data/%s/%s/%s_%s.trans.txt'%(md_name,small_name, small_name, md_name)
            with open(k, 'r', encoding = 'cp949') as f: 
                te = f.read()
                tmp_1 = re.sub("/|o/|b/|n/|u/|[-=+,#/\?;:^$.@*\"※~&%ㆍ!』\\‘|\[\]\<\>`\'…》]",'',te)
                tmp_2 = re.sub(r'\([^\d)]*\)', '', tmp_1)
                text = re.sub('\)|\(', '', tmp_2)
                print(text)
            with open(export_dir, 'a',encoding='utf-8') as f:
                f.write(small_name+"_"+md_name+"_"+text_name+" "+text)
                print(small_name+"_"+md_name+"_"+text_name+" "+text)
#del_dir =  glob.glob(train_data_dir+"/KsponSpeech_*")
#os.remove(del_dir)
print('end')
        

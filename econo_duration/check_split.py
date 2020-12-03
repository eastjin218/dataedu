import os, glob, os.path, shutil
import numpy as np
import kss
import pymysql
from konlpy.tag import Mecab
mecab= Mecab()
import pandas as pd

from word_nomalize import  *
from transliteration import translate
transliter = translate.Transliteration()
import nltk
#nltk.download('punkt')

def split_word(idx, texts):

    output='/data/training_model/Tacotron2-Wavenet-Korean-TTS/logdir-tacotron2/%s'%idx
    os.makedirs(output,exist_ok=True)
    print('---------------%s-------------'%idx)
    body = re.search('<div.*/div>',texts, re.I|re.S)
    if not body:
        body = re.search('<p.v*/p>', texts, re.I|re.S)
    try:
        text = body.group()
        text = re.sub('<figure.*?</figure>', '', text, 0,re.I|re.S)
        text = re.sub('<img.*?>', '', text, 0, re.I|re.S)
        text = re.sub('<p>','<\p> ',text)
        text = re.sub('<.+?>', '', text, 0, re.I|re.S)
        text = re.sub('&.+?;', '', text, 0, re.I|re.S)
        text = re.sub('''\t|\r|\n''', '', text)
    except:
        text=texts 
    text = re.sub('<IMG.*?>','',text,0,re.I|re.S)
    text = re.sub('<img.*?>','',text,0,re.I|re.S)
    text = re.sub(r'([가-힣])\, ([가-힣])', r'\1\n\2', text)
    text = re.sub(r'([가-힣])\. ([가-힣])', r'\1\n\2', text)
    text = re.sub(r'([가-힣])\.([가-힣])', r'\1\n\2', text)
    text = re.sub(r'([가-힣])\? ([가-힣])', r'\1\n\2', text)
    text = re.sub(r'([가-힣])\?([가-힣])', r'\1\n\2', text)
    text = normalize(text)
    text = re.sub("[●△∑Ⅰ,■·#/\▲〉▼?:^$.*☎★◆▶▣◇★\♥◈○:〈▷☞\"～※~&ㆍ!』→\\‘|\[\]\<\>`\'…》\)|\(]",' ',text)
    text = re.sub(r'([가-힣])-([가-힣])', r'\1 다시 \2', text)
    text = re.sub(r'([가-힣]) - ([가-힣])', r'\1 다시 \2', text)
    text = re.sub(r'([가-힣])- ([가-힣])', r'\1 다시 \2', text)
    text = re.sub(r'([가-힣]) -([가-힣])', r'\1 다시 \2', text)
    text = re.sub(r'([가-힣])-([a-zA-Z])', r'\1 다시 \2', text)
    text = re.sub(r'([가-힣]) -([a-zA-Z])', r'\1 다시 \2', text)
    text = re.sub(r'([가-힣])- ([a-zA-Z])', r'\1 다시 \2', text)
    text = re.sub(r'([가-힣]) - ([a-zA-Z])', r'\1 다시 \2', text)
    text = re.sub(r'([a-zA-Z])-([가-힣])', r'\1 다시 \2', text)
    text = re.sub(r'([a-zA-Z]) -([가-힣])', r'\1 다시 \2', text)
    text = re.sub(r'([a-zA-Z])- ([가-힣])', r'\1 다시 \2', text)
    text = re.sub(r'([a-zA-Z]) - ([가-힣])', r'\1 다시 \2', text)
    text = re.sub(r'([a-zA-Z])-([a-zA-Z])', r'\1 다시 \2', text)
    text = re.sub(r'([a-zA-Z]) - ([a-zA-Z])', r'\1 다시 \2', text)
    text = re.sub(r'([a-zA-Z])- ([a-zA-Z])', r'\1 다시 \2', text)
    text = re.sub(r'([a-zA-Z]) -([a-zA-Z])', r'\1 다시 \2', text)
    text = re.sub(r'([a-zA-Z])@([a-zA-Z])', r'\1 골뱅이  \2', text)
    
    text = text.split('\n')
    li1 =[]
    for li in text:
        li = ' '.join(li.split())
        li = Eng2han(li, transliter)
        if korean_count(li) >= 140:
            sent = me_token(li,'josa')
            if not sent:
                sent = me_token(li,'f_josa')
            li1.extend(sent)
        else:
            li1.append(li)
    for i in li1:
        with open ('%s/count_%s.txt'%(output, idx),'a',encoding='utf-8') as f:
            f.write(i+'  ---\n')
    
    return '  ---\n'.join(li1)

############################################################
con = pymysql.connect(host='220.119.175.200', user='dataedu', password='dataedu!1', db='econoi')
curs = con.cursor()
curs.execute("SELECT n_idx, contents ,split_contents FROM news_title WHERE split_contents=' '  ORDER BY n_idx DESC")
row = curs.fetchall()
data=pd.DataFrame(data=row)
data = data.rename({0:'idxno',1:'body',2:'split_con'},axis='columns')
#print(data)
curs.close()
data['split_YN'] = data['body']
for j,i in enumerate(data['body']):

    data['split_con'][j]=split_word(data['idxno'][j],i)
    if not data['split_con'][j]:
        data['split_YN'][j] = 'N'
    else:
        data['split_YN'][j] ='Y'

#print(data.head(50))
con = pymysql.connect(host='220.119.175.200', user='dataedu', password='dataedu!1', db='econoi')
curs = con.cursor()
for index, row in data.iterrows():
    curs.execute("UPDATE news_title SET split_YN=%s, split_contents=%s WHERE n_idx=%s",
            (row.split_YN, row.split_con, row.idxno))
con.commit()
curs.close()

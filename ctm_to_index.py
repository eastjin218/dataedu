import pandas as pd
import os, os.path, glob
from chatspace import ChatSpace

def classific(text):
  if text.endswith('니다'):
    return text
  elif text.endswith('요'):
    return text
  elif text.endswith('죠'):
    return text 
  else:  
    return 'NaN'

ctm_list = []
for i in ctm_list:

    df = pd.read_csv(i, encoding='utf-8', header=None)
    df['sec'] = df[0].apply(lambda x : x.split(' ')[2])
    df['plus'] = df[0].apply(lambda x : x.split(' ')[3])
    df['plus'] = df['plus'].astype(float)
    df['sec'] = df['sec'].astype(float)
    df['time'] = df['sec']+df['plus']
    df['index'] = df['time'].apply(lambda x : int(x * 16000))
    df['text'] = df[0].apply(lambda x : x.split(' ')[4])
    df['texts'] = df['text'].apply(lambda x : classific(x))
    df_index=df[['time','index','text']].drop(df.loc[df['texts']=='NaN'].index)


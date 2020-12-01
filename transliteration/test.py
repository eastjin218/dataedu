import os, glob, os.path
import translate

text = ['kakao', 'agreement','econoi']
transliter = translate.Transliteration()
for i in text:
    trans = translate.decoding(i,transliter)
    print(trans)

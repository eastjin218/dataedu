import webvtt, sys, re

vtt_file_name = sys.argv[1]
tempText = []

for caption in webvtt.read(vtt_file_name):
    print(caption.start)
    print(caption.end)
    # &lt;나 &gt;태그를 제거
    srcText = re.sub('&lt(;)?(/)?([a-zA-Z]*)(\\s[a-zA-Z]*=[^>]*)?(\\s)*(/)?&gt(;)?', '', caption.text)
    # < > 태그형태를 제거
    srcText = re.sub('<(/)?([a-zA-Z]*)(\\s[a-zA-Z]*=[^>]*)?(\\s)*(/)?>', '', srcText)
    # 일부 특수문자 제거 ( . , ? )
    srcText = re.sub('[.,?\[\]\']','', srcText)

    tempText.append(srcText.strip())
    
finalText = ' '.join(tempText)
print(finalText)

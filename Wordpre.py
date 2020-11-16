import os, os.path, copy
from glob import glob 
import re

# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

# 한글 자모 분리
def korean_to_be_englished(korean_word):
    
    r_lst = []
    for w in list(korean_word.strip()):
        ## 영어인 경우 구분해서 작성함. 
        if '가'<=w<='힣':
            ## 588개 마다 초성이 바뀜. 
            ch1 = (ord(w) - ord('가'))//588
            ## 중성은 총 28가지 종류
            ch2 = ((ord(w) - ord('가')) - (588*ch1)) // 28
            ch3 = (ord(w) - ord('가')) - (588*ch1) - 28*ch2
            r_lst.append([CHOSUNG_LIST[ch1], JUNGSUNG_LIST[ch2], JONGSUNG_LIST[ch3]])
#         else:
#             if w == 'a':
#                 w = '에이'          
#                 r_lst.append(w)
    return r_lst


## 한글 자모 숫자
def korean_count(korean_word):
    
    r_lst = []
    for w in list(korean_word.strip()):
        ## 영어인 경우 구분해서 작성함. 
        if '가'<=w<='힣':
            ## 588개 마다 초성이 바뀜. 
            ch1 = (ord(w) - ord('가'))//588
            ## 중성은 총 28가지 종류
            ch2 = ((ord(w) - ord('가')) - (588*ch1)) // 28
            ch3 = (ord(w) - ord('가')) - (588*ch1) - 28*ch2
            r_lst.append(CHOSUNG_LIST[ch1])
            r_lst.append(JUNGSUNG_LIST[ch2])
            if JONGSUNG_LIST[ch3] == ' ':
                pass
            else:
                r_lst.append(JONGSUNG_LIST[ch3])
        if w == ' ':
            r_lst.append(' ')
        
#         else:
#             if w == 'a':
#                 w = '에이'          
#                 r_lst.append(w)
    return len(r_lst)

def readNumber( i):
    units = ['','십','백','천','만','십만']
    num = '일이삼사오육칠팔구'
    result = []
    j = 0
    while i >0 :
        i ,r = divmod(i,10)
        if r > 0:
            result.append(num[r-1]+units[j])
        j += 1
    return ''.join(result[::-1])

def stringNumber(text):
    num_to_kor = {'0': '영','1': '일','2': '이', '3': '삼','4': '사','5': '오','6': '육','7': '칠','8': '팔', '9': '구'}
    tmp_text = []
    for i in text:
        if i in num_to_kor:
            tmp_text.append(num_to_kor[i])
        else:
            tmp_text.append(i)
    return ''.join(tmp_text)

def trasNumber(text):
    tmp = text.split(' ')
    text = []
    for i in tmp:
        if i.startswith('점'):
            text.append(stringNumber(i)+' ')
        elif i.startswith('0'):
            text.append(stringNumber(i)+' ')
        elif i.isdigit():
            text.append(readNumber(int(i))+' ')
        else:
            text.append(i+' ')
    return ''.join(text)


def Eng2han(text):
    upper_to_kor = {'A': '에이','B': '비','C': '씨','D': '디','E': '이', 'F': '에프', 'G': '지', 'H': '에이치', 'I': '아이', 'J': '제이', 'K': '케이', 'L': '엘', 'M': '엠', 'N': '엔',
            'O': '오', 'P': '피', 'Q': '큐','R': '알', 'S': '에스', 'T': '티', 'U': '유','V': '브이','W': '더블유','X': '엑스','Y': '와이','Z': '지'}
    tmp_text = []
    for i in text:
        i = i.upper()
        if i in upper_to_kor:
            tmp_text.append(upper_to_kor[i])
        else:
            tmp_text.append(i)
    return ''.join(tmp_text)


def costum(text):
    custom_lex = {'NAVER':'네이버'}
    tmp_text = []
    text = text.split(' ')
    for i in text:
        i = i.upper()
        if i in custom_lex:
            tmp_text.append(custom_lex[i]+' ')
        else:
            tmp_text.append(i+' ')
    return ''.join(tmp_text)



def pre_text(text):
    ## 단위
    text = re.sub(r'(\d)(m)', r'\1 미터', text)
    text = re.sub(r'(\d)(%)', r'\1 퍼센트', text)
    text = re.sub(r'(\d)(%)', r'\1 퍼센트', text)
    text = re.sub(r'(\d)(%)', r'\1 퍼센트', text)
    text = re.sub(r'(\d)(%)', r'\1 퍼센트', text)
    text = re.sub(r'(\d)(%)', r'\1 퍼센트', text)
    
    ## 사용자 변화 
    text = re.sub('''['|"|“|”|’|‘|]''','',text)
    text = re.sub(r'(\d)-([a-zA-Z])', r'\1 다시 \2', text)
    text = re.sub(r'([a-zA-Z])-(\d)', r'\1 다시 \2', text)
    text = re.sub(r'([가-힣])-([가-힣])', r'\1  다시 \2', text)
    text = re.sub(r'([가-힣])–([가-힣])', r'\1  다시 \2', text)
    text = re.sub(r'([가-힣])=([가-힣])', r'\1은 \2', text)
    text = re.sub(r'([가-힣]) - ([가-힣])', r'\1  다시 \2', text)
    text = re.sub(r'([가-힣]) – ([가-힣])', r'\1  다시 \2', text)
    text = re.sub(r'(\d)-([가-힣])', r'\1  다시 \2', text)
    text = re.sub(r'([가-힣])-(\d)', r'\1  다시 \2', text)
    text = re.sub(r'(\d)\.(\d)', r'\1 점\2', text)
    text = re.sub(r'([a-zA-Z])\.([a-zA-Z])', r'\1 점 \2', text)
    text = re.sub('://', ' 땡땡 슬러쉬 슬러쉬 ', text)
    
    text = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', text)
    text = re.sub(r'(\d)([가-힣])', r'\1 \2', text)
    
    ## 숫자 한글변화
    text = trasNumber(text)
    
    ## 특수문자 제거
    text = re.sub('''[.|?|,|:|'|"|“|”|’|]''',' ',text)
    text = re.sub("[●,#/\?:^$.@*\"※~&ㆍ!』\\‘|\[\]\<\>`\'…》]",' ',text) 
    text = re.sub('\)|\(', ' ', text)
    
    ## 한글 영어 숫자 띄우기
    
    text = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', text)
    text = re.sub(r'([a-zA-Z])([가-힣])', r'\1 \2', text)
    text = re.sub(r'([가-힣])([a-zA-Z])', r'\1 \2', text)
    text = re.sub(r'([가-힣])(\d)', r'\1 \2', text)
    
    ## 숫자 한글변화
    text = trasNumber(text)
    
    ## 사용자 사전 영어 발음식
    text = costum(text)
    
    ## 영어 알파벳변화
    text = Eng2han(text)
        
    return text

## 종결어미 기준 텍스트 분리
def Text_split(text):
    Terminate_word = ['니다' , '이다','었다','한다','았다','했다','졌다','됐다','된다','하다','왔다','인다','진다','냈다','혔다','있다','났다','많다','적다','크다','적다','봤다','본다',
                 '난다','친다','섰다','겠다','단다','든다','낸다','간다','킨다','란다','른다','린다','좋다','같다','들다','안다','쉽다','준다','긴다','헤드경제','어요','까요','워요',
                     '아요','들죠','하죠','해요','이죠','이요','지요','기죠','했죠','져요','나요','에요','세요','치다']
    sleep_word = ['하고','때면','리고','러나','런데','때','않고','는데','팔고','지만']
    custom_word = ['부터','이유죠','사이트죠','혔죠','보단','일  일','이  일','삼  일','사  일','오  일','육  일','칠  일','팔  일','구  일']
    for i in Terminate_word:
        text = text.replace('%s '%i, '%s \n'%i)
    for j in sleep_word:
        text = text.replace('%s '%j, '%s \n'%j)
    for j in custom_word:
        text = text.replace('%s '%j, '%s \n'%j)
    return text


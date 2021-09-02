# -*- coding: utf-8 -*-
"""Data_Preprocessing_FINAL .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YDJ5bkOTCEgbMy8XKjeBh4rK13qiViiI

#전처리개발
"""

!apt-get update
!apt-get install g++ openjdk-8-jdk python-dev python3-dev
!pip3 install JPype1-py3
!pip3 install konlpy
!JAVA_HOME="C:\Program Files\Java\jdk-16.0.1"

from konlpy.tag import Okt
okt = Okt()

import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical

data = pd.read_csv('textvp.txt', sep='\t')
data[:50]

import nltk
nltk.download('punkt')

from nltk.tokenize import word_tokenize
example = '일단 잘 알겠구요. 저희들이 KB 금융 예로 KB 저축은행인데요. 지금 5월달에 저희들이 자급적으로 나온 대출상품이 있어요. 네 그리고 님 직접 8프로 대로 진행하는 부분이고 상환기간이 5년까지고요. 중도 상환가능하고 수수료 발생에 지금 원리금균등분할 상환 혹은 만기시 상환적으로 이자만 갚으시면 되는 부분이에요. 네 그리고 자급적으로 5천만원까지인데 5천만원부터 받으실거예요? 일단 잘 알겠구요. 맞으시죠? 예. 고객님 혹시 지금 그 사용하고 계신 휴대폰은 본인 이름으로 돼있는거 맞으세요? 예 통신사는 SKT예요 LG예요. 예 삼성 스마트폰 맞으세요? 혹시 카톡은 사용하고 계세요? 그러면은요 카톡 추가를 해서 저희 상호하고 제 이름 넣어드릴게요. 어.. 고객님 저한테 전화를 주셔서 통화중에 제가 전화를 못받으면 카톡으로 연락을 할 수도 있어서 그러는 거 아니에요. 예?'
stop_words_new = pd.read_csv('stop_words_new.txt',names = ['words'], encoding='utf-16')

word_tokens = okt.morphs(example)
stop_data = np.array(stop_words_new['words']).tolist()
result = []
for w in word_tokens:
   if w not in stop_data:
      result.append(w)
print(word_tokens,'\n')
print(result)

import pandas as pd
text_data = pd.read_csv('textvp.txt',names=['data','label'] , sep='|')
text_train = text_data['data'].to_numpy()
text_target=text_data['label'].to_numpy()

print(text_train[:10])
print(text_train.shape)
print(text_data.shape)

#t = Tokenizer()
#t.fit_on_texts(s)
#print(t.word_index)
#for data in train_data:
#  word = okt.nouns(train_data)
#for data in train_data:
#  train_token=okt.morphs(train_data)

result = []
for text in text_train:
  tokenSet=okt.morphs(text)
  result.append(tokenSet)

print(result[0])

"""#**불용어처리**"""

tokenize = []
for text in text_train:
  tokenSet = okt.morphs(text)
  tokenize.append(tokenSet)

result = []
body = []
for tokenSet in tokenize:
  for token in tokenSet:
    if token not in stop_data:
      result.append(token)
  body.append(result)
  result=[]

#result엔 뭐가 들어있는거지
print("토큰화 한 샘플(tokenize) = ",tokenize[0]) #토큰화 한 샘플
print("불용어 처리 된 샘플(body) = ",body[0]) #불용어 처리 된 샘플
print(len(tokenize[0]))
print(len(body[0]))
#문제: 숫자랑 문자로 표현된 숫자 불용어 처리 어떻게 할 건지

"""#**어휘사전만들기**"""

from tensorflow.keras.preprocessing.text import Tokenizer

t = Tokenizer()
t.fit_on_texts(body)
print(t.word_index)

sequence_data = t.texts_to_sequences(body) #transform 
print(sequence_data[0])
#단어사전 줄이기 1/30 6800->250개

np.set_printoptions(threshold=np.inf)
#print(t.word_index)
#print(len(t.word_index))
hj=list(t.word_index)
#print(hj)

hjdata=np.array(hj)
type(hjdata)
#hjdata.reshape(-1,10)

"""#**PAD_SEQUENCES**"""

import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical

import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import nltk
nltk.download('punkt')

tokenizer = Tokenizer()
tokenizer.fit_on_texts(text_train)

encoded = tokenizer.texts_to_sequences(text_train)
print(encoded)

padded = pad_sequences(encoded) #앞을 0으로 채우기
print(padded)

padded_post = pad_sequences(encoded, padding = 'post') #뒤를 0으로 채우기
print(padded_post)

padded = pad_sequences(encoded, truncating = 'post', maxlen = 500)
print(padded)

#앞을 0으로 채울지 뒤로 채울지 생각해보기(RNN) -> 순환하니까 마지막에 있는 셀의 영향이 크다 (첫번째에 있는 셀이 두번째에 쓰이고... 그렇게되면 마지막 셀의 영향이 커짐)
#maxlen 얼마나 자를지 정하기 / 샘플 중 가장 긴 것 길이 알아보기 / 원핫인코딩 해야하는지(단어 임베딩 층이 존재하므로 안해도 된다) / 파이썬 APP 으로 옮기기 / Git에 지금까지 한 거 올리기 / 뉴런의 개수 : 8개 / 검증데이터 나누기 / 한 코드로 만들기
#다음회의 때 RNN 엔진 코드 같이 돌려보기 
#길이가 maxlen보다 짧은 문서들은 0으로 패딩되고, 기존에 maxlen보다 길었다면 데이터가 손실된다
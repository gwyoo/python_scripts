# 파이썬 생활 프로그래밍 / 김창현

##############################################################

# reg 이용해서 숫자의 comma 삭제후 숫자 변환

import re

r = re.sub(',', '', '123,456')
f = float(r)

print f
##############################################################

# 참고 - https://github.com/skytreesea/do-it-python/blob/master/06/quote.py
# 명언 수집  (Do it 파이썬 생활프로그래밍) 초판 2020: 218페이지
import os , re, usecsv
import urllib.request as ur

from bs4 import BeautifulSoup as bs
url = 'http://quotes.toscrape.com/' 
html = ur.urlopen(url)
soup=bs(html.read(), 'html.parser')

#명언 하나만 가져오기
print(soup.find_all('span')[0].text)

# quote 명언 하나만 가져오기
print(soup.find_all('div',{"class":"quote"})[0])

# 해당 페이지의 명언 모두 출력하기
for i in soup.find_all('div',{"class":"quote"}):
	print(i.text)
#################################################################








# BeautifulSoup 이용
# 참고   - https://github.com/skytreesea/do-it-python/blob/master/06/article.py


import os, re
import urllib.request as ur
from bs4 import BeautifulSoup as bs

url='https://media.daum.net/'
# 마법의 명령어
soup=bs(ur.urlopen(url).read(),'html.parser')

# 특정 클래스 속성을 출력하기
print(soup.find_all('div', {"class" : "item_issue"}))

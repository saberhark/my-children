from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
from selenium.webdriver.common.by import By


# 함수 정의: 검색어 조건에 따른 url 생성
def insta_searching(word):
    url = "https://www.instagram.com/explore/tags/" +  str(word)
    return url


# 함수 정의: 열린 페이지에서 첫 번째 게시물 클릭 + sleep 메소드 통하여 시차 두기
def select_first(driver):
    first = driver.find_elements_by_css_selector("div._aagw")[0]
    first.click()
    time.sleep(3)


# 함수 정의: 본문 내용, 작성일자, 좋아요 수, 위치 정보, 해시태그 가져오기
def get_content(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    # 본문 내용
    try:
        content = soup.select('div._a9zs')[0].text
    except:
        content = ''
    # 해시태그
    tags = re.findall(r'#[^\s#,\\]+', content)

    # 작성일자
    date = soup.select('time._aaqe')[0]['datetime'][:10]

    # 좋아요
    try:
        like = soup.select('div._aacl._aaco._aacw._aacx._aada._aade')[0].findAll('span')[-1].text
    except:
        like = 0
    # 위치
    try:
        place = soup.select('div._aaqm')[0].text
    except:
        place = ''

    data = [content, date, like, place, tags]
    return data


# 함수 정의: 첫 번째 게시물 클릭 후 다음 게시물 클릭
def move_next(driver):
    right = driver.find_element_by_css_selector("div._aaqg._aaqh") # 2022/01/11 수정
    right.click()
    time.sleep(3)


# 크롤링 시작
"""
driver.get(url)을 통해 검색 페이지 접속하고,
target 변수에 크롤링할 게시글의 수를 바인딩
"""

# 크롬 브라우저 열기
driver = webdriver.Chrome('chromedriver.exe')

driver.get('https://www.instagram.com')
time.sleep(3)

# 인스타그램 로그인을 위한 계정 정보
email = 'saber4with@naver.com'
input_id, input_pw = driver.find_elements(By.CSS_SELECTOR, 'input._aa4b._add6._ac4d')
input_id.clear()
input_id.send_keys(email)

password = 'asdasd12'
input_pw.clear()
input_pw.send_keys(password)
input_pw.submit()

time.sleep(5)
word = input("검색어 입력")
word = str(word)
url = insta_searching(word)

# 검색 결과 페이지 열기
driver.get(url)
time.sleep(10) # 코드 수행 환경에 따라 페이지가 로드되는 데 시간이 더 걸릴 수 있어 8초로 변경(2022/01/11)

# 첫 번째 게시물 클릭
select_first(driver)

# 본격적으로 데이터 수집 시작
results = []
## 수집할 게시물의 수
target = 10
for i in range(target):

    try:
        data = get_content(driver)
        results.append(data)
        move_next(driver)
    except:
        time.sleep(2)
        move_next(driver)
    time.sleep(5)

print(results[:2])
print(len(results))



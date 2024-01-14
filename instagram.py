from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

# 함수 정의: 검색어 조건에 따른 url 생성
def insta_searching(word):
    return "https://www.instagram.com/explore/tags/" + str(word)


# 함수 정의: 열린 페이지에서 첫 번째 게시물 클릭 + sleep 메소드 통하여 시차 두기
def select_first(driver):
    first = driver.find_elements(By.CSS_SELECTOR, 'div._aagw')[10]
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
        print("dasdsa")

    print(content)
    # 작성일자
    date = soup.select('time._aaqe')[0]['datetime'][:10]
    '''
    # 해시태그
    tags = re.findall(r'#[^\s#,\\]+', content)

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
    '''
    #data = [content, date, like, place, tags]

    return [content, date]


# 함수 정의: 첫 번째 게시물 클릭 후 다음 게시물 클릭
def move_next(driver):
    right = driver.find_elements(By.CSS_SELECTOR, 'div._aaqg._aaqh')[0] # 2022/01/11 수정
    right.click()
    time.sleep(3)


def scroll_down(driver):
    SCROLL_PAUSE_SEC = 1

    # 스크롤 높이 가져옴
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # 끝까지 스크롤 다운
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 1초 대기
        time.sleep(SCROLL_PAUSE_SEC)

        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


# 크롤링 시작
"""
driver.get(url)을 통해 검색 페이지 접속하고,
target 변수에 크롤링할 게시글의 수를 바인딩
"""


def open_chrome():
    # 크롬 브라우저 열기
    # Selenium WebDriver 설정
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.instagram.com')
    return driver


def insta_login(driver):
    # 인스타그램 로그인을 위한 계정 정보
    email = 'saber4with@naver.com'
    input_id, input_pw = driver.find_elements(By.CSS_SELECTOR, 'input._aa4b._add6._ac4d')
    input_id.clear()
    input_id.send_keys(email)

    password = 'asdasd12'
    input_pw.clear()
    input_pw.send_keys(password)
    input_pw.submit()


def main():
    driver = open_chrome()
    time.sleep(3)

    action = ActionChains(driver)

    insta_login(driver)
    time.sleep(5)

    # 검색 결과 페이지 열기
    search_url = insta_searching('캐리커쳐')
    driver.get(search_url)
    time.sleep(10)

    '''
    # 스크롤 순회하면서 본문 내용 크롤링
    row = driver.find_elements(By.CSS_SELECTOR, 'div._ac7v._aang')
    print(len(row))
    print(row[-1])
    print(row[0])
    action.move_to_element(row[6]).perform()
    time.sleep(3)
    row = driver.find_elements(By.CSS_SELECTOR, 'div._ac7v._aang')
    print(len(row))

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    print("dsaadsad")
    for a in soup.select('div._aagv'):
        print(a.text)
    '''
    select_first(driver)
    print(get_content(driver))

    move_next(driver)






main()

'''
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


date = datetime.today().strftime('%Y-%m-%d')

results_df = pd.DataFrame(results)
#results_df.columns = ['content', 'date', 'like', 'plcae', 'tags']
results_df.columns = ['content', 'date']
results_df.to_excel(date+'_about '+word+' insta crawling.xlsx')
'''
# 라이브러리 준비하기
import csv
import requests
from bs4 import BeautifulSoup
# selenium의 webdriver를 사용하기 위한 import
from selenium import webdriver

# selenium으로 키를 조작하기 위한 import
from selenium.webdriver.common.keys import Keys

# 페이지 로딩을 기다리는데에 사용할 time 모듈 import
import time


#driver_path = '/Users/minkooksun/Documents/PythonWorkspace/chromedriver'
#driver = webdriver.Chrome(driver_path)
# 옵션 생성
options = webdriver.ChromeOptions()
# 창 숨기는 옵션 추가
options.add_argument("headless")

driver = webdriver.Chrome(options=options) 

url ="https://docs.swift.org/swift-book/documentation/the-swift-programming-language"

# 웹 페이지 열기
driver.get(url)
 
# 로딩을 위해 잠시 대기
time.sleep(3)

# 페이지 소스 출력
page_source = driver.page_source
#print(page_source)
soup = BeautifulSoup(page_source , "lxml")

menus = soup.find_all('a', attrs={"class": "leaf-link"}) # 인기 급상승 영역에서 'a'태그 모두 찾아 변수 cartoons에 할당
#print(f"soup = {soup}")

#search_box = driver.find_element(By.CLASS_NAME, 'gLFyf.gsfi')

# 드라이버 종료
driver.quit()
 
i = 1

pages = ""
# 반복문으로 제목 가져오기(터미널 창 출력 및 엑셀 저장)
for menu in menus: 
  title = menu.get("href") 

  driver = webdriver.Chrome(options=options) 

  url =f"https://docs.swift.org{title}" 

  print(f"url: {url}") 

  # 웹 페이지 열기
  driver.get(url)
  
  # 로딩을 위해 잠시 대기
  time.sleep(3)

  # 페이지 소스 출력
  page_source = driver.page_source
  #print(page_source)
  soup = BeautifulSoup(page_source , "lxml") 
  page = soup.find_all('main', attrs={"class": "main"}) # 인기 급상승 영역에서 'a'태그 모두 찾아 변수 cartoons에 할당
  #print(f"soup = {soup}")
  pages += str(page)
  i += 1

output_filename = 'swift_manual.html'
html_file = open(output_filename, 'w')
html_file.write(str(pages))
html_file.close()

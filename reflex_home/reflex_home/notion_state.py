import time
from notion_client import Client
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By  # By 모듈 추가
from selenium.webdriver.common.keys import Keys
from sqlmodel import select
import reflex as rx
from .models import Movie 
 
class NotionState(rx.State):
    """The app state."""
    movies: list[Movie] = []
    _notion = Client(auth="secret_qm3XicHotTo7sReAJ91YJNOqRzLui6nKw2")  # auth 파라미터 수정
    title: str
    video_id:str 
    thumbnail: str 

    def get_movies(self):
        """The onboarding page.""" 
            
        url ="https://www.youtube.com/@jocoding/videos"

        # 옵션 생성
        options = webdriver.ChromeOptions()
        # 창 숨기는 옵션 추가
        options.add_argument("headless")

        driver = webdriver.Chrome(options=options) 
        # 웹 페이지 열기
        driver.get(url)
        
        # 로딩을 위해 잠시 대기
        time.sleep(3)

        # 페이지 소스 출력
        page_source = driver.page_source
        #print(page_source)
        soup = BeautifulSoup(page_source , "lxml")

        menus = soup.find_all('a', attrs={"id": "video-title-link"})  # 인기 급상승 영역에서 'a'태그 모두 찾아 변수 cartoons에 할당
        #print(f"soup = {soup}")

        #search_box = driver.find_element(By.CLASS_NAME, 'gLFyf.gsfi')

        # 드라이버 종료
        driver.quit()
        
        # 반복문으로 제목 가져오기(터미널 창 출력 및 엑셀 저장)
        for menu in menus:   
            title = menu.get("title")  
            video_id = menu.get("href").replace("/watch?v=", "")
            movie = Movie()
            movie.title = title
            movie.video_id = video_id
            movie.thumbnail = f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"  # f-string 사용
            self.movies.append(movie) 

        print("Movies fetched and parsed successfully.")


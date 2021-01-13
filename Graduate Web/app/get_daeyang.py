import platform

from selenium import webdriver
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import shutil
import json
import time
# 세종대학교 포탈 url


def main():
    info = Daeyang("16011140" , "960923").return_info()
    print(info)
class Daeyang:
    id =""
    password = ""
    #URL = 'https://portal.sejong.ac.kr/jsp/login/loginSSL.jsp?rtUrl=classic.sejong.ac.kr/ssoLogin.do'
    URL = ""
    mybooks = []
    major = ""
    driver = ""
    html = ""
    book_pass = ""
    name = ""
    info = {
        'id': '',
        'name': '',
        'major': '',
        'year': '',
        'book': [],
        'book_pass' :''
    }
    def __init__(self , id , password): # 아이디 패스워드 받아서 진행시키기
        self.id = id
        self.password = password
        self.set_book()  # 책 권수
        self.set_major_name() # 전공
        self.set_pass() # 통과했는지 안했는지 true&false
        self.info['id'] = id
        self.info['major'] = self.major
        self.info['book'] = self.mybooks
        self.info['year'] = self.id[:2]
        self.info['name'] = self.name
        self.info['book_pass'] = self.book_pass
        self.driver.quit()
    def return_info(self):
        return self.info
    def set_major_name(self):
        soup = BeautifulSoup(self.html , 'html.parser')
        soup_major = soup.select_one("li > dl > dd")
        self.major = soup_major.string.strip().strip()
        for dd in soup_major:
            if dd.string.strip() == '' :  # 공백제거 및 필요없는 문자 지우기
                continue
            self.major = dd.string.strip()
        self.name = BeautifulSoup(self.html , 'html.parser').select("li > dl > dd")[2].string


    def set_book(self):
        self.driver = self.get_Driver()  # 크롬 드라이버 <-- 실행하는 로컬 프로젝트 내에 존재해야됨 exe 파일로 존재
        checked = self.driver.find_element_by_xpath('//*[@id="chkNos"]').get_attribute('checked')
        if checked:
            self.driver.find_element_by_xpath('//*[@id="chkNos"]').click() # 체크창 클릭
            alert = self.driver.switch_to_alert()
            print(alert.text)
            alert.dismiss()
        # id , pw 입력할 곳 찾기
        tag_id = self.driver.find_element_by_id("id")  # id 입력할곳 찾기 변수는 id태그
        tag_pw = self.driver.find_element_by_id("password")
        tag_id.clear()
        # id , pw 보내기
        tag_id.send_keys(self.id)
        tag_pw.send_keys(self.password)
        # 로그인버튼 클릭
        login_btn = self.driver.find_element_by_id('loginBtn')
        login_btn.click() # 로그인 실패했을 때 처리해야함 -> try catch 로 잡아야함
        self.driver.switch_to.frame(0)
        self.driver.find_element_by_class_name("box02").click()  # 고전독서 인증현황 페이지로 감
     #------------------------------------------------------------------------------------------------- selenium part
        self.html = self.driver.page_source  # 페이지 소스 가져오기 , -> 고전독서 인증현황 페이지 html 가져오는것
        soup = BeautifulSoup(self.html, 'html.parser')
        soup1 = soup.select_one("tbody > tr")  # tbody -> tr 태그 접근
        i = 0
        book = []  # 0 : 서양 , 1 : 동양 , 2: 동서양 ,3 : 과학 , 4 : 전체
        for td in soup1:
            if td.string.strip() == '' or td.string.strip()[0].isalpha():  # 공백제거 및 필요없는 문자 지우기
                continue
            book.append((int)(td.string.strip().strip().replace('권', '')))
        self.driver.quit()
        self.mybooks = book

    def set_pass(self):
        soup = BeautifulSoup(self.html , 'html.parser')
        soup2 = soup.find('ul' , class_= 'tblA').select('li > dl > dd')
        soup2 = soup2[7].string.replace('\n','').replace('\t' , '').strip()
        if '이수' in soup2 or '인증' in soup2:
            print("이수했습니다")
            self.book_pass = True
        else :
            print("이수하지못하였습니다")
            self.book_pass = False
        # 이수 , 인증 ,

    def get_Driver(self):
        self.URL ="https://portal.sejong.ac.kr/jsp/login/loginSSL.jsp?rtUrl=classic.sejong.ac.kr/ssoLogin.do"
        options = webdriver.ChromeOptions()
        # 크롬창을 열지않고 백그라운드로 실행
        # options.add_argument("headless")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # 다운로드될 경로 지정
        if platform.system() == 'Windows':
            root = os.getcwd() + '\\app\\uploaded_media'
        else:
            root = os.getcwd() + '/app/uploaded_media'
        options.add_experimental_option('prefs', {'download.default_directory': root})
        driver = webdriver.Chrome(
            '/Users/anjaehyeon/Desktop/2020-1학기/myselenium/chromedriver', options=options)  # 크롬드라이버의 절대경로
        driver.get(self.URL)
        return driver


if __name__ == '__main__':
    main()

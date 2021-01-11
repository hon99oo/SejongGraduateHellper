import os
import platform

from selenium import webdriver
from bs4 import BeautifulSoup
import time

class Uis():
    driver = ""
    id = ""
    pw = ""
    eng = "" # String , True / False
    def __init__(self , ID , PASSWORD):
        self.id = ID
        self.pw = PASSWORD
        self.driver = self.get_Driver()
        self.get_uis()
    def get_Driver(self):
        URL = 'https://portal.sejong.ac.kr/jsp/login/uisloginSSL.jsp?rtUrl=uis.sejong.ac.kr/app/sys.Login.servj?strCommand=SSOLOGIN'
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
            '/Users/anjaehyeon/Desktop/2020-1학기/myselenium/chromedriver' , options = options)  # 크롬드라이버의 절대경로
        driver.get(URL)
        return driver

    def get_uis(self):
        tag_id = self.driver.find_element_by_id("id")  # id 입력할곳 찾기 변수는 id태그
        tag_pw = self.driver.find_element_by_id("password")
        tag_id.clear()
        # id , pw 보내기
        tag_id.send_keys(self.id)
        tag_pw.send_keys(self.pw)
        # 로그인버튼 클릭
        login_btn = self.driver.find_element_by_id('logbtn')
        login_btn.click()
    # ------------------------------- 로그인 완료
        # 프레임전환
        self.driver.switch_to.frame(2)
        # 수업/성적 메뉴선택
        self.driver.execute_script("javascript:onMenu('SELF_STUDSELF_SUB_30');")
        # 성적 및 강의평가 선택
        self.driver.execute_script("javascript:onMenu('SELF_STUDSELF_SUB_30SCH_SUG05_STUD');")
        time.sleep(1)
        # 기이수성적조회로 클릭 이동
        self.driver.find_element_by_xpath('''//*[@id="SELF_STUDSELF_SUB_30SCH_SUG05_STUD"]/table/tbody/tr[1]''').click()
        time.sleep(1)
        # 최상위(default) 프레임으로 이동
        self.driver.switch_to.default_content()
        # 프레임 경우의 수 다 찾고 이동
        self.driver.switch_to.frame(3)
        self.driver.switch_to.frame(0)
        # 다운로드 버튼 x_path 클릭
        self.driver.find_element_by_xpath('''//*[@id="btnDownload_btn"]''').click()
        # ------------------------------------------ 영어 가져오는 part
        self.driver.switch_to_default_content()
        self.driver.switch_to.frame(2)
        self.driver.execute_script("javaScript:frameResize(this);")
        time.sleep(1)
        self.driver.execute_script("javascript:onMenu('SELF_STUDSELF_SUB_20SCH_SUH_STUD');")
        time.sleep(1)  # 자바스크립트 실행시간 기다려줘야함 must need
        self.driver.find_element_by_xpath('//*[@id="SELF_STUDSELF_SUB_20SCH_SUH_STUDSuhJudgeSelfQ"]').click()
        # k = driver.switch_to_window()
        time.sleep(1)  # 마찬가지로 창 뜨고 기다려줘야 팝업창 볼 수 있음
        mywindow = self.driver.window_handles[0] # uis 창
        popup = self.driver.window_handles[1] # 팝업 창
        self.driver.switch_to_window(popup)
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="ckb1_item0"]/table/tbody/tr/td/table/tbody/tr/td/input').click()

        self.driver.find_element_by_xpath('//*[@id="ckb2_item0"]/table/tbody/tr/td/table/tbody/tr/td/input').click()
        self.driver.find_element_by_id('btnClose_btn').click()

        #print(driver.current_window_handle)
        self.driver.switch_to_window(self.driver.window_handles[0]) # 다시 uis 창으로 윈도우 바꿔놓기
        self.driver.switch_to_frame(3) # 이 사이트에서는 프레임 0 - 3 총 4개
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')  # 드라이버의 현재 source(html) 가져오기
        #print(soup)
        #print("이부분이 첫번째프레임")
        # 3  , 1
        self.driver.switch_to_frame(0)

        soup = BeautifulSoup(self.driver.page_source , 'html.parser') # 드라이버의 현재 source(html) 가져오기
        k  = soup.find('div' , id = 'lbl179').select_one('div').string.strip().replace('\n' , '') # 영어 합격 불합격 저장하는변수 , true false 로 변경 예정

        if k == '불합격':  self.eng  = False
        elif k == '합격' : self.eng = True

        return k



# ---------------------------------------------------------------------------------------------
    # try : # 여기가 예외에 걸리는부분 !!!
    #     driver.switch_to_alert()  # 여기서 alert 뜨게되면 try 문으로 진입 그게 아니면 except 문으로 가기 (이곳이 판단 부분 !)
    #     print("alert 이 떴습니다 드라이버 종료!!!! ")
    #     driver.quit()
    #
    #
    # except Exception as error: # 로그인이 안되면 드라이버를 꺼야함 아이디 비번 일치하지 않으면 jsp 화면 뜨고 아이디나 비밀번호 둘중 하나만 입력안하면 alert 뜸
    #     time.sleep(1)
    #     driver.switch_to.frame(2)
    #     # driver.execute_script("javascript:onMenu('SELF_STUDSELF_SUB_20);")
    #     driver.execute_script("javascript:onMenu('SELF_STUDSELF_SUB_20SCH_SUH_STUD');")
    #     time.sleep(1)  # 자바스크립트 실행시간 기다려줘야함 must need
    #     driver.find_element_by_xpath('//*[@id="SELF_STUDSELF_SUB_20SCH_SUH_STUDSuhJudgeSelfQ"]').click()
    #     # k = driver.switch_to_window()
    #     time.sleep(1)  # 마찬가지로 창 뜨고 기다려줘야 팝업창 볼 수 있음
    #     mywindow = driver.window_handles[0] # uis 창
    #     popup = driver.window_handles[1] # 팝업 창
    #     driver.switch_to_window(popup)
    #     time.sleep(1)
    #     driver.find_element_by_xpath('//*[@id="ckb1_item0"]/table/tbody/tr/td/table/tbody/tr/td/input').click()
    #
    #     driver.find_element_by_xpath('//*[@id="ckb2_item0"]/table/tbody/tr/td/table/tbody/tr/td/input').click()
    #     driver.find_element_by_id('btnClose_btn').click()
    #
    #     #print(driver.current_window_handle)
    #     driver.switch_to_window(driver.window_handles[0]) # 다시 uis 창으로 윈도우 바꿔놓기
    #     driver.switch_to_frame(3) # 이 사이트에서는 프레임 0 - 3 총 4개
    #     soup = BeautifulSoup(driver.page_source, 'html.parser')  # 드라이버의 현재 source(html) 가져오기
    #     #print(soup)
    #     #print("이부분이 첫번째프레임")
    #     # 3  , 1
    #     driver.switch_to_frame(0)
    #
    #     soup = BeautifulSoup(driver.page_source , 'html.parser') # 드라이버의 현재 source(html) 가져오기
    #     k  = soup.find('div' , id = 'lbl179').select_one('div').string.strip().replace('\n' , '') # 영어 합격 불합격 저장하는변수 , true false 로 변경 예정
    #
    #     if k == '불합격' :
    #         print("진짜불합격")
    #     elif k == '합격' :
    #         print("진짜합격")
    #     driver.quit()
        # 아이디가 입력되지 않았을 때 : 학번/직번을 입력하십시요
        # 아이디가 입력되고 비밀번호는 입력되지 않았을 때 : 비밀번호를 입력하십시요.
        # 일치하지 않았을 때 : 아이디나 비밀번호가 일치하지 않습니다.





    #driver.switch_to_window(mywindow)
    #print(driver.current_window_handle)
    #CDwindow-6357E71CE601AAE9454C5646D90B4AEB
    # #-------------------------------------------------------- 마무리

    # *[ @ id = "SELF_STUDSELF_SUB_30SCH_SUG05_STUDSugRecordQ"]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    myclass = Uis('16011140' , '960923')
    print(myclass.eng)

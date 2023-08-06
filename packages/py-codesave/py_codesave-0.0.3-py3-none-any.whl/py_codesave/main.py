#!/usr/bin/env python
# coding: utf-8

# In[71]:


import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions    import NoSuchWindowException
from selenium.common.exceptions    import WebDriverException
import time

import requests
from bs4 import BeautifulSoup
import lxml
import re

from github import Github

import collections


# In[94]:


class Boj():
    """
    boj 사이트에서 정답을 맞춘 코드를 가져옵니다.
    """
    def __init__(self):
        self.result_dict = collections.defaultdict(str)
        self.check_id = ''
        self.boj_url = 'https://www.acmicpc.net/'
        chrome_option = webdriver.ChromeOptions()  # ChromeOptions 메소드를 통해 시크릿 옵션 추가
        chrome_option.add_argument("--incognito")

        self.driver = webdriver.Chrome('chromedriver.exe', options=chrome_option)
        self.crt_url = ''

    def move_url(self, target):
        self.driver.get(url=target)    
        
    def login(self):    # boj 사이트 접속
        boj_login_url = self.boj_url+'login'
        self.move_url(boj_login_url)
        
    def get_crt_url(self):
        try:
            self.crt_url = self.driver.current_url
        except NoSuchWindowException:    # 창이 종료되면 전체 종료
            sys.exit('창이 종료되었습니다. 다시 실행해주세요.')
        except WebDriverException:
            sys.exit('창이 종료되었습니다. 다시 실행해주세요.')
            
    def get_lxml(self):
        page_source = self.driver.page_source
        page_lxml = BeautifulSoup(page_source, "lxml")
        return page_lxml

    def check_page(self, url):
        if 'from_mine=1' in url:    # 현재 페이지가 제출 결과 페이지라면
            return url

    def get_code_url(self):
        solution_id = self.result_dict['제출 번호']
        code_url = self.boj_url+'source/'+solution_id
        return code_url

    def get_scoreboard(self, page_lxml):
        keys_tag = page_lxml.select('table > thead > tr > th')
        keys = [ key.get_text() for key in keys_tag ]
        scoreboard = page_lxml.select('tbody > tr')[0]    # 제일 첫번째 줄만 들고오기
        score_value = [v.get_text() for v in scoreboard]
        for i in range(9):
            self.result_dict[keys[i]] = score_value[i]

    def get_code(self, page_lxml):        
        code_html_list = page_lxml.select('.CodeMirror-line')
        code = "\n".join([code.get_text() for code in code_html_list])
        return code
        
    def get_title(self, page_lxml):
        title = page_lxml.select('table > tbody > tr > td')[3].get_text()
        return title

    def run_scoreboard(self):
        self.get_crt_url()
        if 'from_mine=1' in self.crt_url:
            scoreboard_lxml = self.get_lxml()
            self.get_scoreboard(scoreboard_lxml)
    
    def check_result(self):
        while '채점 중' in self.result_dict["결과"]:
            self.run_scoreboard()       
        if self.result_dict["결과"] == "맞았습니다!!" and self.check_id != self.result_dict["제출 번호"]:
            return 1
        else:
            return 0
        
    def run_code(self):
        self.check_id = self.result_dict["제출 번호"]
        code_url = self.get_code_url()
        self.move_url(code_url)
        code_page_lxml = self.get_lxml()
        title = self.get_title(code_page_lxml)
        code = self.get_code(code_page_lxml)
        return title, code
            
    # start
    def run(self):
        self.run_scoreboard()
        check = self.check_result()
        return check
                
class Upload():
    """
    자신의 github repository
    """
    def __init__(self, token, repository):
            self.g = Github(token)    # git login
            self.repo = self.g.get_repo(repository)
            
    def get_repo_name(self):    # github에 있는 repository name list 들고오기
        repo_list = self.repo.get_contents("Baekjoon")
        repo_name_list = [i.path.split('/')[-1] for i in repo_list]
        return repo_name_list
    
    def create_file(self, title, code):
        self.repo.create_file(f"Baekjoon/{title}.py", f"Create {title}", code, branch="master")
    
    def update_file(self, title, code):
        contents = self.repo.get_contents(f"Baekjoon/{title}.py", ref="master")
        self.repo.update_file(contents.path, f"Update {title}", code, contents.sha, branch="master")  
    
    def run(self, title, code):
        repo_name_list = self.get_repo_name()
        
        if f'{title}.py' in repo_name_list:
            self.update_file(title, code)
        else:
            self.create_file(title, code)
            
def help():
    print('원하는 사이트와 github 토큰, repository를 입력하세요.')
    print('가능한 사이트 : boj')
    print('입력예시: run(boj, 토큰값, repository)')
    
    
def run(site, token, repository):
    print(f'site: {site} \ntoken: {token} \nrepository: {repository}')
    if site == 'boj':
        boj = Boj()
    else:
        sys.exit('잘못된 사이트 입니다. 가능한 사이트 목록은 help를 통해 확인 가능합니다.')
    git = Upload(token, repository)
    boj.login()
    while 1:
        check = boj.run()
        if check == 1:
            title, code = boj.run_code()
            git.run(title, code)
        elif check == 0:
            continue  
        time.sleep(3)

if __name__ == "__main__":           
    print('백준 문제를 풀고 정답을 맞춘 코드를 자동으로 깃헙에 업로드 해줍니다.')
    print('"help()" 를 입력하면 입력예시를 포함한 사용에 도움을 줍니다. :)')


# In[ ]:





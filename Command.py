import rule_chatter as rc
import random as rd
import os
import pandas as pd

from bs4 import BeautifulSoup
import json
import requests
import re
from datetime import datetime, timedelta

import links

# rule_chatter -> Rule_Chat() -> Classified_QA_List
class Commands():
    def __init__(self):
        pass

    def Subjects(self,var):
        data = pd.read_csv('teachers.csv')
        p = re.compile('.{3,4}(?=선생님)|.{3,4}(?=쌤)')
        teacher = p.findall(var)
        for i, x in enumerate(teacher):
            teacher[i] = x.replace(' ', '')
        sss = ''
        for x in teacher:
            if x not in list(data['선생님']):
                sss += '{}이라는 이름을 가진 선생님이 검색되지 못했습니다.. 정확한 이름을 넣어주세요.'.format(x)
            else:
                main = list(data[data['선생님'] == x]['주과목'])[0]
                detailed = list(data[data['선생님'] == x]['세부과목'])[0]
                sss += '%s 선생님은 %s 과목(%s)을(를) 맡으십니다.\n' % (x, main, detailed)
        return sss

    def Subjects_teacher(self,var):
        data = pd.read_csv('teachers.csv')
        p = re.compile('.{3,5}(?=과목)')
        subs = p.findall(var)
        for i, x in enumerate(subs):
            subs[i] = x.replace(' ', '')
        sss = ''
        for x in subs:
            if x not in list(data['주과목']):
                sss += '{}라는 과목이 검색되지 못했습니다. 주과목을 입력해주세요.(ex: 물리학 과목, 생명과학 과목)\n'.format(x)
            else:
                tea = data[data['주과목'] == x]
                sss += '{} 과목을 맡으시는 선생님은'.format(x)
                teachers = list(tea['선생님'])
                detailed = list(tea['세부과목'])
                for i in range(len(teachers)):
                    sss += ' {} 선생님({})  '.format(teachers[i], detailed[i])
                sss += '입니다.\n'
        return sss

    def Today_sagam(self,var):
        sagam = rc.Load_variable("Sagam").split()
        return "{} 오늘의 생활지도 선생님은 {} 선생님이에요!".format(sagam[1],sagam[0])

    def Geupsik(self,var):
        def get_html(url):
            _html = ""
            resp = requests.get(url)
            if resp.status_code == 200:
                _html = resp.text
            return _html

        def get_meal(code, ymd, weekday):
            schMmealScCode = code  # int=
            schYmd = ymd  # str

            num = weekday+1

            URL = ("http://stu.jje.go.kr/sts_sci_md01_001.do?"
                   "schulCode=T100000156&schulCrseScCode=4&schulKndScCode=04"
                   "&schMmealScCode=%d&schYmd=%s" % (schMmealScCode, schYmd))
            html = get_html(URL)
            soup = BeautifulSoup(html, 'html.parser')
            element = soup.find_all("tr")
            element = element[2].find_all('td')
            try:
                element = element[num]  # num
                element = str(element)
                # element = element.replace('[', '')
                # element = element.replace(']', '')
                element = element.replace('<br/>', ' ')
                element = element.replace('<td class="textC last">', '')
                element = element.replace('<td class="textC">', '')
                element = element.replace('</td>', '')
                # element = element.replace('(h)', '')
                element = element.replace('.', '')
                element = element.replace('·', '')
                element = re.sub(r"\d", "", element)
            except:
                element = " "

            list_element = element.split(" ")
            list_element = list(filter(None, list_element))
            json_element = {}
            json_num = 0
            for i in list_element:
                json_element[json_num] = i
                json_num += 1

            return json_element


        today = datetime.now()
        todayDate = today.strftime("%Y.%m.%d")
        tomorrow = today + timedelta(days=1)
        tomorrowDate = tomorrow.strftime("%Y.%m.%d")

        breakfast = get_meal(1,tomorrowDate,today.weekday())
        lunch = get_meal(2,todayDate,today.weekday())
        dinner = get_meal(3,todayDate,today.weekday())

        geupsik_format = "[{}년 {}월 {}일 식단] \n\n\n <점심> \n{} <저녁> \n{} \n\n\n [{}월 {}일] \n\n <아침> {} \n\n 뭔진 몰라도 맛있겠네요!"

        return geupsik_format.format(today.year,today.month,today.day,lunch,dinner,tomorrow.month,tomorrow.day,breakfast)

    def SpecialRoom(self,var):
        return "채팅봇 자체 특별실 신청은 준비중입니다!"

    def Jaribachi(self,var):
        return links.jaribachi

    def Kkutmal(self,var):
        return links.kkutmal

    def Sadari(self,var):
        return "사다리타기는 준비중입니다!"

    def Links(self,var):
        return "\n".join(links.link_list)

    def The_Legend_of_Junsu_God(self,var):
        legends = ["그는 신이야!","ㅈㅅㅈㅅ","ㅈㅅㅁ ㅠㅠㅠㅠ","이스터에그는 이스터에그인채가 재밌는 법입니다.",
                   "번지 잘못 찾아왔나요? 그래도 찬양해요 ㅈㅅㅈㅅ"]
        return rd.choice(legends)

    def Constants(self,var):
        return "무슨 상수가 좋을지 고민중입니다!"

    def Notifications(self,var):
        notification = rc.Load_variable("Notification")
        return notification

    def Jinsu_Byeonsin(self,var):
        # 그런 거 업다
        return "진수 변환기 기능은 준비중입니다!"

    def Aca_calendar(self,var):
        url = "https://stu.jje.go.kr/sts_sci_sf01_001.do"
        now = datetime.now()
        para = {'schulCode': 'T100000156', 'schulCrseScCode': '4', 'schulKndScCode': '04', 'ay': str(now.year),
                'mm': '%02d' % (now.month)}
        re = requests.get(url, params=para)  # 나이스 학사일정 조회

        html = BeautifulSoup(re.text, 'html.parser')  # 파싱 준비
        html = html.find_all('td')  # td(테이블 구분) 태그만 불러옴

        html_size = len(html)  # 몇줄 있는지 확인
        calendar = {}

        for i in range(0, html_size):  # 날짜 및 일정 내용 분류
            html_date = str(html[i].find('em'))  # 날짜 정보 빼오기
            html_body = str(html[i].find('strong'))  # 일정 정보 빼오기

            for sakje in ['<em>', '</em>', '<em class="point2">']:
                html_date = html_date.replace(sakje, '')  # html 태그 제거

            for sakje in ['<strong>', '</strong>']:
                html_body = html_body.replace(sakje, '')  # html 태그 제거

            if html_body == "None":  # 학사일정 미 존재시
                html_body = "-"  # 안내멘트

            if html_date == "":  # 날짜정보 미 존재시
                continue  # 반복문 탈출

            calendar[html_date] = html_body  # 딕셔너리 추가

        mm = now.month
        sss = '<%d월의 학사일정>\t\n' % mm
        for key, value in calendar.items():
            sss += '%02d월 %s일: %s\t\n' % (mm, key, value)

        sss+='\n 아직도 할게 많아요!'
        return sss

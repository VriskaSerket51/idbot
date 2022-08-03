import csv

def prepare_file():
    try:
        # 이곳에서 변수를 편집합니다.
        # 귀찮으니까 파일로 입력받겠다 하지마새요
        Variables = {
            "None": "",
            "Notification": "개발진: 이디저디 채팅봇 '이디봇'이 테스트 운행중입니다! 설문조사에 참여해주세요!",
            "Sagam":"이상규 2022.08.03"
        }




        """fileread = open("variables.csv", "r")
        reader = csv.reader(fileread)

        
        for rline in reader:
            csvdata.append(rline)

        
        for wline in csvdata:
            writer.writerow(wline)"""

        csvdata = []
        filewrite = open("variables.csv", "w", newline='')
        writer = csv.writer(filewrite)
        p = [i for i in Variables.keys() if i not in [d[0] for d in csvdata]]

        print(csvdata)
        print(p)
        for t in p:
            writer.writerow([t, Variables[t]])
    except:
        return False
    return True

prepare_file()

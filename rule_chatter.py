import csv
import re
from Command import Commands


def Update_QAList():
    global path
    qa_list=[]
    with open(path+"QA.txt","r",encoding='utf-8') as qa:
        lines = qa.readlines()
        for line in lines:
            # 해당 파일에서, '#'로 시작하는 부분은 주석 처리됩니다.
            if not line.startswith("#") and "=>" in line and "," in line:
                splited = line.split("=>")
                question, ans_list = splited[0],[i for i in splited[1].split(",")]
                qa_list.append([question,ans_list])
    return qa_list

# Override file
def Update_variable(key, data):
    fileread = open(path + datafile, "r")
    reader = csv.reader(fileread)

    csvdata = []
    for rline in reader:
        csvdata.append(rline)

    filewrite = open(datafile, "w", newline='')
    writer = csv.writer(filewrite)
    for wline in csvdata:
        if wline[0] == key:
            wline = [key, data]
            writer.writerow(wline)

def Load_variable(key):
    read = open(path + datafile, "r")
    reader = csv.reader(read)

    values = dict()

    for val in reader:
        values[val[0]] = val[1]
    return values[key]

def get_value(index, question):
    # question=question.replace(".","")
    splited = [s for s in QA_List[index][0].split(".")]
    value = question
    for s in splited:
        value = value.replace(s, "")
    return value


def Load_variable(key):
    read = open(path + datafile, "r")
    reader = csv.reader(read)

    values = dict()

    for val in reader:
        values[val[0]] = val[1]

    return values[key]

def replace_value(key, answer):
    value = Load_variable(key)
    answer = answer.replace("<variable>", value)
    return answer

def run_command(index, task, key, question, answer):
    global QA_List
    if task == "Save":
        val = get_value(index, question)
        Update_variable(key, val)
    if task == "Load":
        answer = replace_value(key, answer)
    if task == "Update_qa":
        QA_List = Update_QAList()

    if task == "Add_Command":
        # Form: [ command:Q=>T,V,A ]
        try:
            Com = question.split(":")[1]
            test1 = Com.split("=>")[0]
            test2 = len(Com.split("=>")[1].split(","))
            if test2 != 3:raise Exception("형식도 못맞추는 허접♡")
            with open(path+"QA.txt","a",newline='',encoding='utf-8') as qa:
                qa.write(Com+"\n")
            answer = test1+"커맨드를 성공적으로 추가했습니다."
        except Exception as ex:
            answer = "형식에 맞지 않습니다 : " + str(ex)
    return answer

path = "./"
datafile = "variables.csv"
QA_List = Update_QAList()

def Rule_Chat(sentence,user_input):
    global datafile
    global path
    global QA_List

    Answer = ""

    Classified_QA_List = [
        Commands.Subjects,  # num 1
        Commands.Subjects_teacher,  # num 2
        Commands.Today_sagam,  # num 3
        Commands.Geupsik, # num 4
        Commands.SpecialRoom, # num 5
        Commands.Jaribachi, # num 6
        Commands.Kkutmal, # num 7
        Commands.Sadari, # num 8
        Commands.Links, # num 9
        Commands.The_Legend_of_Junsu_God, # num 10
        Commands.Constants, # num 11
        Commands.Notifications, # num 12
        Commands.Jinsu_Byeonsin, # num 13
        Commands.Aca_calendar, # num 14
    ]

    flag = False  # 룰 기반 진행 시 True, 자연어 생성으로 진행해야 할 경우 False

    if user_input.isdecimal():
        # 정의됨
        try:
            number_index = int(user_input)
        except:
            return flag
        Answer = Classified_QA_List[number_index - 1](Commands,sentence)  # Run Classified
        flag = True
    else:
        user_input.replace(".", "")
        # 기타 입력
        questions = []
        for q_index in range(len(QA_List)):
            questions.append((q_index, re.compile(QA_List[q_index][0])))

        for question in questions:
            if question[1].match(user_input):
                idx = question[0]
                Answer = run_command(idx, QA_List[idx][1][0], QA_List[idx][1][1], user_input, QA_List[idx][1][2])
                flag = True
                
    Answer = str(Answer).replace("\n","")
    return flag, Answer




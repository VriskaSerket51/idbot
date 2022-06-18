from predictor import predict_sentence, predict_classify
while(True):
    sentence=input("나: ")
    if sentence=="!종료":
        break
    k=predict_classify(sentence)
    if k==0:
        s=predict_sentence(sentence)
    else:
        s=k
    print("이디봇: "+str(s))

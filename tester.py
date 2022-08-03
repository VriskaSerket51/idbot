from predictor import predict_sentence, predict_classify
import rule_chatter as rc

while(True):
    sentence=input("나: ")
    if sentence=="!종료":
        break

    #Rule_Chat
    isUncRule,answer = rc.Rule_Chat(sentence,'nonerule')
    if (isUncRule):
        print("이디봇: "+answer)
    else:
        k=predict_classify(sentence)
        if k==0:
            # Predict_sentence
            s=predict_sentence(sentence)
        else:
            #Rule_Prepared
            s=k
            var=None
            s = rc.Rule_Chat(sentence,str(s))[1]

        print("이디봇: "+str(s))

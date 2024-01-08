

def collect_user_feedback():
    # Implemented logic to process user feedback
    feedback_list=[]
    for i in range(5):
        dic={}
        question=input("what is the question id ?")
        com=input("any comments")
        dic["question_id"]=question
        dic["comment"]=com
        feedback_list.append(dic)
    


    
    return feedback_list

from dataclasses import dataclass
import random as r 
minidb=[["QUESTION 1","a","b","c",'d',"TOPIC A"],
                            ["Q2","1","2","3","4","TOPIC B"],
                            ["Q3","MAR","VAR","PAR","RAM","TOPIC C"],
                            ["Q4","X","Y","Z","W","TOPIC D"],
                            ["Q5","1a","2b","3c","4b","TOPIC E"]]
@dataclass
class Question():
    text:str
    distractor1:str 
    distractor2: str
    distractor3: str
    correct: str
    topic: int
    user: int | None = None
class test():
    def __init__(self):
         self.display_question()
    def display_question(self):
            question=self.loadQuestion(2)
            options=[question.distractor1,question.distractor2,question.distractor3,question.correct]
            r.shuffle(options)
            self.option1=options[0]
            self.option2=options[1]
            self.option3=options[2]
            self.option4=options[3]
            print(self.option1)
            

    def loadQuestion(self,questionnum):
        questiondata=minidb[questionnum]
        text,opt1,opt2,opt3,correct,topic=questiondata
        question=Question(text=text,
                            distractor1=opt1,
                            distractor2=opt2,
                            distractor3=opt3,
                            correct=correct,
                            topic=topic)
        return question
x=test()
import tkinter as tk
import random as r
from dataclasses import dataclass
import database as db
@dataclass
class Question():
    text:str
    distractor1:str
    distractor2: str
    distractor3: str
    correct: str
    topic: int
    user: int | None = None
class QuizLogic():
    def __init__(self):
        self.database=db.database()
        self.questionanswered=0
        self.questionqueue=[]
        for i in range (r.randint(0,20)):
            qnum=r.randint(0,20)
            if qnum in self.questionqueue:
                pass
            else:
                self.questionqueue.append(qnum)
        self.currentquestionindex=0
        self.responses=[]
        self.answer = tk.StringVar()
    def submit_answer(self,answer):
        selected_answer = answer

        if self.questionanswered< len(self.questionqueue) -1:
            self.responses.append(selected_answer)
            self.questionanswered+=1
            self.currentquestionindex+=1
            print(self.responses)
            return True
        else:
            self.responses.append(selected_answer)
            self.resetQuiz()
            return False
    def markQuiz(self):
        score=0
        for i in self.questionqueue:
            question=self.loadQuestion(i)
            if self.responses[i]== question.correct:
                score+=1
        return score 
    def questionsremaining(self):
        return len(self.questionqueue)-self.questionanswered




    def loadQuestion(self,questionnum): 
        #calls the database method to fetch questions from the datbase
        questiondata=self.database.get_question_by_id(questionnum)
        text,opt1,opt2,opt3,correct,topic=questiondata
        #creates a question object using question data
        question=Question(text=text,
                            distractor1=opt1,
                            distractor2=opt2,
                            distractor3=opt3,
                            correct=correct,
                            topic=topic)
        return question 

    def resetQuiz(self):
        self.currentquestionindex=0
        self.questionanswered=0
        

from dataclasses import dataclass
import random as r 
import database as db 
from collections import Counter
from datetime import datetime,timedelta,timezone
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
         self.database=db.database()
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

    def generate_question_queue(self):
        ##Fetches the question ids from the database and randomly selects a number of questions to be used in the quiz
        available_questions = self.database.get_question_ids(7)
        self.questionqueue=[]
        weights=[]
        topicnames=[]
        topics=self.database.get_user_performance(7)
        for i in topics:
            topic_name,total_questions,numberQsAttempted,numberQsCorrect,= i
            print(f'numQsAttempted:{numberQsAttempted},numberQsCorrect:{numberQsCorrect}')
            if self.database.get_topic_attempts(7,topic_name)==0:
                    total_attempts=1
            else:
                    total_attempts=self.database.get_topic_attempts(7,topic_name=topic_name)
            print(total_attempts)
            topic_completion = (numberQsAttempted / total_questions) 
            dampened_completion= topic_completion ** 0.5 
            topic_accuracy=numberQsCorrect/total_attempts
            topic_mastery= dampened_completion * topic_accuracy
            topic_difficulty=self.database.get_topic_difficulty(topic_name=topic_name) / 10
            if topic_mastery < 1:
                topic_mastery= 1.01 - topic_mastery 
                topic_weight=topic_mastery*topic_difficulty

            weights.append(topic_weight)

            topicnames.append(topic_name)
            print(f'name:{topic_name},\n mastery:{topic_mastery},\n topic_weight:{topic_weight},\n TOPIC difficulty{topic_difficulty},\n completion:{topic_completion},\n accuracy:{topic_accuracy} \n ==========')
        maxquestions=len(available_questions)
        count= r.randint(3,maxquestions)
        self.selectedtopics = r.choices(topicnames,weights=weights,k=count)
        questions_per_topic=Counter(self.selectedtopics)
        print(questions_per_topic)
        print(f"selected topics: {self.selectedtopics}") 
        for topic_name,amount in questions_per_topic.items():
            questions=self.database.get_questions_by_topic(7,topic_name=topic_name)
            question_weights=[]
            for i in questions:
                attempts=self.database.get_attempts_by_question(user_id=7,question_id=i)
                if attempts==0:
                    distanceindays=14
                else:
                    FMT = "%Y-%m-%d %H:%M:%S"

                    last_attempt = datetime.strptime(
                        test_instance.database.get_most_recent_attempt(user_id=7, question_id=2), FMT
                    ).replace(tzinfo=timezone.utc)

                    now = datetime.now(timezone.utc)
                    days_since_attempt = (now - last_attempt).total_seconds() / 86400

                    days_since_attempt+=1
                    dampened_attempts=attempts*0.5
                    dampened_attempts+=1
                weight=days_since_attempt/ dampened_attempts
                    
                question_weights.append(weight)
            print(f'questions:{questions}')
            print(f'weights:{question_weights}')
            if amount>len(questions):
                amount=len(questions)
            for i in range(amount):
                
                selectedquestion=r.choices(questions,weights=question_weights,k=1)[0]
                print(selectedquestion)
                index = questions.index(selectedquestion)

                questions.pop(index)
                question_weights.pop(index)
                self.questionqueue.append(selectedquestion)
                
        print(self.questionqueue)

test_instance= test()
test_instance.generate_question_queue()
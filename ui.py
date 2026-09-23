import tkinter as tk
from tkinter import ttk
import random as r
from dataclasses import dataclass

main_color = "#2570C0"
accent_color = "#7FD0FB"
white_color = "#FFFFFF"
text_color = "#000000"
text_color2 = "#8317EE"
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
class controller():
    def __init__(self, root):
        self.root = root
        self.sidebar = sidebar(self.root, self)
        self.sidebar.grid(row=0, column=0, sticky="ns")  # place the sidebar
        self.frames = {Login:None, 
                       Dashboard:None,
                       Quiz:None,
                       Review:None,
                       Create:None,
                       signUp:None}

        for i in (Login,Dashboard,Quiz,Review,Create,signUp):
            frame=i(parent=root.container,controller=self)
            self.frames[i]=frame # store the frame using self.frames
            frame.grid(row=0,column=0,sticky="nsew") # place each frame
        self.show_frame(Login) # show the login frame first
        self.sidebar_visible = False
    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar.grid_remove()  # hide the sidebar
        else:
            self.sidebar.grid()  # show the sidebar
        self.sidebar_visible = not self.sidebar_visible
    def show_frame(self, frame_class):
        buttons={Login:self.sidebar.login,
                 Dashboard:self.sidebar.dashboard,
                 Quiz:self.sidebar.quiz,
                 Review: self.sidebar.review,
                 Create: self.sidebar.create}
        frame = self.frames[frame_class]
        for i in buttons.values():
            i.config(bg=white_color)
        try:
            buttons[frame_class].config(bg="#00B7FF")
        except:
            pass
        frame.tkraise() # bring the frame to the front
        self.sidebar.grid_remove()

class root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My Application")
        self.geometry("800x600")
        self.frames = {}
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0) # sidebar stays fixed width
        self.grid_columnconfigure(1, weight=1)
        self.container = tk.Frame(self)
        self.container.grid(row=0, column=1, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)


class Login(tk.Frame):
    def __init__(self, parent,controller):
        super().__init__(parent)
        self.controller = controller
        self.create_layout()
        self.create_subframes()
        self.create_widgets()
        self.controller.sidebar.grid_remove()

    def create_layout(self):
        self.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)
        self.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)
    def create_subframes(self):
        self.header= tk.Frame(self, bg=main_color)
        self.header.grid(row=0, column=0, columnspan=10, sticky='nsew')
        self.header.grid_propagate(False)
        self.header.grid_rowconfigure(0, weight=2)
        self.header.grid_rowconfigure(1, weight=1)
        self.header.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)

        self.main_content = tk.Frame(self, bg='#FFFFFF')
        self.main_content.grid_rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)
        self.main_content.grid_columnconfigure((0,1,2,3,4,5,6,7,8), weight=1)
        self.main_content.grid(row=1, column=0,rowspan=9,columnspan=10, sticky='nsew')
        self.main_content.grid_propagate(False)

    def create_widgets(self):
        self.title_label = tk.Label(self.header, text="Welcome to the Quiz Builder", font=("Helvetica", 24), bg=main_color, fg=white_color)
        self.title_label.grid(row=0, column=0, columnspan=10, sticky='nsew')

        self.username_label = tk.Label(self.main_content, text="Username:", font=("Helvetica", 14), bg=white_color, fg=text_color)
        self.username_label.grid(row=1, column=4, sticky='w')
        self.username_entry = tk.Entry(self.main_content, font=("Helvetica", 14),relief='solid', bg="#D5CECE")
        self.username_entry.grid(row=2, column=4, sticky='ew')

        self.password_label = tk.Label(self.main_content, text="Password:", font=("Helvetica", 14), bg=white_color, fg=text_color)
        self.password_label.grid(row=3, column=4, sticky='w')
        self.password_entry = tk.Entry(self.main_content, show="*", font=("Helvetica", 14),relief='solid', bg="#D5CECE")
        self.password_entry.grid(row=4, column=4, sticky='ew')

        self.login_button = tk.Button(self.main_content, text="Login", 
                                      font=("Helvetica", 14),
                                      fg=text_color, bg=accent_color, 
                                      relief='raised',command=lambda: self.controller.show_frame(Dashboard))
        self.login_button.grid(row=5, column=4, ipadx=10)

        self.signup_button = tk.Button(self.main_content, text="Sign Up", 
                                      font=("Helvetica", 14),
                                      fg=text_color, bg=accent_color, 
                                      relief='raised',command=lambda: self.controller.show_frame(signUp))
        self.signup_button.grid(row=6, column=4)

        


class Dashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_layout()
        self.create_subframes()
        self.create_widgets()

    def create_layout(self):
        self.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1)
        self.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1)

    def create_subframes(self):
        self.header= tk.Frame(self, bg="#2570C0")
        self.header.grid(row=0, column=0, columnspan=11, sticky='nsew')
        self.header.grid_propagate(False)
        self.header.grid_rowconfigure(0, weight=2)
        self.header.grid_rowconfigure(1, weight=1)
        self.header.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1)

        self.main_content = tk.Frame(self, bg='#FFFFFF')
        self.main_content.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)
        self.main_content.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)
        self.main_content.grid(row=1, column=0,rowspan=10,columnspan=11, sticky='nsew')
        self.main_content.grid_propagate(False)
        self.stats= tk.Frame(self.main_content, bg='#FFFFFF', relief='solid')
        self.stats.grid(row=3, column =5 , rowspan=8, columnspan=5, sticky='nsew')
        self.stats.grid_propagate(False)
        self.stats.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1)
        self.stats.grid_columnconfigure((0,1,2,3,4), weight=1)

        self.progress= tk.Frame(self.main_content, bg='#FFFFFF', relief='solid',bd=1)
        self.progress.grid(row=3, column =0 , rowspan=8, columnspan=5, sticky='nsew')
        self.progress.grid_propagate(False)
        self.progress.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)
        self.progress.grid_columnconfigure((0,1,2,3,4), weight=1)

        self.topics= tk.Frame(self.main_content, bg='#FFFFFF', relief='solid',bd=1)
        self.topics.grid(row=0, column =0 , rowspan=3, columnspan=11, sticky='nsew')
        self.topics.grid_propagate(False)
        self.topics.grid_rowconfigure((0,1,2,3,4,5), weight=1)
        self.topics.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)



    def create_widgets(self):
        self.title_label = tk.Label(self.header, text="Dashboard", font=("Helvetica", 24), bg=main_color, fg=white_color)
        self.title_label.grid(row=0, column=5, sticky='nsew')
        self.message_label = tk.Label(self.header, text="Welcome , Lewis", font=("Helvetica", 14), bg=main_color, fg=white_color)
        self.message_label.grid(row=1, column=5, sticky='nsew')
        self.sidebar_button=tk.Button(self.header, text="☰", font=("Helvetica", 14), bg=main_color,
                                       fg=white_color, relief='flat',command= lambda: self.controller.toggle_sidebar())
        self.sidebar_button.grid(row=0,column=0,columnspan=1,rowspan=2,sticky='nsew')

        self.progress_value = tk.IntVar(value=0)
        
        self.questionsanswered_label = tk.Label(self.stats, text="Questions Answered", font=("Helvetica", 14, "bold"), bg=white_color, fg=text_color)
        self.questionsanswered_label.grid(row=2, column=0, sticky='w', padx=(10,0))
        self.questionsanswered_value = tk.Label(self.stats, text="0", font=("Helvetica", 24, "bold"), bg=white_color, fg=text_color)
        self.questionsanswered_value.grid(row=3, column=0, sticky='w', padx=(10,0))
        
        self.topic_label = tk.Label(self.stats, text="Topics Covered", font=("Helvetica", 14, "bold"), bg=white_color, fg=text_color)
        self.topic_label.grid(row=4, column=0, sticky='w', padx=(10,0))
        self.topic_value = tk.Label(self.stats, text="0", font=("Helvetica", 24, "bold"), bg=white_color, fg=text_color)
        self.topic_value.grid(row=5, column=0, sticky='w', padx=(10,0))
        
        self.progress_label = tk.Label(self.progress, text="Topic Completion", font=("Helvetica", 14, "bold"), bg=white_color, fg=text_color)
        self.progress_label.grid(row=0, column=0, sticky='w', padx=(10,0))
        self.topic1_label = tk.Label(self.progress, text="Topic 1: 100%", font=("Helvetica", 14), bg=white_color, fg=text_color)
        self.topic1_label.grid(row=2, column=0, sticky='w', padx=(10,0))
        self.topic2_label = tk.Label(self.progress, text="Topic 2: 75%", font=("Helvetica", 14), bg=white_color, fg=text_color)
        self.topic2_label.grid(row=4, column=0, sticky='w', padx=(10,0))
        self.topic3_label = tk.Label(self.progress, text="Topic 3: 50%", font=("Helvetica", 14), bg=white_color, fg=text_color)
        self.topic3_label.grid(row=6, column=0, sticky='w', padx=(10,0))

        self.besttopic_label = tk.Label(self.topics, text="Best Topic", font=("Helvetica", 14, "bold"), bg=white_color, fg=text_color)
        self.besttopic_label.grid(row=0, column=0, sticky='w', padx=(10,0))
        self.worsttopic_label = tk.Label(self.topics, text="Worst Topic", font=("Helvetica", 14, "bold"), bg=white_color, fg=text_color)
        self.worsttopic_label.grid(row=0, column=3, sticky='w', padx=(10,0))
        self.besttopic_value = tk.Label(self.topics, text="Topic 1", font=("Helvetica", 14), bg=white_color, fg=text_color)
        self.besttopic_value.grid(row=1, column=0, sticky='w', padx=(10,0))
        self.worsttopic_value = tk.Label(self.topics, text="Topic 3", font=("Helvetica", 14), bg=white_color, fg=text_color)
        self.worsttopic_value.grid(row=1, column=3, sticky='w', padx=(10,0))
        self.quizzescompleted_label = tk.Label(self.topics, text="Quizzes Completed", font=("Helvetica", 14, "bold"), bg=white_color, fg=text_color)
        self.quizzescompleted_label.grid(row=0, column=6, sticky='w', padx=(10,0))
        self.quizzescompleted_value = tk.Label(self.topics, text="0", font=("Helvetica", 14), bg=white_color, fg=text_color)
        self.quizzescompleted_value.grid(row=1, column=6, sticky='w', padx=(10,0))

        self.progressbar=ttk.Progressbar(self.progress,orient='horizontal',length=300,mode='determinate')
        self.progressbar.step(60)
        self.progressbar.grid(row=3,column=0)

        for i in range(9):
            progressbar=ttk.Progressbar(self.progress,orient='horizontal',length=300,mode='determinate')
            progressbar.step(self.get_progress())
            if i != 1 and i % 2 !=0:
                progressbar.grid(row=i,column=0)
    def get_progress(self):
        return r.randint(0,100)

        
class Quiz(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller = controller
        self.quiz_state= True
        self.questionanswered=0
        self.questionqueue=[0,1,2,3,4]
        self.currentquestionindex=0
        self.responses=['x','x','x','x','x']
        self.create_layout()
        self.create_subframes()
        self.create_widgets()
        self.resetQuiz()
    def create_layout(self):
        self.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)
        self.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)
    def create_subframes(self):
        self.header= tk.Frame(self, bg=main_color)
        self.header.grid(row=0, column=0, columnspan=10, sticky='nsew')
        self.header.grid_propagate(False)
        self.header.grid_rowconfigure(0, weight=2)
        self.header.grid_rowconfigure(1, weight=1)
        self.header.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1)

        self.question=tk.Frame(self, bg=white_color)
        self.question.grid(row=2, column=0,rowspan=8,columnspan=10, sticky='nsew')
        self.question.grid_propagate(False)
        self.question.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)
        self.question.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)

        self.stats= tk.Frame(self, bg=white_color, relief='solid')
        self.stats.grid(row=1, column =0 ,columnspan=10, sticky='nsew')
        self.stats.grid_propagate(False)
        self.stats.grid_rowconfigure((0,1,2,3,4), weight=1)
        self.stats.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)

    def questionsremaining(self):
        return (len(self.questionqueue)-self.currentquestionindex)
    def create_widgets(self):
        # IMPLEMENT A FUNCTION THAT PREVENTS THE USER FROM SUBMITTING THE FINAL QUESTION IS PREVIOUS QUESTIONS DO NOT HAVE A RESPONSE
        self.title_label = tk.Label(self.header, text="Quiz", font=("Helvetica", 24), bg=main_color, fg=white_color)
        self.title_label.grid(row=0, column=0, sticky='nsew',columnspan=10)

        self.question_number_label = tk.Label(self.stats, text="Question 1", font=("Helvetica", 14), bg=white_color, fg=text_color)
        self.question_number_label.grid(row=0, column=0, sticky='w', padx=(10,0))
        self.questions_remaining_label = tk.Label(self.stats, text="Questions Remaining: 9", font=("Helvetica", 14), bg=white_color, fg=text_color)
        self.questions_remaining_label.grid(row=0, column=9, sticky='e', padx=(0,10))
        self.previous_button = tk.Button(self.stats, text="Previous", font=("Helvetica", 14), bg=white_color, fg=text_color, relief='raised',command=self.previousQuestion)
        self.previous_button.grid(row=0, column=1, sticky='w')

        # CREATE A SEPERATE FUNCTION TO MOVE TO THE NEXT QUESTION WITHOUT SUBMITTING RESPONSE
        self.next_button = tk.Button(self.stats, text="Next", font=("Helvetica", 14), bg=white_color, fg=text_color, relief='raised',command=self.nextQuestion)
        self.next_button.grid(row=0, column=2, sticky='w')
        self.quit_button = tk.Button(self.stats, text= 'Quit', font=("Helvetica",14), bg= white_color, fg=text_color, relief='raised',command=self.quitQuiz)
        self.quit_button.grid(row=0 ,column= 3,sticky='w')



        self.question_text = tk.Label(self.question, text="What does WAP stand for?", font=("Helvetica", 14), bg=white_color, fg=text_color)
        self.question_text.grid(row=0, column=0,sticky='nsew',columnspan=9, padx=(10,0))
        self.indicator = tk.Label(self.question,bg=main_color)
        self.answer = tk.StringVar()
        self.option1 = tk.Radiobutton(self.question, text=" Wireless Application Protocol", 
                                      variable=self.answer, value="Wireless Application Protocol", 
                                      font=("Helvetica", 14), bg=white_color, fg=text_color, selectcolor=main_color,
                                      command=lambda: self.setindicator(self.option1))
        self.option1.grid(row=1, column=4,sticky='nsew',columnspan=1, padx=(10,0))

        self.option2 = tk.Radiobutton(self.question, text=" Wide Area Protocol",
                                       variable=self.answer, value="Wide Area Protocol",
                                         font=("Helvetica", 14), bg=white_color, fg=text_color, selectcolor=main_color,
                                         command=lambda: self.setindicator(self.option2))
        self.option2.grid(row=2,column=4,sticky='nsew',columnspan=1, padx=(10,0))

        self.option3 = tk.Radiobutton(self.question, text="web application protocol",
                                       variable=self.answer, value="web application protocol",
                                         font=("Helvetica", 14), bg=white_color, fg=text_color,selectcolor=main_color
                                         ,command=lambda: self.setindicator(self.option3))
        self.option3.grid(row=3,column=4,sticky='nsew',columnspan=1, padx=(10,0))

        self.option4 = tk.Radiobutton(self.question, text="Wireless Access Point", variable=self.answer,
                                      value="Wireless Access Point", font=("Helvetica", 14),
                                        bg=white_color, fg=text_color,selectcolor=main_color,
                                        command=lambda: self.setindicator(self.option4))
        self.option4.grid(row=4,column=4,sticky='nsew',columnspan=1, padx=(10,0))
        self.submit_button = tk.Button(self.question, text="Submit",
                                        font=("Helvetica", 14),background=main_color,
                                          fg=white_color, relief='raised', command=self.submit_answer)
        
        self.submit_button.grid(row=5,column=4,sticky='ew', padx=(10,0))

    def submit_answer(self):
        selected_answer = self.answer.get()
        self.answer.set('x')
        self.responses[self.currentquestionindex]=(selected_answer)
        self.nextQuestion()
    def setindicator(self, selected_option):
        # Reset the background color of all options
        for option in [self.option1, self.option2, self.option3, self.option4]:
            option.config(bg=white_color)
        # Set the background color of the selected option
        selected_option.config(bg=accent_color)
    def allsubmitted(self):
        for i in self.responses:
            print(i)
            if i == None or i == 'x':
                print('false')
                return False
        return True
        
    def nextQuestion(self):
        try:
            self.error.grid_forget()
        except:
            pass
        
        if self.questionanswered < len(self.questionqueue):
            print(self.responses)
            self.display_question(self.questionqueue[self.currentquestionindex])
            for option in [self.option1, self.option2, self.option3, self.option4]:
                option.config(bg=white_color)
            self.questionanswered+=1
            self.currentquestionindex+=1
        elif self.currentquestionindex == len(self.questionqueue): # quiz complete successfully
            if self.allsubmitted:
                self.quiz_state=False
                self.controller.show_frame(Review)
                self.resetQuiz()
            else:
                self.redoQuestion
        else:
            #display the question where the response == None
            while self.allsubmitted != True:
                self.redoQuestion()

    def redoQuestion(self):
        for i in range (len(self.responses)):
            if self.responses [i] == 'x':
                self.display_question(self.questionqueue[i])
    def previousQuestion(self):
        if self.currentquestionindex > 0:
            self.currentquestionindex-=1
            self.display_question(self.questionqueue[self.currentquestionindex])
            for option in [self.option1, self.option2, self.option3, self.option4]:
                option.config(bg=white_color)
        else:
            self.error=tk.Label(self.stats, text="No Previous Questions", font=("Helvetica", 18,'bold'), bg=white_color, fg="#DB0000")
            self.error.grid(row=0,column=4,sticky='ew')

            

    def display_question(self,questionnum):
            self.question_number_label.config(text=f'Question {self.currentquestionindex}')
            self.questions_remaining_label.config(text=f'Questions Remaining: {self.questionsremaining()}')
            question=self.loadQuestion(questionnum)
            self.question_text.config(text=question.text)
            options=[question.distractor1,question.distractor2,question.distractor3,question.correct]
            #r.shuffle(options)
            self.option1.config(text=options[0],value=options[0])
            self.option2.config(text=options[1],value=options[1])
            self.option3.config(text=options[2],value=options[2])
            self.option4.config(text=options[3],value=options[3])



    def loadQuestion(self,questionnum): # This will interact with the database in the real project, seperating database code from program logic
        questiondata=minidb[questionnum]
        text,opt1,opt2,opt3,correct,topic=questiondata
        question=Question(text=text,
                            distractor1=opt1,
                            distractor2=opt2,
                            distractor3=opt3,
                            correct=correct,
                            topic=topic)
        return question 

    def resetQuiz(self):
        self.answer.set('x')
        self.currentquestionindex=0
        self.display_question(self.currentquestionindex)
        for option in [self.option1, self.option2, self.option3, self.option4]:
            option.config(bg=white_color)
        try:
            self.error.grid_forget()
        except: 
            pass 
    def quitQuiz(self):
        self.controller.show_frame(Dashboard)
        self.resetQuiz()

class Review(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller = controller
        self.create_layout()
        self.create_subframes()
        self.create_widgets()
    def create_layout(self):
        self.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)
        self.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)
    def create_subframes(self):
        self.header= tk.Frame(self, bg=main_color)
        self.header.grid(row=0, column=0, columnspan=10, sticky='nsew')
        self.header.grid_propagate(False)
        self.header.grid_rowconfigure(0, weight=2)
        self.header.grid_rowconfigure(1, weight=1)
        self.header.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1)

        self.question=tk.Frame(self, bg=white_color)
        self.question.grid(row=2, column=0,rowspan=8,columnspan=10, sticky='nsew')
        self.question.grid_propagate(False)
        self.question.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)
        self.question.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)

        self.stats= tk.Frame(self, bg=white_color, relief='solid')
        self.stats.grid(row=1, column =0 ,columnspan=10, sticky='nsew')
        self.stats.grid_propagate(False)
        self.stats.grid_rowconfigure((0,1,2,3,4), weight=1)
        self.stats.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)

    def create_widgets(self):
        self.title_label = tk.Label(self.header, text="Review", font=("Helvetica", 24), bg=main_color, fg=white_color)
        self.title_label.grid(row=0, column=0, sticky='nsew',columnspan=10)

        self.score_label = tk.Label(self.stats, text="Score: 8", font=("Helvetica", 14,"bold"), 
                                    bg=white_color, fg=text_color)
        self.score_label.grid(row=0, column=0, sticky='w', padx=(10,0))
        self.previous_button = tk.Button(self.stats, text="Previous",font=("Helvetica", 14), bg=white_color,fg=text_color, relief='raised',width=10)
        self.previous_button.grid(row=0, column=9, sticky='e')
        self.next_button = tk.Button(self.stats, text="Next",font=("Helvetica", 14), bg=white_color,fg=text_color, relief='raised',width=10)
        self.next_button.grid(row=0, column=8, sticky='e')
        self.question_number_label = tk.Label(self.stats, text="Question 1", font=("Helvetica", 14),
                                               bg=white_color, fg=text_color)
        self.question_number_label.grid(row=0, column=1,sticky='w', padx=(10,0))
        self.status_label = tk.Label(self.stats, text="Correct", font=("Helvetica", 14),
                                          bg=white_color, fg="#00FF00")
        self.status_label.grid(row=0, column=2,sticky='w', padx=(10,0))
        self.totalquestions_label = tk.Label(self.stats, text="Questions: 10", font=("Helvetica", 14),
                                              bg=white_color, fg=text_color)
        self.totalquestions_label.grid(row=0, column=3, sticky='w', padx=(10,0))


        self.question_label = tk.Label(self.question, text="What does WAP stand for?", font=("Helvetica", 14, "bold"),
                                        bg=white_color, fg=text_color)
        self.question_label.grid(row=0, column=0,sticky='nsew',columnspan=9, padx=(10,0))
        self.option1_label = tk.Label(self.question, text="1.Wireless Application Protocol", font=("Helvetica", 14),
                                 bg=white_color, fg=text_color)
        self.option1_label.grid(row=1, column=0, sticky='nsew',columnspan=9, padx=(10,0))
        self.option2_label = tk.Label(self.question, text="2.Wide Area Protocol", font=("Helvetica", 14),
                                 bg=white_color, fg=text_color)
        self.option2_label.grid(row=2, column=0, sticky='nsew', columnspan=9,padx=(10,0))
        self.option3_label = tk.Label(self.question, text="3.Web application protocol", font=("Helvetica", 14),
                                 bg=white_color, fg=text_color)
        self.option3_label.grid(row=3, column=0, sticky='nsew', columnspan=9, padx=(10,0))
        self.option4_label = tk.Label(self.question, text="4.Wireless Access Point", font=("Helvetica", 14,'bold'),
                                 bg=white_color, fg="#00FF00")
        self.option4_label.grid(row=4, column=0, sticky='nsew', padx=(10,0), columnspan=9)

        self.sidebar_button = tk.Button(self.header, text="☰", font=("Helvetica", 14), bg=main_color, fg=white_color, relief='flat', command=self.controller.toggle_sidebar)
        self.sidebar_button.grid(row=0, column=0, sticky='w', padx=(10,0))
    
class sidebar(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2570C0")
        self.controller = controller
        self.create_widgets()
        self.create_layout()
        

    def create_layout(self):
        self.grid_rowconfigure((0,1,2,3,4,5,6,8,9,10,11), weight=1)

    def create_widgets(self):
        self.login = tk.Button(
            self, text="Login",bg=white_color,fg=main_color,
            command=lambda: self.controller.show_frame(Login))
        self.login.grid(row=2,column=0,sticky='ew')
        
        self.dashboard = tk.Button(
            self, text="Dashboard",bg=white_color,fg=main_color,
            command=lambda: self.controller.show_frame(Dashboard)
        )
        self.dashboard.grid(row=4, column=0, sticky="ew")

        self.quiz = tk.Button(
            self, text="Quiz", bg=white_color,fg=main_color,
            command=lambda: self.controller.show_frame(Quiz)
        )
        self.quiz.grid(row=6, column=0, sticky="ew")

        self.review = tk.Button(
            self, text="Review",bg=white_color,fg=main_color,
            command=lambda: self.controller.show_frame(Review)
        )
        self.review.grid(row=8, column=0, sticky="ew")
        
        self.create=tk.Button(self,text='Create Question',
        bg=white_color,fg=main_color,
        command=lambda:self.controller.show_frame(Create))
        self.create.grid(row=10,column=0,sticky='ew')

        


class Create(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent,bg=white_color)

        self.controller=controller
        self.create_layout()
        self.create_subframes()
        self.create_widgets()

    def create_layout(self):
        self.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9),weight=1)
        self.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9),weight=1)

    def create_subframes(self):
        self.header= tk.Frame(self, bg=main_color)
        self.header.grid(row=0, column=0, columnspan=10, sticky='nsew')
        self.header.grid_propagate(False)
        self.header.grid_rowconfigure(0, weight=2)
        self.header.grid_rowconfigure(1, weight=1)
        self.header.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1)
        self.main_content=tk.Frame(self,bg=white_color)
        self.main_content.grid(row=1,column=0,columnspan=10,rowspan=9,sticky="nsew")
        self.main_content.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9),weight=1)
        self.main_content.grid_columnconfigure((0,1,2,4,5,6,7,8,9),weight=1)

    def create_widgets(self):

        self.header_text=tk.Label(self.header,text="Create Question", fg= white_color ,bg=main_color,font=("Helvetica",24))
        self.header_text.grid(row=0,column=0,columnspan=10,sticky='nsew')
        self.text_label=tk.Label(self.main_content,text='Question Text:',fg=text_color,bg=white_color, font=("Helvetica", 14))
        self.text_label.grid(row=1,column=0,sticky='w',padx=(10,0))
        self.question_text = tk.Entry(self.main_content, font=("Helvetica", 14),relief='solid', bg="#D5CECE")
        self.question_text.grid(row=1, column=1, sticky='w')

        self.distractorlabels=tk.Label(self.main_content,text='Distractor Responses',
                                       fg=text_color,bg=white_color, font=("Helvetica", 14))
        for i in range(3,6):
            f=tk.Label(self.main_content,text=f'Distractor {i-2}',fg=text_color,bg=white_color, font=("Helvetica", 14))
            f.grid(row=i,column=0,sticky='w')

        self.distractor1=tk.Entry(self.main_content,font=('Helvetica',14),relief="solid",bg='#D5CECE')
        self.distractor2=tk.Entry(self.main_content,font=('Helvetica',14),relief="solid",bg='#D5CECE')
        self.distractor3=tk.Entry(self.main_content,font=('Helvetica',14),relief="solid",bg='#D5CECE')
        self.distractor1.grid(row=3,column=1,sticky='ew')
        self.distractor2.grid(row=4,column=1,sticky='ew')
        self.distractor3.grid(row=5,column=1,sticky='ew')

        self.correct_answer=tk.Entry(self.main_content,font=('Helvetica',14),relief="solid",bg="#D5CECE")
        self.correct_answer.grid(row=7,column=1,sticky='w')
        self.correct_answer_label=tk.Label(self.main_content,text="Correct Choice",fg="#84C470",bg=white_color,font=("Helvetica",14))
        self.correct_answer_label.grid(row=7,column=0,sticky="w")

        self.value=tk.StringVar()
        self.value.set("Select a Topic")
        self.optionlist=['System Architecture','Operating Systems','Data Structures & Algorithms','Boolean Algebra','Networking','Ethics & Legislation','Applications Generation']
        self.topic=tk.OptionMenu(self.main_content,self.value,*self.optionlist)

        # Change to actual function later
        self.submit_button=tk.Button(self.main_content,text="Create Question",bg=main_color,fg=white_color,relief='raised',command=print("Question Created "))
        self.submit_button.grid(row=3, column=6,sticky='ew')
        self.topic.grid(row=1 ,column= 6,sticky='ew')
        self.sidebar_button = tk.Button(self.header, text="☰", font=("Helvetica", 14), bg=main_color, fg=white_color, relief='flat', command=self.controller.toggle_sidebar)
        self.sidebar_button.grid(row=0, column=0, sticky='w', padx=(10,0))
class signUp(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent,bg=white_color)
    
        self.controller=controller
        self.create_layout()
        self.create_subframes()
        self.create_widgets()

    def create_layout(self):
        self.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9),weight=1)
        self.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9),weight=1)

    def create_subframes(self):
        self.header= tk.Frame(self, bg=main_color)
        self.header.grid(row=0, column=0, columnspan=10, sticky='nsew')
        self.header.grid_propagate(False)
        self.header.grid_rowconfigure(0, weight=2)
        self.header.grid_rowconfigure(1, weight=1)
        self.header.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1)
        self.main_content=tk.Frame(self,bg=white_color)
        self.main_content.grid(row=1,column=0,columnspan=10,rowspan=9,sticky="nsew")
        self.main_content.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9),weight=1)
        self.main_content.grid_columnconfigure((0,1,2,4,5,6,7,8,9),weight=1)
    def create_widgets(self):
        self.title_label = tk.Label(self.header, text="Sign Up", font=("Helvetica", 24), bg=main_color, fg=white_color)
        self.title_label.grid(row=0, column=0, columnspan=10,sticky='nsew')
        self.username_label = tk.Label(self.main_content, text="Username:", font=("Helvetica", 14), bg=white_color, fg=text_color)
        self.username_label.grid(row=2, column=0, columnspan=9)
        self.username_entry = tk.Entry(self.main_content, font=("Helvetica", 14),relief='solid', bg="#D5CECE")
        self.username_entry.grid(row=3, column=0, columnspan=9)

        self.password_label = tk.Label(self.main_content, text="Password:", font=("Helvetica", 14), bg=white_color, fg=text_color)
        self.password_label.grid(row=4, column=0, columnspan=9)
        self.password_entry = tk.Entry(self.main_content, show="*", font=("Helvetica", 14),relief='solid', bg="#D5CECE")
        self.password_entry.grid(row=5, column=0, columnspan=9)

        self.signUp_button = tk.Button(self.main_content, text="Create Account", 
                                        font=("Helvetica", 14),
                                        fg=text_color, bg=accent_color, 
                                        relief='raised',command=lambda: self.controller.show_frame(Dashboard))
        self.signUp_button.grid(row=6, column=0, columnspan=9)
    
    
if __name__ == "__main__":
    app = root()
    controller = controller(app)
    app.mainloop()

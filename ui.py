import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random as r
from dataclasses import dataclass
import sqlite3 as sql

from click import progressbar

main_color = "#2570C0"
accent_color = "#7FD0FB"
white_color = "#FFFFFF"
text_color = "#000000"
text_color2 = "#8317EE"
error_color = "#DB0000"
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
@dataclass
class uprogress():
    topic: str
    numberQsAttempted: int
    numberQsCorrect: int
    total_questions: int
    topic_completion: float
    
class controller():
    def __init__(self, root):
        self.root = root
        self.database = database(controller=self)
        self.sidebar = sidebar(self.root, self)
        self.sidebar.grid(row=0, column=0, sticky="ns")  # place the sidebar
        self.current_user = None  
        self.frames = {Login:None, 
                       Dashboard:None,
                       Quiz:None,
                       Review:None,
                       Create:None,
                       signUp:None}
        for i in (Login,Dashboard,Quiz,Review,Create,signUp):
            frame=i(parent=root.container,controller=self,database=self.database)
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


class database():
    def __init__(self,controller):
        self.controller=controller
        self.conn = sql.connect("quiz.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")  # Enable foreign key support
        self.create_database()
    def create_database(self):
        #====USERS=====
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        #============QUESTIONS ======
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS questions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL,
            choice1 TEXT NOT NULL,
            choice2 TEXT NOT NULL,
            choice3 TEXT NOT NULL,
            correct_choice TEXT NOT NULL,
            topic_id INTEGER NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
            FOREIGN KEY (topic_id) REFERENCES topics(id)
        )''')

        #=======TOPICS======
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS topics(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_name TEXT NOT NULL,
            total_questions INTEGER,
            topic_difficulty INTEGER
        )''')
        #======QUIZZES======
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS quizzes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            accuracy REAL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )''')
        #=USER_QUESTIONS=========
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user_questions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            question_id INTEGER,
            user_answer TEXT,
            is_correct BOOLEAN,
            attempt_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user_performance(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            topic_id INTEGER,
            numberQsAttempted INTEGER DEFAULT 0,
            numberQsCorrect INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (topic_id) REFERENCES topics(id)
        )''')
        self.conn.commit()
    def add_user(self, username, password):
        if username == "" or password == "":
            self.error=tk.Label(self.controller.frames[signUp], text="Username or Password cannot be empty", font=("Helvetica", 14), bg=white_color, fg=error_color)
            self.error.grid(row=9, column=4, sticky='ew')

            return False  # Indicate that the user was not added due to empty fields
        if len(username) < 3 or len(username)>30:
            self.error=tk.Label(self.controller.frames[signUp],text='Username must be between 3 and 30 characters',font=("Helvetica",14),bg=white_color,fg=error_color)
            self.error.grid(row=9, column=4,sticky='ew')
            return False
        if len(password) < 6 :
            self.error=tk.Label(self.controller.frames[signUp],text='Password must be at least 6 characters',font=("Helvetica",14),bg=white_color,fg=error_color)
            self.error.grid(row=9, column=4, sticky='ew')
            return False

        if self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone():
            self.error=tk.Label(self.controller.frames[signUp], text="Username already exists", font=("Helvetica", 14), bg=white_color, fg=error_color)
            self.error.grid(row=9, column=4, sticky='ew')
            return False
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.conn.commit()
        return True
    def validate_login(self, username, password):
            self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = self.cursor.fetchone()
            if user:
                self.controller.current_user=user[0]
                return True
            else:
                self.error=tk.Label(self.controller.frames[Login], text="Invalid username or password", font=("Helvetica", 14), bg=white_color, fg=error_color)
                self.error.grid(row=9, column=0, sticky='nsew',columnspan=10)
                return False
    def add_question(self, question_text, choice1, choice2, choice3, correct_choice, topic, user_id):

        if not all([question_text, choice1, choice2, choice3, correct_choice]) or topic == "Select a Topic":
            self.error=tk.Label(self.main_content,text="Please fill in all fields and select a topic.",fg=error_color,bg=white_color,font=("Helvetica",12))
            self.error.grid(row=10,column=0,columnspan=9,sticky='nsew')
            return False
        if len(set([choice1, choice2, choice3, correct_choice])) < 4:
            self.error=tk.Label(self.main_content,text="All answer choices must be unique.",fg=error_color,bg=white_color,font=("Helvetica",12))
            self.error.grid(row=10,column=0,columnspan=9,sticky='nsew')
            return False
        self.cursor.execute("SELECT id FROM topics WHERE topic_name = ?", (topic,))
        self.topic_id = self.cursor.fetchone()[0]
        self.cursor.execute('''INSERT INTO questions (question_text, choice1, choice2, choice3, correct_choice, topic_id, user_id)
                               VALUES (?, ?, ?, ?, ?, ?, ?)''',
                            (question_text, choice1, choice2, choice3, correct_choice, self.topic_id, user_id))
        self.conn.commit()
        return True
    def get_user_performance(self, user_id):
        self.cursor.execute('''SELECT topics.topic_name, user_performance.numberQsAttempted, user_performance.numberQsCorrect,topics.total_questions
                               FROM user_performance
                               JOIN topics ON user_performance.topic_id = topics.id
                               WHERE user_performance.user_id = ?''', (user_id,))
        return self.cursor.fetchall()
    def get_username(self, user_id):
        self.cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None
    def get_question_by_id(self, question_id):
        self.cursor.execute('''SELECT question_text, choice1, choice2, choice3, correct_choice, topic_id 
                            FROM questions 
                            WHERE id = ?''', (question_id,))
        return self.cursor.fetchone()
            
            
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
    def __init__(self, parent,controller,database):
        super().__init__(parent)
        self.controller = controller
        self.database = database
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
                                      relief='raised',command=lambda: self.login())
        self.login_button.grid(row=5, column=4, ipadx=10)

        self.signup_button = tk.Button(self.main_content, text="Sign Up", 
                                      font=("Helvetica", 14),
                                      fg=text_color, bg=accent_color, 
                                      relief='raised',command=lambda: self.controller.show_frame(signUp))
        self.signup_button.grid(row=6, column=4)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.database.validate_login(username, password):
            self.controller.show_frame(Dashboard)
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        else:
            pass


class Dashboard(tk.Frame):
    def __init__(self, parent, controller, database):
        super().__init__(parent)
        self.controller = controller
        self.database = database
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

        #creates the progress bars and adds them to a list for easy access 
        self.progressbars=[]
        for i in range(9):
            progressbar=ttk.Progressbar(self.progress,orient='horizontal',length=300,mode='determinate')
            if i != 1 and i % 2 !=0:
                progressbar.grid(row=i,column=0)
                self.progressbars.append(progressbar)
    # updates the progress bars based on the user's performance in the database
    def update_progressbars(self):
        self.topics=self.get_progress()
        for i in range(3):
            try:
                self.topic1_label.config(text=f"{self.topics[0].topic}: {self.topics[0].topic_completion}%")
                self.topic2_label.config(text=f"{self.topics[1].topic}: {self.topics[1].topic_completion}%")
                self.topic3_label.config(text=f"{self.topics[2].topic}: {self.topics[2].topic_completion}%")
                self.progressbars[i].step(self.topics[i].topic_completion)
            except IndexError:
                pass
    # updates the dashboard with the user's username 
    def update_dashboard(self):
        self.username=self.database.get_username(self.controller.current_user)
        print(self.username)
        self.message_label = tk.Label(self.header, text=f"Welcome , {self.username.title()}", font=("Helvetica", 14), bg=main_color, fg=white_color)
        self.message_label.grid(row=1, column=5, sticky='nsew')
    #gets the user's progress from the database, turns each record into an object and returns a list of objects sorted by completion percentage
    def get_progress(self):
        topics = []
        self.performance = self.database.get_user_performance(self.controller.current_user)

        for i in self.performance:
            topic_name, numberQsAttempted, numberQsCorrect, total_questions = i
            if total_questions > 0:
                topic_completion = (numberQsAttempted / total_questions) * 100
            else:
                topic_completion = 0
            topic= uprogress(topic=topic_name,
                             numberQsAttempted=numberQsAttempted,
                             numberQsCorrect=numberQsCorrect,
                             total_questions=total_questions,topic_completion=topic_completion)
            topics.append(topic)
            #Sorts the topics based on completion percentage in descending order
        topics.sort(key=lambda x: x.topic_completion, reverse=True)
        return topics[:3]

        
class Quiz(tk.Frame):
    def __init__(self,parent,controller,database):
        super().__init__(parent)
        self.controller = controller
        self.database = database
        self.quiz_state= True
        self.questionanswered=0
        self.questionqueue=[2,3,4,5,6]
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
        self.title_label = tk.Label(self.header, text="Quiz", font=("Helvetica", 24), bg=main_color, fg=white_color)
        self.title_label.grid(row=0, column=0, sticky='nsew',columnspan=10)

        self.question_number_label = tk.Label(self.stats, text="Question 1", font=("Helvetica", 14), bg=white_color, fg=text_color)
        self.question_number_label.grid(row=0, column=0, sticky='w', padx=(10,0))
        self.questions_remaining_label = tk.Label(self.stats, text="Questions Remaining: 9", font=("Helvetica", 14), bg=white_color, fg=text_color)
        self.questions_remaining_label.grid(row=0, column=9, sticky='e', padx=(0,10))
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
        self.answer.set('')
        try:
            self.SubmitError.grid_forget()
        except:
            print('no error')
        if self.questionanswered< len(self.questionqueue) -1:
            if selected_answer != '':
                self.responses[self.currentquestionindex]=selected_answer
                self.questionanswered+=1
                self.currentquestionindex+=1
                print(self.responses)
                self.nextQuestion()
            else:
                self.SubmitError=tk.Label(self.stats, text="No Response selected", font=("Helvetica", 18,'bold'), bg=white_color, fg=error_color)
                self.SubmitError.grid(row=0,column=4,sticky='ew')
        else:
            self.quiz_state=False
            self.controller.show_frame(Review)
            self.responses[self.currentquestionindex]=selected_answer
            self.resetQuiz()

    def markQuiz(self):
        score=0
        for i in self.questionqueue:
            question=self.loadQuestion(i)
            if self.responses[i]== question.correct:
                score+=1
        return score 
            
    def setindicator(self, selected_option):
        # Reset the background color of all options
        for option in [self.option1, self.option2, self.option3, self.option4]:
            option.config(bg=white_color)
        # Set the background color of the selected option
        selected_option.config(bg=accent_color)
   
    def nextQuestion(self):
        if self.questionanswered < len(self.questionqueue):
            self.display_question(self.questionqueue[self.currentquestionindex])
            for option in [self.option1, self.option2, self.option3, self.option4]:
                option.config(bg=white_color)

            

    def display_question(self,questionnum):
            self.question_number_label.config(text=f'Question {self.currentquestionindex}')
            self.questions_remaining_label.config(text=f'Questions Remaining: {self.questionsremaining()}')
            question=self.loadQuestion(self.questionqueue[self.currentquestionindex])
            self.question_text.config(text=question.text)
            options=[question.distractor1,question.distractor2,question.distractor3,question.correct]
            #r.shuffle(options)
            self.option1.config(text=options[0],value=options[0])
            self.option2.config(text=options[1],value=options[1])
            self.option3.config(text=options[2],value=options[2])
            self.option4.config(text=options[3],value=options[3])



    def loadQuestion(self,questionnum): 
        #in the real project, there will be a method to select the questions using the weighted algorithm, 
        # and these ids will be passed in 
        questiondata=self.database.get_question_by_id(questionnum)
        text,opt1,opt2,opt3,correct,topic=questiondata
        question=Question(text=text,
                            distractor1=opt1,
                            distractor2=opt2,
                            distractor3=opt3,
                            correct=correct,
                            topic=topic)
        return question 

    def resetQuiz(self):
        self.answer.set(None)
        self.currentquestionindex=0
        self.questionanswered=0
        self.display_question(self.currentquestionindex)
        for option in [self.option1, self.option2, self.option3, self.option4]:
            option.config(bg=white_color)
        try:
            self.error.grid_forget()
            self.SubmitError.grid_forget()
        except: 
            pass 
    def quitQuiz(self):
        self.controller.show_frame(Dashboard)
        self.resetQuiz()

class Review(tk.Frame):
    def __init__(self,parent,controller,database):
        super().__init__(parent)
        self.controller = controller
        self.database = database
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
    def __init__(self,parent,controller,database):
        super().__init__(parent,bg=white_color)
        self.database=database
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
        self.submit_button=tk.Button(self.main_content,text="Create Question",bg=main_color,fg=white_color,relief='raised',command=self.create_question)
        self.submit_button.grid(row=3, column=6,sticky='ew')
        self.topic.grid(row=1 ,column= 6,sticky='ew')
        self.sidebar_button = tk.Button(self.header, text="☰", font=("Helvetica", 14), bg=main_color, fg=white_color, relief='flat', command=self.controller.toggle_sidebar)
        self.sidebar_button.grid(row=0, column=0, sticky='w', padx=(10,0))
    def create_question(self):
        question_text = self.question_text.get()
        distractor1 = self.distractor1.get()
        distractor2 = self.distractor2.get()
        distractor3 = self.distractor3.get()
        correct_answer = self.correct_answer.get()
        topic = self.value.get()
        try:
            self.database.error.grid_forget()
        except:
            pass

        
        if self.database.add_question(question_text=question_text, 
                                   choice1=distractor1,
                                   choice2=distractor2, 
                                   choice3=distractor3, 
                                   correct_choice=correct_answer, 
                                   topic=topic,
                                   user_id=self.controller.current_user):
            
            self.message=tk.Label(self.main_content,text="Question Created Successfully!",fg=main_color,bg=white_color,font=("Helvetica",16))
            self.message.grid(row=8,column=0,columnspan=9,sticky='nsew')
        else:
            pass
class signUp(tk.Frame):
    def __init__(self,parent,controller,database):
        super().__init__(parent,bg=white_color)
    
        self.controller=controller
        self.database=database
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
                                        relief='raised',command=lambda: self.create_account())
        self.signUp_button.grid(row=6, column=0, columnspan=9)
    def create_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.database.add_user(username, password):
            self.controller.show_frame(Login)
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            try:
                self.controller.error.grid_forget()
                self.database.error.grid_forget()
            except:
                pass
        else:
            pass

if __name__ == "__main__":
    app = root()
    controller = controller(app)
    app.mainloop()

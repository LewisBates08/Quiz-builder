import tkinter as tk
# CONTROLLER CLASS
# PASSED INTO EACH CLASS IN ORDER TO USE STANDARD METHODS
class App(tk.Tk):
    def __init__(self):
        #=====ROOT FRAME CREATION==========
        super().__init__() # calls constructors for tk instance to create a root frame
        #Sets attributes for root frame using setters
        self.title("Quiz Builder")
        self.geometry("800x500")
        #====GLOBAL VARIABLES====
        self.score=0 
        self.qsanswered= 0
        self.quizzesTaken=0
        self.sbtoggle=True
        self.frames={}
        #=======MAIN SUBFRAME==================
        #creates a containter which stores all frames
        container= tk.Frame(self)
        container.grid(row=0, column=1, sticky="nsew")

        #=====HEADER FRAME =======
        self.header=tk.Frame(self,background="#F0E9E9",height=60)
        self.header.propagate(False)
        self.header.grid_columnconfigure(0,weight=1)
        
        #======GRID CONFIG=========
        #tells the grid to expand into the space left by the root frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)


        
        ##=====SIDEBAR=========
        #Creates sub frame for sidebar
        self.sidebar=tk.Frame(self,width=200,background="#5276F6")
        self.sidebar.grid(row=0,column=0,sticky="ns")
        self.sidebar.propagate(False) # Prevents sidebar resizing 
        tk.Label(self.sidebar,text="Quiz Builder", font= ("Arial", 18 , "underline"),background="#5276F6"
        ).pack(pady=30,padx=10)
        #Log Out Button
        self.log=tk.Button(self.sidebar,
                      text="Log Out",
                      command=lambda:self.logOut(),
                      highlightbackground="#5276F6")
        #Dashboard button
        self.dash=tk.Button(self.sidebar,
                            text="Dashboard",
                            command=lambda:self.dashboard(),
                            highlightbackground="#5276F6")
        #Quiz Button
        self.quiz=tk.Button(self.sidebar,
                            text="Start Quiz",
                            command=lambda:self.showFrame(Quiz),
                            highlightbackground="#5276F6")
        #Displays each button
        self.log.pack(pady=28)
        self.dash.pack(pady=26)
        self.quiz.pack(pady=24)
        #Toggle sidebar on off (togglesidebar function)
        self.toggle=tk.Button(self,text="Menu",command=lambda:self.togglesidebar(sidebar=self.sidebar))
        self.toggle.grid(row=0,column=0,sticky="n")
        
        ##=====FRAME CREATION=======
        # creates an instance of the frame, passing in the container frame as a base 
        #and the current class(App) as a controller to allow for manipulation through the class
        for i in (Login,Dashboard,Quiz,Progress):
            frame=i(parent=container,controller=self)
            self.frames[i]=frame # store the frame using self.frames
            frame.grid(row=0,column=0,sticky="nsew") # place each frame
        self.showFrame(Login)
        self.removeSidebar()
    #====SHOW FRAME=====
    # shows the frame lol        
    def showFrame(self,frame):
        f= self.frames[frame]
        f.tkraise()

    #===SIDEBAR CONTROL====
    def dashboard(self):
        self.frames[Quiz].endQuiz(self)
        self.showFrame(Dashboard)
    #hide/unhide sidebar... pretty self explanatory i guess
    def removeSidebar(self):
        self.toggle.grid_forget()
        self.sidebar.grid_forget()
    def createSidebar(self):
        self.toggle.grid(row=0,column=0,sticky="n")
        self.sidebar.grid(row=0,column=0,sticky="ns")
    
    ##=====SIDEBAR LOG OUT BUTTON=======
    # clears entry boxes when user is logged out, hides sidebar, etc. 
    def logOut(self):
        loginframe=self.frames[Login]
        loginframe.username.delete(0,tk.END)
        loginframe.password.delete(0,tk.END)
        self.showFrame(Login)
        self.removeSidebar()
    
    ##====TOGGLE SIDEBAR=====
    #Checks is sidebar is being displayed , changes to the opposite state
    def togglesidebar(self,sidebar):
            if self.sbtoggle==True:
                sidebar.grid_forget()
                self.sbtoggle=False
            else:
                sidebar.grid(row=0,column=0,sticky="ns")
                self.sbtoggle=True
            
#Creates the login screen using the frame class
class Login(tk.Frame):
    def __init__(self,parent,controller):
        #=====FRAME CONFIG==========
        self.controller=controller 
        super().__init__(parent)# initialises the frame using tk frame class, passing in the container frame to act as a base
        
        #tells each row/column to expand by the same amount when the frame is created
        #rather than sticking to their minimum size in the top left corner
        for i in range(5):
            self.grid_rowconfigure(i,weight=1)
            self.grid_columnconfigure(i,weight=1)
        #====SUB FRAME 1 ( MAIN CONENT, DONT WANT TO RENAME) ==========  
        self.container=tk.Frame(self)
        #places in the middle of the current frame. I then place each widget in this sub frame so that they are centred
        self.container.grid(row=2,column=2)
        #==== HEADER FRAME ========
        self.header=tk.Frame(self,background="#F0E9E9",height=60)
        self.header.grid(row=0,column=0,sticky="new",columnspan=5)
        self.header.propagate(False)
        self.header.grid_columnconfigure(0,weight=1)

        tk.Label(self.header, text= "Login", font=("Arial",20)).grid(row=0, column=0,padx=20,pady=5)
        
        
        #Displays username text and allows for text entry
        tk.Label(self.container, text="Username").grid(row=1,column=0)
        self.username=tk.Entry(self.container)
        self.username.grid(row=1,column=1)
        

        #Displays password text and allows for entry of data
        tk.Label(self.container, text="Password").grid(row=2,column=0)
        self.password = tk.Entry(self.container, show="*",)
        self.password.grid(row=2,column=1)
        
        #calls function to simulate login validation and move to dash frame
        self.submit=tk.Button(self.container,
                  text="Login",
                  command=lambda:self.loginbutton(self.controller))
        self.submit.grid(row=3,column=1)   
    
    #checks if the value in the entry boxes is equal to a stored value ( simulate login validation)
    #moves to the dashboard frame
    def loginbutton(self,controller):
        if self.username.get()=="LEWIS" and self.password.get()=="171008":
            controller.showFrame(Dashboard)
            controller.createSidebar()
            ##controller.dash.grid_forget()
            try:
                self.loginmessage.grid_forget()
            except:
                self.score=0
        else:
            self.submit.config(fg="#D0260A",highlightbackground="#ED2929")
            self.loginmessage=tk.Label(self.container,text="Invalid login details",font=("Helvetica,18"),fg="#D02626")
            self.loginmessage.grid(row=4,column= 1,ipady=10)


#====== QUIZ FRAME ===========
class Quiz(tk.Frame):
    def __init__(self,parent,controller):
        self.controller=controller
        #======MINI DATABASE========
        #Mini data structure used to respresent questions relation in the database using a 2D ARRAY, where each array is a question
        #array[0] represents question text, array[1-4] are the options, array[5] is the correct choice, and array[6] is the topic
        self.questionqueue=[["QUESTION 1","a","b","c","d","b","TOPIC A"],
                            ["Q2","1","2","3","4","3","TOPIC B"],
                            ["Q3","MAR","VAR","PAR","RAM","MAR","TOPIC C"],
                            ["Q4","X","Y","Z","W","W","TOPIC D"],
                            ["Q5","1a","2b","3c","4b","4b","TOPIC E"]]
        self.questionnumber=0
        self.optionsbuttons=[]
        #====FRAME CONFIG =====
        #initialises the frame
        super().__init__(parent)
        self.answer_var = tk.StringVar()
        for i in range (5):
            self.grid_rowconfigure(i,weight=1)
            self.grid_columnconfigure(i,weight=1)
        self.container= tk.Frame(self)
        self.container.grid(row=2,column=2)

        tk.Label(self.container,text="Quiz",font=("Arial",16)).grid(row=0,column=0)
        self.createQuizWidgets()
        self.startQuiz(controller)

    def createQuizWidgets(self):
        self.question=tk.Label(self.container)
        self.question.grid(row=1,column=0)

        for i in range(4):
            #creates 4 selectable buttons and adds them to a list to be accessed later
            r=tk.Radiobutton(
                self.container,
                variable=self.answer_var
            )
            r.grid(row=i+2,column=0)
            self.optionsbuttons.append(r)

        self.submit=tk.Button(
            self.container,
            text="Submit",
            command=lambda:self.nextQuestion(self.controller)
        )
        self.submit.grid(row=6,column=0)

        self.quit=tk.Button(
            self.container,
            text="Quit",
            command=lambda: self.endQuiz(self.controller)
        )
        self.quit.grid(row=7,column=0)

    def startQuiz(self,controller):
        self.resetQuiz(controller)
        self.loadQuestion()

    def resetQuiz(self,controller):
        controller.qsanswered=0
        self.questionnumber=0
        controller.score=0

    def endQuiz(self,controller):
        self.startQuiz(controller)
        controller.showFrame(Dashboard)

    def currentQuestion(self):
        return self.questionqueue[self.questionnumber]

    def currentQuestionText(self):
        return self.currentQuestion()[0]

    def currentOptions(self):
        return self.currentQuestion()[1:5]

    def currentCorrectAnswer(self):
        return self.currentQuestion()[5]

    def loadQuestion(self):
        self.answer_var.set("")
        self.question.config(text=self.currentQuestionText())
        for x,option in enumerate(self.currentOptions()):
            self.optionsbuttons[x].config(text=option,value=option)

    def markQuestion(self,controller):
        #checks if the selected answer is equal to the stored correct choice
        if self.answer_var.get() == self.currentCorrectAnswer():
            controller.score+=1

    def quizFinished(self,controller):
        return controller.qsanswered==len(self.questionqueue)

    def finishQuiz(self,controller):
        controller.showFrame(Progress)
        controller.frames[Progress].updateScore(controller)
        controller.quizzesTaken+=1
        self.startQuiz(controller)
    
    #changes the text to the next question, passing in the frame, sub frame and question number to access
    def nextQuestion(self,controller):
        self.markQuestion(controller=controller)
        #increments next item to access in the array   
        self.questionnumber+=1
        controller.qsanswered+=1

        #checks if all questions have been answered            
        if self.quizFinished(controller):
            self.finishQuiz(controller)
            return
        
        self.loadQuestion()

class Dashboard(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        for i in range(5):
            self.grid_rowconfigure(i,weight=1)
            self.grid_columnconfigure(i,weight=1)
        
        #container=tk.Frame(self)
        #container.grid(row=2,column=2,sticky="nsew",columnspan=5)
        container = tk.Frame(self)
        container.grid(row=1, column=0, sticky="n", pady=45)
        container.grid_columnconfigure((0, 1), weight=1)

        self.header = tk.Frame(self, bg="#FFFFFF", height=150)
        self.header.grid(row=0, column=0, sticky="ew",columnspan=5)
        self.header.grid_propagate(False)
        self.header.grid_columnconfigure(0, weight=1)

        
        tk.Label(self.header,text="Dashboard",font=("Arial",22)
                 ,bg="#FFFFFF",fg="#111111").grid(row=0,column=0)
        tk.Label(self.header,text="Welcome, Lewis",
                 font=("Helvetica",16),bg="#FFFFFF",fg="#111111").grid(row=1,column=0)
        start=tk.Button(container,
                  text="Start Quiz",
                  command=lambda:controller.showFrame(Quiz))
        start.grid(row=0,column=2,ipadx=10,ipady=10)

        tk.Label(container,text=f"Previous quiz result:{controller.score}",
                 fg="#244AE2",font=("Arial",16),height=10).grid(row=2,column=0,sticky="w")
        tk.Label(container,text=f"Quizzes Taken : {controller.quizzesTaken}"
                 ,fg="#244AE2",font=("Arial",16),height=10).grid(row=3,column=0,sticky="w")


class Progress(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        for i in range(5):
            self.grid_rowconfigure(i,weight=1)
            self.grid_columnconfigure(i,weight=1)
        
        self.container=tk.Frame(self)
        self.container.grid(row=2,column=2)
        title=tk.Label(self.container, text="Progress", font=("Arial",16))
        title.grid(row=0, column=1)
        self.score=tk.Label(self.container,padx=5,pady=10)
        self.score.grid(row=2, column=1)
        tk.Button(self.container,text="Dashboard",command=lambda:controller.showFrame(Dashboard)).grid(row=3,column=1,ipadx=1.5)
    def updateScore(self,controller):
        self.score.config(text= (controller.score,"/", controller.qsanswered))
ui=App()   
ui.mainloop()

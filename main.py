import tkinter as tk
#Create a root class that initialises and controls
#each frame
class App(tk.Tk):
    def __init__(self):
        super().__init__() # calls constructors for tk instance to create a root frame
        #Sets attributes for root frame using setters
        self.title("Quiz Builder")
        self.geometry("800x500")

        self.score=0 
        self.qsanswered= 0


        #creates a containter which stores all frames
        container= tk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")
        
        #tells the grid to expand into the space left by the root frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames={}
        # creates an instance of the frame, passing in the container frame as a a base 
        #and the current class(App) as a controller to allow for manipulation through the class
        for i in (Login,Dashboard,Quiz,Progress):
            frame=i(container,self)
            self.frames[i]=frame # store the frame using self.frames
            frame.grid(row=0,column=0,sticky="nsew") # place each frame
        #method used to present a frame my raising it to the top of the stack
        self.showFrame(Login)
    def showFrame(self,frame):
        f= self.frames[frame]
        f.tkraise()

#Creates the login screen using the frame class
class Login(tk.Frame):
    def __init__(self,parent,controller):
        self.controller=controller 
        super().__init__(parent)# initialises the frame using tk frame class, passing in the container frame to act as a base
        
        #tells each row/column to expand by the same amount when the frame is created
        #rather than sticking to their minimum size in the top left corner
        for i in range(5):
            self.grid_rowconfigure(i,weight=1)
            self.grid_columnconfigure(i,weight=1)
        #creates a sub frame   
        container=tk.Frame(self)
        #places in the middle of the current frame. I then place each widget in this sub frame so that they are centred
        container.grid(row=2,column=2)
        self.label=tk.Label(container, text= "Login", font=("Arial",20)).grid(row=0, column=1)
        #Displays username text and allows for text entry
        tk.Label(container, text="Username").grid(row=1,column=0)
        self.username=tk.Entry(container)
        self.username.grid(row=1,column=1)
        

        #Displays password text and allows for entry of data
        tk.Label(container, text="Password").grid(row=2,column=0)
        self.password = tk.Entry(container, show="*")
        self.password.grid(row=2,column=1)
        
        #calls function to simulate login validation and move to dash frame
        tk.Button(container,
                  text="Login",
                  command=lambda:self.loginbutton(self.controller)
                ).grid(row=3,column=1)   
    
    #checks if the value in the entry boxes is equal to a stored value ( simulate login validation)
    #moves to the dashboard frame
    def loginbutton(self,controller):
        if self.username.get()=="LEWIS" and self.password.get()=="171008":
            controller.showFrame(Dashboard)
        else:
            tk.Label(self,text="Invalid login details",font=("Helvetica,18")).grid(row=5,column= 2)


#Quiz Frame
#new frame, no functionality
class Quiz(tk.Frame):
    def __init__(self,parent,controller):
        #maybe change into a 2D array, each item if the text[1],option[2-5]?
        #maybe initliase each item as an object in a new class, with option /correct option/ question attributes?
        #for now ill just have the text in an array

        #Mini data structure used to respresent questions relation in the database using a 2D ARRAY, where each array is a question
        #array[0] represents question text, array[1-4] are the options, array[5] is the correct choice, and array[6] is the topic
        self.questionqueue=[["QUESTION 1","a","b","c","d","b","TOPIC A"],
                            ["Q2","1","2","3","4","3","TOPIC B"],
                            ["Q3","MAR","VAR","PAR","RAM","MAR","TOPIC C"],
                            ["Q4","X","Y","Z","W","W","TOPIC D"],
                            ["Q5","1a","2b","3c","4b","4b","TOPIC E"]]
        self.questionnumber=0
        self.optionsbuttons=[]


        super().__init__(parent)
        for i in range (5):
            self.grid_rowconfigure(i,weight=1)
            self.grid_columnconfigure(i,weight=1)
        container= tk.Frame(self)
        container.grid(row=2,column=2)

        tk.Label(container,text="Quiz",font=("Arial",16)).grid(row=0,column=0)

        self.question=tk.Label(container,text=self.questionqueue[self.questionnumber][0])
        self.question.grid(row=1,column=0)

        self.answer_var = tk.StringVar()

        for i in range(4):
            #creates 4 selectable buttons and adds them to a list to be accessed later, storing each button is the answer_var variable
            r=tk.Radiobutton(
                container,#belongs to the sub frame
                text=self.questionqueue[self.questionnumber][i+1],#defines text displayed 
                variable=self.answer_var,#defines where value is stored
                value=self.questionqueue[self.questionnumber][i+1]#defines what value is stored

            )
            r.grid(row=i+2,column=0)
            self.optionsbuttons.append(r)
        submit=tk.Button(container,text="Submit",command=lambda:self.nextQuestion(controller) )
        submit.grid(row=6,column=0)

        tk.Button(
            container,
            text="Back",
            command=lambda: controller.showFrame(Dashboard)
        ).grid(row=7,column=0)
    
    #changes the text to the next question, passing in the frame, sub frame and question number to access
    def nextQuestion(self,controller):

        #checks if the selected answer is equal to the stored correct choice
        if self.answer_var.get() == self.questionqueue[self.questionnumber][5]:
            controller.score+=1

        #increments next item to access in the array   
        self.questionnumber+=1
        controller.qsanswered+=1

        #checks if all questions have been answered            
        if controller.qsanswered==len(self.questionqueue):
            controller.showFrame(Progress)
            controller.frames[Progress].updateScore(controller)
            return
        self.question.config(text=self.questionqueue[self.questionnumber][0])
        for x in range(4):
            self.optionsbuttons[x].config(text=self.questionqueue[self.questionnumber][x+1],
                                          value=self.questionqueue[self.questionnumber][x+1])

        #checks if the selected answer is equal to the stored correct choice
        if self.answer_var.get() == self.questionqueue[self.questionnumber][5]:
            controller.score+=1
class Dashboard(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        for i in range(5):
            self.grid_rowconfigure(i,weight=1)
            self.grid_columnconfigure(i,weight=1)
        
        container=tk.Frame(self)
        container.grid(row=2,column=2)
        
        tk.Label(container,text="Dashboard").grid(row=0,column=2)
        
        start=tk.Button(container,
                  text="Start Quiz",
                  command=lambda:controller.showFrame(Quiz))
        start.grid(row=2,column=1)


        logout=tk.Button(container,
                  text="Log Out",
                  command=lambda:controller.showFrame(Login))
        logout.grid(row=2,column=4)
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
        self.score=tk.Label(self.container,text="x")
        self.score.grid(row=2, column=1)
        
    def updateScore(self,controller):
        self.score.config(text= (controller.score,"/", controller.qsanswered))
ui=App()   
ui.mainloop()

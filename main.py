import tkinter as tk
#Create a root class that initialises and controls
#each frame
class App(tk.Tk):
    def __init__(self):
        super().__init__() # calls constructors for tk instance to create a root frame
        #Sets attributes for root frame using setters
        self.title("Quiz Builder")
        self.geometry("800x500")
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
    
        container=tk.Frame(self)
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
        self.questionqueue=["QUESTION 1","Q2","Q3","Q4","Q5"]
        self.questionnumber=0
        super().__init__(parent)
        for i in range (5):
            self.grid_rowconfigure(i,weight=1)
            self.grid_columnconfigure(i,weight=1)
        container= tk.Frame(self)
        container.grid(row=2,column=2)

        tk.Label(container,text="Quiz",font=("Arial",16)).grid(row=0,column=0)

        self.question=tk.Label(container,text=self.questionqueue[self.questionnumber])
        self.question.grid(row=1,column=0)

        self.answer_var = tk.StringVar()

        for i in range(4):
            tk.Radiobutton(
                container,
                text=f"Option {i+1}",
                variable=self.answer_var,
                value=f"Option {i+1}"

            ).grid(row=i+2,column=0)

        submit=tk.Button(container,text="Submit",command=lambda:self.nextQuestion() )
        submit.grid(row=6,column=0)

        tk.Button(
            container,
            text="Back",
            command=lambda: controller.showFrame(Dashboard)
        ).grid(row=7,column=0)
    
    #changes the text to the next question, passing in the frame, sub frame and question number to access
    def nextQuestion(self):
        self.question.config(text=self.questionqueue[self.questionnumber])
        #increments next item to access in the array   
        self.questionnumber+=1
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
        
        container=tk.Frame(self)
        container.grid(row=2,column=2)
        title=tk.Label(container, text="Progress", font=("Arial",16))
        title.grid(row=0, column=1)
        score=tk.Label(container, text="(SCORE) / (QUESTIONS)")
        score.grid(row=2, column=1)
        #if a question was wrong
        #print question text
        #print question answer

ui=App()    
ui.mainloop()

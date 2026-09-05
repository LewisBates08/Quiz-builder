import tkinter as tk
from tkinter import ttk

main_color = "#2570C0"
accent_color = "#7FD0FB"
white_color = "#FFFFFF"
text_color = "#000000"
text_color2 = "#8317EE"
class controller():
    def __init__(self, root):
        self.root = root
        self.sidebar = sidebar(self.root, self)
        self.sidebar.grid(row=0, column=0, sticky="ns")  # place the sidebar
        self.frames = {Login:None, 
                       Dashboard:None,
                       Quiz:None,
                       Review:None}

        for i in (Login,Dashboard,Quiz,Review):
            frame=i(parent=root.container,controller=self)
            self.frames[i]=frame # store the frame using self.frames
            frame.grid(row=0,column=0,sticky="nsew") # place each frame
        self.show_frame(Review) # show the login frame first
        self.sidebar_visible = True
    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar.grid_remove()  # hide the sidebar
        else:
            self.sidebar.grid()  # show the sidebar
        self.sidebar_visible = not self.sidebar_visible
    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()  # bring the frame to the front

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

    def create_layout(self):
        self.grid_rowconfigure((0,1,2,3,4), weight=1)
        self.grid_columnconfigure((0,1,2,3,4), weight=1)
    def create_subframes(self):
        self.header= tk.Frame(self, bg=main_color)
        self.header.grid(row=0, column=0, columnspan=5, sticky='nsew')
        self.header.grid_propagate(False)
        self.header.grid_rowconfigure(0, weight=2)
        self.header.grid_rowconfigure(1, weight=1)
        self.header.grid_columnconfigure((0,1,2,3,4), weight=1)

        self.main_content = tk.Frame(self, bg='#FFFFFF')
        self.main_content.grid_rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)
        self.main_content.grid_columnconfigure((0,1,2,3,4,5,6,7,8), weight=1)
        self.main_content.grid(row=1, column=0,rowspan=4,columnspan=5, sticky='nsew')
        self.main_content.grid_propagate(False)

    def create_widgets(self):
        self.title_label = tk.Label(self.header, text="Welcome to the Quiz Builder", font=("Helvetica", 24), bg=main_color, fg=white_color)
        self.title_label.grid(row=0, column=0, columnspan=5, sticky='nsew')

        self.username_label = tk.Label(self.main_content, text="Username:", font=("Helvetica", 14), bg=white_color, fg=text_color)
        self.username_label.grid(row=1, column=4, sticky='w')
        self.username_entry = tk.Entry(self.main_content, font=("Helvetica", 14),relief='solid', bg="#D5CECE")
        self.username_entry.grid(row=2, column=4, sticky='nw')

        self.password_label = tk.Label(self.main_content, text="Password:", font=("Helvetica", 14), bg=white_color, fg=text_color)
        self.password_label.grid(row=3, column=4, sticky='w', padx=(0,10))
        self.password_entry = tk.Entry(self.main_content, show="*", font=("Helvetica", 14),relief='solid', bg="#D5CECE")
        self.password_entry.grid(row=4, column=4, sticky='nw', padx=(10,0))

        self.login_button = tk.Button(self.main_content, text="Login", 
                                      font=("Helvetica", 14),
                                      fg=text_color, bg=accent_color, 
                                      relief='raised',command=lambda: self.controller.show_frame(Dashboard))
        self.login_button.grid(row=5, column=4, sticky= 'ew', padx=(10,0))


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
        self.sidebar_button=tk.Button(self.header, text="☰", font=("Helvetica", 14), bg=main_color, fg=white_color, relief='flat')
        self.stats= tk.Frame(self.main_content, bg='#FFFFFF', relief='solid',bd=1)
        self.stats.grid(row=3, column =5 , rowspan=8, columnspan=5, sticky='nsew')
        self.stats.grid_propagate(False)
        self.stats.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1)
        self.stats.grid_columnconfigure((0,1,2,3,4), weight=1)

        self.progress= tk.Frame(self.main_content, bg='#FFFFFF', relief='solid',bd=1)
        self.progress.grid(row=3, column =0 , rowspan=8, columnspan=5, sticky='nsew')
        self.progress.grid_propagate(False)
        self.progress.grid_rowconfigure((0,1,2,3,4), weight=1)
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
        self.progress_label.grid(row=0, column=2, sticky='w', padx=(10,0))
        self.topic1_label = tk.Label(self.progress, text="Topic 1: 100%", font=("Helvetica", 14), bg=white_color, fg=text_color)
        self.topic1_label.grid(row=1, column=2, sticky='w', padx=(10,0))
        self.topic2_label = tk.Label(self.progress, text="Topic 2: 75%", font=("Helvetica", 14), bg=white_color, fg=text_color)
        self.topic2_label.grid(row=2, column=2, sticky='w', padx=(10,0))
        self.topic3_label = tk.Label(self.progress, text="Topic 3: 50%", font=("Helvetica", 14), bg=white_color, fg=text_color)
        self.topic3_label.grid(row=3, column=2, sticky='w', padx=(10,0))

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

        
class Quiz(tk.Frame):
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
        self.header.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)

        self.main_content = tk.Frame(self, bg=white_color)
        self.main_content.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)
        self.main_content.grid_columnconfigure((0,1,2,3,4,5,6,7), weight=1)
        self.main_content.grid(row=2, column=0,rowspan=8,columnspan=10, sticky='nsew')
        self.main_content.grid_propagate(False)

        self.stats= tk.Frame(self, bg="#7FD0FB", relief='solid')
        self.stats.grid(row=1, column =0 ,columnspan=10, sticky='nsew')
        self.stats.grid_propagate(False)
        self.stats.grid_rowconfigure((0,1,2,3,4), weight=1)
        self.stats.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)


    def create_widgets(self):
        self.title_label = tk.Label(self.header, text="Quiz", font=("Helvetica", 24), bg=main_color, fg=white_color)
        self.title_label.grid(row=0, column=5, sticky='nsew')

        self.question_number_label = tk.Label(self.stats, text="Question 1", font=("Helvetica", 14), bg="#7FD0FB", fg=text_color)
        self.question_number_label.grid(row=0, column=0, sticky='w', padx=(10,0))
        self.questions_remaining_label = tk.Label(self.stats, text="Questions Remaining: 9", font=("Helvetica", 14), bg="#7FD0FB", fg=text_color)
        self.questions_remaining_label.grid(row=0, column=9, sticky='e', padx=(0,10))
        self.previous_button = tk.Button(self.stats, text="Previous", font=("Helvetica", 14), bg="#7FD0FB", fg=text_color, relief='raised')
        self.previous_button.grid(row=0, column=3, sticky='w')
        self.next_button = tk.Button(self.stats, text="Next", font=("Helvetica", 14), bg="#7FD0FB", fg=text_color, relief='raised')
        self.next_button.grid(row=0, column=4, sticky='e')

        self.question_number_label = tk.Label(self.main_content, text="What does WAP stand for?", font=("Helvetica", 14), bg=white_color, fg=text_color)
        self.question_number_label.grid(row=0, column=1,sticky='w', padx=(10,0))
        self.indicator = tk.Label(self.main_content,bg=main_color)
        self.answer = tk.StringVar()
        self.option1 = tk.Radiobutton(self.main_content, text=" Wireless Application Protocol", 
                                      variable=self.answer, value="Wireless Application Protocol", 
                                      font=("Helvetica", 14), bg=white_color, fg=text_color, selectcolor=main_color,
                                      command=lambda: self.setindicator(self.option1))
        self.option1.grid(row=1, column=1, sticky='w', padx=30)

        self.option2 = tk.Radiobutton(self.main_content, text=" Wide Area Protocol",
                                       variable=self.answer, value="Wide Area Protocol",
                                         font=("Helvetica", 14), bg=white_color, fg=text_color, selectcolor=main_color,
                                         command=lambda: self.setindicator(self.option2))
        self.option2.grid(row=2, column=1, sticky='w', padx=30)

        self.option3 = tk.Radiobutton(self.main_content, text="web application protocol",
                                       variable=self.answer, value="web application protocol",
                                         font=("Helvetica", 14), bg=white_color, fg=text_color,selectcolor=main_color
                                         ,command=lambda: self.setindicator(self.option3))
        self.option3.grid(row=3, column=1, sticky='w', padx=30)

        self.option4 = tk.Radiobutton(self.main_content, text="Wireless Access Point", variable=self.answer,
                                      value="Wireless Access Point", font=("Helvetica", 14),
                                        bg=white_color, fg=text_color,selectcolor=main_color,
                                        command=lambda: self.setindicator(self.option4))
        self.option4.grid(row=4, column=1,padx=30,sticky='w')
        self.submit_button = tk.Button(self.main_content, text="Submit",
                                        font=("Helvetica", 14),background=main_color,
                                          fg=white_color, relief='raised', command=self.submit_answer)
        
        self.submit_button.grid(row=5, column=2, sticky='w', padx=20)

    def submit_answer(self):
        selected_answer = self.answer.get()
        print(f"Selected answer: {selected_answer}")
        # Here you can add logic to check the answer and update the quiz state
    def setindicator(self, selected_option):
        # Reset the background color of all options
        for option in [self.option1, self.option2, self.option3, self.option4]:
            option.config(bg=white_color)
        # Set the background color of the selected option
        selected_option.config(bg=accent_color)

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
        self.header.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)

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
        self.previous_button = tk.Button(self.stats, text="Previous",
                                          font=("Helvetica", 14), bg=white_color,
                                             fg=text_color, relief='raised',width=10)
        self.previous_button.grid(row=0, column=9, sticky='e')
        self.next_button = tk.Button(self.stats, text="Next",
                                        font=("Helvetica", 14), bg=white_color,
                                           fg=text_color, relief='raised',width=10)
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
        self.question_label.grid(row=0, column=1,sticky='w', padx=(10,0))
        self.option1_label = tk.Label(self.question, text="1.Wireless Application Protocol", font=("Helvetica", 14),
                                 bg=white_color, fg=text_color)
        self.option1_label.grid(row=1, column=1, sticky='w', padx=(10,0))
        self.option2_label = tk.Label(self.question, text="2.Wide Area Protocol", font=("Helvetica", 14),
                                 bg=white_color, fg=text_color)
        self.option2_label.grid(row=2, column=1, sticky='w', padx=(10,0))
        self.option3_label = tk.Label(self.question, text="3.Web application protocol", font=("Helvetica", 14),
                                 bg=white_color, fg=text_color)
        self.option3_label.grid(row=3, column=1, sticky='w', padx=(10,0))
        self.option4_label = tk.Label(self.question, text="4.Wireless Access Point", font=("Helvetica", 14),
                                 bg="#26db3e", fg=text_color)
        self.option4_label.grid(row=4, column=1, sticky='w', padx=(10,0))

        self.sidebar_button = tk.Button(self.header, text="☰", font=("Helvetica", 14), bg=main_color, fg=white_color, relief='flat', command=self.controller.toggle_sidebar)
        self.sidebar_button.grid(row=0, column=0, sticky='w', padx=(10,0))
        
class sidebar(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=main_color)
        self.controller = controller
        self.setup_style()
        self.create_widgets()
        self.create_layout()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')  # 'clam' respects custom colors; mac default ('aqua') doesn't

        style.configure(
            "Sidebar.TButton",
            background=main_color,
            foreground=white_color,
            font=("Helvetica", 14),
            borderwidth=0,
            focuscolor=main_color,
            relief='flat',
        )
        style.map(
            "Sidebar.TButton",
            background=[('active', accent_color)],  # color while pressed/hovered
            foreground=[('active', white_color)],
        )

    def create_layout(self):
        self.grid_rowconfigure((0,1,2,3,4,5,6,8,9), weight=1)

    def create_widgets(self):
        self.dashboard_button = ttk.Button(
            self, text="Dashboard", style="Sidebar.TButton",
            command=lambda: self.controller.show_frame(Dashboard)
        )
        self.dashboard_button.grid(row=4, column=0, sticky="ew")

        self.quiz_button = ttk.Button(
            self, text="Quiz", style="Sidebar.TButton",
            command=lambda: self.controller.show_frame(Quiz)
        )
        self.quiz_button.grid(row=2, column=0, sticky="ew")

        self.review_button = ttk.Button(
            self, text="Review", style="Sidebar.TButton",
            command=lambda: self.controller.show_frame(Review)
        )
        self.review_button.grid(row=6, column=0, sticky="ew")
if __name__ == "__main__":
    app = root()
    controller = controller(app)
    app.mainloop()
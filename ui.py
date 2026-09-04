import tkinter as tk
from tkinter import ttk

main_color = "#2570C0"
accent_color = "#8317EE"
white_color = "#FFFFFF"
text_color = "#000000"
text_color2 = "#8317EE"

SIDEBAR_WIDTH = 220


class controller():
    def __init__(self, root):
        self.root = root
        self.root.controller = self
        self.frames = {Login:None, 
                       Dashboard:None}

        for i in (Login,Dashboard):
            frame=i(parent=root.container,controller=self)
            self.frames[i]=frame # store the frame using self.frames
            frame.grid(row=0,column=0,sticky="nsew") # place each frame
        self.show_frame(Login) # show the login frame first
        self.sidebar_visible = True

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()  # bring the frame to the front

    def toggle_sidebar(self):
        if self.sidebar_visible:
            # `place_forget` removes only the overlay; the page below it keeps
            # exactly the same size because it is not sharing a grid column.
            self.root.sidebar.place_forget()
        else:
            self.root.sidebar.place(x=0, y=0, width=SIDEBAR_WIDTH, relheight=1)

        self.sidebar_visible = not self.sidebar_visible
        self.root.update_toggle_button(self.sidebar_visible)


class root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My Application")
        self.geometry("800x600")
        self.frames = {}
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # The content always owns the whole window.  The sidebar is added with
        # `place` below, so opening it does not push or shrink this container.
        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.sidebar=sidebar(self)
        self.sidebar.place(x=0, y=0, width=SIDEBAR_WIDTH, relheight=1)

        # This lives on the root, not in a page header, so it remains usable
        # no matter which page is currently raised.
        self.toggle_button = tk.Button(
            self,
            text="✕",
            font=("Helvetica", 14, "bold"),
            bg=main_color,
            fg=white_color,
            activebackground=accent_color,
            activeforeground=white_color,
            relief="flat",
            command=self.toggle_sidebar,
        )
        self.update_toggle_button(is_sidebar_visible=True)

    def toggle_sidebar(self):
        """Forward root-level toggle clicks to the shared controller."""
        self.controller.toggle_sidebar()

    def update_toggle_button(self, is_sidebar_visible):
        """Keep the toggle accessible beside an open sidebar or at the edge."""
        if is_sidebar_visible:
            self.toggle_button.configure(text="✕")
            self.toggle_button.place(x=SIDEBAR_WIDTH + 8, y=8, width=36, height=36)
        else:
            self.toggle_button.configure(text="☰")
            self.toggle_button.place(x=8, y=8, width=36, height=36)

        # Replacing the sidebar with `place` can bring it above other widgets.
        # Raise the button again so there is always a visible way to close it.
        self.toggle_button.lift()



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

class sidebar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=SIDEBAR_WIDTH, bg=main_color)
        self.pack_propagate(False)
        self.create_layout()
        self.create_widgets()

    def create_layout(self):
        self.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)
        self.grid_columnconfigure(0, weight=1)

    def create_widgets(self):
        self.dashboard_button = tk.Button(self, text="Dashboard", font=("Helvetica", 14), bg=main_color, fg=white_color,
                                          command=lambda: self.master.controller.show_frame(Dashboard))
        self.dashboard_button.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
if __name__ == "__main__":
    app = root()
    controller = controller(app)
    app.mainloop()

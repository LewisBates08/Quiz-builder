

import sqlite3 as sql
class database():
    def __init__(self):
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
            return 'null'

        if len(username) < 3 or len(username)>30:
            return 'username_length'
        if len(password) < 6 :
            return 'password_length'

        if self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone():
            return 'non_unique_username'
        
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.conn.commit()
        return True
    def validate_login(self, username, password):
            self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = self.cursor.fetchone()
            if user:
                
                return user[0]
            else:
                return False
    def add_question(self, question_text, choice1, choice2, choice3, correct_choice, topic, user_id):

        if not all([question_text, choice1, choice2, choice3, correct_choice]) or topic == "Select a Topic":
            return 'emptyfields'
        if len(set([choice1, choice2, choice3, correct_choice])) < 4:
            return 'unique_choices'
        if question_text.isdigit():
            return 'questiontypeerror'
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
            
            

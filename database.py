

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
        self.cursor.execute('''SELECT t.topic_name,t.total_questions,up.numberQsAttempted,up.numberQsCorrect
                            FROM user_performance AS up JOIN topics AS t ON up.topic_id=t.id
                            WHERE up.user_id=?''', (user_id,))

        return self.cursor.fetchall()
    def get_username(self, user_id):
        self.cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
    def get_question_by_id(self, question_id):
        self.cursor.execute('''SELECT question_text, choice1, choice2, choice3, correct_choice, topic_id 
                            FROM questions 
                            WHERE id = ?''', (question_id,))
        return self.cursor.fetchone()
            
    def get_question_ids(self,current_user_id):
        self.cursor.execute("SELECT id FROM questions WHERE user_id IS NULL OR user_id = ?", (current_user_id,))
        ids=[]
        for i in self.cursor.fetchall():
            ids.append(i[0])
        return ids
    def update_user_performance(self, user_id, topic_id, is_correct,question_id):
        #checks if the user already has a record this topic 
        self.cursor.execute('''SELECT numberQsAttempted, numberQsCorrect 
                               FROM user_performance 
                               WHERE user_id = ? AND topic_id = ?''', (user_id, topic_id))
        result = self.cursor.fetchone()
        self.cursor.execute('''SELECT is_correct FROM user_questions WHERE question_id = ? AND user_id = ?''',(question_id,user_id))
        if self.cursor.fetchone():
            qAttempted=True
        else:
            qAttempted= False
        #if the user already has a record for this topic, we increment the number of questions
        #if the question was answered correctly, we also increment the number of correct questions

        if result:
            numberQsAttempted, numberQsCorrect = result
            if qAttempted == False:
                numberQsAttempted += 1
            if is_correct:
                numberQsCorrect += 1
        #update the record in the database with the new values
            self.cursor.execute('''UPDATE user_performance 
                                   SET numberQsAttempted = ?, numberQsCorrect = ? 
                                   WHERE user_id = ? AND topic_id = ?''', 
                                   (numberQsAttempted, numberQsCorrect, user_id, topic_id))
    
        # if the user does not have a record for this topic, we create a new record with the initial values
        else:
            numberQsAttempted = 1
            if is_correct:
                numberQsCorrect = 1
            else:
                numberQsCorrect=0
            
            self.cursor.execute('''INSERT INTO user_performance (user_id, topic_id, numberQsAttempted, numberQsCorrect) 
                                VALUES (?, ?, ?, ?)''', 
                                (user_id, topic_id, numberQsAttempted, numberQsCorrect))

    def update_quizzes(self,user_id,score):
        
        self.cursor.execute('''INSERT INTO quizzes (user_id,accuracy) VALUES (?,?)''', 
                            (user_id,score))
        self.conn.commit()

    def get_quiz_count(self,user_id):
        self.cursor.execute('''SELECT accuracy FROM quizzes WHERE user_id = ?''',(user_id,))
        quizzes=self.cursor.fetchall()
        return len(quizzes)
    def get_average_accuracy(self,user_id):
        self.cursor.execute('''SELECT AVG(score) FROM quizzes WHERE user_id = ?''',(user_id,))
        return self.cursor.fetchone()[0]
    def get_question_count(self,user_id):
        self.cursor.execute('''SELECT question_id FROM user_questions WHERE user_id = ?''',(user_id,))
        return len(self.cursor.fetchall())
    def write_question(self,user_id,question_id,user_answer,is_correct):
        self.cursor.execute('''INSERT INTO user_questions (user_id,question_id,user_answer,is_correct) 
                            VALUES (?,?,?,?)''',
                            (user_id,question_id,user_answer,is_correct))
    def get_topic_count(self,user_id):
        self.cursor.execute('''SELECT topic_id FROM user_performance WHERE user_id = ?''',(user_id,))
        return len(self.cursor.fetchall())
    def get_topic_attempts(self, user_id, topic_name):
            self.cursor.execute(
                '''SELECT COUNT(*)
                FROM user_questions AS uq
                JOIN questions AS q ON uq.question_id = q.id
                JOIN topics AS t ON q.topic_id = t.id
                WHERE uq.user_id = ? AND t.topic_name = ?''',
                (user_id, topic_name)
            )
            return self.cursor.fetchone()[0]
    def get_topic_difficulty(self,topic_name):
        self.cursor.execute('''SELECT topic_difficulty FROM topics WHERE topic_name=?''',(topic_name,))
        return self.cursor.fetchone()[0]
    def get_questions_by_topic(self,user_id,topic_name):
        self.cursor.execute('''SELECT q.id FROM questions AS q 
        JOIN topics AS t ON q.topic_id=t.id 
        WHERE (q.user_id IS NULL OR q.user_id = ? )AND t.topic_name=?''',
        (user_id,topic_name))
        return [row[0] for row in self.cursor.fetchall()]
    def get_attempts_by_question(self,user_id,question_id):
        self.cursor.execute('''SELECT COUNT(id) FROM user_questions WHERE user_id=? AND question_id=?''',(user_id,question_id))
        return self.cursor.fetchone()[0]
    def get_most_recent_attempt(self,user_id,question_id):
        self.cursor.execute('''SELECT MAX(attempt_date) FROM user_questions WHERE user_id=? AND question_id=?''',(user_id,question_id))
        return self.cursor.fetchone()[0]
    def get_topic_names(self):
        self.cursor.execute('''SELECT topic_name FROM topics''')
        return [row[0] for row in self.cursor.fetchall()]
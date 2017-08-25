import tkinter as tk
import sqlite3 as sql
import os
import random as rnd
from tkinter.messagebox import *
import time


LARGE_FONT= ("Verdana", 12)
PATH = ".{}database".format(os.sep)
PATH_1 = ".{}database{}data.db".format(os.sep, os.sep)

class PuzzleApp(tk.Tk):
    

    def __init__(self, *args, **kwargs):
        
        file_path, db_path = self.control_resources()
        if file_path and db_path:
            pass
        elif not file_path:
            os.mkdir(PATH)
            Operations.create_table()
        elif file_path and not db_path:
            Operations.create_table()
            
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Language Skills")
        self.resizable(width=False, height=False)
        self.geometry('{}x{}'.format(372, 372))
        
        container = tk.Frame(self)
        container.pack()
        #container.pack(side="top", fill="both", expand = True)
        #container.grid_rowconfigure(0, weight=1)
        #container.grid_columnconfigure(0, weight=1)
        

        self.frames = {}

        for F in (StartPage, AddWords, FindWords, Dictionary, WordQuiz, DeleteWord):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    def control_resources(self):
        
        x = os.path.exists(PATH)
        y = os.path.exists(PATH_1)
        
        return x, y
            

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.head_label = tk.Label(self, text="Language Skılls",
                            relief = tk.GROOVE, borderwidth=5,
                            width=20,fg="black",
                            bg="gray", font=("Helvetica", 24))
        self.head_label.grid(row = 0, column = 0)
        
        self.option_1 = tk.Button(self, text="Add Words",
                            relief=tk.RAISED, width=20,
                            borderwidth=2,
                            command=lambda: controller.show_frame(AddWords),
                            font=("Helvetica", 12))
        self.option_1.grid(row=1, column=0)
        
        self.option_2 = tk.Button(self, text="Find Words",
                            relief=tk.RAISED, width=20,
                            borderwidth=2,
                            font=("Helvetica", 12),
                            command=lambda: controller.show_frame(FindWords))
        self.option_2.grid(row=2, column=0)
        
        self.option_3 = tk.Button(self, text="Dictionary",
                            relief=tk.RAISED, width=20,
                            borderwidth=2,
                            font=("Helvetica", 12),
                            command=lambda: controller.show_frame(Dictionary))
        self.option_3.grid(row=3, column=0)
        
        self.option_4 = tk.Button(self, text="Word Quiz",
                            relief=tk.RAISED, width=20,
                            borderwidth=2,
                            font=("Helvetica", 12),
                            command=lambda: controller.show_frame(WordQuiz))
        self.option_4.grid(row=4, column=0)
        self.option_5 = tk.Button(self, text="Remove Words",
                                  relief=tk.RAISED, width=20,
                                  borderwidth=2,
                                  font=("Helvetica", 12),
                                  command=lambda: controller.show_frame(DeleteWord))
        self.option_5.grid(row=5, column=0)
        
        info_text = "There are {} words in database."
        self.info_box = tk.Label(self, text=info_text.format(str(len(
                                 Operations.get_all()))), 
                                 font=("Helvetica", 12))
        self.info_box.grid(row=6, column=0)
        



class AddWords(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        entry = tk.Entry(self, relief = tk.RIDGE,
                         borderwidth=5, width=20,
                         bg="gray", font=("Helvetica", 24))
        entry.grid(row=0, column=0, columnspan=3)
        
        entry_1 = tk.Entry(self, relief = tk.RIDGE,
                         borderwidth=5, width=20,
                         bg="gray", font=("Helvetica", 24))
        entry_1.grid(row=1, column=0, columnspan=3)

        def add_data():
            word_in_dict = Operations.control_word_in_db(entry.get())
            word = str(entry.get())
            mean = str(entry_1.get())
            if word_in_dict == None:
                data = (word, mean)
                Operations.insert_in_db(data)
            else:
                if askyesno("Word is already exists !",
                            'This word is already in your dictionary.\nDo you want to change ?\n'):
                    Operations.change_meaning_in_db(word, mean)
                    showinfo("Success", "Meaning of this word is successfully changed.")
                else:
                    showinfo("Nothing", "This word stays same.")

            entry.delete(0, tk.END)
            entry_1.delete(0, tk.END)

        button = tk.Button(self, text="Add",
                           command=add_data)
        button.grid(row=2, column=1)
        
        def chance_page():
            controller.show_frame(StartPage)
            
        button1 = tk.Button(self, text="Back to Home",
                            command=chance_page)
        button1.grid(row=4, column=1)

class DeleteWord(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        entry = tk.Entry(self, relief=tk.RIDGE,
                         borderwidth=5, width=20,
                         bg="gray", font=("Helvetica", 24))
        entry.grid(row=0, column=0, columnspan=3)

        def remove_data():
            word = str(entry.get())
            word_1 = Operations.control_word_in_db(word)
            if word_1 != None:
                if askyesno("Are you sure", "Are you sure for delete '{}' from your database ?".format(word)):
                    Operations.delete_from_db(word)
                    showinfo("Success", "'{}' successfully deleted from database.".format(word))
                    entry.delete(0, tk.END)
                else:
                    showinfo("Message", "'{}' is not deleted".format(word))
                    entry.delete(0, tk.END)
            else:
                showinfo("Unknown word", "This word is not in your database.")
                entry.delete(0, tk.END)

        button = tk.Button(self, text="Remove",
                           command=remove_data)
        button.grid(row=2, column=1)

        def chance_page():
            controller.show_frame(StartPage)

        button1 = tk.Button(self, text="Back to Home",
                            command=chance_page)
        button1.grid(row=4, column=1)


class FindWords(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "")
        
        entry = tk.Entry(self, relief = tk.RIDGE,
                         borderwidth=5, width=20,
                         bg="gray", font=("Helvetica", 24))
        entry.grid(row=0, column=0, columnspan=3)

        def create_label():
            word = (str(entry.get()),)
            word_1 = str(entry.get())
            label_text = Operations.find_in_db(word)
            if label_text != None:
                label["text"] = label_text
                label.grid(row=2, column=1)
                entry.delete(0, tk.END)
            else:
                showinfo("Unknown Word", "There is no word ' {} ' in your database.".format(word_1))
                label.grid(row=0,column=0)
                entry.delete(0, tk.END)
        button = tk.Button(self, text="Find",
                  command = create_label)
        button.grid(row=1, column=1)
        
        def chance_page():
            label.grid_forget()
            controller.show_frame(StartPage)
            
        button1 = tk.Button(self, text="Back to Home",
                            command= chance_page)
        button1.grid(row=4, column=1)
        
        
class Dictionary(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        word_set = Operations.get_all()
        rnd.shuffle(word_set)
        if len(word_set) > 10:
            sample_list = rnd.sample(word_set,10)
        else:
            sample_list = rnd.sample(word_set,len(word_set))
        
        for i in range(len(sample_list)):
            word, mean = sample_list[i]
            
            label = tk.Label(self, text = word, width = 16)
            label.grid(row = i, column = 1)
            
            label_1 = tk.Label(self, text = "--->", width = 16)
            label_1.grid(row=i, column = 2)
            
            label_2 = tk.Label(self, text = mean, width = 16)
            label_2.grid(row = i, column = 3)

        
        def chance_page():
            controller.show_frame(StartPage)
            
        button1 = tk.Button(self, text="Back to Home",width=16,
                            command=chance_page)
        button1.grid(row = 10 , column = 2)
        
class WordQuiz(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.user_score = 0
        score_label = tk.Label(self, text = str(self.user_score))
        score_label.grid(row = 0, column = 0)
        message_label = tk.Label(self, text = "")
        message_label.grid(row = 0, column = 1)
        def answer(word, entry_label):
            word_1 = entry_label.get()
            if word == word_1:
                self.user_score += 1
                score_label["text"] = str(self.user_score)
                message_label["text"] = "True"
            else:
                message_label["text"] = "False"
        
        word_set = Operations.get_all()
        rnd.shuffle(word_set)
        if len(word_set) < 5:
            sample_list = rnd.sample(word_set,len(word_set))
        else:
            sample_list = rnd.sample(word_set,5)
        for i in range(len(sample_list)):
            w, m = sample_list[i]
            q_label = tk.Label(self, text = w)
            q_label.grid(row = i+1, column = 0)
            q_entry = tk.Entry(self)
            q_entry.grid(row = i+1, column = 1)
            answer_button = tk.Button(self, text="Answer",
                                      command = lambda m=m, q_entry=q_entry: answer(m, q_entry)) 
            answer_button.grid(row = i+1, column = 2)
        
                 
        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.grid(row = 7, column = 0)
        
        def new_quiz():
            quiz = WordQuiz(parent, controller)
            controller.frames[WordQuiz] = quiz
            quiz.grid(row=0, column=0, sticky="nsew")
            controller.show_frame(WordQuiz)
            
        button2 = tk.Button(self, text="New Quiz", command=new_quiz)
        button2.grid(row = 7, column = 1)
        
class Operations:
    
    def __init__(self):
        pass
    @classmethod   
    def connect_database(cls):
        cls.con = sql.connect(PATH_1)
        cls.cur = cls.con.cursor()
        return cls.cur
    @classmethod    
    def create_table(cls):
        cls.connect_database()
        cls.cur.execute( """CREATE TABLE Dict (Word text,
                                                Mean text)""" )
        cls.stop_database()
    @classmethod    
    def stop_database(cls):
        cls.con.commit()
        cls.con.close()
    @classmethod    
    def insert_in_db(cls, data):
        cls.connect_database()
        cls.cur.execute("INSERT INTO Dict VALUES (?, ?)",data)
        cls.stop_database()
    @classmethod    
    def find_in_db(cls, word):
        cls.connect_database()
        cls.cur.execute("SELECT Mean From Dict WHERE Word = ?",word)
        mean = cls.cur.fetchone()
        cls.stop_database()
        return mean
    @classmethod
    def get_all(cls):
        cls.connect_database()
        cls.cur.execute("SELECT * FROM Dict")
        all_item = cls.cur.fetchall()
        cls.stop_database()
        return all_item

    @classmethod
    def change_meaning_in_db(cls, word, mean):
        cls.connect_database()
        cls.cur.execute("UPDATE Dict SET Mean = ? WHERE Word = ?", (mean, word))
        cls.stop_database()

    @classmethod
    def control_word_in_db(cls, word):
        cls.connect_database()
        cls.cur.execute("SELECT Word From Dict WHERE Word = '%s';" % word.strip())
        word_1 = cls.cur.fetchone()
        cls.stop_database()
        return word_1

    @classmethod
    def delete_from_db(cls, data):
        cls.connect_database()
        cls.cur.execute("DELETE FROM Dict WHERE Word = '%s';" % data.strip())
        cls.stop_database()
    
if __name__ == "__main__":
    app = PuzzleApp()
    app.mainloop()

from tkinter import *
from tkinter import messagebox #import all modules
import sqlite3
from collections import Counter



conn = sqlite3.connect("Recepies.db")   #connect or create db
curr = conn.cursor()
conn.execute( """  CREATE TABLE IF NOT EXISTS recepies (Name text, ingridients text, way text, time text) """)

window = Tk()   #main window


font = ('Courie', 20)

class StartWindow:
    def __init__(self, master):     #class window to write or find a recepie
        self.win = master
        self.master = master


        #can`t resise and title set
        self.win.title('option')
        self.win.resizable(False, False)
        #buttons to write or search for a recepie
        b1 = Button(self.win, text = 'Write', font =('Courie', 16), command = self.add ).grid(column = 0, row = 0, pady = 20, padx = 20)
        b2 = Button(self.win, text = 'Find Recepies', font =('Courie', 16), command = self.search ).grid(column = 1, row = 0, pady = 20, padx = 20)

    def add(self):
        #create another window and hide another
        #can`t resise and title set
        self.win.withdraw()
        self.win_add = Toplevel(self.master)
        self.win_add.title('Add a Recepie')
        self.win_add.resizable(False, False)
        #set function on red cross so the program will finish if its pressed
        self.win_add.protocol("WM_DELETE_WINDOW",on_closing)


        #front-end of the add window
        l = Label(self.win_add, text = 'Create a new recepie', font = ('Courie', 20)).grid(columnspan = 3, row = 0, pady = 20)
        l1 = Label(self.win_add, text = 'Name:', font = ('Courie', 12)).grid(column = 0, row = 1, pady = 20, padx = 20, sticky = 'e')
        l2 = Label(self.win_add, text = 'Ingrigients:', font = ('Courie', 12)).grid(column = 0, row = 2, pady = 20, padx = 20, sticky = 'e')
        l3 = Label(self.win_add, text = 'Way to coock:', font = ('Courie', 12)).grid(column = 0, row = 3, pady = 20, padx = 20, sticky = 'e')
        l4 = Label(self.win_add, text = 'Time to coock:', font = ('Courie', 12)).grid(column = 0, row = 4, pady = 20, padx = 20, sticky = 'e')

        self.e1 = Entry(self.win_add, font = ('Courie', 12), bd = 4, width = 30)
        self.e2 = Entry(self.win_add, font = ('Courie', 12), bd = 4, width = 30)
        self.e3 = Text(self.win_add, font = ('Courie', 12), bd = 4, width = 30, height = 7)
        self.e4 = Entry(self.win_add, font = ('Courie', 12), bd = 4, width = 30)

        self.e1.grid(column = 1, row = 1, padx = 20)
        self.e2.grid(column = 1, row = 2, padx = 20)
        self.e3.grid(column = 1, row = 3, padx = 20)
        self.e4.grid(column = 1, row = 4, padx = 20)

        b = Button(self.win_add, text = 'Submit', font = ('Courie', 20), command = self.submit_add).grid(columnspan = 3, row = 5, pady = 20)
        #go back button
        exit = Button(self.win_add, text = '<--', font = ('Courie', 13), command = lambda:back(self.win, self.win_add)).grid(columnspan = 1, row = 5, padx = 10)

    def submit_add(self):
        #get the values in inputs a
        self.name = self.e1.get()
        self.ingridients = self.e2.get()
        self.way = self.e3.get('1.0', END)
        self.way = self.way.strip()
        self.time_to_cook = self.e4.get()
        #create array and sanitise it
        params = [self.name, self.ingridients, self.way, self.time_to_cook]
        for i in params:
            if i == '':
                params[params.index(i)] = None
        #write into DB values
        curr.execute("INSERT INTO recepies VALUES (?, ?, ?, ?) ", params)
        conn.commit()
        #show that values were added and close window(go back)
        messagebox.showinfo(title = 'Success', message = 'Recepie was written down successfully')
        self.win_add.destroy()
        self.win.deiconify()





    def search(self):
        #build another window and hide previous one
        self.win.withdraw()
        self.win_search = Toplevel(window)
        self.win_search.title ('Ingridients')
        self.win_search.resizable(False, False)
        #front end
        l1 = Label(self.win_search, text = 'To include:', font = ('Courie', 14)).grid(column = 0, row = 0, pady = 20, padx = 20, sticky = 'e')
        l2 = Label(self.win_search, text = 'To exclude:', font = ('Courie', 14)).grid(column = 0, row = 1, pady = 20, padx = 20, sticky = 'e')
        self.text1 = Entry(self.win_search, width = 20, font = ('Courie', 14), bd = 4)
        self.text2 = Entry(self.win_search, width = 20, font = ('Courie', 14), bd = 4)
        self.text1.grid(column = 1, row = 0, sticky = 'e', padx = 20)
        self.text2.grid(column = 1, row = 1, sticky = 'e', padx = 20)


        #2 buttons: submit and go back
        b = Button(self.win_search, text = 'Submit', font = ('Courie', 20), command = self.submit_search).grid(columnspan = 3, row = 2, pady = 20, padx = 20)
        exit = Button(self.win_search, text = '<--', font = ('Courie', 13), command = lambda: back(window,self.win_search, )).grid(columnspan = 1, row = 2, padx = 10)

        #set function on red cross so the program will finish if its pressed
        self.win_search.protocol("WM_DELETE_WINDOW",on_closing)

    def submit_search(self):
        #get the values from inputs and sanitise it
        self.include = input_sanitation(self.text1.get())
        self.exclude = input_sanitation(self.text2.get())
        #get an array of values that are ok with criterias
        result = search(self.include, self.exclude)#

        #if result is not None or not empty array
        if result:
            d = Display(result)
            d.display()

        else:
            #show message that there is no recepie that matches all criterias
            messagebox.showerror(title = 'Error', message = 'No recepie Found')
            self.text1.delete(0, END)
            self.text2.delete(0, END)



class Display:
    #creates a window that consists of names of the recepie and are clickable so it will open another window whick contains everything
    def __init__(self, output_list):
        self.win = Toplevel(window)
        self.win.deiconify()
        #open main window

        scrollbar = Scrollbar(self.win)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.listbox = Listbox(self.win, width = 30, height = 10, font = ('Courie', 20), activestyle = 'none')
        self.listbox.pack(pady = 10, padx = 10, ipady = 10, ipadx = 10)
        self.listbox.bind('<Double-Button-1>', self.on_select)

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        self.output_list = output_list


    def display(self):
        for value in self.output_list:
            self.listbox.insert(END, value[0].upper())

    def on_select(self, event):
        a = (event.widget.curselection())

        elem = self.output_list[a[0]]

        win_f = Toplevel(self.win)
        win_f.title(elem[0].upper())
        win_f.resizable(False, False)
        win_f.maxsize(400, 600)

        name = elem[0]
        ingridients = elem[1]
        way = elem[2]
        time = elem[3]

        l1 = Label(win_f, text = name, font = ('Courier', 20)).grid(columnspan = 3, row = 0, pady = 20, padx = 20)
        l2 = Label(win_f, text = ingridients, font = ('Courier', 14), wraplength = 150).grid(column = 0, row = 1, pady = 20, padx = 20)
        l2 = Label(win_f, text = time, font = ('Courier', 14)).grid(column = 1, row = 1, pady = 20, padx = 20)
        l3 = Label(win_f, text = way, font = ('Courier',16), wraplength = 300).grid(columnspan = 3, row = 3)


    #displays buttons


#function that destroys mother window and finishes programme
def on_closing():
    window.destroy()

#functon to go back to mother window
def back (parent, child):
    child.withdraw()
    parent.deiconify()

#search throughout all DB
def search(include, exclude):
    result = []
    out = []
    #if inputs are the same it gives an Error, excluding if inputs are empty: it will give all recepies in db
    if include == exclude:
        if include == []:
            out = [row for row in  curr.execute(f"SELECT * FROM  recepies ")]
        else:
            return (None)

    #checks if only exclude in on
    elif include == [] and exclude !=[]:
        #creates array with all recepies in db
        out = [row for row in curr.execute(f"SELECT * FROM  recepies ")]


        #for each ingridient in exclude input it will comare to the list and delete record from all recepies so only recepies without exclude will remain
        for ingridient in exclude:
            curr.execute(f"SELECT * FROM  recepies WHERE ingridients LIKE '%{ingridient}%'")
            for row in curr:
                if row in out:
                    out.remove(row)


    #if both include and exclude inputs exist
    else:
        #creates array of includes
        for ingridient in include:
            curr.execute(f"SELECT * FROM  recepies WHERE ingridients LIKE '%{ingridient}%'")
            for row in curr:
                result.append(row)
        #takes only the most common of all inputs (inner join like)
        out = [r[0] for r in Counter(result).most_common() if r[1] > len(list(include))-1]


        #deletes exclude inputs from it
        if out:
            for ex in exclude:
                curr.execute(f"SELECT * FROM  recepies WHERE ingridients LIKE '%{ex}%'")

                for row in curr:
                    if row in out:
                        out.remove(row)

    if out:
        return(out)

    return (None)


#input sanitation just removes empty strings, splits and strips each ingridient
def input_sanitation(user):
    output = []
    if user:
        user = user.split(',')
        for word in user:
            word = word.strip()
            output.append(word)

    output = (list(filter(None, output)))

    return(output)

if __name__ == '__main__':

    StartWindow(window)



    window.mainloop()
    curr.close()

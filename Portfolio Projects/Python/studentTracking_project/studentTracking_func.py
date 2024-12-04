import os
from tkinter import *
import tkinter as tk
import tkinter.messagebox as mgbx
import sqlite3

import studentTracking_main as main
import studentTracking_gui as gui



def center_window(self, w, h): #pass in the tkinter frame (master) reference and the w and h
    #get user's screen width and height
    screen_width = self.master.winfo_screenwidth()
    screen_height = self.master.winfo_screenheight()
    #calculate x and y coordinates to paint the app centered on the user's screen
    x = int((screen_width/2) - (w/2))
    y = int((screen_height/2) - (h/2))
    centerGeo = self.master.geometry('{}x{}+{}+{}'.format(w, h, x, y))
    return centerGeo

#catch if the user's clicks on the windows upper-right 'X' to ensure they want to close
def ask_quit(self):
    if mgbx.askokcancel("Exit program","Okay to exit application?"):
        #This closes app
        self.master.destroy()
        os._exit(0)


#==========================================================================================
def create_db(self):
    conn = sqlite3.connect('students.db')
    with conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS tbl_students( \
                    ID INTEGER PRIMARY KEY AUTOINCREMENT, \
                    col_fname TEXT, \
                    col_lname TEXT, \
                    col_fullname TEXT, \
                    col_phone TEXT, \
                    col_email TEXT, \
                    col_course TEXT \
                    );")
        #You must commit() to save changes and close the database connection
        conn.commit()
    conn.close()
    first_run(self)

def first_run(self):
    data = ('Elisha', 'Stevens', 'Elisha Stevens', '702-886-1195', \
            'elisha.stevens@gmail.com', 'Software Development')
    conn = sqlite3.connect('students.db')
    with conn:
        cur = conn.cursor()
        cur, count = count_records(cur)
        if count < 1:
            cur.execute("""INSERT INTO tbl_students (col_fname, col_lname, col_fullname, \
                        col_phone, col_email, col_course) VALUES (?,?,?,?,?,?)""", \
                        (data[0], data[1], data[2], data[3], data[4], data[5]))
            conn.commit()
    conn.close()

def count_records(cur):
    count = ""
    cur.execute("""SELECT COUNT(*) FROM tbl_students""")
    count = cur.fetchone()[0]
    return cur, count

#Select item in Listbox
def onSelect(self, event):
    #calling the event is the self.lstList1 widget
    varList = event.widget
    select = varList.curselection()[0]
    value = varList.get(select)
    conn = sqlite3.connection('students.db')
    with conn:
        cur = conn.cursor()
        cur.execute("""SELECT col_fname, col_lname, col_phone, col_email, col_course \
                        FROM tbl_students WHERE col_fullname = (?)""", [value])
        varBody = cur.fetchall()
        #This returns a tuple and we can slice it into parts using data[] during the
        # iteration
        for data in varBody:
            self.txt_fname.delete(0,END)
            self.txt_fname.insert(0,data[0])
            self.txt_lname.delete(0,END)
            self.txt_lname.insert(0,data[1])
            self.txt_phone.delete(0,END)
            self.txt_phone.insert(0,data[2])
            self.txt_email.delete(0,END)
            self.txt_email.insert(0,data[3])
            self.txt_course.delete(0,END)
            self.txt_course.insert(0,data[4])


def submitToList(self):
    var_fname = self.txt_fname.get().strip().title()
    var_lname = self.txt_lname.get().strip().title()
    var_fullname = ("{} {}".format(var_fname, var_lname))
    print("var_fullname: {}".format(var_fullname))
    var_phone = self.txt_phone.get().strip()
    var_email = self.txt_email.get().strip()
    if not "@" or not "." in var_email:
        print("Incorrect email format!!!")
    if (len(var_fname) > 0) and (len(var_lname) > 0) and (len(var_phone) > 0) and \
       (len(var_email) > 0):
        conn = sqlite3. connect('students.db')
        with conn:
            cur = conn.cursor()
            #Check the database for existance of the fullname, if so we will alert user and
            # disregard the request
            cur.execute("""SELECT COUNT(col_fullname) FROM tbl_students WHERE \
                        col_fullname = '{}'""".format(var_fullname))
            count = cur.fetchone()[0]
            chkName = count
            if chkName == 0: #if this is 0 then there is no existence of the fullname and
                # we can add new data
                print("chkName: {}".format(chkName))
                cur.execute("""INSERT INTO tbl_students (col_fname, col_lname, col_fullname, \
                            col_phone, col_email, col_course) VALUES (?,?,?,?,?,?)"""), \
                            [var_fname, var_lname, var_fullname, var_phone, var_email, var_course]
                self.lstList1.insert(END, var_fullname) #update listbox with the new fullname
                onClear(self) #call function to clear all of the textboxes
            else:
                mgbx.showerror("Name Error", "'{}' already exists in the database! Please choose a different name.".format(var_fullname))
                onClear(self) #call function to clear all textboxes
        conn.commit()
        conn.close()
    else:
        mgbx.showerror("Missing Text Error", "Please ensure that there is data in all four fields.")
        

def onDelete(self):
    var_select = self.lstList1.get(self.lstList1.curselection()) #Listbox's selected value
    conn = sqlite3.connect('students.db')
    with conn:
        cur = conn.cursor()
        #check cont to ensure that this is not the last record in
        # the database...cannot delete last record or we will get an error
        cur.execute("""SELECT COUNT(*) FROM tbl_students""")
        count = cur.fetchone()[0]
        if count > 1:
            confirm = mgbx.askokcancel("Delete Confirmation", "All information associated \
            with ({}) \nwill be permanently deleted.".format(var_select))
            if confirm:
                conn = sqlite3.connect('students.db')
                with conn:
                    cur = conn.cursor()
                    cur.execute("""DELETE FROM tbl_students WHERE col_fullname = \
                    '{}'""".format(var_select))
                onDeleted(self) #call function to clear all of the textboxes and the selected
                # selected index of listbox
                ###onRefresh(self) #update the listbox of the changes
                conn.commit()
        else:
            confirm = mgbx.showerror("Last Record Error", "({}) is the last record in the \
                database and cannot be deleted at this time.".format(var_select))
    conn.close()

def onDeleted(self):
    #clear the text in these textboxes
    onClear(self)
    ##onRefresh(self) #update the listbox of the changes
    try:
        index = self.lstList1.curselection()[0]
        self.lstList1.delete(index)
    except IndexError:
        pass

def onClear(self):
    #clear the text in these textboxes
    self.txt_fname.delete(0,END)
    self.txt_lname.delete(0,END)
    self.txt_phone.delete(0,END)
    self.txt_email.delete(0,END)
    self.txt_course.delete(0,END)

def onRefresh(self):
    #Populate the listbox, coinciding with the database
    self.lstList1.delete(0,END)
    conn = sqlite3.connect('students.db')
    with conn:
        cur = conn.cursor()
        cur.execute("""SeleCt COUNT(*)FROM tbl_students""")
        count = cur.fetchone()[0]
        i = 0
        while i < count:
            cur.execute("""SELECT col_fullname FROM tbl_students""")
            varList = cur.fetchall()[i]
            for item in varList:
                self.lstList1.insert(0,str(item))
                i = i + i
    conn.close()




if __name__ == "__main__":
    pass

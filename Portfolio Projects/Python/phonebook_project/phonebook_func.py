import os
from tkinter import *
import tkinter as tk
import tkinter.messagebox as mgbx
import sqlite3

import phonebook_main
import phonebook_gui




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
    if mgbx.askokcancel("Exit program", "Okay to exit application?"):
        #This closes app
        self.master.destroy()
        os._exit(0)


#========================================================================
def create_db(self):
    conn = sqlite3.connect('phonebook.db')
    with conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS tbl_phonebook( \
                    ID INTEGER PRIMARY KEY AUTOINCREMENT, \
                    col_fname TEXT, \
                    col_lname TEXT, \
                    col_fullname TEXT, \
                    col_phone TEXT, \
                    col_email TEXT \
                    );")
        #You must commit() to save changes & close the database connection
        conn.commit()
    conn.close()
    first_run(self)

def first_run(self):
    data = ('John', 'Doe', 'John Doe', '111-222-3333', 'john.doe@gmail.com')
    conn = sqlite3.connect('phonebook.db')
    with conn:
        cur = conn.cursor()
        cur, count = count_records(cur)
        if count < 1:
            cur.execute("""INSERT INTO tbl_phonebook (col_fname, col_lname, col_fullname, col_phone, col_email) VALUES (?,?,?,?,?)""", (data[0], data[1], data[2], data[3], data[4]))
            conn.commit()
    conn.close()


def count_records(cur):
    count = ""
    cur.execute("""SELECT COUNT(*) FROM tbl_phonebook""")
    count = cur.fetchone()[0]
    return cur, count

#Select item in ListBox
def onSelect(self, event):
    #calling the event is the self.lstList1 widget
    varList = event.widget
    select = varList.curselection()[0]
    value = varList.get(select)
    conn = sqlite3.connect('phonebook.db')
    with conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT col_fname, col_lname, col_phone, col_email FROM \
tbl_phonebook WHERE col_fullname = (?)""", [value])
        varBody = cursor.fetchall()
        #This returns a tuple and we can slice it into 4 parts using data[] during the iteration
        for data in varBody:
            self.txt_fname.delete(0,END)
            self.txt_fname.insert(0,data[0])
            self.txt_lname.delete(0,END)
            self.txt_lname.insert(0,data[1])
            self.txt_phone.delete(0,END)
            self.txt_phone.insert(0,data[2])
            self.txt_email.delete(0,END)
            self.txt_email.insert(0,data[3])

def addToList(self):
    var_fname = self.txt_fname.get()
    var_lname = self.txt_lname.get()
    #normalize the data to keep it consistent in the database
    var_fname = var_fname.strip() #This will remove any blank spaces before and after the user's entry
    var_lname = var_lname.strip() 
    var_fname = var_fname.title() #This will ensure that the first character in each word is capitalized
    var_lname = var_lname.title()
    var_fullname = ("{} {}".format(var_fname, var_lname)) #combine our normalized names into a full name
    print("var_fullname: {}".format(var_fullname))
    var_phone = self.txt_phone.get().strip()
    var_email = self.txt_email.get().strip()
    if not "@" or not "." in var_email: #will use this soon
        print("Incorrect email format!!!")
    if (len(var_fname) > 0) and (len(var_lname) > 0) and (len(var_phone) > 0) and (len(var_email) > 0): #enforce user to provide all fields
        conn = sqlite3.connect('phonebook.db')
        with conn:
            cur = conn.cursor()
            #Check the database for existance of the fullname, if so we will alert user and disregard request
            cur.execute("""SELECT COUNT(col_fullname) FROM tbl_phonebook WHERE \
col_fullname = '{}'""".format(var_fullname))
            count = cur.fetchone()[0]
            chkName = count
            if chkName == 0: #if this is 0 then there is no existence of the fullname and we can add new data
                print("chkName: {}".format(chkName))
                cur.execute("""INSERT INTO tbl_phonebook (col_fname, col_lname, \
col_fullname, col_phone, col_email) VALUES (?,?,?,?,?)""", [var_fname, var_lname, var_fullname, var_phone, var_email])
                self.lstList1.insert(END, var_fullname) #update listbox with the new fullname
                onClear(self) #call the function to clear all of the textboxes
            else:
                mgbx.showerror("Name Error", "'{}' already exists in the database! Please choose a different name.".format(var_fullname))
                onClear(self) #call the function to clear all of the textboxes
        conn.commit()
        conn.close()
    else:
        mgbx.showerror("Missing Text Error", "Please ensure that there is data in all four fields.")

def onDelete(self):
    var_select = self.lstList1.get(self.lstList1.curselection()) #Listbox's selected value
    conn = sqlite3.connect('phonebook.db')
    with conn:
        cur = conn.cursor()
        #check count to ensure that this is not the last record in
        #the database...cannot delete last record or we will get an error
        cur.execute("""SELECT COUNT(*) FROM tbl_phonebook""")
        count = cur.fetchone()[0]
        if count > 1:
            confirm = mgbx.askokcancel("Delete Confirmation", "All information associated \
with, ({}) \nwill be permanantly deleted.".format(var_select))
            if confirm:
                conn = sqlite3.connect('phonebook.db')
                with conn:
                    cur = conn.cursor()
                    cur.execute("""DELETE FROM tbl_phonebook WHERE col_fullname = '{}'""".format(var_select))
                onDeleted(self) #call function to clear all of the textboxes and the
                #selected index of listbox
                ###onRefresh(self) #update the listbox of the changes
                conn.commit()
        else:
            confirm = mgbx.showerror("Last Record Error", "({}) is the last record in the \
database and cannot be deleted at this time.".format(var_select))
    conn.close()


def onDeleted(self):
    #clear the text in these textboxes
    self.txt_fname.delete(0,END)
    self.txt_lname.delete(0,END)
    self.txt_phone.delete(0,END)
    self.txt_email.delete(0,END)
##  onRefresh(self) #update the listbox of the changes
    try:
        index = self.lstList1.curselection()[0]
        self.lstList1.delete(index)
    except IndexError:
        pass

def onClear(self):
    #clear text in these textboxes
    self.txt_fname.delete(0,END)
    self.txt_lname.delete(0,END)
    self.txt_phone.delete(0,END)
    self.txt_email.delete(0,END)

def onRefresh(self):
    #Populate the listbox, coinciding with the database
    self.lstList1.delete(0,END)
    conn = sqlite3.connect('phonebook.db')
    with conn:
        cur = conn.cursor()
        cur.execute("""SELECT COUNT(*) FROM tbl_phonebook""")
        count = cur.fetchone()[0]
        i = 0
        while i < count:
            cur.execute("""SELECT col_fullname FROM tbl_phonebook""")
            varList = cur.fetchall()[i]
            for item in varList:
                self.lstList1.insert(0,str(item))
                i = i + 1
    conn.close()

def onUpdate(self):
    try:
        var_select = self.lstList1.curselection()[0] #index of the list selection
        var_value = self.lstList1.get(var_select) #list selection's text value
    except:
        mgbx.showinfo("Missing selection","No name was selected from the list box. \nCancelling the Update request.")
        return
    #The user will only be allowed to update changes for phone and emails.
    #For name changes, the user will need to delete the entire record and start over.
    var_phone = self.txt_phone.get().strip() #normalize the data to maintain database integrity
    var_email = self.txt_email.get().strip()
    if (len(var_phone) > 0) and (len(var_email) > 0): #ensure that there is data present
        conn = sqlite3.connect('phonebook.db')
        with conn:
            cur = conn.cursor()
            #count records to see if the user's changes are already in
            #the database...meaning, there are no changes to update
            cur.execute("""SELECT COUNT(col_phone) FROM tbl_phonebook WHERE col_phone = '{}'""".format(var_phone))
            count = cur.fetchone()[0]
            print(count)
            cur.execute("""SELECT COUNT(col_email) FROM tbl_phonebook WHERE col_phone = '{}'""".format(var_email))
            count2 = cur.fetchone()[0]
            print(count2)
            if count == 0 or count2 == 0: #if proposed changes are not already in the database, then proceed
                response = mgbx.askokcancel("Update Request","The following changes ({}) and ({}) will be implemented for ({}). \nProceed with the update?".format(var_phone, var_email, var_value))
                print(response)
                if response:
                    with conn:
                        cur = conn.cursor()
                        cur.execute("""UPDATE tbl_phonebook SET col_phone = '(0)',col_email = '(1)' WHERE col_fullname = '(2)'""")
                        onClear(self)
                        conn.commit()
                else:
                    mgbx.showinfo("Cancel request","No changes havde been made to ({}).".format(var_value))
            else:
                 mgbx.showinfo("No changes detected","Both ({}) and ({}) \nalready exist in the database for this name. \n\nYour update request cannot be completed.".format(var_phone, var_email))
            onClear(self)
        conn.close()
    else:
        mgbx.showerror("Missing Information","Please select a name from the list. \nThen edit the phone or email information.")
    onClear(self)



if __name__ == "__main__":
    pass
























    
                                                                                   
                    







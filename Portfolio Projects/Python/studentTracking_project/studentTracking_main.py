# Python Ver:   3.11.7
#
# Author:       Elisha K Stevens
#
# Purpose:      Student Tracking App. Demonstrating OOP, Tkinter GUI module,
#               using Tkinter Parent and Child relationships
#
# Tested OS:    This code was written and tested to work with Windows 10.



#import Tkinter and our own created modules
from tkinter import *
import tkinter as tk
import studentTracking_gui as gui
import studentTracking_func as func


#Frame is the Tkinter frame class that our own class will inherit from
class ParentWindow(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        #define our master frame configuration
        self.master = master
        self.master.minsize(800,400) #(Height,Width)
        self.master.maxsize(800,400)
        #This CenterWindow method will center our app on the user's screen
        func.center_window(self,800,400)
        self.master.title("Student Tracking")
        self.master.config(bg="#d8bfd8")
        #This protocol method is a tkinter built-in method to catch if the
        #user clicks the upper corner, "X" on Windows OS
        self.master.protocol("WM_DELETE_WINDOW", lambda: func.ask_quit(self))
        arg = self.master
        #load in the GUI widgets from separate module,
        #keeping code compartmentalized and clutter free
        gui.load_gui(self)



if __name__ == "__main__":
    root = tk.Tk()
    App = ParentWindow(root)
    root.mainloop()

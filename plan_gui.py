# -*- coding: utf-8 -*-
"""
Created on Fri May 18 22:17:19 2018

@author: Kyran Adams
"""

from tkinter import filedialog
from tkinter import *
import pandas as pd
import plan

class Window(Frame):
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        
        self.save_file = None
        
        self.plan_model = plan.PlanModel()
        
        self.class_data = plan.ClassData()
        #reference to the master widget, which is the tk window                 
        self.master = master

        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget      
        self.master.title("Four Year Planner")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the file object)
        file = Menu(menu)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        file.add_command(label="Open", command=self.open_file)
        file.add_command(label="Update Class Data", command=self.update_class_data)
        file.add_command(label="Save", command=self.save)
        file.add_command(label="Save As", command=self.save_as)
        file.add_command(label="Exit", command=self.client_exit)

        #added "file" to our menu
        menu.add_cascade(label="File", menu=file)

        # create the file object)
        edit = Menu(menu)

        edit.add_command(label=":/")

        #added "file" to our menu
        menu.add_cascade(label="Help", menu=edit)
        self.create_spreadsheet()
        self.cellframe.pack()
        self.pack()
        
    def create_spreadsheet(self, years=4, num_classes=8):
        # Frame for all the cells
        self.cellframe = Frame(self)
        self.cellframe.pack(side='top')

        # Column labels
        blank = Label(self.cellframe)
        blank.grid(row=0, column=0)
        for y in range(years):
            for j in range(3):
                label = Label(self.cellframe, text="Year %d" % (y+1))
                label.grid(row=num_classes*y+2, column=0)
                semester = ['fall', 'spring', 'summer'][j]
                label = Label(self.cellframe, text=semester)
                label.grid(row=num_classes*y, column=j+2)

        self.sva = {}
        self.entries = {}
        # Fill in the rows
        for y in range(years):
            for j in range(3):
                for i in range(num_classes):
                    rowlabel = Label(self.cellframe, text=str(i + 1))
                    rowlabel.grid(row=2+i + y*num_classes, column=1)
                    sem = ['fall', 'spring', 'summer'][j]
                    ind = (y, sem, i)
                    self.sva[ind] = StringVar()
                    self.sva[ind].trace('w', 
                            lambda name, index, mode, 
                            var=self.sva[ind], 
                            y=y, 
                            semester=sem, 
                            i=i:
                              self.sync_validate(var.get(), y, semester, i))
                    field = Entry(self.cellframe, textvariable=self.sva[ind])
                    self.entries[ind] = field
                    field.grid(row=2+i + y*num_classes, column=2+j)


    def sync_validate(self, value, year, semester, class_ind):
        """
        Whenever a value is typed into an entry, this callback function is 
        called.
        Arguments:
            value: The string value of the entry
            year: The 0 indexed year of the entry
            semester: Either 'fall', 'spring', or 'summer'
            class_ind: The 0 indexed class index
        """
        self.plan_model.set_class(value, year, semester, class_ind)
        self.validate(year, semester, class_ind)
        
    def validate(self, year, semester, class_ind):
        class_name = self.plan_model.get_class(year, semester, class_ind)
        ind = (year, semester, class_ind)
        entry = self.entries[ind]
        entry.config({"background": 'white'})
        # Invalid class
        if pd.isnull(class_name):
            return
        if not self.class_data.class_exists(class_name):   
            entry.config({"background": 'red'})
            print("Class %s does not exist" % class_name)
            return
        elif not self.class_data.offered_last_semester(class_name, semester):
            entry.config({"background": 'yellow'})
            print("Class %s was not offered last %s" % (class_name, semester))
        self.update()
    
    def save(self):
        if self.save_file == None:
            self.save_as()
        else:
            self.plan_model.save(self.save_file)
        
    def save_as(self):
        f = filedialog.asksaveasfilename(defaultextension=".pln")
        if f is None:
            return
        self.save_file=f
        self.save()
        
    def open_file(self):
        f = filedialog.askopenfilename(defaultextension=".pln")
        if f is None:
            return
        self.plan_model.open_file(f)
        for (year, semester, row), sv in self.sva.items():
            class_name = self.plan_model.get_class(year, semester, row)
            if pd.isnull(class_name):
                sv.set("")
            else:
                sv.set(class_name)
    
    def update_class_data(self):
        self.class_data.update_data()
    
    def client_exit(self):
        self.save()
        exit()
        

root = Tk()

root.geometry("600x900")

#creation of an instance
app = Window(root)

#mainloop 
root.mainloop()  
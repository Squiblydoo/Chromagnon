from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as st
from tkinterdnd2 import DND_FILES, TkinterDnD

import sys
import os
currentDirectory = os.path.dirname(os.path.realpath(__file__))
parentDirectory = os.path.dirname(currentDirectory)
sys.path.append(parentDirectory)

import chromagnonSession

class main_window(TkinterDnD.Tk):
    def __init__(self):
        TkinterDnD.Tk.__init__(self)
        self.geometry("800x600")
        self.title("Chromagnon Session Viewer")
        treeviewStyle = ttk.Style()
        treeviewStyle.configure("Treeview", 
                background="white")
        treeviewStyle.map("Treeview",
                background=[('selected', 'blue')])
        
        instructionLabel = Label(self, text="Drag and drop Session or Tab file into window")
        instructionLabel.pack()

        treeFrame = Frame(self)
        treeFrame.pack(pady=20)
        verticalScroll = Scrollbar(treeFrame)
        horizontalScroll = Scrollbar(treeFrame, orient='horizontal')
        self.dataTable = ttk.Treeview(treeFrame, yscrollcommand=verticalScroll.set, xscrollcommand=horizontalScroll.set, height=500)
        verticalScroll.config(command=self.dataTable.yview)
        horizontalScroll.config(command=self.dataTable.xview)
        verticalScroll.pack(side=RIGHT, fill=Y)
        horizontalScroll.pack(side=BOTTOM, fill=X)
        self.dataTable.pack()


        ## Design table
        self.dataTable['columns'] = ('Command',)

        self.dataTable.column("#0", width=50, minwidth = 25)
        self.dataTable.column("Command", anchor=W, width=800)

        ## Headings
        self.dataTable.heading("#0", text="")
        self.dataTable.heading("Command", text="Command", anchor=W)
        

        ## Handle drag-and-drop
        self.dataTable.drop_target_register(DND_FILES)
        self.dataTable.dnd_bind("<<Drop>>", self.processFileUpload)
        self.dataTable.pack()

    ## Function to remove all records when necessary
    def removeRecords(self):
        for record in self.dataTable.get_children():
            self.dataTable.delete(record)

    ## Handle uploading of SNSS files
    def processFileUpload(self, event):
        ## We remove all records in the event that the user
        ## has already uploaded a file, but uploads a second one.
        self.removeRecords()

        ## Take the path of the file, parse the file
        ## Display the data.
        filePath = event.data
        if filePath[0] == '{' and filePath[-1] == '}':
            filePath=filePath[1:-1]
        sessionParse = chromagnonSession.guiParse(filePath)
        self.count = 0
        self.sessionEntry = 0

        ## At the current time sessionParse returns raw data
        ## from the SNSS files. This will likely be changed and
        ## Parses more intentionally at a later time.
        for record in sessionParse:
            self.dataTable.insert(parent='', index='end', iid=self.count, text=self.sessionEntry,
                                  values=(record,))
            self.count += 1
            self.sessionEntry += 1




def main():
    root = main_window()
    root.mainloop()

if __name__=="__main__":
    main()
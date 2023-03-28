from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as st
from tkinterdnd2 import DND_FILES, TkinterDnD

import sys
import os
import pyperclip
import itertools

currentDirectory = os.path.dirname(os.path.realpath(__file__))
parentDirectory = os.path.dirname(currentDirectory)
sys.path.append(parentDirectory)

import chromagnonSession
import chromagnonGUI.chromagnonAbout

class main_window(TkinterDnD.Tk):
    def __init__(self):
        TkinterDnD.Tk.__init__(self)
        self.geometry("1200x600")
        self.title("Chromagnon Session Viewer")
        treeviewStyle = ttk.Style()
        treeviewStyle.configure("Treeview", 
                background="white")
        treeviewStyle.map("Treeview",
                background=[('selected', 'blue')])
        
        ## Create menu bar
        menubar = Menu(self)
        helpMenu = Menu(menubar, tearoff=0)
        helpMenu.add_command(label="About...", command=self.showAbout)
        menubar.add_cascade(label="Help", menu=helpMenu)
        self.config(menu=menubar)

        
        instructionLabel = Label(self, \
                                 text="Drag and drop Session or Tab file into window")
        instructionLabel.pack()

        treeFrame = Frame(self)
        treeFrame.pack(pady=20, expand=True, anchor=W)
        verticalScroll = Scrollbar(treeFrame)
        horizontalScroll = Scrollbar(treeFrame, orient='horizontal')
        self.dataTable = ttk.Treeview(treeFrame, \
                                      yscrollcommand=verticalScroll.set,\
                                      xscrollcommand=horizontalScroll.set, \
                                      height=500)
        verticalScroll.config(command=self.dataTable.yview)
        horizontalScroll.config(command=self.dataTable.xview)
        verticalScroll.pack(side=RIGHT, fill=Y)
        horizontalScroll.pack(side=BOTTOM, fill=X)
        self.dataTable.pack(anchor=W)

        ## Allow user to copy using Control+C
        self.dataTable.bind("<Control-Key-c>", self.copyFromTreeview)
        
        ## Create a menu for copying using right-click
        self.popupMenu = Menu(self.dataTable, tearoff=0)
        self.popupMenu.add_command(command=self.copyFromTreeview, label="Copy")
        self.dataTable.bind('<Button-3>', self.handlePopUpMenu )



        ## Design table
        self.dataTable['columns'] = ('Command',)

        self.dataTable.column("#0", width=50, minwidth = 25)
        self.dataTable.column("Command", anchor=W, width=2000)

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
            self.dataTable.insert(parent='', 
                                  index='end', 
                                  iid=self.count, 
                                  text=self.sessionEntry,
                                  values=(record,))
            self.count += 1
            self.sessionEntry += 1


    def showAbout(self):
        newWindow = chromagnonAbout.main_window()

    ## Copy entire selected row
    def copyFromTreeview(self):
        selection = self.dataTable.selection()
        copyValues = []
        for each in selection:
            value = self.dataTable.item(each)["values"]
            copyValues.append(value)
        copyList = list(itertools.chain.from_iterable(copyValues))
        copyString = " ".join(map(str,copyList))
        pyperclip.copy(copyString)

    ## Handle Popup menu for Right-click; Highlight right-clicked row
    def handlePopUpMenu(self, event):
        selectedRow = self.dataTable.identify_row(event.y)
        self.dataTable.identify_row(event.y)
        self.dataTable.selection_set(selectedRow)
        self.popupMenu.post(event.x_root, event.y_root)




def main():
    root = main_window()
    root.mainloop()

if __name__=="__main__":
    main()
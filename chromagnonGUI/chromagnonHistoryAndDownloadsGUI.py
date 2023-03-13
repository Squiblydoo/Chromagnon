from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as st
from tkinterdnd2 import DND_FILES, TkinterDnD

import sys
import os

###
### Since the visited links are stored in a salted hash table, it is not possible
### to extract the item of the hash table. It only possible to verify if a given
### list is in the hash table.
###


currentDirectory = os.path.dirname(os.path.realpath(__file__))
parentDirectory = os.path.dirname(currentDirectory)
sys.path.append(parentDirectory)

import chromagnonHistory
import chromagnonDownload
import chromagnonAbout

class main_window(TkinterDnD.Tk):
    def __init__(self):
        TkinterDnD.Tk.__init__(self)
        self.geometry("800x600")
        self.title("Chromagnon History and Downloads Viewer")
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

        instructionLabel = Label(self, text="Drag and drop History file into window")
        instructionLabel.pack()

        treeFrame = Frame(self)
        treeFrame.pack(pady=20, expand=True, anchor=W)
        verticalScroll = Scrollbar(treeFrame)
        horizontalScroll = Scrollbar(treeFrame, orient='horizontal')
        self.dataTable = ttk.Treeview(treeFrame, yscrollcommand=verticalScroll.set, xscrollcommand=horizontalScroll.set, height=500)
        verticalScroll.config(command=self.dataTable.yview)
        horizontalScroll.config(command=self.dataTable.xview)
        verticalScroll.pack(side=RIGHT, fill=Y)
        horizontalScroll.pack(side=BOTTOM, fill=X)
        self.dataTable.pack(anchor=W)


        ## Design table
        self.dataTable['columns'] = ('Event Time', 'Event Type', 'Full Entry')

        self.dataTable.column("#0", width=50, minwidth = 25)
        self.dataTable.column("Event Time", width=150)
        self.dataTable.column("Event Type", width=90)
        self.dataTable.column("Full Entry", width=2000)

        ## Headings
        self.dataTable.heading("#0", text="")
        self.dataTable.heading("Event Time", text="Event Time", anchor=W)
        self.dataTable.heading("Event Type", text="Event Type", anchor=W)
        self.dataTable.heading("Full Entry", text="Full Entry", anchor=W)
        

        ## Handle drag-and-drop
        self.dataTable.drop_target_register(DND_FILES)
        self.dataTable.dnd_bind("<<Drop>>", self.processFileUpload)
        self.dataTable.pack(expand=True)


    ## Process file when uploaded via GUI
    def processFileUpload(self, event):
        filePath = event.data
        if filePath[0] == '{' and filePath[-1] == '}':
            filePath=filePath[1:-1]

        ## Parse files and combine the output.
        historyParse = chromagnonHistory.guiParse(filePath)
        downloadParse = chromagnonDownload.guiParse(filePath)
        combinedOutput = historyParse + downloadParse
        
        ## Sort output by date
        combinedOutput.sort(key=lambda x: x[1])


        ## Load and sort output into table
        self.count = 0
        self.sessionEntry = 0
        for record in combinedOutput:
            if record[0] == "Download Event":
                self.dataTable.insert(parent='', index='end', iid=self.count, text=self.sessionEntry,
                                    values=(record[1], "Download", record[4] + "--- Chromium Disposition: " + record[6]))
                self.count += 1
                self.dataTable.insert(parent=self.count - 1, index='end', iid=self.count , text = self.sessionEntry,
                                      values=(record[1], "Referrer: ", record[2]))
                self.count += 1
                self.dataTable.insert(parent=self.count - 2, index='end', iid=self.count , text = self.sessionEntry,
                                      values=(record[1], "URL: ", record[3]))
                self.count += 1
                self.dataTable.insert(parent=self.count - 3, index='end', iid=self.count , text = self.sessionEntry,
                                      values=(record[1], "State: ", record[5]))
                self.count += 1
                self.dataTable.insert(parent=self.count - 3, index='end', iid=self.count , text = self.sessionEntry,
                                      values=(record[1], "State: ", record[6]))
                
                self.count += 1
                self.sessionEntry += 1
            elif record[0] == "History Event":
                self.dataTable.insert(parent='', index='end', iid=self.count, text=self.sessionEntry,
                                    values=(record[1], "History", record,))
                self.count += 1
                self.sessionEntry += 1
                

    def showAbout(self):
        newWindow = chromagnonAbout.main_window()


def main():
    root = main_window()
    root.mainloop()

if __name__=="__main__":
    main()
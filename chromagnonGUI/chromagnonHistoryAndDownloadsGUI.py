from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as st
from tkinterdnd2 import DND_FILES, TkinterDnD
from pathlib import Path
import sys
import os
import pyperclip
import itertools

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
import chromagnonGUI.chromagnonAbout

class main_window(TkinterDnD.Tk):
    def __init__(self):
        TkinterDnD.Tk.__init__(self)
        self.geometry("1200x600")
        self.title("Chromagnon History and Downloads Viewer")
        treeviewStyle = ttk.Style()
        treeviewStyle.configure("Treeview", 
                background="self[background]", foreground="self[foreground]")
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

        ## Define table properties
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

        ## Allow user to copy using Control+C
        self.dataTable.bind("<Control-Key-c>", self.copyFromTreeview)
        
        ## Create a menu for copying using right-click
        self.popupMenu = Menu(self.dataTable, tearoff=0)
        self.popupMenu.add_command(command=self.copyFromTreeview, label="Copy")
        self.dataTable.bind('<Button-2>', self.handlePopUpMenu )
        self.dataTable.bind('<Button-3>', self.handlePopUpMenu )

        ## Design table
        self.dataTable['columns'] = ('Event Time', 'Event Type', 'Title/Download', 'URL' )

        self.dataTable.column("#0", width=60, minwidth = 50)
        self.dataTable.column("Event Time", width=150,minwidth = 150)
        self.dataTable.column("Event Type", width=90, minwidth = 90)
        self.dataTable.column("Title/Download", width=150, minwidth = 150)
        self.dataTable.column("URL", width=2000)

        ## Headings
        self.dataTable.heading("#0", text="")
        self.dataTable.heading("Event Time", text="Event Time", anchor=W)
        self.dataTable.heading("Event Type", text="Event Type", anchor=W)
        self.dataTable.heading("Title/Download", text="Title/Download", anchor=W)
        self.dataTable.heading("URL", text="URL", anchor=W)
        
        ## Data tags
        self.dataTable.tag_configure("DownloadHighlight", background="#d8ffcc")
        self.dataTable.tag_configure("HistoryHighlight", background="white")


        ## Handle drag-and-drop
        self.dataTable.drop_target_register(DND_FILES)
        self.dataTable.dnd_bind("<<Drop>>", self.processFileUpload)
        self.dataTable.pack(expand=True)
        
    ## Function to remove all records when necessary
    def removeRecords(self):
        for record in self.dataTable.get_children():
            self.dataTable.delete(record)

    ## Process file when uploaded via GUI
    def processFileUpload(self, event):
        ## We remove all records in the event that the user
        ## has already uploaded a file, but uploads a second one.
        self.removeRecords()

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
        self.recordEntry = 0
        for record in combinedOutput:
            if record[0] == "Download Event":
                self.dataTable.insert(parent='', index='end', iid=self.count, text=self.recordEntry,
                                    values=(record[1], "Download", Path(record[4]).name, record[3]),
                                    tags=("DownloadHighlight",))
                self.count += 1
                self.dataTable.insert(parent=self.count - 1, index='end', iid=self.count , text = self.recordEntry,
                                      values=(record[1], "Referrer: ", "--------------------->" , record[2]),
                                    tags=("DownloadHighlight",))
                
                self.count += 1
                self.dataTable.insert(parent=self.count - 2, index='end', iid=self.count , text = self.recordEntry,
                                      values=(record[1], "Ref Tab Url: ", "--------------------->" , record[7]),
                                    tags=("DownloadHighlight",))
                self.count += 1
                self.dataTable.insert(parent=self.count - 3, index='end', iid=self.count , text = self.recordEntry,
                                      values=(record[1], "Disposition: ", record[6]),
                                    tags=("DownloadHighlight",))
                self.count += 1
                self.dataTable.insert(parent=self.count - 4, index='end', iid=self.count , text = self.recordEntry,
                                      values=(record[1], "State: ", record[5]),
                                    tags=("DownloadHighlight",))
                self.count += 1
                self.dataTable.insert(parent=self.count - 5, index='end', iid=self.count , text = self.recordEntry,
                                      values=(record[1], "File Path: ", record[4]),
                                    tags=("DownloadHighlight",))
                
                self.count += 1
                self.recordEntry += 1
            elif record[0] == "History Event":
                self.dataTable.insert(parent='', index='end', iid=self.count, text=self.recordEntry,
                                    values=(record[1], "History", record[4] , record[5],),
                                    tags=("HistoryHighlight",))
                self.count += 1
                self.dataTable.insert(parent=self.count - 1, index='end', iid=self.count , text = self.recordEntry,
                                      values=(record[1], "Transition: ", record[3]))
                
                self.count += 1
                self.dataTable.insert(parent=self.count - 2, index='end', iid=self.count , text = self.recordEntry,
                                      values=(record[1], "Visit Count: ", record[2]))
                
                self.count += 1
                self.recordEntry += 1
                

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
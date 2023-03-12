from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as st
from tkinterdnd2 import DND_FILES, TkinterDnD
import sys
import os

## Import links to each GUI

import chromagnonGUI.chromagnonSessionGUI  
import chromagnonGUI.chromagnonHistoryAndDownloadsGUI

class main_window(TkinterDnD.Tk):
    def __init__(self):
        TkinterDnD.Tk.__init__(self)
        self.geometry("300x300")
        self.title("Chromagnon")

        ## Define buttons for new windows. These will likely be redesigned at a later point.
        historyAndDownloadsViewer = Button(self, text="History and Downloads Viewer", state=DISABLED, command=self.launchHistoryAndDownloadsViewer)
        vistedLinksViewer = Button(self, text="Visited Links Viewer", state=DISABLED)
        cacheDataViewer = Button(self, text="Cache Data Viewer", state=DISABLED)
        sessionViewer = Button(self, text="Session and Tab Viewer", command=self.launchSessionViewer)

        ## Pack buttons to window.
        historyAndDownloadsViewer.pack()
        vistedLinksViewer.pack()
        cacheDataViewer.pack()
        sessionViewer.pack()


    ## Define commands for launching windows.
    def launchSessionViewer(self):
        newWindow = chromagnonGUI.chromagnonSessionGUI.main_window()

    def launchHistoryAndDownloadsViewer(self):
        newWindow = chromagnonGUI.chromagnonHistoryAndDownloadsGUI.main_window()



def main():
    root = main_window()
    root.mainloop()

if __name__=="__main__":
    main()
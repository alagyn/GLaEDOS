# Gui for GLaEDO


import tkinter as tk
from tkinter import N, E, S, W
from ui.UIconsts import *
from typing import List
import model.library as lib


class Gui(tk.Frame):
    def __init__(self):
        super().__init__(tk.Tk())
        self.master.title(GUI_TITLE)
        self.master.protocol('WM_DELETE_WINDOW', self.close)

        # MENU BAR
        self.menubar = tk.Menu(self)
        self.setupMenuBar()

        # DATA
        self.games: List[lib.Game] = []
        self.gameNames: List[str] = []
        self.currentTags: List[str] = []
        self.totalTags: List[str] = []

        self.loadLibrary()

        # MAIN FRAMES
        self.setupMainFrames()

    def loadLibrary(self):
        self.games, self.totalTags = lib.readLibrary(LIB_FILE)
        self.setNames()

    def setNames(self):
        self.gameNames = []
        for x in self.games:
            self.gameNames.append(x.name)

    def setupMainFrames(self):
        self.grid(column=0, row=0)
        lFrame = tk.Frame(self, borderwidth=3, relief='groove')
        rFrame = tk.Frame(self, borderwidth=3, relief='groove')
        lFrame.grid(column=0, row=0)
        rFrame.grid(column=1, row=0)
        lFrame.grid_columnconfigure(0, weight=1)
        rFrame.grid_columnconfigure(0, weight=1)

        lList = tk.Listbox(lFrame, height=15, listvariable=tk.StringVar(value=self.gameNames))
        rList = tk.Listbox(rFrame, height=15, listvariable=tk.StringVar(value=self.currentTags))

        lScroll = tk.Scrollbar(lFrame, orient=tk.VERTICAL, command=lList.yview)
        rScroll = tk.Scrollbar(rFrame, orient=tk.VERTICAL, command=rList.yview)

        lList.configure(yscrollcommand=lScroll.set)
        rList.configure(yscrollcommand=rScroll.set)

        lList.grid(column=0, row=0, sticky=(N, S, W, E))
        lScroll.grid(column=1, row=0, sticky=(N, S))
        rList.grid(column=0, row=0, sticky=(N, S, W, E))
        rScroll.grid(column=1, row=0, sticky=(N, S))

    def setupMenuBar(self):
        self.master.option_add('*tearOff', False)
        self.master['menu'] = self.menubar

        menu_file = tk.Menu(self.menubar)
        menu_file.add_command(label='Close', command=self.close)

        menu_edit = tk.Menu(self.menubar)
        menu_edit.add_command(label='New Game', command=self.addNewGame)

        self.menubar.add_cascade(menu=menu_file, label='File')
        self.menubar.add_cascade(menu=menu_edit, label='Edit')

    def close(self):
        lib.writeLibrary(self.games, LIB_FILE)
        print("Close")
        exit()

    def addNewGame(self):
        # TODO add new game cmd
        pass

    def addNewTag(self):
        val = tk.StringVar()
        # TODO add new tag cmd prompt

        if not self.totalTags.__contains__(val.get()):
            self.totalTags.append(val.get())

    def editGame(self, game: lib.Game):
        # TODO edit game cmd
        pass

    def rmTag(self, tag: str):
        # TODO rmTag dialog
        self.totalTags.remove(tag)

    def randFromTags(self, tags: List[str]) -> lib.Game:
        sortedList = self.games
        for x in tags:
            sortedList = lib.sortByTag(x, sortedList)
        return lib.selectRandGame(sortedList)

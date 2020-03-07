# Gui for GLaEDOS


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
        # TODO save/retrieve last opened library
        self.library: lib.Library = lib.readLibrary("")
        #
        self.namesVar = tk.StringVar()
        self.currentTags = tk.StringVar()

        # MAIN FRAMES
        self.setupMainFrames()

    def setupMainFrames(self):
        self.grid(column=0, row=0)
        lFrame = tk.Frame(self, borderwidth=3, relief='groove')
        rFrame = tk.Frame(self, borderwidth=3, relief='groove')
        lFrame.grid(column=0, row=0)
        rFrame.grid(column=1, row=0)
        lFrame.grid_columnconfigure(0, weight=1)
        rFrame.grid_columnconfigure(0, weight=1)

        lList = tk.Listbox(lFrame, height=15, listvariable=self.namesVar)
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
        menu_file.add_command(label='Open Library', command=self.openLib)
        menu_file.add_command(label='Save Library', command=self.saveLib)
        menu_file.add_command(label='Close', command=self.close)

        menu_edit = tk.Menu(self.menubar)
        menu_edit.add_command(label='New Game', command=self.addNewGame)

        self.menubar.add_cascade(menu=menu_file, label='File')
        self.menubar.add_cascade(menu=menu_edit, label='Edit')

    def close(self):
        # TODO Save lib on close
        lib.writeLibrary(self.library, "")
        # print("Close")
        exit()

    def updateGameList(self):
        self.namesVar.set(self.library.getNames())

    def createNewGame(self, name: str, i: bool, c: bool, tags: List[str]):
        pass

    def openLib(self):
        # TODO save before load - overwrite prompt?
        inFile = tk.StringVar()

        # TODO Open lib prompt

        self.library = lib.readLibrary(inFile.get())

    def saveLib(self):
        outFile = tk.StringVar()
        # TODO Save lib prompt
        try:
            lib.writeLibrary(self.library, outFile.get())
        except FileNotFoundError:
            # TODO saveLib FNF error
            pass

    def addNewGame(self):
        # TODO add new game cmd
        prompt = tk.Toplevel()
        nameLabel = tk.Label(prompt, text='Name')
        nameLabel.grid(column=0, row=0)

        nameInput = tk.Entry(prompt)
        nameInput.grid(column=1, row=0)
        nameVar = tk.StringVar()
        nameInput['textvariable'] = nameVar

        def accept():
            # TODO
            #   self.createNewGame()
            self.updateGameList()
            prompt.destroy()

        def cancel():
            # TODO new game cancel
            prompt.destroy()

        confBtn = tk.Button(prompt, text='Accept', command=accept)
        confBtn.grid(column=0, row=1)
        cancBtn = tk.Button(prompt, text='Cancel', command=cancel)
        cancBtn.grid(column=1, row=1)

    def addNewTag(self):
        val = tk.StringVar()
        # TODO add new tag cmd prompt
        self.library.addTag(val.get())

    def editGame(self, game: lib.Game):
        # TODO edit game cmd
        pass

    def rmTag(self):
        val = tk.StringVar()
        # TODO rmTag dialog
        self.library.removeTag(val.get())

    def randFromTags(self, tags: List[str]) -> lib.Game:
        sLib = self.library
        for x in tags:
            sLib = lib.sortByTag(x, sLib)

        return sLib.selectRandGame()

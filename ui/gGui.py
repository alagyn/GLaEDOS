# Gui for GLaEDOS


import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import N, E, S, W
from typing import List
import model.library as lib
import shelve
from os.path import isfile

from .UIconsts import *
from . import shelfKeys as keys


class Gui(tk.Frame):
    def __init__(self):
        super().__init__(tk.Tk())
        self.master.title(GUI_TITLE)
        self.master.protocol('WM_DELETE_WINDOW', self.close)

        # MENU BAR
        self.menubar = tk.Menu(self)
        self.setupMenuBar()

        # DATA
        self.session = shelve.open(SESSION)
        self.curLibFile = ''
        self.loadStartingLib()
        self.library: lib.Library = lib.readLibrary(self.curLibFile)
        self.needToSave = False

        self.namesVar = tk.StringVar()
        self.currentTags = tk.StringVar()

        # MAIN FRAMES
        self.setupMainFrames()

    def loadStartingLib(self):
        try:
            self.curLibFile = self.session[keys.CUR_LIB]
            if not isfile(self.curLibFile):
                self.curLibFile = None
        except KeyError:
            self.curLibFile = None

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
        menu_file.add_command(label='Open', command=self.openLib)
        menu_file.add_command(label='Save', command=self.saveLib)
        menu_file.add_command(label='Save As', command=self.saveAsLib)
        menu_file.add_separator()
        menu_file.add_command(label='Close', command=self.close)

        menu_edit = tk.Menu(self.menubar)
        menu_edit.add_command(label='New Game', command=self.addNewGame)
        menu_edit.add_command(label='New Tag', command=self.addNewTag)

        self.menubar.add_cascade(menu=menu_file, label='File')
        self.menubar.add_cascade(menu=menu_edit, label='Edit')

    def close(self):
        self.saveLib()
        self.session[keys.CUR_LIB] = self.curLibFile
        self.session.close()
        exit()

    def updateGameList(self):
        self.namesVar.set(self.library.getNames())

    def createNewGame(self, name: str, i: bool, c: bool, tags: List[str]):
        pass

    def openLib(self):
        if self.needToSave:
            self.saveLib()

        inFile = tk.StringVar()

        # TODO Open lib prompt

        self.curLibFile = inFile.get()
        self.library = lib.readLibrary(inFile.get())

    def saveLib(self):
        if self.curLibFile is not None:
            try:
                lib.writeLibrary(self.library, self.curLibFile)
            except FileNotFoundError:
                messagebox.showerror(message='Error: File Not Found')
        else:
            self.saveAsLib()

        self.needToSave = False

    def saveAsLib(self):
        file = filedialog.asksaveasfilename(defaultextension=LIB_EXT, initialfile=self.curLibFile)
        if len(file) != 0:
            self.curLibFile = file
            self.saveLib()

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
            self.needToSave = True
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
        self.needToSave = True

    def editGame(self, game: lib.Game):
        # TODO edit game cmd
        pass

    def rmTag(self):
        val = tk.StringVar()
        # TODO rmTag dialog
        self.library.removeTag(val.get())
        self.needToSave = True

    def randFromTags(self, tags: List[str]) -> lib.Game:
        sLib = self.library
        for x in tags:
            sLib = lib.sortByTag(x, sLib)

        return sLib.selectRandGame()

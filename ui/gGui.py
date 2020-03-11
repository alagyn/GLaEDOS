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
        self.tagList = self.library.getTags()
        self.currentTags = tk.StringVar(value=self.tagList)

        # MAIN FRAMES
        self.setupMainFrames()
        self.updateLists()

    def loadStartingLib(self):
        try:
            self.curLibFile = self.session[keys.CUR_LIB]
            if self.curLibFile is not None and not isfile(self.curLibFile):
                self.curLibFile = None
        except KeyError:
            self.curLibFile = None

    def setupMainFrames(self):
        self.grid(column=0, row=0)
        lFrame = tk.LabelFrame(self, text='Games', borderwidth=3, relief='groove')
        rFrame = tk.LabelFrame(self, text='Tags', borderwidth=3, relief='groove')
        lFrame.grid(column=0, row=0)
        rFrame.grid(column=1, row=0)
        lFrame.grid_columnconfigure(0, weight=1)
        rFrame.grid_columnconfigure(0, weight=1)

        lList = tk.Listbox(lFrame, height=15, listvariable=self.namesVar)
        rList = tk.Listbox(rFrame, height=15, listvariable=self.currentTags)

        lScroll = tk.Scrollbar(lFrame, orient=tk.VERTICAL, command=lList.yview)
        rScroll = tk.Scrollbar(rFrame, orient=tk.VERTICAL, command=rList.yview)

        lList.configure(yscrollcommand=lScroll.set)
        rList.configure(yscrollcommand=rScroll.set)

        lList.grid(column=0, row=0, sticky=(N, S, W, E))
        lScroll.grid(column=1, row=0, sticky=(N, S))
        rList.grid(column=0, row=0, sticky=(N, S, W, E))
        rScroll.grid(column=1, row=0, sticky=(N, S))

        # TODO MAIN GUI
        #   Add game btn
        #   Add tag btn
        #   Sort/rand btn
        #   Remove tag btn
        #   Edit/Remove Game btn

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

        self.menubar.add_cascade(menu=menu_file, label='File')
        self.menubar.add_cascade(menu=menu_edit, label='Edit')

    def close(self):
        self.saveLib()
        self.session[keys.CUR_LIB] = self.curLibFile
        self.session.close()
        exit()

    def updateLists(self):
        self.namesVar.set(self.library.getNames())
        self.tagList = self.library.getTags()
        self.currentTags.set(self.tagList)

    def createNewGame(self, name: str, i: bool, c: bool, tags: List[str]):
        pass

    def openLib(self):
        if self.needToSave:
            self.saveLib()

        inFile = filedialog.askopenfilename(defaultextension=LIB_EXT, initialfile=self.curLibFile)

        self.library = lib.readLibrary(inFile)
        self.curLibFile = inFile
        self.updateLists()

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

    def genTagFrame(self, frame) -> List[tk.BooleanVar]:
        idx = 0
        intVars = []
        height = 200
        canv = tk.Canvas(frame, height=height, width=100)

        intFrame = tk.Frame(canv)

        for x in self.tagList:
            var = tk.BooleanVar()
            intVars.append(var)
            btn = tk.Checkbutton(intFrame, text=x, variable=var, onvalue=True, offvalue=False)
            btn.grid(column=0, row=idx, sticky=W)
            idx += 1

        s = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canv.yview)
        canv.grid(column=0, row=0, sticky=(N, E, W, S))
        s.grid(column=1, row=0, sticky=(N, S, W, E))

        canv.create_window(0, 0, window=intFrame, anchor='nw')

        self.update_idletasks()

        canv.configure(scrollregion=canv.bbox('all'))
        canv.configure(yscrollcommand=s.set)

        return intVars

    def addNewGame(self):
        prompt = tk.Toplevel()

        inputFrame = tk.LabelFrame(prompt, text='Data')
        tagFrame = tk.LabelFrame(prompt, text='Tags')

        inputFrame.grid(column=0, row=0, sticky=(N, S), ipadx=4, ipady=4)
        tagFrame.grid(column=1, row=0, sticky=(N, S), ipadx=4, ipady=4)

        nameLabel = tk.Label(inputFrame, text='Name')
        nameLabel.grid(column=0, row=0)

        nameInput = tk.Entry(inputFrame)
        nameInput.grid(column=1, row=0)
        nameVar = tk.StringVar()

        installed = tk.BooleanVar()
        completed = tk.BooleanVar()

        check_installed = tk.Checkbutton(inputFrame, text='Installed', variable=installed, onvalue=True, offvalue=False)
        check_completed = tk.Checkbutton(inputFrame, text='Completed', variable=completed, onvalue=True, offvalue=False)

        check_installed.grid(column=0, row=1, columnspan=2)
        check_completed.grid(column=0, row=2, columnspan=2)

        tagListFrame = tk.LabelFrame(tagFrame, text='Select Tags')
        tagListFrame.grid(column=0, row=0, columnspan=2, sticky=(N, S, E, W))
        selectionVars = self.genTagFrame(tagListFrame)
        tagInputVar = tk.StringVar()

        def addTag():
            self.addNewTag(tagInputVar.get())
            tagInputVar.set('')
            self.updateLists()
            nonlocal selectionVars
            selectionVars = self.genTagFrame(tagListFrame)

        tagInput = tk.Entry(tagFrame, textvariable=tagInputVar)
        tagAddBtn = tk.Button(tagFrame, text='Add Tag', command=addTag)
        tagInput.grid(column=0, row=1)
        tagAddBtn.grid(column=1, row=1)
        nameInput['textvariable'] = nameVar

        def accept():
            if len(nameVar.get()) != 0:
                i = 0
                idxs = []
                for x in selectionVars:
                    if x.get():
                        idxs.append(i)
                    i += 1

                tags = set()
                for x in idxs:
                    tags.add(self.tagList[x])
                self.library.addGame(lib.Game(name=nameVar.get(), installed=installed.get(), completed=completed.get(),
                                              tags=tags))
                self.needToSave = True
                self.updateLists()
                prompt.destroy()

        def cancel():
            prompt.destroy()

        confBtn = tk.Button(prompt, text='Accept', command=accept)
        confBtn.grid(column=0, row=1)
        cancBtn = tk.Button(prompt, text='Cancel', command=cancel)
        cancBtn.grid(column=1, row=1)

    def addNewTag(self, tag: str):
        self.library.addTag(tag)
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

from textwrap import fill
import tkinter
import os
from tkinter import *

from tkinter.messagebox import *

from tkinter.filedialog import *

from ctypes import windll
#fix blurriness of text caused by high DPI
windll.shcore.SetProcessDpiAwareness(1)

class Notepad:
    __root = Tk()
    #default shtuff
    __width = 300
    __height = 300
    __textArea = Text(__root)
    __menuBar = Menu(__root)
    __fileMenu = Menu(__menuBar, tearoff=0)
    __editMenu = Menu(__menuBar, tearoff=0)
    __helpMenu = Menu(__menuBar, tearoff=0)

    #scrollbar support
    __scrollBar = Scrollbar(__textArea)
    __file = None


    def __init__(self,**kwargs):
        #setting icon
        try:
            self.__root.wm_iconbitmap(default="noteslogo_bDw_icon.ico")
        except:
            pass

        try:
            self.__width = kwargs['width']
        except KeyError:
            pass

        #setting window size other than default
        try:
            self.__height = kwargs['height']
        except KeyError:
            pass

        #set title of window
        self.__root.title("Untitled - Note")

        #centering window
        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()

        #left and right alignment
        left = (screenWidth/2) - (self.__width/2)
        top = (screenHeight/2) - (self.__height/2)

        #top and bottom alignment
        self.__root.geometry("%dx%d+%d+%d" % (self.__width,
                                            self.__height,
                                            left, top))

        #text area auto resize
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)

        #add controls
        #New Edit Save Wumbo?
        self.__textArea.grid(sticky= N + E + S + W)

        #new file
        self.__fileMenu.add_command(label="New", command=self.__newFile)

        #open file
        self.__fileMenu.add_command(label="Open", command=self.__openFile)

        #save file
        self.__fileMenu.add_command(label="Save", command=self.__saveFile)

        #line of dialog
        self.__fileMenu.add_separator()
        self.__fileMenu.add_command(label="Exit", command=self.__quitApplication)

        self.__menuBar.add_cascade(label="File", menu=self.__fileMenu)

        #cut copy paste
        self.__editMenu.add_command(label="Cut", command=self.__cut)
        self.__editMenu.add_command(label="Copy", command=self.__copy)
        self.__editMenu.add_command(label="Paste", command=self.__paste)

        #edit
        self.__menuBar.add_cascade(label="Edit", menu=self.__editMenu)

        #description feature
        self.__helpMenu.add_command(label="About Notepad", command=self.__showAbout)
        self.__menuBar.add_cascade(label="Help", menu=self.__helpMenu)

        self.__root.config(menu=self.__menuBar)

        self.__scrollBar.pack(side=RIGHT,fill=Y)

        #scrollbar auto adjust
        self.__scrollBar.config(command=self.__textArea.yview)
        self.__textArea.config(yscrollcommand=self.__scrollBar.set)

    def __quitApplication(self):
        self.__root.destroy()
        #goodbye window

    def __showAbout(self):
        showinfo("Notepad", "By Gavin Harrold")

    def __openFile(self):
        self.__file = askopenfilename(defaultextension=".txt",
                                        filetypes=[("All Files", "*.*"),
                                        ("Text Documents", "*.txt")])
        if self.__file == "":
            self.__file = None
        else:
            self.__root.title(os.path.basename(self.__file) + " - Note")
            self.__textArea.delete(1.0,END)
            file = open(self.__file, "r")
            self.__textArea.insert(1.0, file.read())
            file.close()

    def __newFile(self):
        self.__root.title("Untitled Note")
        self.__file = None
        self.__textArea.delete(1.0,END)
    
    def __saveFile(self):
        if self.__file == None:
            self.__file = asksaveasfilename(initialfile="untitled.txt",
                                            defaultextension=".txt",
                                            filetypes=[("All Files","*.*"),
                                                ("Text Documents", "*.txt")])
            if self.__file == "":
                self.__file = None
            else:
                file = open(self.__file, "w")
                file.write(self.__textArea.get(1.0, END))
                file.close()

                self.__root.title(os.path.basename(self.__file) + "- Note")

        else:
            file = open(self.__file, "w")
            file.write(self.__textArea.get(1.0, END))
            file.close()

    def __cut(self):
        self.__textArea.event_generate("<<Cut>>")

    def __copy(self):
        self.__textArea.event_generate("<<Copy>>")

    def __paste(self):
        self.__textArea.event_generate("<<Paste>>")

    def run(self):
        self.__root.mainloop()

notepad = Notepad(width=600, height=400)
notepad.run()
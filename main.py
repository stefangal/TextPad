import os
from tkinter import *
from tkinter import filedialog, messagebox
import pathlib
import time

__version__ = "1.00"
__author__ = "StefPy"

class TextPad:
    def __init__(self, master):
        self.master = master
        self.master.wm_title('TextPad')
        self.master.iconbitmap('img/TextEditorIcon.ico')
        self.master.geometry(f"900x900+250+250")
        self.master.minsize(900, 900)
        #self.master.bind('<Escape>', lambda e: master.destroy()) # debug quick exit
        self.file_name = ""
        self.orig_openfile = ""

# MENUBAR
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar, background='darkgray')

# FILE < MENUBAR
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label='New         Ctrl+N', command=self.new_file)
        self.file_menu.add_command(label='Open        Ctrl+O', command=self.open_file)
        self.file_menu.add_command(label='Save        Ctrl+S', command=self.save_file)
        self.file_menu.add_command(label='Save as ...', command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Quit        Ctrl+Q', command=self.quit)
        self.menubar.add_cascade(label='File', menu=self.file_menu, underline=0)
# EDIT < MENUBAR
        self.edit_menu = Menu(self.menubar, tearoff=0)
        self.edit_menu.add_command(label='Undo    Ctrl+Z', command=self.undo)
        self.edit_menu.add_command(label='Redo    Ctrl+Y', command=self.redo)
        self.edit_menu.add_command(label='Copy    Ctrl+C', command=self.copy)
        self.edit_menu.add_command(label='Cut      Ctrl+X', command=self.cut)
        self.edit_menu.add_command(label='Paste   Ctrl+V', command=self.paste)
        self.menubar.add_cascade(label='Edit', menu=self.edit_menu, underline=0)
# FORMAT < MENUBAR
        self.format_menu = Menu(self.menubar, tearoff=0)
# FORMAT SUBMENU
        self.format_submenu = Menu(self.format_menu, tearoff=0)

        self.format_menu.add_command(label='Uppercase     Ctrl+U', command=self.uppercase)
        self.format_menu.add_command(label='Lowercase     Ctrl+L', command=self.lowercase)
        self.menubar.add_cascade(label='Format', menu=self.format_menu, underline=0)
# HELP < MENUBAR
        self.help_menu = Menu(self.menubar, tearoff=0)

        self.help_menu.add_command(label='About', command=self.about)
        self.menubar.add_cascade(label='Help', menu=self.help_menu, underline=0)
# FONTS < MENUBAR
        self.menubar.config(font=(None, 10))
        self.file_menu.config(font=(None, 10))
        self.edit_menu.config(font=(None, 10))
        self.format_menu.config(font=(None, 10))
        self.format_submenu.config(font=(None, 10))
        self.help_menu.config(font=(None, 10))
# BAR with filename open or saved
        self.topFrame = Frame(self.master).pack(anchor='ne', fill=X, side=BOTTOM)
        self.bottomFrame = Frame(self.master, relief='solid')
        self.bottomFrame.pack(anchor='sw', fill=X, side=BOTTOM)
# CANVAS
        self.canvas = Canvas(self.topFrame)
        self.canvas.pack(side=TOP, fill=BOTH, anchor='n',expand=True, ipadx=150, padx=100)
# TEXT EDITOR
        self.txt_editor = Text(self.canvas, background='white', relief='raised', borderwidth=0, undo=True)
        self.txt_editor.pack(side=LEFT, anchor='s', expand=True, fill=BOTH)

        self.scrollbar_editor = Scrollbar(self.canvas, command=self.txt_editor.yview)
        self.scrollbar_editor.pack(side=RIGHT, anchor='w', fill=Y)
        self.txt_editor.configure(yscrollcomman=self.scrollbar_editor.set)
# BOTTOM BAR
        self.lbl_bottom = Label(self.bottomFrame, text="New file ... not saved yet.", font=("Helvetica", 10))
        self.lbl_bottom.pack(side=LEFT, fill=X, expand=True)
# BINDINGS
        self.txt_editor.bind('<Control-n>',lambda e: self.new_file())
        self.txt_editor.bind('<Control-o>',lambda e: self.open_file())
        self.txt_editor.bind('<Control-s>',lambda e: self.save_file())
        self.txt_editor.bind('<Control-q>',lambda e: self.quit())
        self.txt_editor.bind('<Control-z>',lambda e: self.undo())
        self.txt_editor.bind('<Control-y>',lambda e: self.redo())
        self.txt_editor.bind('<Control-u>',lambda e: self.uppercase())
        self.txt_editor.bind('<Control-l>',lambda e: self.lowercase())

#==============================================================================================================================================

    def footer_info(self, filepath, tm=None):
        file_size = round(os.stat(filepath).st_size/1024, 2)
        unit = "kB"
        if file_size > 1024:
            file_size = round(file_size / 1024, 3)
            unit = "MB"
        if tm is None:
            tm = time.ctime()
        footerstring = f"File: {filepath}    Last modification:{tm}    Size: {file_size}{unit}"
        self.lbl_bottom.configure(text=footerstring)

    def _content_compare(self):
        self.new_content = self.txt_editor.get(1.0, END)
        self.new_content = str(self.new_content)[:-1]
        return self.orig_openfile.encode() != self.new_content.encode()

# FILE==========================================================================================================================================

    def open_file(self):
        self.file_name = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("text files", "*.txt"),))
        if self.file_name:
            with open(self.file_name, 'r', encoding='utf-8') as f:
                self.orig_openfile = f.read()
        #LOAD DATA
                self.txt_editor.delete(1.0, END)
                self.txt_editor.insert(END, str(self.orig_openfile))
        # OPEN FILE TIMESTAMP
                timestamp = os.stat(self.file_name).st_mtime
                timestamp = time.ctime(timestamp)
        # FOOTER
                self.footer_info(self.file_name, timestamp)

    def new_file(self):
        self.txt_editor.delete(1.0, END)
        self.lbl_bottom.configure(text="New file ... not saved yet.")
        self.file_name = ""

    def save_file(self):
        if self.file_name:
            with open(self.file_name, 'w') as f:
                if f is None: return
                f.write(self.txt_editor.get(1.0, END))
                f.close()
        elif self._content_compare():
            self.save_as_file()
            return
        # FOOTER
        self.footer_info(self.file_name)

    def save_as_file(self):
        file = filedialog.asksaveasfile(initialdir="/", mode='w', defaultextension=".txt", title='Save file')
        if file:
            self.file_name = file.name
        with open(self.file_name, 'w') as f:
            f.write(str(self.txt_editor.get(1.0, END)))
            self.orig_openfile = str(self.txt_editor.get(1.0, END))[:-1]  #save content
            f.close()
        # FOOTER
            self.footer_info(self.file_name)

    def quit(self):
        root.destroy()

# EDIT==========================================================================================================================================

    def undo(self):
        try:
            self.txt_editor.edit_undo()
        except TclError:
            pass

    def redo(self):
        try:
            self.txt_editor.edit_redo()
        except TclError:
            pass

    def paste(self):
        #TODO fire virtual event
        self.txt_editor.event_generate('<Control-v>')

    def copy(self):
        #TODO fire virtual event
        self.txt_editor.event_generate('<Control-c>')

    def cut(self):
        #TODO fire virtual event
        self.txt_editor.event_generate('<Control-x>')

# FORMAT=========================================================================================================================================

    def uppercase(self):
        selection = self.txt_editor.selection_get()
        self.txt_editor.replace(SEL_FIRST, SEL_LAST, selection.upper())

    def lowercase(self):
        selection = self.txt_editor.selection_get()
        self.txt_editor.replace(SEL_FIRST, SEL_LAST, selection.lower())

# ABOUT=========================================================================================================================================

    def about(self):
        self.about_message = messagebox.showinfo(title='About', message=f""" {" "*12}  TextPad {__version__} \n\n This is a simple text editor/viewer.\n\n {" "*12} Author:  {__author__}""")


if __name__ == "__main__":
    root = Tk()
    tp = TextPad(root)
    root.mainloop()

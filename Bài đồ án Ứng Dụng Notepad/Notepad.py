from tkinter import *
from tkinter import messagebox, filedialog
from tkinter import PhotoImage
import os

root = Tk()
# Basic Setup
root.title("tk")
root.geometry("450x300")

# Adding Menubar in the widget
menubar = Menu(root)

# Load Icons for File Menu
newicon = PhotoImage(file='icons/new_file.png')
openicon = PhotoImage(file='icons/open_file.png')
saveicon = PhotoImage(file='icons/save.png')
saveasicon = PhotoImage(file='icons/save_as.png')

# Load Icons for Edit Menu 
undoicon = PhotoImage(file='icons/undo.png')
redoicon = PhotoImage(file='icons/redo.png')
cuticon = PhotoImage(file='icons/cut.png')
copyicon = PhotoImage(file='icons/copy.png')
pasteicon = PhotoImage(file='icons/paste.png')


# File Menu 
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", accelerator='Ctrl + N', image=newicon, compound=LEFT, underline=0, command=lambda: new_file())
filemenu.add_command(label="Open", accelerator='Ctrl + O', image=openicon, compound=LEFT, underline=0, command=lambda: open_file())
filemenu.add_command(label="Save", accelerator='Ctrl + S', image=saveicon, compound=LEFT, underline=0, command=lambda: save_file())
filemenu.add_command(label="Save As", accelerator='Ctrl+Shift+S', image=saveasicon, compound=LEFT, underline=0, command=lambda: save_as_file())
filemenu.add_separator()
filemenu.add_command(label="Exit", accelerator='Alt+F4', command=lambda: exit_file())
menubar.add_cascade(label="File", menu=filemenu)
# File Operations
def new_file():
    root.title("Untitled")
    global filename
    filename = None
    textPad.delete(1.0, END)
def open_file():
    global filename
    filename = filedialog.askopenfilename(defaultextension=".txt", 
                                          filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if filename == "":
        filename = None
    else:
        root.title(os.path.basename(filename) + " - pyPad")
        textPad.delete(1.0, END)
        with open(filename, "r") as fh:
            textPad.insert(1.0, fh.read())
def save_file():
    global filename
    try:
        f = open(filename, 'w')
        letter = textPad.get(1.0, 'end')
        f.write(letter)
        f.close()
    except:
        save_as_file()
def save_as_file():
    global filename
    try:
        file = filedialog.asksaveasfilename(initialfile='Untitled.txt', 
                                            defaultextension=".txt", 
                                            filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if file:
            filename = file
            with open(file, 'w') as fh:
                textoutput = textPad.get(1.0, END)
                fh.write(textoutput)
            root.title(os.path.basename(file) + " - pyPad")
    except:
        pass
def exit_file(event=None):
  if messagebox.askokcancel("Quit", "Do you really want to  quit?"):
    root.destroy()
    root.protocol('WM_DELETE_WINDOW', exit_file)


# Edit Menu 
editMenu = Menu(menubar, tearoff=0)
editMenu.add_command(label="Undo", accelerator='Ctrl + Z', image=undoicon, compound=LEFT, command=lambda: textPad.edit_undo())
editMenu.add_command(label="Redo", accelerator='Ctrl + Y', image=redoicon, compound=LEFT, command=lambda: textPad.edit_redo())
editMenu.add_separator()
editMenu.add_command(label="Cut", accelerator='Ctrl + X', image=cuticon, compound=LEFT, command=lambda: cut())
editMenu.add_command(label="Copy", accelerator='Ctrl + C', image=copyicon, compound=LEFT, command=lambda: copy())
editMenu.add_command(label="Paste", accelerator='Ctrl + V', image=pasteicon, compound=LEFT, command=lambda: paste())
editMenu.add_separator()
editMenu.add_command(label="Find", accelerator='Ctrl + F', command=lambda: on_find())
editMenu.add_separator()
editMenu.add_command(label="Select All", accelerator='Ctrl + A', underline=7, command=lambda: select_all())
menubar.add_cascade(label="Edit", menu=editMenu)
# Edit Operations 

def redo():textPad.event_generate("<<Redo>>")
def cut():textPad.event_generate("<<Cut>>")
def copy():textPad.event_generate("<<Copy>>")
def paste():textPad.event_generate("<<Paste>>")
def select_all():textPad.tag_add("sel", "1.0", END)
# Find  
def on_find():
    t2 = Toplevel(root)
    t2.title('Find')
    t2.geometry('262x65+200+250')
    t2.transient(root)
    Label(t2, text="Find All:").grid(row=0, column=0, sticky='e')
    v = StringVar()
    e = Entry(t2, width=25, textvariable=v)
    e.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    e.focus_set()
    c = IntVar()
    Checkbutton(t2, text='Ignore Case', variable=c).grid(row=1, column=1, sticky='e', padx=2, pady=2)
    Button(t2, text="Find All", underline=0, command=lambda: search_for(v.get(), c.get(), textPad, t2, e)).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)
def search_for(needle, cssnstv, textPad, t2, e):
    textPad.tag_remove('match', '1.0', END)
    count = 0
    if needle:
        pos = '1.0'
        while True:
            pos = textPad.search(needle, pos, nocase=cssnstv, stopindex=END)
            if not pos:
                break
            lastpos = '%s+%dc' % (pos, len(needle))
            textPad.tag_add('match', pos, lastpos)
            count += 1
            pos = lastpos
    textPad.tag_config('match', foreground='red', background='yellow')
    e.focus_set()
    t2.title('%d matches found' % count)


# View Menu 
viewMenu = Menu(menubar, tearoff=0)
themesMenu = Menu(viewMenu, tearoff=0)
showln = IntVar()  
showln.set(1)
showinbar = IntVar()
theme = StringVar()  
viewMenu.add_checkbutton(label="Show Line Number", variable=showln, command=lambda: update_line_number())
viewMenu.add_checkbutton(label="Show Info Bar at Bottom", variable=showinbar ,command=lambda:show_info_bar())
hltln = IntVar()
viewMenu.add_checkbutton(label="Highlight Current Line", onvalue=1, offvalue=0, variable=hltln, command=lambda:toggle_highlight())
menubar.add_cascade(label="View", menu=viewMenu)
# Show Line Number
def update_line_number(event=None):
  textPad.bind("<Any-KeyPress>", update_line_number)
  txt = ''
  if showln.get(): 
     endline, endcolumn = textPad.index('end-1c').split('.')
     txt = '\n'.join(map(str, range(1, int(endline))))
  lnlabel.config(text=txt, anchor='nw')
# Show Info Bar at Bottom
def show_info_bar():
  val = showinbar.get()
  if val:
    infobar.pack(expand=NO, fill=None, side=RIGHT,  
       anchor='se')
  elif not val:
    infobar.pack_forget()
 # Highlighting line 
def highlight_line(interval=100):
    textPad.tag_remove("active_line", 1.0, "end")
    textPad.tag_add("active_line", "insert linestart", "insert  lineend+1c")
    textPad.after(interval, toggle_highlight)
def undo_highlight():
    textPad.tag_remove("active_line", 1.0, "end")
def toggle_highlight(event=None):
  val = hltln.get()
  undo_highlight() if not val else highlight_line()
  textPad.tag_configure("active_line", background="ivory2")


# About Menu 
aboutMenu = Menu(menubar, tearoff=0)
aboutMenu.add_command(label="About", command=lambda: show_about())
aboutMenu.add_command(label="Help", command=lambda: show_help())
menubar.add_cascade(label="About", menu=aboutMenu)
root.config(menu=menubar)
#  About & Help 
def show_about(event=None):
    messagebox.showinfo("About", "Tkinter GUI Application\nDevelopment Hotshot")
def show_help(event=None):
    messagebox.showinfo("Help", "For help refer to book:\nTkinter GUI Application\nDevelopment Hotshot", icon='question')
 


# Incon In ToolBar 
toolbar_actions = {
    'new_file': new_file,
    'open_file': open_file,
    'save': save_file,
    'cut': cut,
    'copy': copy,
    'paste': paste,
    'undo': undo,
    'redo': redo,
    'on_find': on_find,
    'about': show_about,
}
shortcutbar = Frame(root, height=25, bg='light sea green')
icons = ['new_file', 'open_file', 'save', 'cut', 'copy', 'paste', 'undo', 'redo', 'on_find', 'about']
for icon in icons:
    tbicon = PhotoImage(file='icons/' + icon + '.png')
    cmd = toolbar_actions[icon] 
    toolbar = Button(shortcutbar, image=tbicon, command=cmd)
    toolbar.image = tbicon
    toolbar.pack(side=LEFT)
shortcutbar.pack(expand=NO, fill=X)


# Line Color
lnlabel = Label(root, width=2, bg='antique white')
lnlabel.pack(side=LEFT, anchor='nw', fill=Y)


# TextPad and Scrollbar 
textPad = Text(root, undo=True)  
textPad.pack(expand=YES, fill=BOTH)
scroll = Scrollbar(textPad)
textPad.configure(yscrollcommand=scroll.set)
scroll.config(command=textPad.yview)
scroll.pack(side=RIGHT, fill=Y)
textPad.bind("<Button-3>")


# View Menu Theme options
clrschms = {
    'Default White': '000000.FFFFFF',
    'Greygarious Grey': '83406A.D1D4D1',
    'Lovely Lavender': '202B4B.E1E1FF',
    'Aquamarine': '5B8340.D1E7E0',
    'Bold Beige': '4B4620.FFF0E1',
    'Cobalt Blue': 'ffffBB.3333aa',
    'Olive Green': 'D1E7E0.5B8340',
}
# Themes
def change_theme():
    selected_theme = themechoice.get()
    colors = clrschms.get(selected_theme)
    if colors:
        fg_color, bg_color = colors.split('.')
        textPad.config(bg="#" + bg_color, fg="#" + fg_color)
themesMenu = Menu(viewMenu, tearoff=0)
themechoice = StringVar()
themechoice.set('Default White')
for theme_name in sorted(clrschms):
    themesMenu.add_radiobutton(label=theme_name, variable=themechoice, command=change_theme)
viewMenu.add_cascade(label="Themes", menu=themesMenu)
change_theme()


# Show Line Column
infobar = Label(textPad, text='Line: 1 | Column: 0')
infobar.pack(expand=NO, fill=None, side=RIGHT, anchor='se')
def update_cursor_info_bar(event=None):
    currline, curcolumn = textPad.index("insert").split('.')
    infobar.config(text='Line: %s | Column: %s' % (currline, curcolumn))
textPad.bind("<KeyRelease>", update_cursor_info_bar)
textPad.bind("<ButtonRelease-1>", update_cursor_info_bar)
update_cursor_info_bar()

 
# Adding keyboard shortcuts
textPad.bind('<Control-N>', lambda event: new_file())
textPad.bind('<Control-n>', lambda event: new_file())
textPad.bind('<Control-O>', lambda event: open_file())
textPad.bind('<Control-o>', lambda event: open_file())
textPad.bind('<Control-S>', lambda event: save_file())
textPad.bind('<Control-s>', lambda event: save_file())
textPad.bind('<Control-A>', lambda event: select_all())
textPad.bind('<Control-a>', lambda event: select_all())
textPad.bind('<Control-f>', lambda event: on_find())
textPad.bind('<Control-F>', lambda event: on_find())
textPad.bind('<KeyPress-F1>', lambda event: show_help())


# Thêm Ngữ Cảnh
cmenu = Menu(textPad, tearoff=0)  
for i in ('cut', 'copy', 'paste', 'undo', 'redo'):
    cmd = eval(i)
    cmenu.add_command(label=i, compound=LEFT, command=cmd)
cmenu.add_separator()
cmenu.add_command(label='Select All', underline=7, command=select_all)
# Right-click 
def popup(event):
    cmenu.tk_popup(event.x_root, event.y_root, 0)
textPad.bind("<Button-3>", popup)



root.mainloop()
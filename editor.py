# This is how to create a simple text editor

from tkinter import *

from tkinter import ttk, colorchooser, font, filedialog, messagebox
import os

win = Tk()
win.title("PyText")
width = 1200
height = 600
win.geometry(f"{width}x{height}+150+120")
win.iconbitmap("icons/notepad.ico")

###################################      Main Menu Starts       #################################
main_menu = Menu(win)

# file menu
file = Menu(main_menu, tearoff=False)
# file menu icons
new_icon = PhotoImage(file="icons/new.png")
open_icon = PhotoImage(file="icons/open.png")
save_icon = PhotoImage(file="icons/save.png")
saveas_icon = PhotoImage(file="icons/save_as.png")
exit_icon = PhotoImage(file="icons/exit.png")

file.add_command(label="New File", image=new_icon, compound=LEFT,
                 accelerator="Ctrl + N", command=lambda: new_file())
file.add_command(label="Open", image=open_icon, compound=LEFT,
                 accelerator="Ctrl + O", command=lambda: open_file())
file.add_command(label="Save", image=save_icon, compound=LEFT,
                 accelerator="Ctrl + S", command=lambda: save_file())
file.add_command(label="Save as", image=saveas_icon, compound=LEFT,
                 accelerator="Ctrl + Alt + S", command=lambda: save_as_file())
file.add_command(label="Exit", image=exit_icon, compound=LEFT,
                 accelerator="Ctrl + Q", command=lambda: exitNotepad())
main_menu.add_cascade(label="File", menu=file)


# edit menu
edit = Menu(main_menu, tearoff=False)
# edit menu icons
cut_icon = PhotoImage(file="icons/cut.png")
copy_icon = PhotoImage(file="icons/copy.png")
paste_icon = PhotoImage(file="icons/paste.png")
clearall_icon = PhotoImage(file="icons/clear_all.png")
undo_icon = PhotoImage(file="icons/undo.png")
redo_icon = PhotoImage(file="icons/redo.png")


edit.add_command(label="Cut", image=cut_icon, compound=LEFT,
                 accelerator="Ctrl + X", command=lambda: cut())
edit.add_command(label="Copy", image=copy_icon, compound=LEFT,
                 accelerator="Ctrl + C", command=lambda: copy())
edit.add_command(label="Paste", image=paste_icon, compound=LEFT,
                 accelerator="Ctrl + V", command=lambda: paste())
edit.add_command(label="Clear All", image=clearall_icon, compound=LEFT,
                 accelerator="Ctrl + CA", command=lambda: clear_all())
edit.add_command(label="Undo", image=undo_icon, compound=LEFT,
                 accelerator="Ctrl + U", command=lambda: undo())
edit.add_command(label="Redo", image=redo_icon, compound=LEFT,
                 accelerator="Ctrl + R", command=lambda: redo())
main_menu.add_cascade(label="Edit", menu=edit)


# format menu
format = Menu(main_menu, tearoff=False)
# format icons
font_icon = PhotoImage(file="icons/font.png")
font_color = PhotoImage(file="icons/font_color.png")
find_icon = PhotoImage(file="icons/find.png")

format.add_command(label="Color Picker", image=font_color,
                   compound=LEFT, command=lambda: color_picker())
format.add_command(label="Find/Replace", image=find_icon,
                   compound=LEFT, command=lambda: find())
main_menu.add_cascade(label="Format", menu=format)


# view menu
view = Menu(main_menu, tearoff=False)
# view icons
toolbar_icon = PhotoImage(file="icons/tool_bar.png")
statusbar_icon = PhotoImage(file="icons/status_bar.png")
show_toolbar = BooleanVar()
show_toolbar.set(True)
show_statusbar = BooleanVar()
show_statusbar.set(True)
view.add_checkbutton(label="Show Tool Bar", image=toolbar_icon, onvalue=True,
                     offvalue=0, variable=show_toolbar, compound=LEFT, command=lambda: hide_toolbar())
# view.add_checkbutton(label="Show Status Bar",image=statusbar_icon,onvalue=1,offvalue=False,variable=show_statusbar,compound=LEFT,command=lambda:hide_statusbar())
main_menu.add_cascade(label="View", menu=view)

color_theme = Menu(main_menu, tearoff=False)

# color theme icons
light_default_icon = PhotoImage(file="icons/light_default.png")
light_plus_icon = PhotoImage(file="icons/light_plus.png")
dark_icon = PhotoImage(file="icons/dark.png")
red_icon = PhotoImage(file="icons/red.png")
monokai_icon = PhotoImage(file="icons/monokai.png")
night_blue_icon = PhotoImage(file="icons/night_blue.png")

theme_choice = StringVar()

color_theme_icons = (light_default_icon, light_plus_icon,
                     dark_icon, red_icon, monokai_icon, night_blue_icon)

color_theme_dict = {
    "Light Default": ("#000000", "#ffffff"),
    "Light Plus": ("#474747", "#e0e0e0"),
    "Dark": ("#d3b774", "#2d2d2d"),
    "Red": ("#2d2d2d", "#ffe8e8"),
    "Monokai": ("#d3b774", "#347890"),
    "Night Blue": ("#000000", "#6b9dc2")
}
count = 0
for i in color_theme_dict:
    color_theme.add_radiobutton(
        label=i, image=color_theme_icons[count], variable=theme_choice, compound=LEFT, command=lambda: change_theme())
    count += 1

main_menu.add_cascade(label="Color Theme", menu=color_theme)

# help menu
help = Menu(main_menu, tearoff=False)
# help icons
about_icon = PhotoImage(file="icons/about.png")

help.add_command(label="About Notepad", image=about_icon,
                 compound=LEFT, command=lambda: about_notepad())
main_menu.add_cascade(label="Help", menu=help)

# --------------------------------------    Main Menu Ends  ------------------------------------#

########################################   Toolbar Starts  ###################################

tool_bar = Label(win, relief=RIDGE, bg="lightgray")
tool_bar.pack(side=TOP, fill=X, padx=40, pady=2)

tool_bar_label = Label(tool_bar, text="ToolBar : ",
                       font="Arial 15 bold", fg="blue", underline=0)
tool_bar_label.pack(side=LEFT)

# font-family combobox
font_tuple = font.families()
ffamily_var = StringVar()
font_family_box = ttk.Combobox(
    tool_bar, textvariable=ffamily_var, width=30, state="readonly")
font_family_box["values"] = font_tuple
font_family_box.current(font_tuple.index("Arial"))
font_family_box.pack(side=LEFT, padx=15)


# font-size combobox
fsize_var = IntVar()
font_size_box = ttk.Combobox(
    tool_bar, textvariable=fsize_var, width=15, state="readonly")
font_size_box["values"] = tuple(range(8, 81, 4))
font_size_box.current(1)
font_size_box.pack(side=LEFT, padx=15)

# button icons
bold_icon = PhotoImage(file="icons/bold.png")
italic_icon = PhotoImage(file="icons/italic.png")
underline_icon = PhotoImage(file="icons/underline.png")
align_left = PhotoImage(file="icons/align_left.png")
align_center = PhotoImage(file="icons/align_center.png")
align_right = PhotoImage(file="icons/align_right.png")

# buttons
bold_btn = ttk.Button(tool_bar, image=bold_icon, command=lambda: change_bold())
bold_btn.pack(side=LEFT, padx=15)
italic_btn = ttk.Button(tool_bar, image=italic_icon,
                        command=lambda: change_italic())
italic_btn.pack(side=LEFT, padx=15)
underline_btn = ttk.Button(
    tool_bar, image=underline_icon, command=lambda: change_underline())
underline_btn.pack(side=LEFT, padx=15)
align_left_btn = ttk.Button(
    tool_bar, image=align_left, command=lambda: left_align())
align_left_btn.pack(side=LEFT, padx=15)
align_center_btn = ttk.Button(
    tool_bar, image=align_center, command=lambda: center_align())
align_center_btn.pack(side=LEFT, padx=15)
align_right_btn = ttk.Button(
    tool_bar, image=align_right, command=lambda: right_align())
align_right_btn.pack(side=LEFT, padx=15)

# --------------------------------------   Toolbar Ends    ----------------------------------#

editor = Text(win, relief=RAISED, bg="#fff", undo=True)
editor.config(wrap="word")
editor.pack(fill=BOTH, expand=1)
editor.focus()
url = ""

scroll_y = Scrollbar(editor, cursor="arrow")
scroll_y.pack(side=RIGHT, fill=Y)


editor.config(yscrollcommand=scroll_y.set)
scroll_y.config(command=editor.yview)


status_bar = Label(win, text="Status Bar", font=("Arial", 10))
status_bar.pack(side=BOTTOM, fill=X)

current_font_family = "Arial"
current_font_size = 12
editor.configure(font=("Arial", 12))


###############################  all menus functionalities starts here  ####################################
def new_file(event=None):
    global url
    url = ''
    editor.delete(1.0, END)
    win.title("PyText")


def open_file(event=None):
    global url
    url = filedialog.askopenfilename(initialdir=os.getcwd(
    ), title="Select a file", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    try:
        with open(url, 'r') as fr:
            editor.delete(1.0, END)
            editor.insert(1.0, fr.read())
    except FileNotFoundError:
        return
    except:
        return
    win.title(os.path.basename(url))


def save_file(event=None):
    global url
    try:
        if url:
            content = str(editor.get(1.0, END))
            with open(url, "w", encoding="utf-8") as fw:
                fw.write(content)

        # else:
        #     url = filedialog.asksaveasfile(mode="w", defaultextension=".txt", filetypes=(
        #         ("Text Files", "*.txt"), ("All Files", "*.*")))
        #     content2 = editor.get(1.0, END)
        #     url.write(content2)

        #     url.close()
        #     win.title(os.path.basename(str(url)))

    except:
        return


def save_as_file(event=None):
    global url
    try:
        content = editor.get(1.0, END)
        if content > str(0):

            url = filedialog.asksaveasfile(mode="w", defaultextension=".txt", filetypes=(
                ("Text Files", "*.txt"), ("All Files", "*.*")))
            win.title(url)

            url.write(content)
            url.close()

        else:
            messagebox.showwarning(
                "Can't Saved!", "File is empty, need some content...")
    except:
        return


def exitNotepad(event=None):
    exit_win = messagebox.askokcancel(
        "Exit", "Are you sure you want to exit the window?")
    if (exit_win == True):
        win.destroy()
    else:
        return


def cut(event=None):
    editor.event_generate("<<Cut>>")


def copy(event=None):
    editor.event_generate("<<Copy>>")


def paste(event=None):
    editor.event_generate("<<Paste>>")


def clear_all(event=None):
    editor.delete(1.0, END)


def undo(event=None):
    editor.edit_undo()


def redo(event=None):
    editor.edit_redo()


def color_picker():
    color = colorchooser.askcolor()
    editor.configure(fg=color[1])


def hide_toolbar():
    global show_toolbar
    if show_toolbar:
        tool_bar.pack_forget()
        show_toolbar = False
    else:
        editor.pack_forget()
        status_bar.pack_forget()
        tool_bar.pack(side=TOP, fill=X, padx=40, pady=2)
        editor.pack(fill=BOTH, expand=1)
        status_bar.pack(side="bottom", fill="x")
        show_toolbar = True

# def hide_statusbar():
#       global show_statusbar
#       if show_statusbar:
#             status_bar.pack_forget()
#             show_statusbar=False
#       else:
#             status_bar.pack(side=BOTTOM)
#             show_statusbar=True


# find functionality
def find(event=None):

    def find(event=None):
        word = find_input.get()
        editor.tag_remove("match", "1.0", END)
        matches = 0
        if word:
            start_pos = "1.0"
            while True:
                start_pos = editor.search(word, start_pos, stopindex=END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(word)}c"
                editor.tag_add("match", start_pos, end_pos)
                matches += 1
                start_pos = end_pos
                editor.tag_config("match", foreground="red",
                                  background="yellow")

    def replace(event=None):
        word = find_input.get()
        replace_text = replace_input.get()
        content = editor.get(1.0, END)
        new_content = content.replace(word, replace_text)
        editor.delete(1.0, END)
        editor.insert(1.0, new_content)

    def exit_find(event=None):
        find_dialog.destroy()

    find_dialog = Toplevel()
    find_dialog.title("Find/Replace")
    find_dialog.geometry("400x250+500+300")
    find_dialog.resizable(False, False)
    find_dialog.iconbitmap("icons/find.ico")

    find_frame = LabelFrame(find_dialog, text="Find/Replace", padx=20, pady=20)
    find_frame.pack(pady=30)

    # labels
    text_find_label = Label(find_frame, text="Find")
    text_find_label.grid(row=0, column=0, padx=4, pady=4)

    text_replace_label = Label(find_frame, text="Replace")
    text_replace_label.grid(row=1, column=0, padx=4, pady=4)

    # entry box
    find_input = ttk.Entry(find_frame, width=30)
    find_input.grid(row=0, column=1, padx=4, pady=4)

    replace_input = ttk.Entry(find_frame, width=30)
    replace_input.grid(row=1, column=1, padx=4, pady=4)

    # buttons
    find_btn = ttk.Button(find_frame, text="Find", command=lambda: find())
    find_btn.grid(row=2, column=0, padx=4, pady=4)

    replace_btn = ttk.Button(find_frame, text="Replace",
                             command=lambda: replace())
    replace_btn.grid(row=2, column=1, padx=4, pady=4)

    exit_btn = ttk.Button(find_dialog, text="Quit Window",
                          command=lambda: exit_find())
    exit_btn.pack()


# theme choice
def change_theme(event=None):
    choosen_theme = theme_choice.get()
    color_tuple = color_theme_dict.get(choosen_theme)
    fg_color, bg_color = color_tuple[0], color_tuple[1]
    editor.config(background=bg_color, foreground=fg_color)


editor_icon = PhotoImage(file="icons/notes.png")


def about_notepad():
    global editor_icon
    about_dialog = Toplevel()
    about_dialog.geometry("500x300+500+300")
    about_dialog.title("About Notepad")
    about_dialog.resizable(0, 0)
    about_dialog.iconbitmap("icons/notepad.ico")
    about_dialog.configure(bg="darkslategray")

    def exit_about_window(event=None):
        about_dialog.destroy()

    editor_icon_label = Label(
        about_dialog, image=editor_icon, bg="darkslategray")
    editor_icon_label.pack()

    sugg = Label(about_dialog, wraplength=400, font=("Arial", 11), bg="darkslategray", fg="white",
                 text="This is a simple text editor with all the basic functionalities that you need in a text editor like open,save,cut,copy etc.....")
    sugg.pack(pady=10)

    creator = Label(about_dialog, text="Notepad is created by Kamlesh Sharma", font=(
        "Arial", 16), fg="yellow", bg="darkslategray")
    creator.pack(pady=(30, 10))

    exit_btn = ttk.Button(about_dialog, text="Quit Window",
                          command=lambda: exit_about_window())
    exit_btn.pack()


# ----------------------------- all menu functionalities ends here ---------------------------------#

def changed(event=None):
    if editor.edit_modified():
        words = len(editor.get(1.0, 'end-1c').split())
        characters = len(editor.get(1.0, 'end-1c').replace(' ', ''))
        status_bar.config(text=f"Characters : {characters} | Words : {words}")
    editor.edit_modified(0)


editor.bind("<<Modified>>", changed)


def change_font_family(event=None):
    global current_font_family
    current_font_family = ffamily_var.get()
    editor.configure(font=(current_font_family, current_font_size))


font_family_box.bind("<<ComboboxSelected>>", change_font_family)


def change_font_size(event=None):
    global current_font_size
    current_font_size = fsize_var.get()
    editor.configure(font=(current_font_family, current_font_size))


font_size_box.bind("<<ComboboxSelected>>", change_font_size)


# buttons functionality
def change_bold(event=None):
    text_property = font.Font(font=editor["font"])
    if text_property.actual()["weight"] == "normal":
        editor.configure(font=(current_font_family, current_font_size, "bold"))
    if text_property.actual()["weight"] == "bold":
        editor.configure(
            font=(current_font_family, current_font_size, "normal"))
    editor.focus()


def change_italic(event=None):
    text_property = font.Font(font=editor["font"])
    if text_property.actual()["slant"] == "roman":
        editor.configure(
            font=(current_font_family, current_font_size, "italic"))
    if text_property.actual()["slant"] == "italic":
        editor.configure(
            font=(current_font_family, current_font_size, "roman"))
    editor.focus()


def change_underline(event=None):
    text_property = font.Font(font=editor["font"])
    if text_property.actual()["underline"] == 0:
        editor.configure(
            font=(current_font_family, current_font_size, "underline"))
    if text_property.actual()["underline"] == 1:
        editor.configure(
            font=(current_font_family, current_font_size, "normal"))
    editor.focus()


def left_align():
    text_content = editor.get(1.0, END)
    editor.tag_config("left", justify=LEFT)
    editor.delete(1.0, END)
    editor.insert(INSERT, text_content, "left")
    editor.focus()


def center_align():
    text_content = editor.get(1.0, END)
    editor.tag_config("center", justify=CENTER)
    editor.delete(1.0, END)
    editor.insert(INSERT, text_content, "center")
    editor.focus()


def right_align():
    text_content = editor.get(1.0, END)
    editor.tag_config("right", justify=RIGHT)
    editor.delete(1.0, END)
    editor.insert(INSERT, text_content, "right")
    editor.focus()


######## bind shortcure keys ########
win.bind("<Control-n>", new_file)
win.bind("<Control-o>", open_file)
win.bind("<Control-s>", save_file)
win.bind("<Control-Alt-s>", save_as_file)
win.bind("<Control-q>", exitNotepad)
win.bind("<Control-u>", undo)
win.bind("<Control-r>", redo)
win.bind("<Control-f>", find)
win.bind("<Control-b>", change_bold)
win.bind("<Control-i>", change_italic)
win.bind("<Control-u>", change_underline)


win.config(menu=main_menu)
win.mainloop()

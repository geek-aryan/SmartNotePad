import tkinter as tk
from tkinter import ttk
from tkinter import font, colorchooser, messagebox
from speech_recognition import RequestError, WaitTimeoutError, UnknownValueError
import NotePadFileController
import NotePadDBController
import traceback
from tkinter import filedialog, simpledialog
import os
import threading
import time
from datetime import datetime



class Notepad:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('1200x700')
        self.root.title('SmartNotepad')
        self.root.wm_iconbitmap('icons/icon.ico')

        self.set_icons()
        self.set_menu_bar()
        self.set_tool_bar()
        self.set_tool_bar_event_bindings()
        self.set_status_bar()
        self.set_file_menu_event_bindings()

        self.set_file_sub_menu()
        self.set_edit_sub_menu()
        self.set_view_sub_menu()
        self.set_color_theme()
        self.set_canvas()

        self.set_controllers()
        self.check_db_status()

        self.root.protocol("WM_DELETE_WINDOW", self.exit_func)

    def set_icons(self):
        self.new_icon = tk.PhotoImage(file='icons/new.png')
        self.open_icon = tk.PhotoImage(file='icons/open.png')
        self.save_icon = tk.PhotoImage(file='icons/save.png')
        self.save_as_icon = tk.PhotoImage(file='icons/save_as.png')
        self.exit_icon = tk.PhotoImage(file='icons/exit.png')
        self.copy_icon = tk.PhotoImage(file='icons/copy.png')
        self.paste_icon = tk.PhotoImage(file='icons/paste.png')
        self.cut_icon = tk.PhotoImage(file='icons/cut.png')
        self.clear_all_icon = tk.PhotoImage(file='icons/clear_all.png')
        self.find_icon = tk.PhotoImage(file='icons/find.png')
        self.tool_bar_icon = tk.PhotoImage(file='icons/tool_bar.png')
        self.status_bar_icon = tk.PhotoImage(file='icons/status_bar.png')
        self.light_default_icon = tk.PhotoImage(file='icons/light_default.png')
        self.light_plus_icon = tk.PhotoImage(file='icons/light_plus.png')
        self.dark_icon = tk.PhotoImage(file='icons/dark.png')
        self.red_icon = tk.PhotoImage(file='icons/red.png')
        self.monokai_icon = tk.PhotoImage(file='icons/monokai.png')
        self.night_blue_icon = tk.PhotoImage(file='icons/night_blue.png')

    def set_menu_bar(self):
        self.main_menu = tk.Menu()

        self.file = tk.Menu(self.main_menu, tearoff=False)
        self.edit = tk.Menu(self.main_menu, tearoff=False)
        self.view = tk.Menu(self.main_menu, tearoff=False)
        self.color_theme = tk.Menu(self.main_menu, tearoff=False)
        self.p_file = tk.Menu(self.main_menu, tearoff=False)

        self.theme_choice = tk.StringVar()
        self.color_icons = (
            self.light_default_icon, self.light_plus_icon, self.dark_icon, self.red_icon, self.monokai_icon,
            self.night_blue_icon)
        self.color_dict = {
            'Light Default ': ('#000000', '#ffffff'),
            'Light Plus': ('#474747', '#e0e0e0'),
            'Dark': ('#c4c4c4', '#2d2d2d'),
            'Red': ('#2d2d2d', '#ffe8e8'),
            'Monokai': ('#d3b774', '#474747'),
            'Night Blue': ('#ededed', '#6b9dc2')
        }

        self.main_menu.add_cascade(label='File', menu=self.file)
        self.main_menu.add_cascade(label='Edit', menu=self.edit)
        self.main_menu.add_cascade(label='View', menu=self.view)
        self.main_menu.add_cascade(label='Color Theme', menu=self.color_theme)
        self.main_menu.add_cascade(label='Secure Files', menu=self.p_file, compound=tk.LEFT)
        self.root.config(menu=self.main_menu)

    def set_tool_bar(self):
        self.tool_bar = ttk.Label(self.root)
        self.tool_bar.pack(side=tk.TOP, fill=tk.X)
        self.show_toolbar = tk.BooleanVar()
        self.show_toolbar.set(True)
        ## font box
        self.font_tuple = tk.font.families()
        self.font_family = tk.StringVar()
        self.font_box = ttk.Combobox(self.tool_bar, width=30, textvariable=self.font_family, state='readonly')
        self.font_box['values'] = self.font_tuple
        self.font_box.current(self.font_tuple.index('Arial'))
        self.font_box.grid(row=0, column=0, padx=5)
        ## size box
        self.size_var = tk.IntVar()
        self.font_size = ttk.Combobox(self.tool_bar, width=14, textvariable=self.size_var, state='readonly')
        self.font_size['values'] = tuple(range(8, 81))
        self.font_size.current(4)
        self.font_size.grid(row=0, column=1, padx=5)
        ## bold button
        self.bold_icon = tk.PhotoImage(file='icons/bold.png')
        self.bold_btn = ttk.Button(self.tool_bar, image=self.bold_icon)
        self.bold_btn.grid(row=0, column=2, padx=5)
        ## italic button
        self.italic_icon = tk.PhotoImage(file='icons/italic.png')
        self.italic_btn = ttk.Button(self.tool_bar, image=self.italic_icon)
        self.italic_btn.grid(row=0, column=3, padx=5)
        ## underline button
        self.underline_icon = tk.PhotoImage(file='icons/underline.png')
        self.underline_btn = ttk.Button(self.tool_bar, image=self.underline_icon)
        self.underline_btn.grid(row=0, column=4, padx=5)
        ## font color button
        self.font_color_icon = tk.PhotoImage(file='icons/font_color.png')
        self.font_color_btn = ttk.Button(self.tool_bar, image=self.font_color_icon)
        self.font_color_btn.grid(row=0, column=5, padx=5)
        ## align left
        self.align_left_icon = tk.PhotoImage(file='icons/align_left.png')
        self.align_left_btn = ttk.Button(self.tool_bar, image=self.align_left_icon)
        self.align_left_btn.grid(row=0, column=6, padx=5)
        ## align center
        self.align_center_icon = tk.PhotoImage(file='icons/align_center.png')
        self.align_center_btn = ttk.Button(self.tool_bar, image=self.align_center_icon)
        self.align_center_btn.grid(row=0, column=7, padx=5)
        ## align right
        self.align_right_icon = tk.PhotoImage(file='icons/align_right.png')
        self.align_right_btn = ttk.Button(self.tool_bar, image=self.align_right_icon)
        self.align_right_btn.grid(row=0, column=8, padx=5)
        ## mike
        self.mike_icon = tk.PhotoImage(file='icons/microphone.png')
        self.mike_btn = ttk.Button(self.tool_bar, image=self.mike_icon)
        self.mike_btn.grid(row=0, column=9, padx=5)

    def set_tool_bar_event_bindings(self):
        # font family and font size functionality
        self.current_font_family = 'Arial'
        self.current_font_size = 12
        self.font_box.bind("<<ComboboxSelected>>", self.change_font)
        self.font_size.bind("<<ComboboxSelected>>", self.change_fontsize)
        self.bold_btn.configure(command=self.change_bold)
        self.italic_btn.configure(command=self.change_italic)
        self.underline_btn.configure(command=self.change_underline)
        self.font_color_btn.configure(command=self.change_font_color)
        self.align_right_btn.configure(command=self.align_right)
        self.align_center_btn.configure(command=self.align_center)
        self.align_left_btn.configure(command=self.align_left)
        self.mike_btn.configure(command=self.say_something)

    def set_status_bar(self):
        self.status_bar_root=ttk.Label(self.root)
        self.status_bar_root.pack(side=tk.BOTTOM)
        self.status_bar = ttk.Label(self.status_bar_root, text='Status Bar')
        self.status_bar.pack(side=tk.LEFT)
        self.curr_time=ttk.Label(self.status_bar_root, text='Current time:')
        self.curr_time.pack(side=tk.LEFT,padx=50)
        self.Total_time=ttk.Label(self.status_bar_root, text='Total time:')
        self.Total_time.pack(side=tk.LEFT)
        self.count = 0
        self.show_statusbar = tk.BooleanVar()
        self.show_statusbar.set(True)
        t1=threading.Thread(target=self.set_time)
        t2=threading.Thread(target=self.total_time)
        t1.start()
        t2.start()

    def set_time(self):
        while(True):
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            # print("Current Time =", current_time)
            self.curr_time.config(text=f"Current Time: {current_time}")
            time.sleep(1)

    def total_time(self):
        hours=0
        minutes=0
        seconds=0
        while(True):
            if seconds<59:
                seconds+=1
            elif minutes<59 and seconds==59:
                minutes+=1
                seconds=0
            elif hours<23 and seconds==59 and minutes==59:
                hours+=1
                minutes=0
                seconds=0
            # print("time:",hours,minutes,seconds)
            self.Total_time.config(text=f"Total Time: {hours}:{minutes}:{seconds}")
            time.sleep(1)

    def set_file_menu_event_bindings(self):
        self.root.bind("<Control-n>", self.new_file)
        self.root.bind("<Control-N>", self.new_file)
        self.root.bind("<Control-o>", self.open_file)
        self.root.bind("<Control-O>", self.open_file)
        self.root.bind("<Control-s>", self.save_file)
        self.root.bind("<Control-S>", self.save_file)
        self.root.bind("<Alt-s>", self.save_as)
        self.root.bind("<Alt-S>", self.save_as)
        self.root.bind("<Control-q>", self.exit_func)
        self.root.bind("<Control-Q>", self.exit_func)
        self.root.bind("<Control-f>", self.find_func)
        self.root.bind("<Control-F>", self.find_func)

        self.root.bind("<Control-a>", lambda e: self.say_something())
        self.root.bind("<Control-A>", lambda e: self.say_something())

    def set_file_sub_menu(self):
        self.file.add_command(label='New', image=self.new_icon, compound=tk.LEFT, accelerator='Ctrl+N',
                              command=self.new_file)
        self.url = ''
        self.file.add_command(label='Open', image=self.open_icon, compound=tk.LEFT, accelerator='Ctrl+O',
                              command=self.open_file)
        self.file.add_command(label='Save', image=self.save_icon, compound=tk.LEFT, accelerator='Ctrl+S',
                              command=self.save_file)
        self.file.add_command(label='Save As', image=self.new_icon, compound=tk.LEFT, accelerator='Alt+S',
                              command=self.save_as)
        self.file.add_command(label='Exit', image=self.exit_icon, compound=tk.LEFT, accelerator='Ctrl+Q',
                              command=self.exit_func)
        self.p_file.add_command(label='Secure Files', compound=tk.LEFT, accelerator='Ctrl+P',
                                command=self.secure_file)

    def set_edit_sub_menu(self):
        self.edit.add_command(label='Copy', image=self.copy_icon, compound=tk.LEFT, accelerator='Ctrl+C',
                              command=lambda: self.text_editor.event_generate("<Control c>"))
        self.edit.add_command(label='Paste', image=self.paste_icon, compound=tk.LEFT, accelerator='Ctrl+V',
                              command=lambda: self.text_editor.event_generate("<Control v>"))
        self.edit.add_command(label='Cut', image=self.cut_icon, compound=tk.LEFT, accelerator='Ctrl+X',
                              command=lambda: self.text_editor.event_generate("<Control x>"))
        self.edit.add_command(label='Clear All', image=self.clear_all_icon, compound=tk.LEFT, accelerator='Alt+X',
                              command=lambda: self.text_editor.delete(1.0, tk.END))
        self.edit.add_command(label='Find', image=self.find_icon, compound=tk.LEFT, accelerator='Ctrl+F',
                              command=self.find_func)

    def set_view_sub_menu(self):
        self.view.add_checkbutton(label='Tool Bar', onvalue=True, offvalue=0, variable=self.show_toolbar,
                                  image=self.tool_bar_icon,
                                  compound=tk.LEFT, command=self.hide_toolbar)
        self.view.add_checkbutton(label='Status Bar', onvalue=1, offvalue=False, variable=self.show_statusbar,
                                  image=self.status_bar_icon, compound=tk.LEFT, command=self.hide_statusbar)

    def set_color_theme(self):
        for i in self.color_dict:
            self.color_theme.add_radiobutton(label=i, image=self.color_icons[self.count], variable=self.theme_choice,
                                             compound=tk.LEFT, command=self.change_theme)
            self.count += 1

    def set_canvas(self):
        ############################################## text editor ###################################################
        self.text_editor = tk.Text(self.root)
        self.text_editor.config(wrap='word', relief=tk.FLAT)
        self.text_editor.focus_set()

        self.scroll_bar = tk.Scrollbar(self.root)
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_editor.pack(fill=tk.BOTH, expand=True)
        self.scroll_bar.config(command=self.text_editor.yview)
        self.text_editor.config(yscrollcommand=self.scroll_bar.set)

        self.text_changed = False
        self.text_editor.bind('<<Modified>>', self.changed)

    def set_controllers(self):
        self.file_controller = NotePadFileController.File_Controller()
        self.db_controller = NotePadDBController.Db_Controller()

    def check_db_status(self):
        self.db_status = self.db_controller.get_db_status()
        if self.db_status:
            self.files = self.db_controller.load_files_from_db()
        else:
            messagebox.showerror("Database Error", "Cannot connect to the DB")
            print(traceback.format_exc())

    def exit_func(self, event=None):
        try:
            if self.text_changed:
                mbox=messagebox.askyesno("File not saved!","Do you want to save the file ?")
                if mbox:
                    contant=self.text_editor.get(1.0,tk.END)
                    self.file_controller.save_file(contant)
        except:
            messagebox.showerror("App Error", "Error in closing")
            print(traceback.format_exc())
        finally:
            messagebox.showinfo("Thank you", "Have a good day")
            self.db_controller.close_notepad()
            self.root.destroy()
            exit(0)

    def save_file(self, event=None):
        try:
            content = self.text_editor.get(1.0, tk.END)
            self.file_controller.save_file(content)
        except:
            messagebox.showerror("File Error", "Cannot save the file")
            print(traceback.format_exc())

    def save_as(self, event=None):
        try:
            content = self.text_editor.get(1.0, tk.END)
            self.file_controller.save_as(content)
        except:
            messagebox.showerror("File Error", "Cannot save the file")
            print(traceback.format_exc())

    def open_file(self, event=None):
        try:
            self.msg,self.base=self.file_controller.read_file()
            if self.db_controller.is_file_secure(self.base):
                pwd=self.get_file_pwd()
                if pwd==self.db_controller.get_file_pwd(self.base):
                    self.text_editor.delete(1.0,tk.END)
                    self.text_editor.insert(1.0,self.msg)
                    self.root.title(self.base)
                else:
                    messagebox.showerror("Wrong password", "Password invalid!")
            else:
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(1.0, self.msg)
                self.root.title(self.base)
        except FileNotFoundError:
            messagebox.showerror("Wrong filename", "file does not exist!")
            print(traceback.format_exc())
        except:
            print(traceback.format_exc())


    def new_file(self, event=None):
        self.file_controller.new_file()
        self.root.title("SmartNotePad")
        self.text_editor.delete(1.0,tk.END)

    def changed(self, event=None):
        if self.text_editor.edit_modified():
            self.text_changed=True
            words=len(self.text_editor.get(1.0, 'end-1c').split())
            characters=len(self.text_editor.get(1.0, 'end-1c'))
            self.status_bar.config(text=f'Characters:{characters} Words:{words}')
        self.text_editor.edit_modified(False)

    def find(self):
        word=self.find_input.get()
        self.text_editor.tag_remove('match','1.0',tk.END)
        if word:
            matches=0
            start_pos='1.0'
            while True:
                start_pos=self.text_editor.search(word,start_pos,stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f'{start_pos}+{len(word)}c'
                print(start_pos,end_pos)
                self.text_editor.tag_add('match',start_pos,end_pos)
                self.text_editor.tag_configure('match',background='yellow',foreground='red')
                matches+=1
                start_pos=end_pos


    def replace(self):
        word=self.find_input.get()
        replace_text=self.replace_input.get()
        if len(word.strip())==0 or len(replace_text.strip())==0:
            return
        content=self.text_editor.get(1.0,tk.END)
        new_content=content.replace(word,replace_text)
        self.text_editor.delete(1.0,tk.END)
        self.text_editor.insert(1.0,new_content)

    def find_func(self, event=None):
        self.find_dialogue = tk.Toplevel()
        self.find_dialogue.geometry('450x250+500+200')
        self.find_dialogue.title('Find')
        self.find_dialogue.resizable(0, 0)

        ## frame
        self.find_frame = ttk.LabelFrame(self.find_dialogue, text='Find/Replace')
        self.find_frame.pack(pady=20)

        ## labels
        self.text_find_label = ttk.Label(self.find_frame, text='Find : ')
        self.text_replace_label = ttk.Label(self.find_frame, text='Replace')

        ## entry
        self.find_input = ttk.Entry(self.find_frame, width=30)
        self.replace_input = ttk.Entry(self.find_frame, width=30)

        ## button
        self.find_button = ttk.Button(self.find_frame, text='Find', command=self.find)
        self.replace_button = ttk.Button(self.find_frame, text='Replace', command=self.replace)

        ## label grid
        self.text_find_label.grid(row=0, column=0, padx=4, pady=4)
        self.text_replace_label.grid(row=1, column=0, padx=4, pady=4)

        ## entry grid
        self.find_input.grid(row=0, column=1, padx=4, pady=4)
        self.replace_input.grid(row=1, column=1, padx=4, pady=4)

        ## button grid
        self.find_button.grid(row=2, column=0, padx=8, pady=4)
        self.replace_button.grid(row=2, column=1, padx=8, pady=4)

        self.find_dialogue.mainloop()

    def say_something(self):
        try:
            self.takeAudio=self.file_controller.take_query()
            print(self.takeAudio)
            if self.takeAudio =="":
                messagebox.showinfo("say again","speech not recognized!")
            elif self.takeAudio.lower()=="hey mojo new file":
                self.new_file()
            elif self.takeAudio.lower()=="hey mojo open file":
                self.open_file()
            elif self.takeAudio.lower()=="hey mojo save file":
                self.save_file()
            elif self.takeAudio.lower()=="hey mojo save as file":
                self.save_as()
            elif self.takeAudio.lower()=="hey mojo close app":
                self.exit_func()
            elif self.takeAudio.lower()=="hey mojo text bold":
                self.change_bold()
            elif self.takeAudio.lower()=="hey mojo text italic":
                self.change_italic()
            elif self.takeAudio.lower()=="hey mojo text underline":
                self.change_underline()
            elif self.takeAudio.lower()=="hey mojo align left":
                self.align_left()
            elif self.takeAudio.lower()=="hey mojo align right":
                self.align_right()
            elif self.takeAudio.lower()=="hey mojo align centre":
                self.align_center()
            elif self.takeAudio.lower() == "hey mojo search":
                self.find_func()
            elif self.takeAudio.lower() == "hey mojo hide statusbar":
                self.hide_statusbar()
            elif self.takeAudio.lower() == "hey mojo hide toolbar":
                self.hide_toolbar()
            else:
                messagebox.showerror("Error","Sorry! Your audio not match")
        except RequestError as reque:
            messagebox.showerror("No internet","Please check your internet connection")
        except WaitTimeoutError as waiter:
            messagebox.showerror("Time over", "Time limit exceeded")
        except UnknownValueError as unkwe:
            messagebox.showerror("Non translatable text", "Speech unrecognizable!")

    def align_left(self):
        text_content=self.text_editor.get(1.0,'end')
        self.text_editor.tag_config('left',justify=tk.LEFT)
        self.text_editor.delete(1.0,tk.END)
        self.text_editor.insert(tk.INSERT,text_content,'left')


    def align_center(self):
        text_content = self.text_editor.get(1.0, 'end')
        self.text_editor.tag_config('center', justify=tk.CENTER)
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(tk.INSERT, text_content, 'center')

    def align_right(self):
        text_content = self.text_editor.get(1.0, 'end')
        self.text_editor.tag_config('right', justify=tk.RIGHT)
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(tk.INSERT, text_content, 'right')

    def change_font_color(self):
        color_var=tk.colorchooser.askcolor()
        # print(color_var)
        self.text_editor.config(fg=color_var[1])

    def hide_toolbar(self):
        if self.show_toolbar:
            self.tool_bar.pack_forget()
            self.show_toolbar=False
        else:
            self.text_editor.pack_forget()
            self.status_bar.pack_forget()
            self.tool_bar.pack(side=tk.TOP,fill=tk.X)
            self.text_editor.pack(fill=tk.BOTH,expand=True)
            self.status_bar.pack(side=tk.BOTTOM)
            self.show_toolbar=True

    def hide_statusbar(self):
        if self.show_statusbar:
            self.status_bar.pack_forget()
            self.show_statusbar = False
        else:
            self.status_bar.pack(side=tk.BOTTOM)
            self.show_statusbar = True

    def change_theme(self):
        self.chosen_theme=self.theme_choice.get()
        self.color_tuple=self.color_dict.get(self.chosen_theme)
        fg_color,bg_color=self.color_tuple
        self.text_editor.config(background=bg_color,foreground=fg_color)

    def change_font(self, event=None):
        self.current_font_family=self.font_family.get()
        self.text_editor.configure(font=(self.current_font_family,self.current_font_size))

    def change_fontsize(self, event=None):
        self.current_font_size = self.font_size.get()
        self.text_editor.configure(font=(self.current_font_family, self.current_font_size))

    def change_bold(self):
        self.text_property=tk.font.Font(font=self.text_editor['font'])
        if self.text_property.actual()['weight']=='normal':
            self.text_editor.configure(font=(self.current_font_family, self.current_font_size,'bold'))
        if self.text_property.actual()['weight'] == 'bold':
            self.text_editor.configure(font=(self.current_font_family, self.current_font_size, 'normal'))

    def change_italic(self):
        self.text_property = tk.font.Font(font=self.text_editor['font'])
        if self.text_property.actual()['slant'] == 'roman':
            self.text_editor.configure(font=(self.current_font_family, self.current_font_size, 'italic'))
        if self.text_property.actual()['slant'] == 'italic':
            self.text_editor.configure(font=(self.current_font_family, self.current_font_size, 'roman'))

    def change_underline(self):
        self.text_property = tk.font.Font(font=self.text_editor['font'])
        if self.text_property.actual()['underline']==0:
            self.text_editor.configure(font=(self.current_font_family, self.current_font_size, 'underline'))
        if self.text_property.actual()['underline']==1:
            self.text_editor.configure(font=(self.current_font_family, self.current_font_size, 'normal'))

                        #---------- DATA BASE COE------------
    def secure_file(self, event=None):
        if self.db_status:
            self.file_dialog=tk.Toplevel()
            self.file_dialog.geometry("450x400+500+200")
            self.file_dialog.title("Secure Files")
            self.file_dialog.resizable(0,0)

            ##frame
            self.file_frame=ttk.LabelFrame(self.file_dialog,text="Add Source File")
            self.file_frame.pack(pady=20)

            ##Labels
            self.text_file_owner_label=ttk.Label(self.file_frame,text="File Owner")
            self.text_file_pwd_lebel=ttk.Label(self.file_frame,text="File Password")
            self.total_file=self.db_controller.get_file_count()
            self.total_file_lebel=ttk.Label(self.file_frame,text=f"Total Files: {self.total_file}")

            ##Entry
            self.file_owner_input=ttk.Entry(self.file_frame,width=30)
            self.file_pwd_input=ttk.Entry(self.file_frame,width=30)

            ##button
            self.file_add_button=ttk.Button(self.file_frame,text='Add File',command=self.add_file)
            self.file_open_button = ttk.Button(self.file_frame, text='Open File', command=self.open_secure_file)
            self.file_remove_button = ttk.Button(self.file_frame, text='Remove File', command=self.remove_secure_file)

            ##label grid
            self.text_file_owner_label.grid(row=0,column=0,padx=4,pady=4)
            self.text_file_pwd_lebel.grid(row=1, column=0, padx=4, pady=4)
            self.total_file_lebel.grid(row=3, column=0, padx=4, pady=4)

            ## entry grid
            self.file_owner_input.grid(row=0, column=1, padx=4, pady=4)
            self.file_pwd_input.grid(row=1, column=1, padx=4, pady=4)

            ## button grid
            self.file_add_button.grid(row=2, column=0, padx=8, pady=4)
            self.file_open_button.grid(row=2, column=1, padx=8, pady=4)
            self.file_remove_button.grid(row=2, column=2, padx=8, pady=4)

            ##scrollable list
            scrollbar = ttk.Scrollbar(self.file_dialog, orient="vertical")
            scrollbar.pack(side='right', fill='both')
            self.fileList = tk.Listbox(self.file_dialog)
            # self.fileList.place(relx=0.0, rely=0.30, relheight=1, relwidth=0.972)
            self.fileList.pack(fill='both', expand=True)

            self.fileList.configure(background="white")
            self.fileList.configure(disabledforeground="#a3a3a3")
            self.fileList.configure(font="Lato")
            self.fileList.configure(foreground="black")
            self.fileList.configure(highlightbackground="#d9d9d9")
            self.fileList.configure(highlightcolor="#d9d9d9")
            self.fileList.configure(selectbackground="#c4c4c4")

            self.fileList.configure(selectforeground="black")
            self.fileList.configure(width=10)
            self.fileList.configure(yscrollcommand=scrollbar.set)
            scrollbar.configure(command=self.fileList.yview)

            self.fileList.bind("<Double-1>", self.list_double_click)

            ##load file from DB

            for values in self.files.keys():
                self.f_name = values
                file_owner = self.files.get(self.f_name)[1]
                full_file = self.f_name + "      " + "[ Owner: " + file_owner + " ]"
                self.fileList.insert('end', full_file)
            self.file_dialog.mainloop()
        else:
            messagebox.showerror("Database Error", "Please Connect with the database")


    def list_double_click(self, e):
        self.open_secure_file()

    def open_secure_file(self):
        self.sel_file_index_tuple = self.fileList.curselection()
        if len(self.sel_file_index_tuple) != 0:
            self.full_file_name = self.fileList.get(self.sel_file_index_tuple[0])
            self.file_pos = self.full_file_name.find(' ')
            self.file_name = self.full_file_name[:self.file_pos]
            self.file_path = self.db_controller.get_file_path(self.file_name)
            msg, base = self.file_controller.read_file(self.file_path)
            if self.db_controller.is_file_secure(base):
                pwd = self.get_file_pwd()
            if pwd == self.db_controller.get_file_pwd(base):
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(1.0, msg)
                self.root.title(base)
            else:
                messagebox.showerror('Wrong Password', "Wrong Password!, Please Try Again !!")

        else:
            messagebox.showerror("Error!", "Please select a file")

    def remove_secure_file(self):
        self.sel_file_index_tuple = self.fileList.curselection()
        if len(self.sel_file_index_tuple) != 0:
            self.full_file_name = self.fileList.get(self.sel_file_index_tuple[0])
            self.file_pos = self.full_file_name.find(' ')
            self.file_name = self.full_file_name[:self.file_pos]
            self.db_controller.remove_file(self.file_name)
            self.full_file_name = self.fileList.delete(self.sel_file_index_tuple[0])
            messagebox.showinfo("Success!", "file removed from personal files")
        else:
            messagebox.showerror("Error!", "Please select a fil!e")


    def add_file(self):
        if self.file_owner_input.get() and self.file_pwd_input.get() != "":
            self.file_owner = self.file_owner_input.get()
            self.file_pwd = self.file_pwd_input.get()
            self.file_path = filedialog.askopenfilename(title="select file",filetypes=[("Text Documents", "*.*")])
            self.file_name = os.path.basename(self.file_path)
            result = self.db_controller.add_file(self.file_name, self.file_path, self.file_owner, self.file_pwd)

            if result.find('already') != -1:
                messagebox.showwarning("Error!", result)
            elif result =="":
                messagebox.showinfo("Error!", "something went wrong!")
            else:
                messagebox.showinfo("Success!", result)
        else:
             messagebox.showerror("Error!", "Please First Enter file owner name and password ")


    def is_secure_file(self, file_name):
        return self.db_controller.is_file_secure(file_name)

    def get_file_pwd(self):
        access_pwd=simpledialog.askstring("Password","Enter file password:",show='*')
        return access_pwd

    def run(self):
        self.root.mainloop()


obj = Notepad()
obj.run()

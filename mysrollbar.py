import tkinter
import tkinter.ttk
def show(e=None):
    print('close clicked')
    root.destroy()
root = tkinter.Tk()
root.geometry("500x200")
my_text = tkinter.Text(root)
my_text.config(wrap='word', relief=tkinter.FLAT)
my_scroll_bar=tkinter.ttk.Scrollbar(root)
my_scroll_bar.pack(side=tkinter.RIGHT,fill=tkinter.Y)
my_text.pack(expand=True,fill=tkinter.BOTH)
my_scroll_bar.config(command=my_text.yview)
my_text.config(yscrollcommand=my_scroll_bar.set)
root.protocol('WM_DELETE_WINDOW',show)
root.mainloop()

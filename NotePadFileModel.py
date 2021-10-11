import os
import string
from tkinter.filedialog import *


class File_Model:
    def __init__(self):
        self.url=""
        self.key=string.ascii_letters+''.join([str(x) for x in range(0,10)])
        self.offset=5

    def encrypt(self,plaintext):
        result=""
        for ch in plaintext:
            try:
                ind=self.key.index(ch)
                ind=(ind+self.offset)%62
                result+=self.key[ind]
            except ValueError:
                result+=ch
        return result

    def decrypt(self,ciphertext):
        result=""
        for ch in ciphertext:
            try:
                ind = self.key.index(ch)
                ind = (ind - self.offset) % 62
                result += self.key[ind]
            except ValueError:
                result += ch
        # print(result)
        return result

    def open_file(self):
        self.url=askopenfilename(title="Select File",filetypes=[("Text Documents","*.*")])

    def new_file(self):
        self.url=""

    def save_as(self, msg):
        encrypted_text = self.encrypt(msg)
        self.url = asksaveasfile(mode="w", defaultextension=".ntxt", filetypes=[("All files","*.*"), ("Text Documents","*.*")])
        print(type(self.url))
        print(self.url)
        self.url.write(encrypted_text)
        filepath = self.url.name
        self.url.close()
        self.url = filepath

    def save_file(self,msg):
        if self.url=="":
            self.url = asksaveasfilename(title="Select file name", defaultextension=".ntxt",filetypes=[("Text Documents", "*.*")])
        file_name,file_extension=os.path.splitext(self.url)
        if file_extension==".ntxt":
            msg=self.encrypt(msg)
        with open(self.url,'w',encoding="utf-8") as fw:
            fw.write(msg)

    def read_file(self,url=''):
        if url!='':
            self.url=url
        else:
            self.open_file()
        base=os.path.basename(self.url)
        file_name, file_extension = os.path.splitext(self.url)
        fr=open(self.url,'r')
        contents=fr.read()
        if file_extension=='.ntxt':
            contents=self.decrypt(contents)
        fr.close()
        return contents,base






obj = File_Model()
# plaintext = "BHOPAL"
# obj.decrypt(plaintext)

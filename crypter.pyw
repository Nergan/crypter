from os import remove
from os.path import isfile
from time import sleep
from threading import Thread

from tkinter import Tk, Entry, StringVar, Toplevel, Button, Label
from tkinter.filedialog import askopenfilename
from pyAesCrypt import encryptFile, decryptFile


def setfilepath():
    filepath = askopenfilename()
    pathlabel.config(text=filepath if filepath else '<path>')
    
    
def checkpathloop():
    while True:
        path = pathlabel.cget('text')
        if not isfile(path):
            pathlabel.config(text='<path>')
        elif path == __file__.replace('\\', '/'):
            pathlabel.config(text='<path>')
            popuself()
        sleep(1)
    
def adaptsizeloop():
    while True:
        width = len(pathlabel.cget('text')) * 9
        pathlabel.place(x=200, y=0, width=width, height=40)
        keyfield.place(x=200, y=40, width=width if width > 400 else 400, height=40)
        rootwidth = width + 210
        root.geometry(f'{str(rootwidth if rootwidth > 610 else 610)}x90')
        sleep(1)
        
        
def popupenc():
    popup = Toplevel(root)
    popup.title('crypter')
    popup.geometry('300x50')
    popup.config(background='black')
    popuplabel = Label(popup, text='successfully encrypted', font='system 15')
    popuplabel.config(background='black', foreground='#80FF00')
    popuplabel.place(x=40, y=10)
    
def popupdec():
    popup = Toplevel(root)
    popup.title('crypter')
    popup.geometry('300x50')
    popup.config(background='black')
    popuplabel = Label(popup, text='successfully decrypted', font='system 15')
    popuplabel.config(background='black', foreground='#80FF00')
    popuplabel.place(x=40, y=10)
    
def popuerrincpass():
    popup = Toplevel(root)
    popup.title('crypter')
    popup.geometry('300x50')
    popup.config(background='black')
    popuplabel = Label(popup, text='incorrect password', font='system 15')
    popuplabel.config(background='black', foreground='red')
    popuplabel.place(x=65, y=10)
    
def popuerrnofile():
    popup = Toplevel(root)
    popup.title('crypter')
    popup.geometry('300x50')
    popup.config(background='black')
    popuplabel = Label(popup, text='file not found', font='system 15')
    popuplabel.config(background='black', foreground='red')
    popuplabel.place(x=65, y=10)
    
def popuself():
    popup = Toplevel(root)
    popup.title('crypter')
    popup.geometry('400x50')
    popup.config(background='black')
    popuplabel = Label(popup, text="you can't encrypt the program itself", font='system 15')
    popuplabel.config(background='black', foreground='red')
    popuplabel.place(x=30, y=10)
    
    
def errproc(fun):
    def wrap():
        if isfile(pathlabel.cget('text')):
            try:
                fun()
            except ValueError:
                popuerrincpass()
        else:
            popuerrnofile()
    return wrap


@errproc
def encrypt():
    file = pathlabel.cget('text')
    encryptFile(file, file + '.crp', key.get(), bufsize)
    remove(file)
    pathlabel.config(text=file + '.crp')
    popupenc()
    
@errproc
def decrypt():
    file = pathlabel.cget('text')
    decryptFile(file, file[:-4], key.get(), bufsize)
    remove(file)
    pathlabel.config(text=file[:-4])
    popupdec()


if __name__ == '__main__':    
    root = Tk()
    root.title('crypter')
    root.config(background='black')
    
    key = StringVar()
    bufsize = 512 * 1024

    selectfilebtn = Button(text='select file', command=setfilepath, font='system 15')
    encbtn = Button(text='encrypt', command=encrypt, width=8, font='system 15')
    decbtn = Button(text='decrypt', command=decrypt, width=8, font='system 15')
    pathlabel = Label(text='<path>', font='consolas 13')
    keyfield = Entry(textvariable=key, font='system 15')
    
    selectfilebtn.config(background='#404040', foreground='#80FF00')
    encbtn.config(background='#404040', foreground='#80FF00')
    decbtn.config(background='#404040', foreground='#80FF00')
    pathlabel.config(background='black', foreground='#80FF00')
    keyfield.config(background='#202020', foreground='#80FF00')
    
    keyfield.insert(0, 'key')
    
    selectfilebtn.place(x=0, y=0, width=200, height=40)
    encbtn.place(x=0, y=40, width=100, height=40)
    decbtn.place(x=100, y=40, width=100, height=40)

    Thread(target=checkpathloop).start()
    Thread(target=adaptsizeloop).start()
    root.mainloop()
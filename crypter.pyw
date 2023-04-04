from os import remove
from os.path import isfile
from time import sleep
from threading import Thread
from tkinter import Tk, Entry, StringVar, Toplevel, Button, Label
from tkinter.filedialog import askopenfilename

from pyAesCrypt import encryptFile, decryptFile


def setfilepath(pathlabel):
    filepath = askopenfilename()
    pathlabel.config(text=filepath if filepath else "<path>")


def checkpathloop(pathlabel, root):
    while True:

        path = pathlabel.cget("text")
        if not isfile(path):
            pathlabel.config(text="<path>")
        elif path == __file__.replace("\\", "/"):
            pathlabel.config(text="<path>")
            popupself(root)
        sleep(1)


def adaptsizeloop(pathlabel, keyfield, root):
    while True:
        width = len(pathlabel.cget("text")) * 9
        pathlabel.place(x=200, y=0, width=width, height=40)
        keyfield.place(x=200, y=40, width=width if width > 400 else 400, height=40)
        rootwidth = width + 210
        root.geometry(f"{str(rootwidth if rootwidth > 610 else 610)}x90")
        sleep(1)


def popupenc(root):
    popup = Toplevel(root)
    popup.title("crypter")
    popup.geometry("300x50")
    popup.config(background="black")
    popuplabel = Label(popup, text="successfully encrypted", font="system 15")
    popuplabel.config(background="black", foreground="#80FF00")
    popuplabel.place(x=40, y=10)


def popupdec(root):
    popup = Toplevel(root)
    popup.title("crypter")
    popup.geometry("300x50")
    popup.config(background="black")
    popuplabel = Label(popup, text="successfully decrypted", font="system 15")
    popuplabel.config(background="black", foreground="#80FF00")
    popuplabel.place(x=40, y=10)


def popuerrincpass(root):
    popup = Toplevel(root)
    popup.title("crypter")
    popup.geometry("300x50")
    popup.config(background="black")
    popuplabel = Label(popup, text="incorrect password", font="system 15")
    popuplabel.config(background="black", foreground="red")
    popuplabel.place(x=65, y=10)


def popuperrnofile(root):
    popup = Toplevel(root)
    popup.title("crypter")
    popup.geometry("300x50")
    popup.config(background="black")
    popuplabel = Label(popup, text="file not found", font="system 15")
    popuplabel.config(background="black", foreground="red")
    popuplabel.place(x=65, y=10)


def popupself(root):
    popup = Toplevel(root)
    popup.title("crypter")
    popup.geometry("400x50")
    popup.config(background="black")
    popuplabel = Label(
        popup, text="you can't encrypt the program itself", font="system 15"
    )
    popuplabel.config(background="black", foreground="red")
    popuplabel.place(x=30, y=10)


def errproc(fun):
    def wrap(pathlabel, root, key, bufsize):
        if isfile(pathlabel.cget("text")):
            try:
                fun(pathlabel, root, key, bufsize)
            except ValueError:
                popuerrincpass(root)
        else:
            popuperrnofile(root)

    return wrap


@errproc
def encrypt(pathlabel, root, key, bufsize):
    file = pathlabel.cget("text")
    encryptFile(file, file + ".crp", key.get(), bufsize)
    remove(file)
    pathlabel.config(text=file + ".crp")
    popupenc(root)


@errproc
def decrypt(pathlabel, root, key, bufsize):
    file = pathlabel.cget("text")
    decryptFile(file, file[:-4], key.get(), bufsize)
    remove(file)
    pathlabel.config(text=file[:-4])
    popupdec(root)


def main():
    root = Tk()
    root.title("crypter")
    root.config(background="black")

    key = StringVar()
    bufsize = 256 * 1024

    pathlabel = Label(text="<path>", font="consolas 13")
    keyfield = Entry(textvariable=key, font="system 15")
    selectfilebtn = Button(
        text="select file", command=lambda: setfilepath(pathlabel), font="system 15"
    )
    encbtn = Button(
        text="encrypt",
        command=lambda: encrypt(pathlabel, root, key, bufsize),
        width=8,
        font="system 15",
    )
    decbtn = Button(
        text="decrypt",
        command=lambda: decrypt(pathlabel, root, key, bufsize),
        width=8,
        font="system 15",
    )

    selectfilebtn.config(background="#404040", foreground="#80FF00")
    encbtn.config(background="#404040", foreground="#80FF00")
    decbtn.config(background="#404040", foreground="#80FF00")
    pathlabel.config(background="black", foreground="#80FF00")
    keyfield.config(background="#202020", foreground="#80FF00")

    keyfield.insert(0, "key")

    selectfilebtn.place(x=0, y=0, width=200, height=40)
    encbtn.place(x=0, y=40, width=100, height=40)
    decbtn.place(x=100, y=40, width=100, height=40)

    Thread(target=checkpathloop, args=(pathlabel, root)).start()
    Thread(target=adaptsizeloop, args=(pathlabel, keyfield, root)).start()
    root.mainloop()


if __name__ == "__main__":
    main()


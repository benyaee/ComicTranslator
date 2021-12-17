import ocr
from tkinter import filedialog as fd
import tkinter as tk
import os


def clicked():
    global filenames
    filenames = fd.askopenfilenames()
    window.destroy()


window = tk.Tk()
window.title("Comic Translation")
window.geometry("400x200")

options = {"Word based Inpainting", "Bounding block Based Inpainting","Remove text only"}
options2 = {"eng","fr"}

variable2 = tk.StringVar(window,value="eng")
opt2 = tk.OptionMenu(window,variable2,*options2)
opt2.pack()

variable = tk.StringVar(window,value="Bounding block Based Inpainting")
opt = tk.OptionMenu(window, variable, *options)
opt.pack()
button = tk.Button(window, text = "Open File/Files" , command = clicked ).pack()

window.mainloop()

#Calling other methods after user uploads finals
fn = filenames
ocr.multiTrans(fn,variable2.get(),variable.get())
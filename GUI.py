from tkinter import *

window = Tk()


def getvalue():
    print(e1value.get())
    t1.insert(END, e1value.get())

b1 = Button(window, text="Execute", command=getvalue)
b1.grid(row=0,column=0)

e1value = StringVar()
e1 = Entry(window, textvariable=e1value)
e1.grid(row=0, column=1)

t1=Text(window, height=1, width=20)
t1.grid(row=0, column=2)
window.mainloop()  # at the end of the code , runs until manualy closed
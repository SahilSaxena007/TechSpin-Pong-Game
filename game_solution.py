'''
Main Py File for Tkinter Game
Sahil Saxena
COMP16321

'''
from tkinter import Tk, Canvas, PhotoImage, Label, Frame, Button, Entry, StringVar, messagebox, Event, IntVar

from pong import Frames

    

if __name__=='__main__':
    window = Tk()
    game = Frames(window)
    window.mainloop()
    




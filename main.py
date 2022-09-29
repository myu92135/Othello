import tkinter as tk
from ocero import Ocero
class Game(tk.Frame):
    def __init__(self, master= tk.Tk()):
        super().__init__(self)
        self.gameMaster = Ocero()
        
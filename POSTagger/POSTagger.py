#!/usr/bin/env python3

import tkinter as tk
from .View import View
from .Wizard import Wizard
from .Controller import Controller

class POSTagger(tk.Tk):
    def __init__(self):
        super().__init__()
        cont = Controller()
        Wizard(self, cont)
        View(cont)

if __name__=='__main__':
    POSTagger()
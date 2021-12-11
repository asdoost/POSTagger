import os
from tkinter import font
from tkinter.messagebox import showerror, showwarning, askyesnocancel

class Warnings:
    def __init__(self):
        font1 = font.Font(name='TkCaptionFont', exists=True)
        font1.config(family='courier new', size=11)

    def combine_error(self, lst):
        if len(lst)<2:
            showerror(
                title = "Combine Error", 
                message = "There is no other word in the sentence to combine!"
                )

    def open_corpus_error(self, path):
        if path=='':
            showerror(
                title = "Path Error", 
                message = "The path is empty!")
        elif not os.path.isfile(path):
            showerror(
                title = "File Error", 
                message = "There is no such file!")

    def tag_error(self):
        showerror(
            title = "Tag Error", 
            message = "You didn't select any tag!")
    
    def untagging_error(self):
        showerror(
            title = "Back Error", 
            message = 'You reached the first word of the first sentence. You can\'t go back anymore.')

    def save_warn(self):
        showwarning(
            title='Save Dialog', 
            message='The job is done. Make sure to save it.')

    def open_warn(self):
        showwarning(
            title='Open Dialog', 
            message='You have not added any corpus file yet.')

    def splitting_error(self):
        showerror(
            title = "Splitting Error", 
            message = 'The word can not be splitted anymore.')

    def empty_wizard(self):
        showwarning(
            title='Empty Wizard', 
            message='You didn\'t select a corpus file.')

    def retokenize_error(self):
        showerror(
            title = "Retokenize Error", 
            message = 'There is no tagged sentence to retokenize.')

    def exit_wirning(self):
        return askyesnocancel(
            title= 'Save Warning',
            message='Do you want to save your work?')

    def empty_project(self):
        showerror(
                title = "Empty Project Error", 
                message = "You have not done anything to save!")
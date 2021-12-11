import os
import tkinter as tk
from tkinter import ttk
from .exeptions import Warnings

class View:
    def __init__(self, cont):

        # Create a root window
        self.root = tk.Tk()

        # Assign the name of the window
        self.root.title('</POSTagger>')
        self.root.iconphoto(
            False, tk.PhotoImage(
                file=os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    'imgs',
                    'logo.png'
                )))

        # Set a theme to the window
        theme = ttk.Style()
        theme.theme_use('clam')

        # Set the window's size
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+0+0")

        # Configure the window layout
        self.root.columnconfigure(1, weight=2)

        # Make controller local
        self.cont = cont

        # Create error instance
        self.ER = Warnings()

        # Set padx, pady and sticky for all widgets
        self.options = {'padx': 5, 'pady': 5}

        self.textbox()
        self.wordfrequency()
        self.wordentry()
        self.editbuttons()
        self.categories()
        self.tagbuttons()
        self.menubar()

        # Update main parameters, textBox and wordEntry
        #self.cont.open_corpus()
        # self.update_textBox()
        # self.update_wordEntry()

        # self.root = root
        self.root.mainloop()

    def textbox(self):
        ############
        # Text Box #
        ############
        # Create a textBox fram and a textBox widget for sentences
        text_frame = ttk.Frame(self.root)
        self.sent_box = tk.Text(
            text_frame, 
            height=8, 
            width=60, 
            font=(
                self.cont.font_name, 
                self.cont.font))

        self.sent_box.tag_configure(
            self.cont.dir, 
            justify=self.cont.dir)

        self.sent_box.grid(
            row=0, 
            column=1, 
            ipady=5)
        
        # Create a scrollbar for textbox
        scroll = ttk.Scrollbar(
            text_frame, 
            orient='vertical', 
            command=self.sent_box.yview)

        scroll.grid(
            row=0, 
            column=2, 
            sticky='ns')

        # Set scrollbar to the textBox
        self.sent_box['yscrollcommand'] = scroll.set
        text_frame.grid(
            row=0, 
            column=1, 
            **self.options)
        self.update_textBox()
    
    def wordfrequency(self):
        ###################
        # Frequency Label #
        ###################
        # Get the frequencies
        c,l = self.cont.text.count(self.cont.word), self.cont.corpus_length
        # Create a label for frequency
        self.freq_label = ttk.LabelFrame(self.root)
        self.frequency = ttk.Label(
            self.freq_label,
            text=f'{c} occurrence in {l} words ({c/l if l else 0})'
            )
        self.frequency.grid()
        self.freq_label.grid(row=1, column=1)

    def wordentry(self):
        ##############
        # Word Entry #
        ##############
        # Create a word fram and a word entry widget for words
        word_frame = ttk.Frame(self.root)
        self.word_entry = ttk.Entry(
            word_frame, 
            width=50, 
            font = f'{self.cont.font_name} {self.cont.font} bold',
            justify='center')
        self.word_entry.grid(ipady=5)
        word_frame.grid(
            row=2, 
            column=1, 
            **self.options)
        self.update_wordEntry()

    def editbuttons(self):
        ################
        # Edit Buttons #
        ################
        # Create a merge, split, re-tokenize buttons
        ebutt_frame = ttk.Frame(self.root)
        split_btn = ttk.Button(
            ebutt_frame, 
            text='Re-Tokenize',
            command=self.retokenize)

        split_btn.grid(
            row=0, 
            column=0, 
            **self.options)

        # Split button
        edit_btn = ttk.Button(
            ebutt_frame, 
            text='Split',
            command=self.spliting)
        edit_btn.grid(
            row=0, 
            column=1, 
            **self.options)

        # Merge button
        comb_btn = ttk.Button(
            ebutt_frame, 
            text='Merge',
            command=self.merge)
        comb_btn.grid(
            row=0, 
            column=2, 
            **self.options)

        ebutt_frame.grid(row=3, column=1)

    def categories(self):
        ##############
        # Categories #
        ##############
        # Create tagset radioButtons
        tags = self.cont.get_tagset()
        self.cat_frame = ttk.LabelFrame(self.root)
        # POS radiobuttons
        self.tag = tk.StringVar()
        for idx, tup in enumerate(tags.items()):
            ttk.Radiobutton(
                self.cat_frame, 
                text=tup[0], 
                variable=self.tag, 
                value=tup[1]).grid(
                    row=idx//5, column=idx%5,
                    **self.options, 
                    sticky='w')
        self.cat_frame.grid(row=4, column=1)
        #return cat_frame

    def tagbuttons(self):
        ###################
        # Tagging Buttons #
        ###################
        # Create tagging, undo, and exit buttons
        tagging_button_frame = ttk.Frame(self.root)
        # Tag button
        next_btn = ttk.Button(
            tagging_button_frame, 
            text='Tag',
            command=self.tagging)

        next_btn.grid(
            row=0, 
            column=2, 
            **self.options)
        next_btn.focus_set()

        # Undo button
        back_btn = ttk.Button(
            tagging_button_frame, 
            text='Untag',
            command=self.untag_word)

        back_btn.grid(
            row=0, 
            column=1, 
            **self.options)

        tagging_button_frame.grid(
            row=5, 
            column=1, 
            **self.options)

    def menubar(self):
        ############
        # Menu Bar #
        ############
        # Create a menubar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Create a file, option, and help menu
        file_menu = tk.Menu(menubar, tearoff=0)
        help_menu = tk.Menu(menubar, tearoff=0)

        # Add the File menu to the menubar
        menubar.add_cascade(label="File", menu=file_menu)

        # Add menu items to the file menu
        file_menu.add_command(
            label='Open a Corpus',
            command=self.initiate)

        file_menu.add_command(
            label='Open a Project',
            command=lambda: self.initiate(False))

        file_menu.add_command(
            label='Open a language model', 
            state=tk.DISABLED)

        file_menu.add_command(
            label='Save the project',
            command=self.cont.save_project)
        file_menu.add_command(
            label='Export...',
            command=self.cont.export)
        file_menu.add_command(
            label='Preferences',
            command=self.option_window)
        file_menu.add_command(
            label='Exit', 
            command=self.exiting)

        # Add the option menu to the menubar
        menubar.add_cascade(label="Help", menu=help_menu)

        # Add menu items to the option menu
        help_menu.add_command(
            label='Tutorials', 
            command=self.root.destroy)

        help_menu.add_command(
            label='Documentation', 
            command=self.root.destroy)

    def initiate(self, corpus=True):
        if corpus:
            self.cont.open_corpus()
        else:
            self.cont.open_project()
        self.update_textBox()
        self.update_wordEntry()

    def update_textBox(self):
        # Redirect the the sentence
        sent = self.cont.redirect(' '.join(self.cont.sentence))
        # Update the textBox
        self.sent_box.delete('0.0', tk.END)
        self.sent_box.insert('0.0', sent, self.cont.dir)

    def update_wordEntry(self):
        # Redirect the the word
        word = self.cont.redirect(self.cont.word)
        # Update the frequency label
        c = self.cont.text.count(self.cont.word) if self.cont.word else 0
        l = self.cont.corpus_length
        p = c/l if l else 0
        self.frequency.config(
            text=f'{c} occurrence in {l} words ({p})')
        # Update the wordEntry
        self.word_entry.delete(0, tk.END)
        self.word_entry.insert(0, word)

    def update_categories(self):
        # Update tagset
        self.cat_frame.grid_forget()
        self.categories()

    def next_sentence(self):
        # Check if corpus is empty and the tagged corpus is full
        if not self.cont.corpus and self.cont.tagged_corpus:
            # Empty textBox and wordEntry
            self.sent_box.delete('0.0', tk.END)
            self.word_entry.delete(0, tk.END)
            # Raise save warnning
            return self.ER.save_warn()
        # Check if any corpus is not imported
        elif not self.cont.corpus:
            # Raise open corpus warnning
            return self.ER.open_warn()
        else:
            # Check if tagged sentence is not empty
            if self.cont.tagged_sent:
                # Append the tagged sentence to the tagged corpus
                self.cont.tagged_corpus.append(self.cont.tagged_sent)
                # Empty the tagged sentence
                self.cont.tagged_sent = []
            # Update the current sentence
            self.cont.current_sent = self.cont.corpus[0]
            # Update the sentence
            self.cont.sentence = self.cont.current_sent
            # Update the corpus
            self.cont.corpus = self.cont.corpus[1:]

    def next_word(self):
        # Check if the cuurent sentence is empty
        if not self.cont.current_sent:
            # Update the current, tagged sentence and the corpus
            self.next_sentence()
        if self.cont.current_sent:
            # Update the word
            self.cont.word = self.cont.current_sent[0]
            # Update the current sentence
            self.cont.current_sent = self.cont.current_sent[1:]

    def tagging(self):
        # Get the tag
        tag = self.tag.get()
        # Check if any tag is selected
        if not tag:
            # Raise tagging error
            return self.ER.tag_error()
        # Tag the word based on the POS style that is selected
        if self.cont.pos_style=='<{}>{}</{}>':
            tagged_word = self.cont.pos_style.format(tag, self.cont.word, tag)
        else:
            tagged_word = self.cont.pos_style.format(self.cont.word, tag)
        # Append the tagged word to the tagged sentence
        self.cont.tagged_sent.append(tagged_word)
        # Go to the next word
        self.next_word()
        # Update textBox and wordEntry
        self.update_textBox()
        self.update_wordEntry()

    def untag_sentence(self):
        # Raise the undoing warnning if the tagged sentence is empty
        if not self.cont.tagged_corpus:
            return self.ER.untagging_error()

        # Fill the tagged sentence
        self.cont.tagged_sent = self.cont.tagged_corpus[-1]

        # Update the tagged corpus
        self.cont.tagged_corpus = self.cont.tagged_corpus[:-1]
        
        # Strip the tagged sentence and assign it to the sentence
        self.cont.sentence = [
            self.cont.tag_striping(i) for i in self.cont.tagged_sent]

    def untag_word(self):
        # check if the tagged sentence is empty and fill it
        if not self.cont.tagged_sent:
            self.untag_sentence()
        if self.cont.tagged_sent:
            # Update the current sentence
            self.cont.current_sent = [self.cont.word] + self.cont.current_sent
            # Update the word
            word = self.cont.tagged_sent[-1]
            self.cont.word = self.cont.tag_striping(word)
            # Update the tagged sentence
            self.cont.tagged_sent = self.cont.tagged_sent[:-1]
            # Update the textbox and wordEntry
            self.update_textBox()
            self.update_wordEntry()

    def merge(self):
        # Check if the current sentence is empty
        if not self.cont.current_sent:

            # Save the sentence as sent
            sent = self.cont.sentence

            # Update the current sentence
            self.next_sentence()

            # Merge last sentence to current sentence
            self.cont.sentence = sent + self.cont.sentence

        # Merge the word by the next word
        self.cont.word += f' {self.cont.current_sent[0]}'

        # Update the current sentence
        self.cont.current_sent = self.cont.current_sent[1:]

        # Update textBox and wordEntry
        self.update_textBox()
        self.update_wordEntry()

    def spliting(self):
        # Check if the word is splitable
        if ' ' not in self.cont.word:
            return self.ER.splitting_error()

        # Split the word
        splited = self.cont.word.split(' ')

        # Append the last word to begining of the current sentence
        self.cont.current_sent = [splited[-1]] + self.cont.current_sent

        # Join the remaining splitted word
        self.cont.word = ' '.join(splited[:-1])
        self.update_wordEntry()

    def retokenize(self):
        # Check if the tagged sentence is empty and raise an error
        if not self.cont.tagged_sent:
            return self.ER.retokenize_error()

        # Append the tagged sentence to the tagged corpus
        self.cont.tagged_corpus.append(self.cont.tagged_sent)

        # Empty the tagged sentence
        self.cont.tagged_sent = []
        
        # Update the sentence and textBox
        self.cont.sentence = self.cont.current_sent
        self.update_textBox()

    def exiting(self):
        # Check if the tagged corpus is empty to quit
        if not self.cont.tagged_corpus:
            self.root.quit()
        else:
            # Raise save warning
            flag = self.ER.exit_wirning()
            # Check if the user presses Yes to save file
            if flag:
                self.cont.save_project()
                self.root.quit()
            # Check if user press No
            elif flag==False:
                self.root.quit()

    def option_window(self):
        # Customize the window 
        self.container = tk.Toplevel()
        self.container.title('Preferences')
        theme = ttk.Style()
        theme.theme_use('clam')
        self.container.geometry('350x185')

        # Create a label, and comboBox to import a tagset
        ttk.Label(
            self.container, 
            text='Select A Tagset:'
            ).grid(
                row=0, 
                column=0, 
                **self.options, 
                sticky='w')

        # Assign a string variable
        self.tagset_name = tk.StringVar()

        ttk.Combobox(
            self.container,
            textvariable=self.tagset_name,
            state='readonly',
            values= list(self.cont.tagset_files.keys())
        ).grid(
            row=0, 
            column=1, 
            columnspan=2, 
            **self.options,
            sticky='e')

        # Set default value to the comboBox
        self.tagset_name.set(self.cont.tagset_name)

        # Add font name label and comboBox
        self.font_name = tk.StringVar()

        ttk.Label(
            self.container, 
            text='Font Name:'
            ).grid(
                row=1, 
                column=0, 
                sticky='w')

        ttk.Combobox(
            self.container, 
            textvariable=self.font_name,
            values=self.cont.font_list,
            state='readonly'
            ).grid(
                row=1, 
                column=1, 
                columnspan=2, 
                **self.options,
                sticky='e')

        # Set a default value
        self.font_name.set(self.cont.font_name)

        # Add font size label and comboBox
        self.font_size = tk.IntVar()

        ttk.Label(
            self.container, 
            text='Font Size: '
            ).grid(
                row=2, 
                column=0, 
                sticky='w')

        ttk.Combobox(
            self.container, 
            textvariable=self.font_size,
            state='readonly',
            values=list(range(8,31,2))
            ).grid(
                row=2, 
                column=1, 
                columnspan=2, 
                **self.options,
                sticky='e')

        # Set a default value to font size
        self.font_size.set(self.cont.font)

        # Add font size label and comboBox
        self.direction = tk.StringVar()
        
        ttk.Label(
            self.container, 
            text='Text Direction: '
            ).grid(
                row=3, 
                column=0, 
                sticky='w')

        ttk.Radiobutton(
            self.container, 
            text='Left to Right', 
            value='left', 
            variable=self.direction
            ).grid(
                row=3, 
                column=1, 
                **self.options)

        ttk.Radiobutton(
            self.container, 
            text='Right to Left', 
            value='right', 
            variable=self.direction
            ).grid(
                row=3, 
                column=2, 
                **self.options)

        # Set a default value to text direction
        self.direction.set(self.cont.dir)

        ttk.Button(
            self.container, 
            text='Cancel', 
            command=self.container.destroy
            ).grid(
                row=4, 
                column=0, 
                **self.options)

        ttk.Button(
            self.container, 
            text='OK', 
            command=self.submiting
            ).grid(
                row=4, 
                column=2, 
                **self.options)

        self.container.grab_set()

    def submiting(self):
        # Update font name, font size, and text direction
        self.cont.tagset_name = self.tagset_name.get()
        self.cont.get_tagset()
        #self.cont.tagset_
        self.cont.font_name = self.font_name.get()
        self.cont.font = self.font_size.get()
        self.cont.dir = self.direction.get()
        # Forget sentence box and word entry
        self.sent_box.grid_forget()
        self.word_entry.grid_forget()
        # Rebuild sentence box and word entry
        self.wordentry()
        self.textbox()
        self.update_categories()
        # Destroy the option window
        self.container.destroy()

    def set_as_default(self):
        self.cont.set_as_default()
        self.tagset_name.set(self.cont.tagset_name)
        self.font_name.set(self.cont.font_name)
        self.font_size.set(self.cont.font)
        self.direction.set(self.cont.dir)


if __name__ == "__main__":
    View()
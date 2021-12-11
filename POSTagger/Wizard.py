import os
import tkinter as tk
from tkinter import ttk
from .exeptions import Warnings as WR

class Wizard:
    def __init__(self, root, cont):

        # Make a controller instance
        self.cont = cont

        # Create a wizard window
        root.title('</POSTagger>')
        root.iconphoto(
            False,tk.PhotoImage(
                file=os.path.join(
                    os.path.dirname(os.path.abspath(__file__)), 
                    'imgs','logo.png'
                    )
                )
            )

        root.geometry('680x325')

        # Set a theme to the wizard window
        theme = ttk.Style()
        theme.theme_use('clam')

        # Set padx, pady and sticky for all widgets
        options = {'padx': 5, 'pady': 5}

        # Create import label for project
        ttk.Label(
            root, 
            text='Import a project:'
            ).grid(
                row=0, 
                column=0,
                sticky='w', 
                **options)

        # Create import entry
        self.project_entry = ttk.Entry(root, width=50)
        self.project_entry.grid(
            row=0, 
            column=1,
            columnspan=3,
            sticky='w',
            **options)

        # Create browse button to import a project
        ttk.Button(
            root, 
            text='Import...', 
            command=self.browse_project
            ).grid(
                row=0, 
                column=4,
                sticky='e',
                **options)

        # Create import label for corpus
        ttk.Label(
            root, 
            text='Import a corpus:'
            ).grid(
                row=1, 
                column=0,
                sticky='w',
                **options)

        # Create import entry for corpus
        self.corpus_entry = ttk.Entry(root, width=50)
        self.corpus_entry.grid(
            row=1, 
            column=1,
            columnspan=3,
            sticky='w',
            **options)

        # Create browse button to import corpus
        ttk.Button(
            root, 
            text='Import...', 
            command=self.browse_corpus
            ).grid(
                row=1, 
                column=4,
                sticky='e',
                **options)

        # Create a model label
        ttk.Label(
            root, 
            text='Import Model:'
            ).grid(
                row=2, 
                column=0,
                sticky='w',
                **options)

        # Create model ComboBox
        self.model_name = tk.StringVar()
        self.modelcombo = ttk.Combobox(
            root,
            textvariable=self.model_name,
            values=['This feature is not available yet.'],
            width=49,
            state='disabled')
        self.modelcombo.grid(
            row=2, 
            column=1, 
            columnspan=3,
            sticky='w',
            **options)
        
        # Set a default value for the model entry
        self.model_name.set('This feature is not available yet.')

        # Create a tagset label
        ttk.Label(
            root, 
            text='Slect A Tagset:'
            ).grid(
                row=3, 
                column=0,
                sticky='w',
                **options)
        
        # Create a tagset combobox
        self.tagset_name = tk.StringVar()
        self.tagset_combo = ttk.Combobox(
            root,
            textvariable=self.tagset_name,
            values= list(self.cont.tagset_files.keys()),
            width=49
            )
        self.tagset_combo.grid(
            row=3, 
            column=1, 
            columnspan=3, 
            **options)

        # Set default value to the tagset
        self.tagset_name.set('default')

        # Create a tagging style label
        ttk.Label(
            root, 
            text='POS tagging Style:'
            ).grid(
                row=4, 
                column=0,
                sticky='w',
                **options)
        
        # Create tagging style buttons
        self.style = tk.StringVar()
        self.xml = ttk.Radiobutton(
            root, 
            text='XML', 
            value='<{}>{}</{}>', 
            variable=self.style
            )
        self.xml.grid(
            row=4, 
            column=1,
            sticky='w', 
            **options)

        self.underscore = ttk.Radiobutton(
            root, 
            text='Underscore', 
            value='{}_{}', 
            variable=self.style
            )
        self.underscore.grid(
            row=4, 
            column=2,
            sticky='w',
            **options)

        self.tab = ttk.Radiobutton(
            root, 
            text='Tab', 
            value='{}\t{}\n', 
            variable=self.style
            )
        self.tab.grid(
            row=4, 
            column=3,
            sticky='w',
            **options)

        # Set default value to POS tagging style
        self.style.set('<{}>{}</{}>')
        
        # Create a text direction label
        self.direction = tk.StringVar()
        ttk.Label(
            root, 
            text='Text direction:'
            ).grid(
                row=5, 
                column=0,
                sticky='w',
                **options)

        # Create text direction radioButtons
        ttk.Radiobutton(
            root, 
            text='Left to Right', 
            value='left', 
            variable=self.direction
            ).grid(
                row=5, 
                column=1,
                sticky='w',
                **options)

        ttk.Radiobutton(
            root, 
            text='Right to Left', 
            value='right', 
            variable=self.direction
            ).grid(
                row=5, 
                column=2,
                sticky='w',
                **options)

        # Set default value to text direction
        self.direction.set('left')

        # Create a font size label
        ttk.Label(
            root, 
            text='Font Size:'
            ).grid(
                row=6,
                column=0,
                sticky='w',
                **options)

        # Create a font size comboBox
        self.display_font = tk.IntVar()
        ttk.Combobox(
            root, 
            textvariable=self.display_font, 
            width=5,
            values=list(range(8,31,2))
            ).grid(
                row=6,
                column=1,
                sticky='w',
                **options)

        # Set default value to font size
        self.display_font.set(12)

        # Create OK and cancel buttons
        ttk.Button(
            root, 
            text='Cancel', 
            command=root.destroy
            ).grid(
                row=7, 
                column=0, 
                pady=30)

        ttk.Button(
            root, 
            text='OK', 
            command=lambda: self.starting(root)
            ).grid(
                row=7,
                column=4,
                pady=30)

        root.mainloop()

    def starting(self, root):
        if not self.cont.corpus_path and not self.cont.project_path:
            WR().empty_wizard()
        elif self.cont.corpus_path:
            # Get input variables
            self.cont.tagset_name = self.tagset_name.get()
            self.cont.tagset_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'tagsets', 
                self.cont.tagset_files[self.cont.tagset_name])

            self.cont.pos_style = self.style.get()
        self.cont.font = self.display_font.get()
        self.cont.dir = self.direction.get()
        root.destroy()

    def update_widgets(self):
        self.tagset_name.set(self.cont.tagset_name)
        self.style.set(self.cont.pos_style)
        self.display_font.set(self.cont.font)
        self.direction.set(self.cont.dir)

    def browse_project(self):
        # Open the project
        self.cont.open_project()
        if self.cont.project_path:
            # Update widgets
            self.update_widgets()
            # Disable critical features
            self.tagset_combo.config(state='disabled')
            self.xml.config(state='disabled')
            self.underscore.config(state='disabled')
            self.tab.config(state='disabled')
        # Update the project entry
        self.project_entry.delete(0, tk.END)
        self.project_entry.insert(0, self.cont.project_path)

    def browse_corpus(self):
        # Open corpus
        self.cont.open_corpus()
        # Update the corpus entry
        self.corpus_entry.delete(0, tk.END)
        self.corpus_entry.insert(0, self.cont.corpus_path)


if __name__=='__main__':
    app = tk.Tk()
    Wizard(app)

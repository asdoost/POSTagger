import os
import re
from .Model import Model
import arabic_reshaper
from xml.dom import minidom
from bidi.algorithm import get_display
from .exeptions import Warnings as WR
from tkinter.filedialog import asksaveasfilename, askopenfilename

class Controller:
    def __init__(self):
        self.model = Model()

        # Corpus variables
        self.text = ''
        self.corpus_length = 0
        self.corpus = ''
        self.corpus_path = ''
        self.project_path = ''

        # Working variables
        self.current_sent = ''
        self.sentence = ''
        self.word = ''
        self.tagged_sent = []
        self.tagged_corpus = []
        self.file_name = ''

        # Tagset variables
        self.tagset_files = {
            'default': 'defaultTagset.csv',
            'Brown Tagset': 'BrownTagset.csv',
            'Penn Treebank tagset': 'PENNTagset.csv',
            'Universal POS Tagset': 'UPT.csv',
            'Bijankhan tagset': 'BijankhanTagset.csv'}

        self.tagset_name = 'default'
        self.tagset_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'tagsets', 
            self.tagset_files[self.tagset_name]
            )
        self.tagset = dict()

        self.model_path = ''

        # Style variables
        self.font_list = ['courier', 'Helvetica', 'Tahoma']
        self.pos_style = '<{}>{}</{}>'
        self.font = 12
        self.font_name = 'Tahoma'
        self.dir = 'left'

    def open_corpus(self):
        path = self.get_path()
        if path:
            self.corpus_path = path
            # open the corpus file
            data = self.model.open_file(path)

            # get the file name from the path
            self.file_name = f'project_{os.path.basename(path)}'

            # tokenize the corpus
            self.corpus = self.sent_tokenizer(data)

            # Get normalized text
            self.text = '\n'.join([' '.join(sent) for sent in self.corpus])

            # Get corpus length
            self.corpus_length = len(self.text.split())

            # get the first sentence of the corpus as the current sentence
            self.current_sent = self.corpus[0]
            self.sentence = self.current_sent

            # get the first word of the current sentence as the word
            self.word = self.current_sent[0]
            
            # update the current sentence and the corpus
            self.corpus = self.corpus[1:]
            self.current_sent = self.current_sent[1:]

    def get_tagset(self):
        # Get the path
        self.tagset_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'tagsets', 
            self.tagset_files[self.tagset_name])

        # Open the tagset file
        data = self.model.open_tagset(self.tagset_path)

        # Convert the tagset list to a dictionary
        self.tagset = {key:val for val, key in data}
        return self.tagset
    
    def get_path(
        self, 
        op=True, 
        extension='.txt', 
        filetype=[('Text File','*.txt')]):
        if extension=='.txt' and op:
            initial = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 'corpora')
        elif extension=='.txt':
            initial = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 'tagsets')
        elif extension=='.proj':
            initial = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 'projects')
        elif extension=='.csv':
            initial = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 'tagsets')
        elif extension=='.xml':
            initial = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 'outputs')

        if op:
            # Invoke file window to get the opening path
            path = askopenfilename(
                initialdir=initial,
                defaultextension=extension,
                filetypes=filetype
            )
        else:
            path = asksaveasfilename(
                initialdir=initial,
                defaultextension=extension,
                filetypes=filetype
            )
        return path

    def tag_striping(self, string):
        # Create two regex pattern to find 
        # the first one and replace by the second one
        if self.pos_style == '<{}>{}</{}>':
            pat, rep = re.compile(r'(<\w+>)(.+)(<\/\w+>)'), r'\2'
        else:
            pat, rep = re.compile(r'(.+)([_\t]\w+)'), r'\1'
        # Create a striping function to strip tags
        striping = lambda string: pat.sub(rep, string)
        # Strip leading and tailing spaces
        striped = striping(string).strip()
        return striped

    def redirect(self, text):
        reshaped_text = arabic_reshaper.reshape(text)
        redir_text = get_display(reshaped_text)
        return redir_text

    def text_normalizer(self, text):
        # Strip leading and tailing spaces
        text = text.strip()
        # Replace sequence of more than space by one
        text = re.sub(' {2,}', ' ', text)
        # Add space between word and punctuations
        text = re.sub(
            r'(\w)([.:!،؛؟»\]\)\}«\[\(\{])', 
            r'\1 \2', 
            text)
        return text

    def word_normalizer(self, word):
        # Swap Arabic characters and Persians
        translation_src, translation_dst = ';ىكي','یکی؛'
        # Convert latin digits to Persian digits
        translation_src += '0123456789%'
        translation_dst += '۰۱۲۳۴۵۶۷۸۹٪'
        table = word.maketrans(translation_src, translation_dst)
        word = word.translate(table)
        return word.lower()

    def sent_tokenizer(self, text):
        # Normalize the text
        text = self.text_normalizer(text)
        # Tokenize sentences by period, question mark, exclamation mark, and new line
        sents = re.split('(?<=[.؟!\n])\s*', text)
        # Remove empty lines
        sents = [sent for sent in sents if sent!='']
        # Tokenize sentences and words
        normalized_sents = []
        for sent in sents:
            normalized_words = []
            sent = sent.strip().split()
            for word in sent:
                word = self.word_normalizer(word.strip())
                normalized_words.append(word)
            normalized_sents.append(normalized_words)
        return normalized_sents

    def save_project(self):
        # Check if there is somthing to save
        if not self.corpus and not self.tagged_corpus:
            # Raise error if there is nothing to save
            return WR().empty_project()
        path = self.get_path(
            False, 
            '.proj', 
            [('Project Files', '*.proj')])

        if path:
            proj = dict()
            # Corpus variables
            proj['text'] = self.text
            proj['corpus_length'] = self.corpus_length
            proj['corpus'] = self.corpus
            proj['corpus_path'] = self.corpus_path

            # Working variables
            proj['current_sent'] = self.current_sent
            proj['sentence'] = self.sentence
            proj['word'] = self.word
            proj['tagged_sent'] = self.tagged_sent
            proj['tagged_corpus'] = self.tagged_corpus
            proj['file_name'] = self.file_name

            # Tagset variables
            proj['tagset_name'] = self.tagset_name
            proj['tagset_path'] = self.tagset_path
            proj['tagset'] = self.tagset

            proj['model_path'] = self.model_path

            # Style variables
            proj['font_list'] = self.font_list
            proj['pos_style'] = self.pos_style
            proj['font'] = self.font
            proj['font_name'] = self.font_name
            proj['dir'] = self.dir
            self.model.saving(path, proj, 'wb')

    def open_project(self):
        path = self.get_path(
            True, 
            '.proj', 
            [('Project Files', '*.proj')])

        if path:
            self.project_path = path
            proj = self.model.open_file(path, 'rb')

            self.text = proj['text']
            self.corpus_length = proj['corpus_length']
            self.corpus = proj['corpus']
            self.corpus_path = proj['corpus_path']

            # Working variables
            self.current_sent = proj['current_sent']
            self.sentence = proj['sentence']
            self.word = proj['word']
            self.tagged_sent = proj['tagged_sent']
            self.tagged_corpus = proj['tagged_corpus']
            self.file_name = proj['file_name']

            # Tagset variables
            self.tagset_name = proj['tagset_name']
            self.tagset_path = proj['tagset_path']
            self.tagset = proj['tagset']

            self.model_path = proj['model_path']

            # Style variables
            self.font_list = proj['font_list']
            self.pos_style = proj['pos_style']
            self.font = proj['font']
            self.font_name = proj['font_name']
            self.dir = proj['dir']

    def export(self):
        # Export an XML file
        if self.pos_style == '<{}>{}</{}>':
            self.create_xml()
        else:
            # Assign a delimiter based on pos style
            delimiter = ['\n', ''][self.pos_style=='{}\t{}\n']
            # Prepare the tagged text
            text = delimiter.join(' '.join(i) for i in self.tagged_corpus)
            # Get the path
            path = self.get_path(False)
            # Save the file
            self.model.saving(path, text, 'w')

    def create_xml(self):
        flated = [f"<SENT>{''.join(sent)}</SENT>" for sent in self.tagged_corpus]
        xml_string = f"<TEXT>{''.join(flated)}</TEXT>"
        indented =  minidom.parseString(xml_string).toprettyxml()
        path = self.get_path(False, '.xml', [('XML File', '*.xml')])
        if path:
            self.model.saving(path, indented, 'w')
            

if __name__=='__main__':
    Controller()
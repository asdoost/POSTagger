
<img src="https://live.staticflickr.com/65535/51739592944_72cef6f803_o.png" alt="Logo" width="109" height="74">

# <‌/POSTagger>

POSTagger is a GUI app for semi-automatic POS tagging.

## Installation

To install the app copy the follwing command in your terminal:

`>>> pip install POSTagger`

You can also simply download the repository via Github website or the following command:

`>>> git clone https://github.com/asdoost/POSTagger`

After downloding the repository, go to the POSTagger folder and copy the following command:

`>>> chmod +x POSTagger.py`

## Usage

To start POSTagger, simply type `POSTagger` in your command line:

`>>> POSTagger`

If you downloded the repository using `git clone`, go to the POSTagger folder and type the following command in your command line:

`>>> ./POSTagger.py`

### Opening Wizard

POSTagger starts with an openning wizard. Here, you can either import a project that you already saved, or you can start a new project by importing a corpus.

![Openning wizard](https://live.staticflickr.com/65535/51739596434_5e05e4a48d_o.png)

In the fourth line of the wizard you can choose between tagsets. There are 5 tagsets: _`default`_, _`Brown tagset`_, _`PENN Treebank tagset`_, _`Universal POS Tagset`_, and _`Bijankhan tagset`_.

In the fifth line of the wizard, you can choose between three POS tagging style: _`XML`_, _`underscore`_, and _`tab`_.

After choosing the preferred setting, press `OK` to start tagging.

### Main Window

The main window consists of six parts:

1. Text Box
2. Frequency Label
3. Word Entry
4. Edit Buttons
5. Tagset
6. Tagging Buttons

![Main Window](https://live.staticflickr.com/65535/51739596584_6a592d6e1e_o.png)

**Text Box** displays the current sentence that your are tagging.

**Word Entry** displays the word that should be tagged.

**Frequency Label** displays the frequency of the word that you are tagging.

**Edit Buttons** consist of three buttons:

_`Merge`_ button which combines the cuurent word with the following word.

_`Split`_ button undoes what has been merged.

_`Re-tokenize`_ button retokenize the sentence up to the last word.

**Tagset** provides POS categories.

**Tagging buttons** consist of two buttons:

_`Tag`_  which assigns the chosen tag two the word, using the preferred tagging style.

_`Untag`_ strips the last word out of the chosen tag (untags what have has been tagged).

From the `File menu` choose `Save the project` to save what you have done.

When you finished your project, from the `File menu` choose `Export` to get your work in a single `txt` (for underscore and tab tagging style) or `xml` (for XML tagging style) file.

### Preferences

From the `File menu` choose `Preferences` to change the tagset, font, font size, or text direction.

![Preferences](https://live.staticflickr.com/65535/51739195778_200299a385_o.png)

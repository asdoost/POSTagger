import csv
import pickle

class Model:
    def __init__(self):
        pass

    def open_file(self, path, mode='r'):
        # Open the path
        if mode=='rb':
            with open(path, mode) as file:
                data = pickle.load(file)
        else:
            with open(path, mode, encoding='utf8') as file:
                data = file.read()
        return data

    def saving(self, path, text, mode):
        # Save the twxt to selected path
        if mode=='wb':
            with open(path, mode) as file:
                pickle.dump(text, file)
        else:
            with open(path, mode, encoding='utf8') as file:
                file.write(text)

    def open_tagset(self, path):
        # Open CSV tagset file
        file = open(path, 'r', encoding='utf8')
        data = csv.reader(file)
        return data

if __name__=='__main__':
    Model()
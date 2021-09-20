import os
import pickle
import PySimpleGUI as Sg
from typing import Dict
Sg.ChangeLookAndFeel('Black')


class Gui:
    def __init__(self):
        self.layout: list = [
            [Sg.Text('Search Term', size=(11, 1)),
             Sg.Input(size=(40, 1), focus=True, key="TERM"),
             Sg.Radio('Contains', size=(10, 1), group_id='Choice', key="CONTAINS", default=True),
             Sg.Radio('StatsWith', size=(10, 1),  group_id='Choice', key="STARTSWITH"),
             Sg.Radio('EndsWith', size=(10, 1),  group_id='Choice', key="ENDSWITH")],
            [Sg.Text('Root Path', size=(10, 1)),
             Sg.Input('/home', size=(40, 1), key="PATH"),
             Sg.FolderBrowse('Browse', size=(10, 1)),
             Sg.Button('Re-Index', size=(10, 1), key="_INDEX_"),
             Sg.Button('Search', size=(10, 1), bind_return_key=True, key="_SEARCH_")],
            [Sg.Output(size=(100,  30))]]

        self.window = Sg.Window('File Search Engine', self.layout, element_justification='left',
                                icon=r"/home/rha/PycharmProjects/File-Search/explorer.ico")


class SearchEngine:
    def __init__(self):
        self.file_index = []
        self.results = []
        self.matches = 0
        self.records = 0

    def create_new_index(self, values: Dict[str, str]) -> None:
        root_path = values['PATH']
        self.file_index: list = [(root, files) for root, dirs, files in os.walk(root_path) if files]

        with open('file_index.pkl', 'wb') as f:
            pickle.dump(self.file_index, f)

    def load_existing_index(self):
        try:
            with open('file_index.pkl', 'rb') as f:
                self.file_index = pickle.load(f)
        except Exception as e:
            self.file_index = []
            print(e)

    def search(self, values: Dict[str, str]) -> None:
        self.results.clear()
        self.matches = 0
        self.records = 0
        term = values['TERM']

        for path, files in self.file_index:
            for file in files:
                self.records += 1
                if (values['CONTAINS'] and term.lower() in file.lower() or
                        values['STARTSWITH'] and file.lower().startswith(term.lower()) or
                        values['ENDSWITH'] and file.lower().endswith(term.lower())):

                    result = path.replace('\\', '/') + '/' + file
                    self.results.append(result)
                    self.matches += 1
                else:
                    continue

        # save results
        with open('search_results.txt', 'w') as f:
            for row in self.results:
                f.write(row + '\n')


def main():
    g = Gui()
    s = SearchEngine()
    s.load_existing_index()

    while True:
        event, values = g.window.read()
        if event is None:
            break
        if event == '_INDEX_':
            s.create_new_index(values)
            print()
            print('>> New Index has been created')
            print()

        if event == '_SEARCH_':
            s.search(values)

            # print results to output element
            print()
            for result in s.results:
                print(result)
            print()
            print(">> Searched {:,d} records and found {:,d} matches".format(s.records, s.matches))
            print(">> Results saved in working directory as search_results.txt.")


if __name__ == '__main__':
    print('Starting program...')
    main()

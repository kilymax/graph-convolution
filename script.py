import pandas as pd
import numpy as np
import os
from tkinter import *
from tkinter import filedialog as fd

class Main(Tk):

    def __init__(self):
        super().__init__()
        self.button1 = Button(self, text='Выбрать\nCSV-файл', width=16, height=2, 
                              font='Verdana 12', command=self.open_file)
        self.button1.place(x=20, y=20)

    # функция с основным функционалом
    def open_file(self):

        # выбор и открытие CSV-файла
        # image_path = fd.askopenfilename()
        image_path = 'test.csv'
        df = pd.read_csv(image_path, delimiter='\t', encoding='utf-16')
        cols = df.columns
        colscount = len(cols)
        rows = df[cols[1]][1:]
        rowscount = len(rows)

        self.label1 = Label(text=f'Параметров: {colscount}\nЗначений: {rowscount}', 
                            width=16,font='Verdana 12')
        self.label1.place(x=20, y=80)

        self.param_selection()

    def param_selection(self):
        selection_window = Tk()
        selection_window.geometry('600x600')
        selection_window.title('Выбор параметров')
        selection_window['bg'] = 'white'

        selection_window.mainloop()


file_dir = os.path.split(__file__)[0] + '\\'
if __name__ == "__main__":
    main = Main()
    main.geometry('1280x720')
    main.title('CSV Smoother')
    main['bg'] = 'white'


    main.mainloop()
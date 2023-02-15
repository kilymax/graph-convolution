import pandas as pd
import numpy as np
import os
from tkinter import *
from tkinter import filedialog as fd
from matplotlib import pyplot as plt

class Main(Tk):

    def __init__(self):
        super().__init__()

        paramindexlist = IntVar()

        self.leftframe = Frame(self, bg='#bababa')
        self.leftframe.pack(anchor=NW, side=LEFT, expand=1, fill=Y)

        self.labelframe1 = LabelFrame(self.leftframe, 
                            font=font, bg='#bababa')
        self.labelframe1.pack(padx=5, pady=5, ipadx=5, ipady=5)

        self.button1 = Button(self.labelframe1, text='Выбрать CSV-файл', width=22, height=1, 
                              font='Verdana 12', command=self.open_file)
        self.button1.pack(side=TOP, padx=5, pady=5)

        self.label1 = Label(self.labelframe1, text='', width=20,
                            height=2, bg='#bababa', font=font)
        self.label1.pack()

        self.labelframe2 = LabelFrame(self.leftframe, text='Выбор параметров', font=font, bg='#bababa')
        self.labelframe2.pack(expand=1, fill=Y, padx=5, pady=5, ipadx=5, ipady=5)

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

        # Вывод информации о данных
        self.label1.config(text=f'Параметры: {colscount}\nСтроки: {rowscount}')

        # Выбор параметров для построения графиков
        listbox = Listbox(self.labelframe2, selectmode=MULTIPLE, width=36, height=24)
        for param in cols:
            listbox.insert(END, param)
        listbox.pack(ipadx=5, ipady=5, padx=5, pady=5,)

        self.button2 = Button(self.labelframe2, text='Построить графики', width=18, height=1, 
                              font='Verdana 12', command=self.create_plots)
        self.button2.pack(side=TOP, padx=5, pady=5)

    def create_plots(self):
        paramindexlist = self.listbox.curselection()
        x = np.arange(-10, 10.01, 0.01)
        plt.plot(x, x**2)
        plt.show()


file_dir = os.path.split(__file__)[0] + '\\'
window_size = (1200, 600)
font = 'Verdana 12'
if __name__ == "__main__":
    main = Main()
    main.geometry(f'{window_size[0]}x{window_size[1]}')
    main.title('CSV Smoother')
    # main['bg'] = 'white'


    main.mainloop()
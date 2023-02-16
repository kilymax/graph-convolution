import pandas as pd
import numpy as np
import os
import shutil

from tkinter import *
from tkinter import filedialog as fd
from matplotlib import pyplot as plt

class Main(Tk):

    def __init__(self):
        super().__init__()

        self.original_file_path = ''

        # Левая и правая части интерфейса
        self.leftframe = Frame(self, bg='#bababa')
        self.leftframe.grid(row=0, column=0, sticky="nsew")
        self.rightframe = Frame(self, bg='green')
        self.rightframe.grid(row=0, column=1, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=10)

        # Наполнение левой части
        self.button1 = Button(self.leftframe, text='Выбрать CSV-файл', width=22, height=1, 
                              font=font, command=self.open_file)
        self.button1.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

        self.label1 = Label(self.leftframe, text='', width=20, height=2, bg='#bababa', font=font)
        self.label1.grid(row=1, column=0, sticky="nsew")
        
        self.listbox = Listbox(self.leftframe, selectmode=MULTIPLE, width=36, height=24)
        self.listbox.grid(row=2, column=0, pady=5, padx=10, sticky="nsew")
        self.leftframe.grid_rowconfigure(2, weight=1)

        self.button2 = Button(self.leftframe, text='Построить график', 
                                width=18, height=1, font=font, command=self.create_plots)
        self.button2.grid(row=3, column=0, pady=5, padx=10, sticky="nsew")

        self.label2 = Label(self.leftframe, text='', fg='red', 
                            width=20, height=2, bg='#bababa', font=font)
        self.label2.grid(row=4, column=0, sticky="n")

        # Наполнение правой части
        self.canvas = Canvas(self.rightframe, bg='red')
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.rightframe.grid_columnconfigure(0, weight=1)
        self.rightframe.grid_rowconfigure(0, weight=5)

        self.bottomframe = Frame(self.rightframe, bg='blue')
        self.bottomframe.grid(row=1, column=0, sticky="nsew")

        self.button3 = Button(self.bottomframe, text='Замутить шото', width=30, height=3, 
                              font=font, command=self)
        self.button3.grid(row=0, column=0, pady=5, padx=5)
        self.rightframe.grid_rowconfigure(1, weight=1)    
        

    # функция с основным функционалом
    def open_file(self):
        try:
            # выбор и открытие CSV-файла
            self.original_file_path = fd.askopenfilename()
            self.original_file_name = self.original_file_path.split('/')[-1:][0]
            self.modified_file_path = '/'.join(self.original_file_path.split('/')[:-1:1]) + '/modified_' + self.original_file_name
            shutil.copyfile(self.original_file_path, self.modified_file_path, follow_symlinks=True)

            self.df = pd.read_csv(self.modified_file_path, delimiter='\t', encoding='utf-16')
            self.cols = self.df.columns

            # Вывод информации о данных
            self.label1.config(text=f'Параметры: {self.df.shape[1]-1}\nСтроки: {self.df.shape[0]-1}', 
                                fg='black')

            # Выбор параметров для построения графиков
            for param in self.cols:
                if param != 'DateTime':
                    self.listbox.insert(END, param)

            #self.button2.config(command=self.create_plots)
        except FileNotFoundError:
            self.label1.config(text='Файл не выбран!', fg='red')
            self.label2.config(text='')

    # создание графиков
    def create_plots(self):
        if self.original_file_path != '':
            if self.listbox.curselection() != ():
                self.label2.config(text='')
                paramindexlist = self.listbox.curselection()
                for i in paramindexlist:
                    x = np.arange(0, self.df.shape[0]-1, 1)
                    y = np.array(list(self.df[self.cols[i+1]][1:]), float)
                    print(f'{i+1} параметр ({self.cols[i+1][1:]})\nЗначения: {y}')
                    plt.plot(x, y)
                plt.show()
            else:
                self.label2.config(text='Параметры не выбраны!\n')
        else:
            self.label1.config(text='Файл не выбран!', fg='red')
        

script_dir = os.path.split(__file__)[0] + '\\'
window_size = (1200, 600)
font = 'Verdana 12'
if __name__ == "__main__":
    main = Main()
    main.geometry(f'{window_size[0]}x{window_size[1]}')
    main.title('CSV Smoother')
    # main['bg'] = 'white'


    main.mainloop()
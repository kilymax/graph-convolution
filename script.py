import pandas as pd
import numpy as np
import matplotlib
import os
import shutil

from tkinter import *
from tkinter import filedialog as fd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as ticker

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
                              font=font1, command=self.open_file)
        self.button1.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

        self.label1 = Label(self.leftframe, text='', width=20, height=2, bg='#bababa', font=font1)
        self.label1.grid(row=1, column=0, sticky="nsew")
        
        self.listbox = Listbox(self.leftframe, selectmode=MULTIPLE, width=36, height=24)
        self.listbox.grid(row=2, column=0, pady=5, padx=10, sticky="nsew")
        self.leftframe.grid_rowconfigure(2, weight=1)

        self.button2 = Button(self.leftframe, text='Построить график', 
                                width=18, height=1, font=font1, command=self.create_plots)
        self.button2.grid(row=3, column=0, pady=5, padx=10, sticky="nsew")

        self.label2 = Label(self.leftframe, text='', fg='red', 
                            width=20, height=2, bg='#bababa', font=font1)
        self.label2.grid(row=4, column=0, sticky="n")

        # Наполнение правой части
        self.rightframe.grid_columnconfigure(0, weight=1)
        self.rightframe.grid_rowconfigure(0, weight=1)

        self.figure = plt.Figure()
        self.canvas = FigureCanvasTkAgg(self.figure, self.rightframe)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        self.ax = self.figure.add_axes(111)

        matplotlib.rcParams['font.family'] = 'verdana'
        margins = {
            "left"   : 0.08,
            "bottom" : 0.1,
            "right"  : 0.980,
            "top"    : 0.980   
        }
        self.figure.subplots_adjust(**margins) 
        
        self.bottomframe = Frame(self.rightframe, bg='blue')
        self.bottomframe.grid(row=1, column=0, sticky="nsew")

        self.button3 = Button(self.bottomframe, text='Замутить шото', width=30, height=3, 
                              font=font1, command=self)
        self.button3.grid(row=0, column=0, pady=5, padx=5)
        #self.rightframe.grid_rowconfigure(1, weight=1)    
        

    # функция с основным функционалом
    def open_file(self):
        try:
            # выбор и открытие CSV-файла
            #self.original_file_path = fd.askopenfilename()
            self.original_file_path = 'c:/.My/Freelance/CSVSmoother/test.csv'
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
                self.maxY = 0
                self.label2.config(text='')
                paramindexlist = self.listbox.curselection()
                self.ax.clear()
                self.ax.set_xlabel(f'Временная ось ({self.df.shape[0]-1} сек)')
                if len(paramindexlist) == 1:
                    self.ax.set_ylabel(f'{self.df[self.cols[paramindexlist[0]+1]][0]}')
                else:
                    self.ax.set_ylabel('Единицы измерения')
                for i in paramindexlist:
                    x = np.arange(0, self.df.shape[0]-1, 1)
                    y = np.array(list(self.df[self.cols[i+1]][1:]), float)
                    print(f'{i+1} параметр ({self.cols[i+1][1:]})\nЗначения: {y}')
                    self.ax.plot(x, y, label=f'{self.cols[i+1][1:]} ({self.df[self.cols[i+1]][0]})')
                    self.ax.grid(visible=True, which='major', color = 'gray')
                    self.ax.grid(visible=True, which='minor', color = 'gray', linestyle = ':')
                    if self.maxY < max(y):
                        self.maxY = max(y)
                self.ax.legend(ncol=1, fontsize='8', loc='best') # bbox_to_anchor=(1, 1.15),
                self.ax.xaxis.set_major_locator(ticker.MultipleLocator(500))
                self.ax.xaxis.set_minor_locator(ticker.MultipleLocator(100))
                self.ax.yaxis.set_major_locator(ticker.MultipleLocator(self.maxY/12))
                self.ax.yaxis.set_minor_locator(ticker.MultipleLocator(self.maxY/3))
                self.canvas.draw()
            else:
                self.label2.config(text='Параметры не выбраны!\n')
        else:
            self.label1.config(text='Файл не выбран!', fg='red')
        

script_dir = os.path.split(__file__)[0] + '\\'
window_size = (1200, 600)
font1 = 'Verdana 12'
font2 = 'Verdana 8'
if __name__ == "__main__":
    main = Main()
    main.geometry(f'{window_size[0]}x{window_size[1]}')
    main.title('CSV Smoother')
    # main['bg'] = 'white'


    main.mainloop()
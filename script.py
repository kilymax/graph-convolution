import pandas as pd
import numpy as np
import matplotlib
import os
import shutil

from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as ticker

import plotly.express as px

class Main(Tk):

    def __init__(self):
        super().__init__()

        self.original_file_path = ''
        # self.bind("<MouseWheel>", self.mouse_wheel)

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
                                width=18, height=1, font=font1)
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
        self.bottomframe.grid(row=2, column=0, sticky="nsew")

        # создание бегунков для регулировки масштаба графика
        self.scale1 = Scale(self.bottomframe, orient=HORIZONTAL, 
                            highlightthickness=0, bg='#a30000', fg='black', 
                            font='Verdana 8')
        self.scale1.grid(row=0, column=0, sticky="nsew")

        self.scale2 = Scale(self.bottomframe, orient=HORIZONTAL, 
                            highlightthickness=0, bg='#0a00a3', 
                            fg='black', font='Verdana 8')
        self.scale2.grid(row=1, column=0, sticky="nsew")
        self.bottomframe.grid_columnconfigure(0, weight=1)
        
        self.scale3 = Scale(self.bottomframe, orient=HORIZONTAL, 
                            highlightthickness=0, bg='#0a00a3', 
                            fg='black', font='Verdana 8')
        self.scale3.grid(row=2, column=0, sticky="nsew")
        self.bottomframe.grid_columnconfigure(0, weight=1)
        
        self.scale1.bind("<MouseWheel>", self.sc1_mouse_wheel)
        self.scale1.bind("<Button-4>", self.sc1_mouse_wheel)
        self.scale1.bind("<Button-5>", self.sc1_mouse_wheel)
        self.scale2.bind("<MouseWheel>", self.sc2_mouse_wheel)
        self.scale2.bind("<Button-4>", self.sc2_mouse_wheel)
        self.scale2.bind("<Button-5>", self.sc2_mouse_wheel)
        self.scale3.bind("<MouseWheel>", self.sc3_mouse_wheel)
        self.scale3.bind("<Button-4>", self.sc3_mouse_wheel)
        self.scale3.bind("<Button-5>", self.sc3_mouse_wheel)

        # кнопка сглаживания
        self.button3 = Button(self.bottomframe, text='Сгладить', width=30, height=2, 
                              font=font1)
        self.button3.grid(row=2, column=0, pady=5, padx=5)   
        
    def sc1_mouse_wheel(self, event):
        # respond to Linux or Windows wheel event
        if event.num == 5 or event.delta == -120:
            self.scale1.set(self.scale1.get()-1)
        if event.num == 4 or event.delta == 120:
            self.scale1.set(self.scale1.get()+1)
    def sc2_mouse_wheel(self, event):
        # respond to Linux or Windows wheel event
        if event.num == 5 or event.delta == -120:
            self.scale2.set(self.scale2.get()-1)
        if event.num == 4 or event.delta == 120:
            self.scale2.set(self.scale2.get()+1)
    def sc3_mouse_wheel(self, event):
        # respond to Linux or Windows wheel event
        if event.num == 5 or event.delta == -120:
            self.scale3.set(self.scale2.get()-1)
        if event.num == 4 or event.delta == 120:
            self.scale3.set(self.scale2.get()+1)

    # функция с основным функционалом
    def open_file(self):
        try:
            # выбор и открытие CSV-файла
            #self.original_file_path = fd.askopenfilename()
            self.original_file_path = 'c:/.My/Freelance/CSVSmoother/test.csv'
            self.original_file_name = self.original_file_path.split('/')[-1:][0]
            self.modified_file_path = '/'.join(self.original_file_path.split('/')[:-1:1]) + '/modified_' + self.original_file_name
            shutil.copyfile(self.original_file_path, self.modified_file_path, follow_symlinks=True)

            # Чтение данных и сохранение в dataframe
            self.df = pd.read_csv(self.modified_file_path, delimiter='\t', encoding='utf-16')
            self.cols = self.df.columns
            self.bottomborder = self.df[self.cols[1]][1:].index[0]
            self.upperborder = self.df[self.cols[1]][1:].index[-1]
            print('Нижняя и верхняя временные границы:', self.bottomborder, self.upperborder)
            
            # Добавление конфига для бегунков и кнопки "построить график"
            self.scale1.config(from_=self.bottomborder, to=self.upperborder, 
                                resolution=1, command=lambda event: self.create_plots(self.scale1.get(), self.scale2.get()))
            self.scale2.config(from_=self.bottomborder, to=self.upperborder, 
                                resolution=1, command=lambda event: self.create_plots(self.scale1.get(), self.scale2.get()))
            self.scale3.config(from_=1, to=500, 
                                resolution=1, command=lambda event: self.smoothing(self.scale3.get(), self.scale1.get(), self.scale2.get()))
            self.scale1.set(self.bottomborder)
            self.scale2.set(self.upperborder)
            self.scale3.set(1)

            self.button2.config(command=lambda: self.create_plots(self.scale1.get(), self.scale2.get()))
            self.button3.config(command=lambda: self.save_smooth_result(self.scale1.get(), self.scale2.get()))

            # Вывод информации о данных
            self.label1.config(text=f'Параметры: {len(self.cols)-1}\nСтроки: {self.upperborder}', 
                                fg='black')

            # Выбор параметров для построения графиков
            for param in self.cols:
                if param != 'DateTime':
                    self.listbox.insert(END, param)

        except FileNotFoundError:
            self.label1.config(text='Файл не выбран!', fg='red')
            self.label2.config(text='')

    # создание графиков
    def create_plots(self, sc1, sc2):
        if self.original_file_path != '':
            if self.listbox.curselection() != ():
                self.maxY = 0
                self.label2.config(text='')
                self.paramindexlist = self.listbox.curselection()
                self.ax.clear()

                # Настройка внешнего вида графика
                self.ax.set_xlabel(f'Временная ось ({sc2-sc1+1} сек)')
                if len(self.paramindexlist) == 1:
                    self.ax.set_ylabel(f'{self.df[self.cols[self.paramindexlist[0]+1]][0]}')
                else:
                    self.ax.set_ylabel('Единицы измерения')

                # Прорисовка графика
                for i in self.paramindexlist:
                    self.data = self.df[self.cols[i+1]][1:][sc1-1:sc2]
                    self.x = np.array(self.data.index)
                    self.y = np.array(self.data.values, float)
                    print(f'{i+1} параметр ({self.cols[i+1][1:]})\nВремя: {self.x}\nЗначения: {self.y}')
                    self.ax.plot(self.x, self.y, label=f'{self.cols[i+1][1:]} ({self.df[self.cols[i+1]][0]})')
                    self.ax.grid(visible=True, which='major', color = 'gray')
                    self.ax.grid(visible=True, which='minor', color = 'gray', linestyle = ':')
                    if self.maxY < max(self.y):
                        self.maxY = max(self.y)
                # Настройка внешнего вида графика
                self.ax.legend(ncol=1, fontsize='8', loc='best') # bbox_to_anchor=(1, 1.15),
                self.ax.xaxis.set_major_locator(ticker.MultipleLocator(500))
                self.ax.xaxis.set_minor_locator(ticker.MultipleLocator(100))
                self.ax.yaxis.set_major_locator(ticker.MultipleLocator(abs(self.maxY/12)))
                self.ax.yaxis.set_minor_locator(ticker.MultipleLocator(abs(self.maxY/3)))
                self.canvas.draw()
            else:
                pass
                #self.label2.config(text='Параметры не выбраны\n')
        else:
            self.label1.config(text='Файл не выбран!', fg='red')
        
    def smoothing(self, w, sc1, sc2):
        self.create_plots(sc1, sc2)
        for i in self.listbox.curselection():
            self.smoothset = np.array(self.df[self.cols[i+1]][1:][sc1-1:sc2].values, float)
            print(self.smoothset)
            self.w = np.hanning(w)
            self.convolved = np.convolve(self.w/self.w.sum(), self.y, mode='same')
            self.convolved = np.array(self.convolved, round())
            self.ax.plot(self.x, self.convolved, label=f'{self.cols[i+1][1:]} ({self.df[self.cols[i+1]][0]})')
            self.canvas.draw()
            #print(self.data.index[0], self.data.values)
    
    def save_smooth_result(self, sc1, sc2):
        for i in self.listbox.curselection():
            for j in range(len(self.df[self.cols[i+1]][1:][sc1-1:sc2].values)):
                print(f'{self.df[self.cols[i+1]][1:][sc1-1:sc2].index[j]}: {self.df[self.cols[i+1]][1:][sc1-1:sc2].values[j]} -> {self.convolved[j]}')
                self.df[self.cols[i+1]][1:][sc1-1:sc2].values[j] = self.convolved[j]
        self.create_plots(sc1, sc2)



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
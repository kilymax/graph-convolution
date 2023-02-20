import pandas as pd
import numpy as np
import matplotlib
import os

from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as ticker

class Main(Tk):

    def __init__(self):
        super().__init__()

        self.font1 = 'Verdana 12'
        self.font2 = 'Verdana 8'

        buttonstyle = ttk.Style()
        buttonstyle.configure("TButton", background="grey", foreground="black", 
                                font=self.font1, justify="center")
        defaultlabelstyle = ttk.Style()
        defaultlabelstyle.configure("default.TLabel", foreground="black", 
                                    background="#bababa", font=self.font1, padding=[10, 0])
        dynamiclabelstyle = ttk.Style()
        dynamiclabelstyle.configure("dynamic.TLabel", foreground="black", 
                                    background="#bababa", font=self.font1,
                                    padding=[10, 0], anchor=TOP)

        self.original_file_path = ''
        # self.bind("<MouseWheel>", self.mouse_wheel)

        # Левая и правая части интерфейса
        self.leftframe = Frame(self, bg='#bababa')
        self.leftframe.grid(row=0, column=0, sticky="nsew", padx=3, pady=3)
        self.rightframe = Frame(self, bg='white')
        self.rightframe.grid(row=0, column=1, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=10)

        # Наполнение левой части
        self.button1 = ttk.Button(self.leftframe, text='Выбрать CSV-файл', command=self.open_file)
        self.button1.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

        self.label1 = ttk.Label(self.leftframe, style="default.TLabel", text='\n')
        self.label1.grid(row=1, column=0, sticky="nsew")
        
        self.listbox = Listbox(self.leftframe, selectmode=MULTIPLE, width=36, height=24)
        self.listbox.grid(row=2, column=0, pady=5, padx=10, sticky="nsew")
        self.leftframe.grid_rowconfigure(2, weight=1)

        self.button2 = ttk.Button(self.leftframe, text='Построить/обновить\nграфик',
                                command=lambda: self.notificationlabel.config(text='Файл не выбран', 
                                        style="dynamic.TLabel", foreground='red'))
        self.button2.grid(row=3, column=0, pady=5, padx=10, sticky="nsew")

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
        
        self.bottomframe = Frame(self.rightframe, bg='#bababa')
        self.bottomframe.grid(row=2, column=0, sticky="nsew", padx=3, pady=3)

        # создание бегунков для регулировки масштаба графика
        self.scalelabel = Label(self.bottomframe, fg='black', width=8, height=6,
                                text='Нижняя\nграница\n\nВерхняя\nграница\n\nИнтенс.\nсвертки',  
                                justify=LEFT, bg='#bababa', font=self.font2, padx=5)
        self.scalelabel.grid(row=0, column=0, rowspan=3, sticky="nsew")
        self.scale1 = Scale(self.bottomframe, orient=HORIZONTAL, highlightthickness=0, 
                            bg='#850000', fg='white', font=self.font2, 
                            command=lambda event: self.notificationlabel.config(text='Файл не выбран', 
                                        style="dynamic.TLabel", foreground='red'))
        self.scale1.grid(row=0, column=1, columnspan=3, sticky="nsew")

        self.scale2 = Scale(self.bottomframe, orient=HORIZONTAL, highlightthickness=0, 
                            bg='#000085', fg='white', font=self.font2, 
                            command=lambda event: self.notificationlabel.config(text='Файл не выбран', 
                                        style="dynamic.TLabel", foreground='red'))
        self.scale2.grid(row=1, column=1, columnspan=3, sticky="nsew")
        
        self.scale3 = Scale(self.bottomframe, orient=HORIZONTAL, 
                            highlightthickness=0, bg='#008500', fg='white', font=self.font2, 
                            command=lambda event: self.notificationlabel.config(text='Файл не выбран', 
                                        style="dynamic.TLabel", foreground='red'))
        self.scale3.grid(row=2, column=1, columnspan=3, sticky="nsew")
        
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
        self.button3 = ttk.Button(self.bottomframe, text='Сгладить выбранный\nдиапазон', 
                                width=20, command=lambda: self.notificationlabel.config(text='Файл не выбран', 
                                                    style="dynamic.TLabel", foreground='red'))
        self.button3.grid(row=3, column=1, pady=5, padx=40, sticky="w")
        self.bottomframe.grid_columnconfigure(1, weight=1)

        # Label для уведомлений
        self.notificationlabel = ttk.Label(self.bottomframe, text='', style="dynamic.TLabel")
        self.notificationlabel.grid(row=3, column=2, pady=5, padx=5, sticky="nsew")
        self.bottomframe.grid_columnconfigure(2, weight=2)
        
        # кнопка сохранения в файл
        self.button4 = ttk.Button(self.bottomframe, text='Сохранить в\nновый CSV-файл', 
                                width=20, command=lambda: self.notificationlabel.config(text='Файл не выбран', 
                                        style="dynamic.TLabel", foreground='red'))
        self.button4.grid(row=3, column=3, pady=5, padx=40, sticky="e")
        self.bottomframe.grid_columnconfigure(3, weight=1)   
        
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
            self.scale3.set(self.scale3.get()-1)
        if event.num == 4 or event.delta == 120:
            self.scale3.set(self.scale3.get()+1)

    # функция с основным функционалом
    def open_file(self):
        try:
            # выбор и открытие CSV-файла
            self.original_file_path = fd.askopenfilename()
            # self.original_file_path = 'c:/.My/Freelance/CSVSmoother/test.csv'
            # shutil.copyfile(self.original_file_path, self.modified_file_path, follow_symlinks=True)

            # Чтение данных и сохранение в dataframe
            self.df = pd.read_csv(self.original_file_path, delimiter='\t', encoding='utf-16')
            self.notificationlabel.config(text='Файл успешно загружен', style="dynamic.TLabel", foreground='green')
            self.cols = self.df.columns
            self.bottomborder = self.df[self.cols[1]][1:].index[0]
            self.upperborder = self.df[self.cols[1]][1:].index[-1]
            # print('Нижняя и верхняя временные границы:', self.bottomborder, self.upperborder)
            
            # Добавление конфига для бегунков и кнопки "построить график"
            self.scale1.config(from_=self.bottomborder, to=self.upperborder, 
                                resolution=1, command=lambda event: self.create_plots(self.scale1.get(), self.scale2.get()))
            self.scale2.config(from_=self.bottomborder, to=self.upperborder, 
                                resolution=1, command=lambda event: self.create_plots(self.scale1.get(), self.scale2.get()))
            self.scale3.config(from_=1, to=100, 
                                resolution=1, command=lambda event: self.smoothing(self.scale3.get(), self.scale1.get(), self.scale2.get()))
            self.scale1.set(self.bottomborder)
            self.scale2.set(self.upperborder)
            self.scale3.set(1)

            self.button2.config(command=lambda: self.create_plots(self.scale1.get(), self.scale2.get()))
            self.button3.config(command=lambda: self.fix_smooth_result(self.scale1.get(), self.scale2.get()))

            # Вывод информации о данных
            self.label1.config(text=f'Параметры: {len(self.cols)-1}\nЗначения: {self.upperborder}')

            # Выбор параметров для построения графиков
            for param in self.cols:
                if param != 'DateTime':
                    self.listbox.insert(END, param)

        except FileNotFoundError:
            self.notificationlabel.config(text='Файл не выбран', style="dynamic.TLabel", foreground='red')

    # создание графиков
    def create_plots(self, sc1, sc2):
        if self.original_file_path != '':
            if self.listbox.curselection() != ():
                self.maxY = 1
                self.paramindexlist = self.listbox.curselection()
                self.ax.clear()

                # Настройка внешнего вида графика
                self.ax.set_xlabel(f'Временная ось ({sc2-sc1+1} сек)')
                if len(self.paramindexlist) == 1:
                    self.ax.set_ylabel(f'{self.df[self.cols[self.paramindexlist[0]+1]][0]}')
                else:
                    self.ax.set_ylabel('Единицы измерения')

                # Прорисовка графика на основе исходных данных
                for i in self.paramindexlist:
                    self.data = self.df[self.cols[i+1]][1:][sc1-1:sc2]
                    self.x = np.array(self.data.index)
                    self.y = np.array(self.data.values, float)
                    self.ax.plot(self.x, self.y, label=f'{self.cols[i+1][1:]} ({self.df[self.cols[i+1]][0]})')
                    if self.maxY < abs(max(self.y)):
                        self.maxY = abs(max(self.y))
                # Настройка внешнего вида графика
                
                self.ax.legend(ncol=1, fontsize='8', loc='best') # bbox_to_anchor=(1, 1.15),
                self.ax.grid(visible=True, which='major', color = 'gray')
                self.ax.grid(visible=True, which='minor', color = 'gray', linestyle = ':')
                self.ax.xaxis.set_major_locator(ticker.MultipleLocator(500))
                self.ax.xaxis.set_minor_locator(ticker.MultipleLocator(100))
                self.ax.yaxis.set_major_locator(ticker.MultipleLocator(self.maxY/12))
                self.ax.yaxis.set_minor_locator(ticker.MultipleLocator(self.maxY/3))
                self.canvas.draw()
                self.notificationlabel.config(text='', style="dynamic.TLabel", foreground='red')
            else:
                self.notificationlabel.config(text='Параметры не выбраны', style="dynamic.TLabel", foreground='red')
        else:
            self.notificationlabel.config(text='Файл не выбран', style="dynamic.TLabel", foreground='red')
    
    # Функция свертки (сглаживания)
    def smoothing(self, w, sc1, sc2):
        self.create_plots(sc1, sc2)
        self.w = np.kaiser(w*5, 30)
        self.smoothset = []
        for i in range(len(self.listbox.curselection())):
            k = self.listbox.curselection()[i]
            self.smoothset.append([])
            self.smoothset[i] = np.array(self.df[self.cols[k+1]][1:][sc1-1:sc2].values, float)
            # добавление отступов в датасет для равномерного сглаживания крайних значений
            try:
                self.bottompaddingset = np.full(w, np.array(self.df[self.cols[k+1]][1:].values[sc1-1-1], float))
                self.upperpaddingset = np.full(w, np.array(self.df[self.cols[k+1]][1:].values[sc2], float))
            except:
                self.bottompaddingset = np.full(w,  self.smoothset[i][0])
                self.upperpaddingset = np.full(w,  self.smoothset[i][-1])
            self.smoothset[i] = np.insert (self.smoothset[i], 0, self.bottompaddingset)
            self.smoothset[i] = np.append(self.smoothset[i], self.upperpaddingset)
            # свертка
            self.smoothset[i] = np.convolve(self.w/self.w.sum(), self.smoothset[i], mode='same')
            # возврат к исходному датасету
            self.smoothset[i] = np.around(self.smoothset[i][len(self.bottompaddingset):-len(self.upperpaddingset)], decimals=4)
            # построение графиков по результатам свертки
            self.ax.plot(self.x, self.smoothset[i], label=f'Convolved {self.cols[k+1][1:]} ({self.df[self.cols[k+1]][0]})')
            self.ax.legend(ncol=1, fontsize='8', loc='best')
            self.canvas.draw()
        
    # сохранение изменений в исходном dataframe
    def fix_smooth_result(self, sc1, sc2):
        for i in range(len(self.listbox.curselection())):
            k = self.listbox.curselection()[i]
            for j in range(len(self.df[self.cols[k+1]][1:][sc1-1:sc2].values)):
                # print(f'{self.df[self.cols[k+1]][1:][sc1-1:sc2].index[j]}: {self.df[self.cols[k+1]][1:][sc1-1:sc2].values[j]} -> {self.convolved[i][j]}')
                self.df[self.cols[k+1]][1:][sc1-1:sc2].values[j] = str(self.smoothset[i][j])
        # print(f'{self.df[self.cols[5+1]][1:][sc1-1:sc2].index[0]}: {self.df[self.cols[5+1]][1:][sc1-1:sc2].values[0]} -> {self.convolved[1][0]}')
        # print(self.convolved[1])
        self.button4.config(command=self.save_in_file)
        self.create_plots(sc1, sc2)

    # Сохранение dataframe в файл
    def save_in_file(self):
        self.original_file_name = self.original_file_path.split('/')[-1:][0]
        self.modified_file_path = '/'.join(self.original_file_path.split('/')[:-1:1]) + '/modified_' + self.original_file_name
        self.df.to_csv(self.modified_file_path, sep='\t', index= False, float_format="str", encoding="utf-16")
        self.notificationlabel.config(text='Файл успешно сохранен!', style="dynamic.TLabel", foreground='green')
        self.result_path = '/'.join(self.original_file_path.split('/')[:-1:1])
        os.startfile(self.result_path)

if __name__ == "__main__":
    main = Main()
    main.geometry(f'{1200}x{600}')
    main.title('CSV Convolution')
    main['bg'] = 'white'


    main.mainloop()
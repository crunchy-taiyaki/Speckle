import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import tkinter as tk
import tkinter.ttk as ttk
import sys
from initial_parameters import *
from power_spectrum import *

class Application(tk.Frame):
    def __init__(self, master=None, data=None, files=None):
        tk.Frame.__init__(self,master)
        self.master = master
        self.files = files
        self.data = data
        self.current_image = None
        self.vmax = None
        self.vmin = None
        self.createWidgets()


    def createWidgets(self):
        fig=plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        canvas=FigureCanvasTkAgg(fig,self.master)
        canvas.get_tk_widget().grid(row=0,column=1)
        canvas.draw()

        self.plotbutton=tk.Button(self.master, text="dark", command=lambda: self.show(canvas,ax,self.data.dark))
        self.plotbutton.grid(row=1,column=0)
        self.plotbutton=tk.Button(self.master, text="ref_dark", command=lambda: self.show(canvas,ax,self.data.ref_dark))
        self.plotbutton.grid(row=2,column=0)
        self.plotbutton=tk.Button(self.master, text="flat", command=lambda: self.show(canvas,ax,self.data.flat))
        self.plotbutton.grid(row=3,column=0)
        self.plotbutton=tk.Button(self.master, text="star_ps", command=lambda: self.show(canvas,ax,self.data.star_ps))
        self.plotbutton.grid(row=4,column=0)
        self.plotbutton=tk.Button(self.master, text="ref_ps", command=lambda: self.show(canvas,ax,self.data.ref_ps))
        self.plotbutton.grid(row=5,column=0)
        self.plotbutton=tk.Button(self.master, text="obj\ref_ps", command=lambda: self.show(canvas,ax,self.data.final_ps))
        self.plotbutton.grid(row=6,column=0)
        self.plotbutton=tk.Button(self.master, text="up", command=lambda: self.brighter(canvas,ax))
        self.plotbutton.grid(row=7,column=0)
        self.plotbutton=tk.Button(self.master, text="down", command=lambda: self.darker(canvas,ax))
        self.plotbutton.grid(row=8,column=0)
        self.plotbutton=tk.Button(self.master, text="save", command=lambda: self.save(fig))
        self.plotbutton.grid(row=9,column=0)


    def plot(self,canvas,ax,data):
        ax.imshow(data, cmap='gray',vmin=self.vmin,vmax=self.vmax)
        self.current_image = data
        canvas.draw()
        ax.clear()

    def show(self,canvas,ax,data):
        self.vmax = np.max(data)
        self.vmin = np.min(data)
        self.plot(canvas,ax,data)

    def brighter(self,canvas,ax):
        self.vmax = self.vmax/2
        self.plot(canvas,ax,self.current_image)


    def darker(self,canvas,ax):
        self.vmax = self.vmax*2
        self.plot(canvas,ax,self.current_image)

    def save(self,fig):
        path = self.files.images
        fig.savefig(path + '\\mean_star_ps.png')



files = DataFiles()
files.read_input('C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\inputs\\TEST_star_input.txt')
files.info()
data = Data()
#read data from files
data.read_from(files.data)

root=tk.Tk()
app=Application(root,data,files)
app.mainloop()
print('all done!')
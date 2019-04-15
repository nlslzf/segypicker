import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg



window = tk.Tk()
window.geometry("1366x768")
window.title("SEGYPICKER")


def plot_sth(canvas, figure, loc=(0, 0), x,y):
    x = x.get()
    y = y.get()

    suc = tk.Label(window, text = 'Coordinates have been read').grid(row = 4, column = 2)


    x = x.split(",")
    y = y.split(",")
    
    x = np.asfarray(x, float)
    y = np.asfarray(y, float)
    # x = x.astype(np.float)
    # y = y.astype(np.float)
    print (x, y)
    # print (type(x))



x = tk.StringVar()
y = tk.StringVar()


x_label = tk. Label(window, text = "X coordinates").grid(row = 1, column = 1)
y_label = tk. Label(window, text = "Y coordinates").grid(row = 2, column = 1)



x_coords = tk.Entry(window, textvariable = x).grid(row = 1, column = 2)
y_coords = tk.Entry(window, textvariable = y).grid(row = 2, column = 2)


read_button = tk.Button(window, text = "Read coordinates", command = lambda:plot_sth(x,y)).grid(row = 3, column = 1)




window.mainloop()

import tkinter  as tk
import obspy
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

window = tk.Tk()
window.geometry("1366x768")
window.title("SEGYPICKER")

# label = tkinter.Label(window, text="SEGY File").pack()



# top_frame = tk.Frame(window).pack()
# bottom_frame = tk.Frame(window).pack(side = "bottom")

def read_segy(segy_file_name):
    # if segy_file_name =='':
    #     tk.Lable(window, text = "Please input a SEGY file name").grid(row = 1, column = 5)

    fname = segy_file_name.get()

    segy_file = obspy.read(fname)
    # print (segy_file)
    # print (fname)

    i=0
    for tr in segy_file:
        tr.stats.distance = i
        i +=1

    tk.Label(window, text="SEGY file "+ fname+" has been read").grid(row = 1, column = 5)

    segy_plot = Figure(figsize = (5,3), dpi=300)
    segy_file.plot(type = 'section', show = False)
    canvas = FigureCanvasTkAgg(segy_plot, window)
    canvas.show()
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

segy_file_name = tk.StringVar()
segy_label = tk. Label(window, text = "SEGY File").grid(row = 1, column = 1)
segy_file = tk.Entry(window, textvariable = segy_file_name).grid(row = 1, column = 2)
segy_file_read_button = tk.Button(window, text = "Read SEGY", command = lambda:read_segy(segy_file_name)).grid(row = 1, column = 3)



# button1 = tk.Button(top_frame, text = 'SEGY File', fg = 'gray').pack()
# button2 = tk.Button(top_frame, text = 'Output tx File', fg = 'gray').pack()
# button3 = tk.Button(bottom_frame, text = 'Reduction Velocity (km/s)', fg = 'gray').pack(side = 'left')
# button3 = tk.Button(bottom_frame, text = 'Butterworth Filter', fg = 'gray').pack(side = 'left')

window.mainloop()
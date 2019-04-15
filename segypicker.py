import tkinter  as tk
import obspy import read


window = tk.Tk()
window.geometry("1366x768")
window.title("SEGYPICKER")

# label = tkinter.Label(window, text="SEGY File").pack()



# top_frame = tk.Frame(window).pack()
# bottom_frame = tk.Frame(window).pack(side = "bottom")

def read_segy():




    tk.Label(window, text="SEGY file has been read").grid(row = 1, column = 5)



segy_label = tk. Label(window, text = "SEGY File").grid(row = 1, column = 1)
segy_file = tk.Entry(window).grid(row = 1, column = 2)
segy_file_read = tk.Button(window, text = "Read SEGY", command = read_segy).grid(row = 1, column = 3)
# button1 = tk.Button(top_frame, text = 'SEGY File', fg = 'gray').pack()
# button2 = tk.Button(top_frame, text = 'Output tx File', fg = 'gray').pack()
# button3 = tk.Button(bottom_frame, text = 'Reduction Velocity (km/s)', fg = 'gray').pack(side = 'left')
# button3 = tk.Button(bottom_frame, text = 'Butterworth Filter', fg = 'gray').pack(side = 'left')

window.mainloop()
import tkinter as tk
from tkinter.filedialog import askopenfilename
from obspy import read, Trace, Stream
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import numpy as np
import tkinter.font as tkFont
from matplotlib.figure import Figure
from obspy.core import UTCDateTime

class SEGYPicker:

    def __init__(self, window):

        self.dpi = 150
        self.font = tkFont.Font(family="helvetica", size=12, weight='bold')
        self.segy_file_name = self.read_segy_filename()
        print (self.segy_file_name)

        self.shot_gather = self.read_segy_file()
        print (self.shot_gather)

        self.menu_frame = tk.Frame(window, width=1800, height=100, highlightbackground="black", highlightcolor="blue", highlightthickness=1)
        self.menu_frame.grid(row=0, column=0)

        self.segy_browse_label = tk.Label(self.menu_frame, text = "SEGY file : ", font=self.font, fg='blue', relief=tk.RAISED)
        self.segy_browse_label.grid(row=0, column=1, padx=10, pady=5)

        self.segy_read_status_label = tk.Label(self.menu_frame, text = self.segy_file_name.split("/")[-1], font=self.font, fg='blue', relief=tk.RIDGE)
        self.segy_read_status_label.grid(row=1, column=1, padx=10, pady=5)

        self.plot_button = tk.Button(self.menu_frame, text = "Plot", font=self.font, command=self.plot_gather, fg='blue')
        self.plot_button.grid(row=2, column=0, padx=10, pady=5)

        self.v_red_entry_label = tk.Label(self.menu_frame, text = 'LMO(km/s) : ', font=self.font, fg='green')
        self.v_red_entry_label.grid(row=0, column=3, padx=10, pady=5)

        self.v= tk.StringVar()
        self.v_red_entry_box = tk.Entry(self.menu_frame, textvariable = self.v, font=self.font, fg='green')
        self.v_red_entry_box.grid(row=1, column=3, padx=10, pady=5)

        self.v_red_apply_button = tk.Button(self.menu_frame, text = "Apply LMO", font=self.font, fg='green')
        self.v_red_apply_button.grid(row=2, column=3, padx=10, pady=5)


        self.v_red_apply_button.bind('<Button-1>', self.apply_vred)
        self.v_red_apply_button.bind('<Button-3>', self.remove_vred)


        self.apply_filter_label = tk.Label(self.menu_frame, text = 'Bandpass min,max freqs (Hz)', font=self.font, fg='brown')
        self.apply_filter_label.grid(row =0, column=4, padx=10, pady=5)

        self.bp_min_max_freqs= tk.StringVar()
        self.bp_min_max_freqs_entry_box = tk.Entry(self.menu_frame, textvariable = self.bp_min_max_freqs, font=self.font, fg='brown')
        self.bp_min_max_freqs_entry_box.grid(row=1, column=4, padx=10, pady=5)

        self.apply_filter_button = tk.Button(self.menu_frame, text = "Apply Filter",  font=self.font, fg='brown')
        self.apply_filter_button.grid(row=2, column=4, padx=10, pady=5)

        self.figure_frame = tk.Frame(window, width=1800, height=100, highlightbackground="black", highlightcolor="green", highlightthickness=1)
        self.figure_frame.grid(row=5, column=0, padx=10, pady=5)

        self.figure = plt.figure(figsize=(1800/self.dpi, 900/self.dpi), dpi=self.dpi)

        self.figure_canvas = FigureCanvasTkAgg(self.figure, self.figure_frame)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.toolbar = NavigationToolbar2Tk(self.figure_canvas, self.figure_frame)
        self.toolbar.update()




    def read_segy_filename(self):
        self.segy_file_name = askopenfilename(title = "Select SEGY file", filetypes = (("SEGY files","*.SEGY"),("SGY files","*.SGY"),("segy files","*.segy"),("sgy files","*.sgy"),("all files","*.*")))
        return self.segy_file_name

    def read_segy_file(self):
        self.shot_gather = read(self.segy_file_name, unpack_trace_headers=True)

        for tr in self.shot_gather:
            trhd = tr.stats.segy.trace_header
            offset = trhd.get('distance_from_center_of_the_source_point_to_the_center_of_the_receiver_group')
            tr.stats.distance = float(offset)
            tr.stats.starttime = UTCDateTime("1970-01-01T00:00:00.0")
            # print (offset)

        return self.shot_gather

    def plot_gather(self):
        self.shot_gather.plot(fig=self.figure, type='section', scale=0.5, recordstart=0, recordlength=20, linewidth=0.5, alpha=1)


    def apply_vred(self, event):

        self.v_red_apply_button.config(relief=tk.SUNKEN)

        self.v_red = self.v.get()
        print (self.v_red)
        # self.v_red_apply_button.config(relief= tk.SUNKEN)
        self.reduced_shot_gather = Stream()
        if float(self.v_red) > 0:

            for trace in self.shot_gather:
                new_trace = Trace()
                new_trace.data = trace.data
                new_trace.stats.distance = trace.stats.distance
                new_trace.stats.sampling_rate = trace.stats.sampling_rate
                time_clip = 0.001*np.abs(new_trace.stats.distance)/float(self.v_red)
                new_trace.trim(new_trace.stats.starttime+time_clip)
                self.reduced_shot_gather += new_trace
        elif float(self.v_red) == 0:
            self.reduced_shot_gather = self.shot_gather
        self.reduced_shot_gather.plot(fig=self.figure, type='section', scale=0.5, recordstart=0, recordlength=20, linewidth=0.5, alpha=1)

    def remove_vred(self, event):
        self.shot_gather.plot(fig=self.figure, type='section', scale=0.5, recordstart=0, recordlength=20, linewidth=0.5, alpha=1)

window = tk.Tk()
window.title("SEGY PICKER")
window.geometry("1200x900")

pk = SEGYPicker(window)
window.mainloop()

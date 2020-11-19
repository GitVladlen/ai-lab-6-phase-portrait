import numpy as np
import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

data = open("ЕКГ_КП6_1.txt", "r")
r = []
for line in data:
    r += line.split()

signal = np.array(r, dtype=np.float)

data = open("ЕКГ_КП6_2.txt", "r")
r = []
for line in data:
    r += line.split()
signal2 = np.array(r, dtype=np.float)

signal1 = signal
pause = 1


def plot(plt1, plt2, plt3, ecg_signal, pause_value):
    t = [i * 0.05 for i in range(len(ecg_signal))]
    d = np.gradient(ecg_signal, t)

    y = np.zeros(len(ecg_signal))
    for i in range(pause_value, len(ecg_signal)):
        y[i - pause_value] = ecg_signal[i]

    plt1.clear()
    plt2.clear()
    plt3.clear()

    ax1, = plt1.plot(t, ecg_signal, 'r')
    ax2, = plt2.plot(d, ecg_signal, 'r')
    ax3, = plt3.plot(y, ecg_signal, 'r')

    return ax1, ax2, ax3


root = tkinter.Tk()
root.wm_title("Фазовый портрет сигнала ЕКГ")

fig = Figure(figsize=(10, 6), dpi=100)

fig.subplots_adjust(wspace=0, hspace=0.4)

sub_plot_1 = fig.add_subplot(311)
sub_plot_2 = fig.add_subplot(312)
sub_plot_3 = fig.add_subplot(313)

sub_plot_1.set_title('Original Signal')
sub_plot_2.set_title('Phazes on dz/dt')
sub_plot_3.set_title('Phazez on z(t - pause)')

ecg_plot_1, ecg_plot_2, ecg_plot_3 = plot(
    sub_plot_1, sub_plot_2, sub_plot_3,
    signal1, pause)

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()

canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

var_mode = tkinter.IntVar()
var_mode.set(1)

param_delay = tkinter.IntVar()
param_delay.set(1)

controll_pane = tkinter.PanedWindow(root)
controll_pane.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=1)

label_frame_params = tkinter.LabelFrame(controll_pane, text="Параметры сглаживания")
label_frame_params.pack(pady=5, padx=5, fill=tkinter.BOTH, expand=1)





def reset_plot(*args):
    global signal1
    global pause

    pause = param_delay.get()

    mode = var_mode.get()

    if mode == 1:
        signal1 = signal
    else:
        signal1 = signal2

    global fig
    global sub_plot_1
    global sub_plot_2
    global sub_plot_3
    global ecg_plot_1
    global ecg_plot_2
    global ecg_plot_3
    global canvas

    ecg_plot_1, ecg_plot_2, ecg_plot_3 = plot(
        sub_plot_1, sub_plot_2, sub_plot_3,
        signal1, pause)

    canvas.draw()


def update_plot(*args):
    global ecg_plot_1
    global ecg_plot_2
    global ecg_plot_3

    pause = param_delay.get()

    t = [i * 0.05 for i in range(len(signal1))]
    d = np.gradient(signal1, t)

    y = np.zeros(len(signal1))
    for i in range(pause, len(signal1)):
        y[i - pause] = signal1[i]

    ecg_plot_1.set_xdata(t)
    ecg_plot_2.set_xdata(d)
    ecg_plot_3.set_xdata(y)

    canvas.draw()


tkinter.Radiobutton(label_frame_params,
                    text="File 1",
                    variable=var_mode,
                    value=1,
                    command=reset_plot).pack(anchor=tkinter.W)

tkinter.Radiobutton(label_frame_params,
                    text="File 2",
                    variable=var_mode,
                    value=2,
                    command=reset_plot).pack(anchor=tkinter.W)

scale_pane = tkinter.PanedWindow(label_frame_params)
scale_pane.pack(side=tkinter.LEFT)

tkinter.Scale(scale_pane,
              label="Задержка",
              from_=0,
              to=50,
              orient=tkinter.HORIZONTAL,
              length=300,
              showvalue=1,
              tickinterval=5,
              command=update_plot,
              variable=param_delay).pack()

root.mainloop()
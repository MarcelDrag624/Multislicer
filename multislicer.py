import numpy as np
from matplotlib import pyplot as plt
import soundfile as sf
from scipy.io.wavfile import write
import math

# Zainicjowanie niektórych zmiennych
data_mono = []
x_click = 0
markers = []
starts = []
ends = []
bufor = []
samples_array = []
given_rms_in_db = -15
filtered = []
# counter = 0

# Wczytanie sygnału
data, sps = sf.read("stereo_v2.wav")

# Utworzenie monofonicznego sygnału żeby na wykresie dla każdego x była tylko jedna wartość y
for i in range(0,len(data)):
    bufor = ((data[i][0] + data[i][1])/2)
    data_mono.append(bufor)

# Utworzenie okna i wykresu
fig, ax = plt.subplots()
ax.plot(data_mono)



# This function takes sample-slice and returns it with trimed silence
def filtering_zeros(slice):
    filtering = []
    for i in range(0,len(slice)):
        if bufor[i][0] == 0 and bufor[i][1] == 0:
            filtering.append(False)
        else:
            filtering.append(True)
    filtered = slice[filtering]
    return filtered

def normalize_to_rms(given_rms_in_db, slice):

    input_measured_rms = np.sqrt(np.sum(slice**2)/len(slice))
    input_measured_rms_in_db = 20 * math.log(input_measured_rms,10)

    given_rms_no_unit = 10 ** (given_rms_in_db/20)

    x = np.sqrt(((given_rms_no_unit**2) * len(slice))/np.sum(slice**2))

    scaled_slice = slice * x

    # output_measured_rms = np.sqrt(np.sum(scaled_slice**2)/len(scaled_slice))
    # output_measured_rms_in_db = 20 * math.log(output_measured_rms,10)

    return scaled_slice

    # scaled_slice_int = np.int16(scaled_data * 32767)
    # write("scaled.wav",sps,scaled_data_int)

    # print("RMS value of input signal:",input_measured_rms_in_db)
    # print("RMS value of output signal:",output_measured_rms_in_db)



def NavigCoordin(x,y):
    if x>=0 and x<=len(data_mono):
        return f"x: {int(x+0.5)}, y: {data_mono[int(x+0.5)]:.4f}"
    else:
        return "outside the range"

ax.format_coord = NavigCoordin

# https://stackoverflow.com/questions/71874995/changing-values-displayed-in-top-right-corner-of-plt-diagram?noredirect=1#comment127024319_71874995

# Funkcja, która po zarejestrowaniu kliknięcia lewym przyciskiem myszy tworzy pionową linię w miejscu kliknięcia na wykresie, a po zarejestrowaniu
# kliknięcia prawym przyciskiem myszy usuwa ostatnio utworzoną linię. Każde kliknięcie myszą modyfikuje zawartość listy markers - lpm dodaje do niej nowy element (koordynat x kliknięcia), a ppm usuwa
# ostatni element z listy. Przed dodaniem nowego elementu do listy markers koordynat x kliknięcia jest mnożony razy 2 - wynika to z tego, że na wykresie jest wyświetlany
# sygnał monofoniczy (zawiera on połowę punktów - co drugi punkt - sygnału stereofoniczngo).

def click(event):
    global x_click
    global counter
    x_click = event.xdata
    if event.button == plt.MouseButton.LEFT:
        global line
        line = plt.axvline(event.xdata)
        markers.append(int(round(event.xdata,0)))
    elif event.button == plt.MouseButton.RIGHT:
        plt.gca().lines[-1].remove()
        del markers[-1]

starting_ax_xlim = ax.get_xlim()

def scroll(event, base_scale = 1.5):
    cur_xlim = ax.get_xlim()
    cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
    xdata = event.xdata
    if event.button == 'up':
        # deal with zoom in
        scale_factor = 1/base_scale
    elif event.button == 'down':
        # deal with zoom out
        scale_factor = base_scale
    bufor_left = xdata - cur_xrange*scale_factor
    if bufor_left < starting_ax_xlim[0]:
        bufor_left = starting_ax_xlim[0]
    bufor_right = xdata + cur_xrange*scale_factor
    if bufor_right > starting_ax_xlim[1]:
        bufor_right = starting_ax_xlim[1]
    ax.set_xlim([bufor_left, bufor_right])
# !
# Zrobić tak żeby scroll down działał do pewnego momentu, powyżej którego przywracany jest początkowy xlim
# !

# "Połączenie" kursora z powyższą funkcją.
cid = fig.canvas.mpl_connect('button_press_event', click)
sid = fig.canvas.mpl_connect('scroll_event', scroll)

# Pętla wyświetlająca wykres i odświeżająca go co 0.05 sekundy. Jeśli kliknięcie zostanie zarejestowane powyżej 0.9999 wartości maksymalnej na osi x to pętla jest przerywana.
while True:
    plt.pause(0.05)
    if x_click >= (len(data_mono))*0.9999:
        break

# Przy ostatnim kliknięciu (tym powyżej 0.9999 maksymalnej wartosci na osi x, ktore konczy petle wykresu) nie moze go dodawac do starts ani ends
# Trzeba też dodać zaokrąglanie wartości dodawanych do starts i ends tak żeby były tam tylko wartości całkowite
del markers[-1]
for i in range(0,len(markers)):
    if i%2 == 0:
        starts.append(markers[i])
    else:
        ends.append(markers[i])

for i in range(0,len(starts)):
    bufor = data[starts[i]:ends[i]]
    filtered = filtering_zeros(bufor)
    normalized = normalize_to_rms(given_rms_in_db,filtered)
    normalized_int = np.int16(normalized * 32767)
    write("output"+str(i)+".wav", sps, normalized_int)

# https://stackoverflow.com/questions/11551049/matplotlib-plot-zooming-with-scroll-wheel

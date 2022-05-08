import matplotlib.pyplot as plt
import matplotlib.lines as lines

fig, ax = plt.subplots()
ax.plot()

switch = False
last_click_x_cord = 0
default_xlim = ax.get_xlim()
print(default_xlim)

def dbl_lmb_to_create_rmb_to_delete_line(event):
    global last_click_x_cord
    global make_the_line_follow_mouse_connector
    if event.button == plt.MouseButton.LEFT and event.dblclick == True:
        line = ax.axvline(event.xdata, picker = True, pickradius = 5)
    elif event.button == plt.MouseButton.RIGHT:
        clicked_object_path.remove()
    last_click_x_cord = event.xdata

    make_the_line_follow_mouse_connector = fig.canvas.mpl_connect('motion_notify_event', make_the_line_follow_mouse)


def get_path_to_clicked_object(event):
    global clicked_object_path
    global switch
    clicked_object_path = event.artist
    switch = True
    # print(clicked_object_path)
    return clicked_object_path

def make_the_line_follow_mouse(event):
    global clicked_object_path
    if switch == True:
        clicked_object_path.set_xdata(event.xdata)

def stop_following_mouse_after_button_release(event):
    fig.canvas.mpl_disconnect(make_the_line_follow_mouse_connector)

lmb_to_create_line_connector = fig.canvas.mpl_connect('button_press_event', dbl_lmb_to_create_rmb_to_delete_line)
click_on_line_connector = fig.canvas.mpl_connect('pick_event', get_path_to_clicked_object)
stop_following_mouse_after_button_release_connector = fig.canvas.mpl_connect('button_release_event',stop_following_mouse_after_button_release)

while True:
    plt.pause(0.05)
    if last_click_x_cord > default_xlim[1]*0.9:
        break

list_of_lines = ax.get_lines()

for i in range(0,len(list_of_lines)):
    print(list_of_lines[i].get_xdata())

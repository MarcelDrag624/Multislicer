import matplotlib.pyplot as plt
import matplotlib.lines as lines

fig, ay = plt.subplots()
ay.plot()
path = ay.get_figure().canvas

class draggable_lines:
    def __init__(self, XorY,path):
        # self.ax = ax
        self.c = path
        # self.o = kind
        self.XorY = XorY

        # if kind == "h":
        #     x = [-1, 1]
        #     y = [XorY, XorY]
        #
        # elif kind == "v":
        #     x = [XorY, XorY]
        #     y = [-1, 1]
        self.line = ay.axvline(XorY, picker = True, pickradius = 5)
        # self.ax.add_line(self.line)
        # self.c.draw_idle()
        self.sid = self.c.mpl_connect('pick_event', self.clickonline)

    def clickonline(self, event):
        if event.artist == self.line and event.mouseevent.button == plt.MouseButton.LEFT and event.mouseevent.dblclick != True:
            # print("line selected ", event.artist)
            self.follower = self.c.mpl_connect("motion_notify_event", self.followmouse)
            self.releaser = self.c.mpl_connect("button_press_event", self.releaseonclick)
        elif event.artist == self.line and event.mouseevent.button == plt.MouseButton.RIGHT:
            event.artist.remove()
            self.c.draw_idle()


    def followmouse(self, event):
        # if self.o == "h":
        #     self.line.set_ydata([event.ydata, event.ydata])
        # else:
        self.line.set_xdata([event.xdata, event.xdata])
        self.c.draw_idle()

    def releaseonclick(self, event):
        # if self.o == "h":
        #     self.XorY = self.line.get_ydata()[0]
        # else:
        self.XorY = self.line.get_xdata()[0]

        # print (self.XorY)

        self.c.mpl_disconnect(self.releaser)
        self.c.mpl_disconnect(self.follower)

# fig = plt.figure()
# ax = fig.add_subplot()
# Vline = draggable_lines(ax, 0.5)
Tline = draggable_lines(0.5,path)
Tline2 = draggable_lines(0.1,path)

plt.show()

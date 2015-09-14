# Import for drawing
from Tkinter import *

# Set up for drawing

# Create a canvas to draw on
#aCanvas = Canvas(aTk, width=400, height=400)
#aCanvas.pack()

# Draw several shapes in different colours

def make_oval(aCanvas):
    aCanvas.create_oval(50, 100, 360, 390, fill="blue")
    aCanvas.create_polygon(10, 100, 60, 0, 110, 100, fill="yellow", outline="blue")
    
    
def make_rect(aCanvas, w, h, x, y):
    aCanvas.create_rectangle(h, w, x, y, fill="orange")
    

def finish(aCanvas):
    mainloop()

# Issue: want this to only fire once


def rep():
    for i in range(5):
        aCanvas = Canvas(Tk(), width=400, height=400)
        aCanvas.pack()
        make_oval(aCanvas)
        make_rect(aCanvas, 100, 10, i * 50, i * 30)
        print i
        mainloop()
# Issue: want this to only fire once

#rep()
###################################
import matplotlib.pyplot as plt

def consecutive_ints(curr_num):
    return curr_num + 1

def show(curr_num, stop_num):
    print str(curr_num) + ' is not ' + str(stop_num)
    if curr_num == stop_num:
        plt.show()
    
def make_shapes(curr_num):
    j = curr_num * 0.01
    plt.xticks(())
    plt.yticks(())
    
    circle = plt.Circle((j, j), radius=0.2, fc='y')
    plt.gca().add_patch(circle)
    
    rectangle = plt.Rectangle((j, j), 1, .1, fc='r')
    plt.gca().add_patch(rectangle)
    #points = [[2, 1], [8, 1], [8, 4]]
    points = [[1 * j, 1 * j], [3 * j, 1 * j], [2 * j, 4 * j]]
    polygon = plt.Polygon(points, fill='r')
    plt.gca().add_patch(polygon)
    figure, ax = plt.subplots()
    figure.canvas.draw()

def make_rec():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    rect = ax.patch  # a Rectangle instance
    rect.set_facecolor('green')
    fig.canvas.draw()
    
def run():
    curr_num = 0
    for i in range(4):
        curr_num = consecutive_ints(curr_num)
        #make_shapes(curr_num)
        make_rec()
        #show(curr_num, 5)

run()
'''
import numpy as np
import pylab as pl
n = 1024
X = np.random.normal(0, 1, n)
Y = np.random.normal(0, 1, n)
T = np.arctan2(Y, X)

pl.axes([0.025, 0.025, 0.95, 0.95])
pl.scatter(X, Y, s=100, c=T, alpha=.5)

pl.xlim(-1.5, 1.5)
pl.xticks(())
pl.ylim(-1.5, 1.5)
pl.yticks(())

pl.show()
'''

'''
from pylab import *
import time
    
ion()

tstart = time.time()               # for profiling
x = arange(0,2*pi,0.01)            # x-array
line, = plot(x,sin(x))
for i in arange(1,200):
    line.set_ydata(sin(x+i/10.0))  # update the data
    draw()                         # redraw the canvas
   
print 'FPS:' , 200/(time.time()-tstart)
'''
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FixedLocator, FormatStrFormatter
import matplotlib, time
import random
from math import sqrt
import json
import sys
import math

matplotlib.interactive(True)


class FieldView(object):

    def __init__(self, socceragent):
        # Bind the SoccerAgent
        self.socceragent =socceragent
       
        # Graphical stuff
        self.fig =plt.figure(figsize=(14, 14))
        self.ax =self.fig.add_subplot(111)
	
        # The field
        self.green_x, self.green_y =self.get_green_field()
        
        self.border_green_x, self.border_green_y = self.get_green_border()
       
        # The lines
        self.lines_x =[10 for i in range(6)] + [30 for i in range(6)] + [i for i in range(10,31)]
        self.lines_y =[59 - i for i in range(6)] + [59 -i for i in range(6)] +  [54 for i in range(10,31)]
        
        self.lines_x += [10 for i in range(6)] + [30 for i in range(6)] + [i for i in range(10,31)]
        self.lines_y += [5 - i for i in range(6)] + [5 -i for i in range(6)] +  [5 for i in range(10,31)]
        
        self.lines_x += [i for i in range(40)]
        self.lines_y += [30 for i in range(40)]
        
        self.lines_x += [i for i in range(40)]
        self.lines_y += [29 for i in range(40)]
        
        for i in range(60):
            for j in range(40):
                if i == 0 or i == 59 or j == 0 or j == 39:
                    self.lines_x.append(j)
                    self.lines_y.append(i)
                
        for i in range(0, 181, 5):
            x = int(4*math.cos(2*3.1415296*(i/360.0)))+20
            y = int(5*math.sin(2*3.1415296*(i/360.0)))+29
            self.lines_x.append(x)
            self.lines_y.append(y)
            
        for i in range(180, 361, 5):
            x = int(4*math.cos(2*3.1415296*(i/360.0)))+20
            y = int(5*math.sin(2*3.1415296*(i/360.0)))+30
            self.lines_x.append(x)
            self.lines_y.append(y)
        
       
    def get_green_field(self):
        green_x =[]
        green_y =[]
        for i in range(60):
            for j in range(40):
                green_x.append(j)
                green_y.append(i)
        return (green_x, green_y)
       
    def get_green_border(self):
        green_border_x = []
        green_border_y = []
        for i in [-1, -2, -3, -4, -5, -6, -7] + [40, 41, 42, 43, 44, 45, 46]:
            for j in range(-7, 66):
                green_border_x.append(i)
                green_border_y.append(j)
        for i in range(-7, 47):
            for j in [-1, -2, -3, -4, -5, -6, -7] + [60, 61, 62, 63, 64, 65, 66]:
                green_border_x.append(i)
                green_border_y.append(j)
        return (green_border_x, green_border_y)
        
    def draw_now_and_wait(self, wait=0.1):
        """ The x and y axis are rotated so that the field is horizontal """
        # Clear the current graphics
        self.ax.clear()
        # Set the axis limits
        self.ax.set_xlim([-8,67])
        self.ax.set_ylim([-15,56])
        # Set the markersize
        markersize = 8
        
        # Draw the green underground
        self.ax.plot(self.green_y, self.green_x, "s", markersize=markersize, linestyle="", color="lightgreen")   
        # Draw the green border
        self.ax.plot(self.border_green_y, self.border_green_x, "s", markersize=markersize, linestyle="", color="green")
        # Draw the Goal Area
        self.ax.plot( self.lines_y, self.lines_x,"s", markersize=markersize, linestyle="", color="white")
        # Draw the ball state
        ballx, bally = self.socceragent.ball
        self.ax.plot(bally, ballx, "s", markersize=markersize, linestyle="", color="orange")
        # Draw the agents state
        agentx, agenty =self.socceragent.agent_position
        self.ax.plot(agenty, agentx, "s", markersize=markersize, linestyle="", color="black")
        # Redraw
        plt.draw()  
        #Sleep a little bit
        time.sleep(wait)

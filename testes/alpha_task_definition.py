from math import sqrt, pow, inf
from random import random
from kivy.config import Config
Config.set('graphics', 'minimum_width', 800)
Config.set('graphics', 'minimum_height', 800)
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, InstructionGroup, Line

def euc_dist(p1, p2):
    return sqrt( pow(p1[0]-p2[0],2) + pow(p1[1]-p2[1],2))

def simple_rrt(q0, k, alpha, nearest, step, step_size):
    G = [q0]
    V = []
    for i in range(0,k):
        q_i = alpha(i)
        q_n = nearest(G, q_i)
        q_i = step(q_i, q_n, step_size)        
        G.append(q_i)
        V.append([q_n, q_i])
    return G,V
        
def alpha(i):
    return [800*(random()), 800*(random())]



def step(q_i, q_n, step_size):
    if euc_dist(q_i, q_n) > step_size:
        a = (q_n[1] -q_i[1])/(q_n[0] -q_i[0])
        b = (q_n[0]*q_i[1] - q_n[1]*q_i[0])/(q_n[0] -q_i[0])
        x_3 = (q_n[0]+step_size/sqrt(a*a+1)), (q_n[0]-step_size/sqrt(a*a+1))
        y_3 = a*x_3[0]+b, a*x_3[1]+b
        q_s = euc_dist([x_3[0], y_3[0]], q_n),euc_dist([x_3[1], y_3[1]], q_n)
        return [x_3[0], y_3[0]] if q_s.index(min(q_s)) == 0 else [x_3[1], y_3[1]]
    return q_i

def nearest(G, q_i):
    min_distance = inf
    min_q = None
    for q in G:
        distance = euc_dist(q_i, q)
        if distance < min_distance:
            min_distance = distance
            min_q = q
    return min_q

class DrawRRTWidget(Widget):
    def __init__(self, **kwargs):
        super(DrawRRTWidget, self).__init__(**kwargs)
        g0 = [400,400]
        G,V = simple_rrt(g0, 5000, alpha, nearest, step, 10)
        with self.canvas.before:
            Color(1,0,0,1)
            for v in V:
                points = v[0]+v[1]
                Line(points=points, width=1)
            for g in G:
                Rectangle(pos=g, size=[4,4])
            Color(0,1,0,1)
            Rectangle(pos=g0, size=[4,4])
            


class DrawRRTApp(App):
    def build(self):
        return DrawRRTWidget()

if __name__ == '__main__':
    DrawRRTApp().run()
    
    


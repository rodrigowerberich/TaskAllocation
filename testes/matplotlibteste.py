import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Polygon, Rectangle
from matplotlib.collections import PatchCollection
import numpy as np
from math import sqrt, pow, inf
from random import random
from alpha_figure import alpha_shape

circles = [ [150, 150, 100] , [700, 600, 50], [200, 600, 40], [600,     100, 10]]
rectangles = [ [330, 330, 20, 140] , [350, 450, 120, 20], [450, 270, 20, 180], [350, 330, 40, 20], [270, 270, 180, 20], [270, 290, 20, 240], [290, 510, 240, 20], [510, 220, 20, 290] ]

def euc_dist(p1, p2):
    return sqrt( pow(p1[0]-p2[0],2) + pow(p1[1]-p2[1],2))

def simple_rrt(q0, k, alpha, nearest, step, step_size, connectivity, collision):
    G = [q0]
    V = []
    for i in range(0,k):
        while True:
            q_i = alpha(i)
            q_n = nearest(G, q_i)
            q_i = step(q_i, q_n, step_size)
            v_ni = [q_n, q_i]
            if collision(v_ni) == 0:
                break  
        G.append(q_i)
        V.append(v_ni)
        # if connectivity(q_i) == 1:
        #     return G, V
    return G,V

def simple_rrt_area(q0, area, k, alpha, nearest, step, step_size, connectivity, collision, distance_to_area):
    G = [q0]
    V = []
    distances = distance_to_area(q0, area, collision)
    for i in range(0,k):
        while True:
            if min(distances) is not inf:
                end_q_i = area[distances.index(min(distances))]
                G.append(end_q_i)
                v_ni = [q_i, end_q_i]
                V.append(v_ni)
                return G,V
            else:
                q_i = alpha(i)
                q_n = nearest(G, q_i)
                q_i = step(q_i, q_n, step_size)
                v_ni = [q_n, q_i]
                if collision(v_ni) == 0:
                    distances_q_i = distance_to_area(q_i, area, collision)
                    distances = [ min(dist1, dist2) for dist1,dist2 in zip(distances, distances_q_i) ]
                    break  
        G.append(q_i)
        V.append(v_ni)
    return G,V

def simple_rrt_area2(q0, area, k, alpha, nearest, step, step_size, connectivity, collision, distance_to_area):
    G = [q0]
    V = []
    for i in range(0,k):
        while True:
            if random() < 0.5 or len(area) == 0:
                q_i = alpha(i)
            else:
                q_i = area[round(random()*(len(area)-1))]
            q_n = nearest(G, q_i)
            q_i = step(q_i, q_n, step_size)
            v_ni = [q_n, q_i]
            if collision(v_ni) == 0:
                break
        area = list(filter(lambda x: all(x!=q_i), area))
        G.append(q_i)
        V.append(v_ni)
    return G,V

def simple_rrt_collision_area2(q0, area, k, alpha, nearest, step, step_size, connectivity, collision, distance_to_area):
    G = [q0]
    V = []
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    patches = []
    for circle in circles:
        patches.append(Circle((circle[0], circle[1]), circle[2]))
    for rectangle in rectangles:
        patches.append(Rectangle([rectangle[0],rectangle[1]],rectangle[2], rectangle[3]))
    p = PatchCollection(patches, alpha=0.4)
    ax.add_collection(p)
    qn_plot, = ax.plot(*q0, 'xr')
    qi_plot, = ax.plot(*q0, 'xb')
    qin_plot, = ax.plot(*q0, 'xg')
    ax.axis([0, 800, 0, 800])
    for i in range(0,k):
        if random() < 2 or len(area) == 0:
            q_i = alpha(i)
        else:
            q_i = area[round(random()*(len(area)-1))]
        qi_plot.set_xdata(q_i[0])
        qi_plot.set_ydata(q_i[1])
        q_n = nearest(G, q_i)
        qn_plot.set_xdata(q_n[0])
        qn_plot.set_ydata(q_n[1])
        q_i = step(q_i, q_n, step_size)
        q_i = collision([q_n, q_i]) 
        qin_plot.set_xdata(q_i[0])
        qin_plot.set_ydata(q_i[1])
        v_ni = [q_n, q_i]
        area = list(filter(lambda x: all(x!=q_i), area))
        G.append(q_i)
        V.append(v_ni)
        plt.waitforbuttonpress()
    return G,V

def simple_find_nearest(q_o, k, alpha, connectivity):
    G = []
    min_cost = inf
    min_q = None
    for i in range(0,k):
        q_i = alpha(i)
        cost = euc_dist(q_o, q_i)
        if cost < min_cost:
            min_cost = cost
            min_q = q_i
        G.append(q_i)
    return G, min_q

def simple_rrt_iterative(q0, k, alpha, nearest, step, step_size, connectivity, collision):
    G = [q0]
    V = []
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    patches = []
    for circle in circles:
        patches.append(Circle((circle[0], circle[1]), circle[2]))
    for rectangle in rectangles:
        patches.append(Rectangle([rectangle[0],rectangle[1]],rectangle[2], rectangle[3]))
    p = PatchCollection(patches, alpha=0.4)
    ax.add_collection(p)
    ax.plot(*q0, marker='x', linestyle = 'None', color='blue')
    current, = ax.plot(*q0, marker='x', linestyle = 'None', color='red')
    temp, = ax.plot(0,0)
    ax.axis([0, 800, 0, 800])
    plt.waitforbuttonpress()
    for i in range(0,k):
        while True:
            q_i = alpha(i)
            q_n = nearest(G, q_i)
            temp_v_ni = [q_n, q_i]
            temp_v = np.array(temp_v_ni)
            temp_v = temp_v.transpose()
            temp.set_xdata(temp_v[0])
            temp.set_ydata(temp_v[1])
            q_i = step(q_i, q_n, step_size)
            v_ni = [q_n, q_i]
            if collision(v_ni) == 0:
                break
        G.append(q_i)
        V.append(v_ni)
        ax.plot(*q_i, marker='.',linestyle = 'None', color='green')
        current.set_xdata(q_i[0])
        current.set_ydata(q_i[1])
        v = np.array(v_ni)
        v = v.transpose()
        plt.plot(*v, color='green')
        fig.canvas.draw()
        # plt.waitforbuttonpress()
    plt.waitforbuttonpress()
    return G,V

def rrt_star_iterative(q0, k, alpha, nearest, step, step_size, connectivity, collision, near, choose_parent, rewire):
    q0.append(0)
    G = [q0]
    V = []
    # plt.ion()
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # patches = []
    # for circle in circles:
    #     patches.append(Circle((circle[0], circle[1]), circle[2]))
    # for rectangle in rectangles:
    #     patches.append(Rectangle([rectangle[0],rectangle[1]],rectangle[2], rectangle[3]))
    # p = PatchCollection(patches, alpha=0.4)
    # ax.add_collection(p)
    # ax.plot(*q0, marker='x', linestyle = 'None', color='blue')
    # ax.axis([0, 800, 0, 800])
    # plt.waitforbuttonpress()
    for i in range(0,k):
        while True:
            q_i = alpha(i)
            q_n = nearest(G, q_i)
            q_i = step(q_i, q_n, step_size)
            v_ni = [q_n, q_i]
            if collision(v_ni) == 0:
                break
        qs_near = near(G, q_i, len(G))
        q_min = choose_parent(qs_near, q_n, q_i)
        G.append(q_i)
        v_mini = [q_min, q_i]
        V.append(v_mini)
        G,V = rewire(G, V, qs_near, q_min, q_i)
    # plt.waitforbuttonpress()
    return G,V

def alpha(i):
    return [800*(random()), 800*(random())]

def alpha_connectivity(i):
    p = [800*(random()), 800*(random())]
    while connectivity(p) < 0.5:
        p= [800*(random()), 800*(random())]
    return p

# def alpha(i):
#     p = [800*(random()), 800*(random())]
#     directed = random()
#     if directed > 0.1:
#         while connectivity(p) < 0.5:
#             p= [800*(random()), 800*(random())]
#     return p

def connectivity(q):
    connected = [ euc_dist((circle[0], circle[1]), q) < circle[2] for circle in circles ]
    if any(connected):
        return 1
    else:
        return 0

def collision(q):
    collided = [ (r[0]< q[0] <r[0]+r[2]) and (r[1]< q[1] <r[1]+r[3])  for r in rectangles ]
    if any(collided):
        return 1
    else:
        return 0

def collision_vertex(v):
    a = np.array(v[0][0:2])
    b = np.array(v[1][0:2])
    c = b-a
    for alpha in range(0,100,1):
        d = a + alpha*(c)/100
        if collision(d) == 1:
            return 1
    return 0

def collision_vertex_point(v):
    a = np.array(v[0][0:2])
    b = np.array(v[1][0:2])
    c = b-a
    size = np.linalg.norm(c)
    step = 2
    end = int(np.floor(size/step))
    for alpha in range(0, end,1):
        d = a + alpha*(c)/size
        if collision(d) == 1:
            return a + max([alpha-10,0])*(c)/size
    return b

def step(q_i, q_n, step_size):
    if euc_dist(q_i, q_n) > step_size:
        a = (q_n[1] -q_i[1])/(q_n[0] -q_i[0])
        b = (q_n[0]*q_i[1] - q_n[1]*q_i[0])/(q_n[0] -q_i[0])
        x_3 = (q_n[0]+step_size/sqrt(a*a+1)), (q_n[0]-step_size/sqrt(a*a+1))
        y_3 = a*x_3[0]+b, a*x_3[1]+b
        q_s = euc_dist([x_3[0], y_3[0]], q_i),euc_dist([x_3[1], y_3[1]], q_i)
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

def near(G, q_i, n):
    gamma = 200
    k = gamma*np.sqrt((np.log(n)/n))
    qs_near = []
    for q in G:
        if euc_dist(q, q_i) < k:
            qs_near.append(q)
    return qs_near

def choose_parent(qs_near, q_n, q_i):
    min_cost = inf
    min_q = None
    for q_near in qs_near:
        cost = q_near[2]+euc_dist(q_near, q_i)
        if cost < min_cost:
            min_cost = cost
            min_q = q_near
    cost = q_n[2]+euc_dist(q_n, q_i)
    (min_q, min_cost) = (min_q,min_cost) if min_cost < cost else (q_n, cost)
    if len(q_i) < 3:
        if type(q_i) is np.ndarray:
            np.append(q_i, min_cost)
        else:
            q_i.append(min_cost)
    else:
        q_i[2] = min_cost
    return min_q

def rewire(G, V, qs_near, q_min, q_i):
    for q_near in qs_near:
        cost = q_i[2]+euc_dist(q_i, q_near)
        if cost < q_near[2]:
            for v in V:
                if v[1] == q_near:
                    q_near[2] = cost
                    v[0] = q_i
    return G,V

def shape_distance_to_point(point, shape, collision_vertex):
    return [ euc_dist(point, shape_point) if not collision_vertex([shape_point, point]) else inf  for shape_point in shape]

if __name__ == "__main__":
    g0 = [400,400]
    # G,V = simple_rrt_iterative(g0, 1000, alpha, nearest, step, 50, connectivity, collision_vertex)
    # G,V = rrt_nearest_edge_iterative(g0, 10, alpha, nearest_edge, step, inf, connectivity)
    # G,V = rrt_star_iterative(g0, 1000, alpha, nearest, step, inf, connectivity, collision_vertex, near, choose_parent, rewire)
    # G = [ g[0:2] for g in G]
    fig, ax = plt.subplots()
    # G,V = simple_rrt(g0, 10000, alpha, nearest, step, inf, connectivity, collision_vertex)
    G, q_min = simple_find_nearest(g0, 5000, alpha_connectivity, connectivity)
    G = np.array(G)
    G = G.transpose()
    plt.plot(400, 400, 'xb')
    plt.plot(*G, marker='x',linestyle = 'None', color='green')
    
    points = np.vstack(G).T
    print(points.shape)
    edges = alpha_shape(points, alpha=20, only_outer=True)
    print(len(edges))
    edges_points = []
    for i, j in edges:
        if all([any(point != points[i]) for point in edges_points]):
            edges_points.append(points[i])
        if all([any(point == points[j]) for point in edges_points]):
            edges_points.append(points[j])
        plt.plot(points[[i, j], 0], points[[i, j], 1], marker='o',color='black')
    plt.plot(*q_min, marker='*',linestyle = 'None', color='red')
    G1,V1 = simple_rrt_area2(g0, edges_points, 2000, alpha, nearest, step, inf, connectivity, collision_vertex, shape_distance_to_point)
    # G1,V1 = simple_rrt_collision_area2(g0, edges_points, 1000, alpha, nearest, step, inf, connectivity, collision_vertex_point, shape_distance_to_point)
    print(len(G1))
    for v in V1:
        # v = [ g[0:2] for g in v]
        v = np.array(v)
        v = v.transpose()
        plt.plot(*v, color='purple')


    
    patches = []
    for circle in circles:
        patches.append(Circle((circle[0], circle[1]), circle[2]))
    for rectangle in rectangles:
        patches.append(Rectangle([rectangle[0],rectangle[1]],rectangle[2], rectangle[3]))

    p = PatchCollection(patches, alpha=0.4)
    ax.add_collection(p)
    plt.axis([0, 800, 0, 800])
    plt.show()
    

    # x = np.linspace(0, 2, 100)

    # plt.plot(x, x, label='linear')
    # plt.plot(x, x**2, label='quadratic')
    # plt.plot(x, x**3, label='cubic')

    # plt.xlabel('x label')
    # plt.ylabel('y label')

    # plt.title("Simple Plot")

    # plt.legend()

    # plt.show()
    
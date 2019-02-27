import numpy as np
import matplotlib.pyplot as plt
from random import random
from binary_tree import *
from math import sqrt
from matplotlib.patches import Circle, Wedge, Polygon, Rectangle
from matplotlib.collections import PatchCollection

circles = [ [150, 150, 100] , [700, 600, 50], [200, 600, 40], [600,     100, 10]]
rectangles = [ [330, 330, 20, 140] , [350, 450, 120, 20], [450, 270, 20, 180], [350, 330, 40, 20], [270, 270, 180, 20], [270, 290, 20, 240], [290, 510, 240, 20], [510, 220, 20, 290] ]


def build_roadmad(G, N, alpha, collides, neighborhood, connect):
    # G.init()
    i = 0
    while i < N:
        new_vertex = alpha(i)
        if not collides(new_vertex):
            if not G.near(new_vertex, 5):
                G.add_vertex(new_vertex)
                i += 1

            # for q in neighborhood(new_vertex, G):
            #     if (not G.same_component(q, new_vertex)) and connect([q, new_vertex]):
            #         G.add_edge([new_vertex, q])

                  
class Roadmap:
    def init(self):
        self._edges = []
        self._vertex = []
        self._components = {}

    def add_vertex(self, vertex):
        self._vertex.append(vertex)
        key = 0
        while key in self._components:
            key += 1
        self._components[key] = [vertex]

    def _merge_components(self, component1, component2):
        smaller_component, larger_component = (component1,component2) if len(self._components[component1]) < len(self._components[component2]) else (component2,component1)
        for vertex in self._components[smaller_component]:
            self._components[larger_component].append(vertex)
        del self._components[smaller_component]

    def add_edge(self, edge):
        parent = edge[0]
        child = edge[1]
        parent_component = -1
        child_component = -1
        for key in self._components:
            if any([(parent == vertex) for vertex in self._components[key]]):
                parent_component = key
            if any([(vertex == child) for vertex in self._components[key]]):
                child_component = key
        if parent_component == -1 or child_component == -1:
            return
        if parent_component != child_component:
            self._merge_components(parent_component, child_component)
        self._edges.append(edge)

    def same_component(self, q_1, q_2):
        q_1_component = -1
        q_2_component = -1
        for key in self._components:
            if any([(q_1 == vertex) for vertex in self._components[key]]):
                q_1_component = key
            if any([(vertex == q_2) for vertex in self._components[key]]):
                q_2_component = key
        if q_1_component == -1 or q_2_component == -1 or q_1_component != q_2_component:
            return False
        return True

    def near(self, q, r):
        for v in self._vertex:
            if euc_dist(q, v) < r:
                return True
        return False

def euc_dist_squared(p1, p2):
    return pow(p1[0]-p2[0],2) + pow(p1[1]-p2[1],2)

def euc_dist(p1, p2):
    return sqrt(euc_dist_squared(p1, p2))

def alpha(i):
    return [800*(random()), 800*(random())]

def collision(q):
    collided1 = [ (r[0]< q[0] <r[0]+r[2]) and (r[1]< q[1] <r[1]+r[3]) for r in rectangles ]
    if any(collided1):
        return 1
    else:
        return 0

def collision2(q):
    collided1 = [ (r[0]< q[0] <r[0]+r[2]) and (r[1]< q[1] <r[1]+r[3]) for r in rectangles ]
    collided2 = [ euc_dist(c,q) < c[2] for c in circles ]
    if any(collided1) or any(collided2):
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

def connect(v):
    a = np.array(v[0][0:2])
    b = np.array(v[1][0:2])
    c = b-a
    for alpha in range(0,100,1):
        d = a + alpha*(c)/100
        if collision(d) == 1:
            return 0
    return 1

def neighborhood_k(new_vertex, G, K):
    root = None
    for q in G._vertex:
        node_data = NodeData(euc_dist(new_vertex, q), q)
        if root is not None:
            root.insert(node_data)
        else:
            root = Node(node_data)
    neighborhood_vertex = []
    root.SortedUntil(K, neighborhood_vertex)
    neighborhood_vertex = list(map(lambda x: x.data, neighborhood_vertex))
    return neighborhood_vertex

def neighborhood(new_vertex, G):
    return neighborhood_k(new_vertex, G, 100)

if __name__ == "__main__":
    G = Roadmap()
    G.init()

    # plt.ion()
    fig, ax = plt.subplots()
    patches = []
    for circle in circles:
        patches.append(Circle((circle[0], circle[1]), circle[2]))
    for rectangle in rectangles:
        patches.append(Rectangle([rectangle[0],rectangle[1]],rectangle[2], rectangle[3]))

    p = PatchCollection(patches, alpha=0.4)
    ax.add_collection(p)
    plt.axis([0, 800, 0, 800])
    
    # build_roadmad(G, 100, alpha, collision2, neighborhood, connect)
    # # from matplotlibteste import simple_find_nearest, alpha_connectivity, connectivity, alpha_shape
    # # G1, q_min = simple_find_nearest([400, 400], 5000, alpha_connectivity, connectivity)
    # # points1 = np.vstack(G1)
    # # print(points1.shape)
    # # edges1 = alpha_shape(points1, alpha=50, only_outer=True)
    # # print(len(edges1))
    # # edges_points1 = []
    # # for i, j in edges1:
    # #     if all([any(point != points1[i]) for point in edges_points1]):
    # #         edges_points1.append(points1[i])
    # #     if all([any(point == points1[j]) for point in edges_points1]):
    # #         edges_points1.append(points1[j])
    # #     # plt.plot(points[[i, j], 0], points[[i, j], 1], marker='o',color='black')
    # # for q in edges_points1:
    # #     G.add_vertex(q)
    # for v in G._vertex:
    #     ax.plot(*v, 'xb')
    # p_plot, = ax.plot([],'og')
    # n_plot, = ax.plot([], 'xr')
    # plt.waitforbuttonpress()

    # for v in G._vertex:
    #     # print(v)
    #     n = neighborhood(v, G)
    #     nt = np.array(n).T
    #     n = nt.T

    #     # print(n)
    #     n_plot.set_xdata(nt[0])
    #     n_plot.set_ydata(nt[1])
    #     p_plot.set_xdata(v[0])
    #     p_plot.set_ydata(v[1])
    #     from scipy.spatial import Delaunay
    #     tri = Delaunay(n)
    #     ax.triplot(n[:,0], n[:,1], tri.simplices.copy())
    #     # print(np.append(n[0],v[0]))
    #     # print(np.append(n[1],v[1]))
    #     plt.waitforbuttonpress()
    # plt.waitforbuttonpress()

    # plt.show()


    for i in range(0,1):
        build_roadmad(G, 5000, alpha, collision2, neighborhood, connect)
        from matplotlibteste import simple_find_nearest, alpha_connectivity, connectivity, alpha_shape
        G1, q_min = simple_find_nearest([400, 400], 5000, alpha_connectivity, connectivity)
        points1 = np.vstack(G1)
        print(points1.shape)
        edges1 = alpha_shape(points1, alpha=20, only_outer=True)
        print(len(edges1))
        edges_points1 = []
        for i, j in edges1:
            if all([any(point != points1[i]) for point in edges_points1]):
                edges_points1.append(points1[i])
            if all([any(point == points1[j]) for point in edges_points1]):
                edges_points1.append(points1[j])
            # plt.plot(points[[i, j], 0], points[[i, j], 1], marker='o',color='black')
        for q in edges_points1:
            G.add_vertex(q)
        points2 = np.vstack(G._vertex)
        edges2 = alpha_shape(points2, alpha=15, only_outer=False)
        for i, j in edges2:
            plt.plot(points2[[i, j], 0], points2[[i, j], 1], marker='o',color='black')
        # from scipy.spatial import Delaunay
        # points = np.array(G._vertex)
        # tri = Delaunay(points)
        # edges = []
        # for z in tri.simplices:
        #     pa = points[z[0]]
        #     pb = points[z[1]]
        #     pc = points[z[2]]
        #     if not collision_vertex([pa, pb]):
        #         edges.append([pa, pb])
        #     if not collision_vertex([pb, pc]):
        #         edges.append([pb, pc])                
        #     if not collision_vertex([pa, pc]):
        #         edges.append([pa, pc])                                
        # ax.triplot(points[:,0], points[:,1], tri.simplices.copy())
        for v in G._vertex:
            ax.plot(*v, 'xb')
        # for e in G._edges:
        # for e in edges:
        #     e = np.array(e)
        #     e = e.transpose()
        #     ax.plot(*e, '-r')
        
        # plt.waitforbuttonpress()
        plt.show()
        print(len(G._vertex))
        print(len(G._edges))
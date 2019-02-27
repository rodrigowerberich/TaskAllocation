import numpy as np
import matplotlib.pyplot as plt
from trig_helper import triangles_do_intersect_loose, plot_triangle, plot_polygon
from roadmaptest import alpha, Roadmap, euc_dist, euc_dist_squared
from binary_tree import NodeData, Node

def alpha_decoy(i):
    sequence = [[625.3117296628634, 397.5866829292523], [719.7681734022096, 519.1813590719745], [55.98410250461478, 83.1323024134818], [199.23067410483935, 46.34814091572306], [492.03963094135963, 435.99376393814566], [351.9090716743537, 112.46009151240806], [190.3279313707424, 461.34502351982576], [571.3970537616036, 107.48071642550076], [62.85084038970021, 583.247299131051], [205.0501768934689, 277.42796861911677], [282.18919372198366, 184.09194762559852], [491.7732568218363, 700.7157264432637], [472.3188465397268, 634.441647521053], [716.1247894553006, 241.92373061821922], [225.16377667216528, 637.4250454238121], [285.39314725416995, 703.201830363712], [487.16477079805696, 576.0846351203671], [52.32007880610743, 231.760058147949], [154.78533042377495, 605.0089473387663], [162.755898751118, 394.8591079086651], [624.1311039066165, 86.113577301367], [597.9931076895245, 302.41739789961775], [548.459076751483, 108.30421936566958], [203.92533045584383, 367.25821334681956], [447.37450976422497, 601.0300797069748], [560.6386780648156, 135.79990016364204], [553.0632358322638, 148.47596545529552], [389.7863717302262, 350.47364970250123], [632.3253171588242, 666.3564192231237], [396.20812559625324, 629.2699408667178]]
    return sequence[i]

def neighborhood_k(index, points, K):
    root = None
    for q,i in zip(G._vertex, range(len(G._vertex))):
        node_data = NodeData(euc_dist(points[index], q), i)
        if root is not None:
            root.insert(node_data)
        else:
            root = Node(node_data)
    neighborhood_vertex = []
    root.SortedUntil(K, neighborhood_vertex)
    neighborhood_vertex = list(map(lambda x: x.data, neighborhood_vertex))
    return neighborhood_vertex

def on_semi_plan_opposed(r1, r2, po, p):
    a = (r2[1]-r1[1])/(r2[0]-r1[0])
    b = r1[1] - a*r1[0]
    if a*po[0]+b < po[1] and a*p[0]+b > p[1]:
        return True
    if a*po[0]+b > po[1] and a*p[0]+b < p[1]:
        return True
    return False


def get_oposition_points_by_distance(edge_indexes, alone_vertex_index, points):
    root = None
    edge = points[(edge_indexes)]
    alone_vertex = points[alone_vertex_index]
    k = 0
    for (point_index, point) in zip(range(len(points)),points):
        if point_index not in edge_indexes and on_semi_plan_opposed(*edge, alone_vertex, point):
            node_data = NodeData(distance_to_segment2(*edge, point), point_index)
            # node_data = NodeData(distance_to_segment(*edge, point), point_index)
            k += 1
            if root is not None:
                root.insert(node_data)
            else:
                root = Node(node_data)
    neighborhood_vertex = []
    if root:
        root.SortedUntil(k, neighborhood_vertex)
        neighborhood_vertex = list(map(lambda x: x.data, neighborhood_vertex))
    return neighborhood_vertex

def get_triangles_to_look(edge_indexes, alone_vertex_index, triangles, points):
    triangles_to_look = []
    edge = points[(edge_indexes)]
    alone_vertex = points[alone_vertex_index]
    for triangle in triangles:
        for point_index in triangle:
            if on_semi_plan_opposed(*edge, alone_vertex, points[point_index]):
                triangles_to_look.append(triangle)
                break
    return triangles_to_look


def distance_to_segment2(v, w, p):
    return euc_dist_squared(v,p)+euc_dist_squared(w,p)

def distance_to_segment(v, w, p):
    l2 = np.dot(w-v,w-v)  # i.e. |w-v|^2 -  avoid a sqrt
    if (l2 == 0.0):
        return euc_dist(p, v)   # v == w case
    # Consider the line extending the segment, parameterized as v + t (w - v).
    # We find projection of point p onto the line.
    # It falls where t = [(p-v) . (w-v)] / |w-v|^2
    # We clamp t from [0,1] to handle points outside the segment vw.
    t = max(0, min(1, np.dot(p - v, w - v) / l2))
    projection = v + t * (w - v)  # Projection falls on the segment
    return euc_dist(p, projection)

def check_triangle_intersection(triangle_to_check, triangles, points):
    for triangle in triangles:
        if triangles_do_intersect_loose(*points[triangle_to_check], *points[triangle]):
            return True
    return False

def order_indexes(i1, i2, i3):
    if i1 > i2:
        if i2 > i3:
            return (i3, i2, i1)
        elif i1 > i3:
            return (i2, i3, i1)
        else:
            return (i2, i1, i3)
    elif i2 > i3:
        if i1 > i3:
            return (i3, i1, i2)
        else:
            return (i1, i3, i2)
    else:
        return (i1, i2, i3)

def connect_graph(G):
    points = np.array(G._vertex)
    initial_point = 0
    initial_triangle = order_indexes(*neighborhood_k(initial_point, points, 3))
    plot_triangle(plt,*points[np.array(initial_triangle)])
    triangles = np.array([ initial_triangle ])
    triangles_visited = None
    while len(triangles) > 0:
        edges = np.array( triangles[0,((0,1),(0,2), (1,2))])
        edge_oposing_points = triangles[0, (2,1,0)]
        for edge,edge_oposing_point in zip(edges, edge_oposing_points):
            candidate_points = get_oposition_points_by_distance(edge, edge_oposing_point, points)
            for candidate_point in candidate_points:
                new_triangle = np.array(order_indexes(*[*edge, candidate_point]))
                can_add = not check_triangle_intersection(new_triangle, triangles, points)
                if triangles_visited is not None:
                    can_add = can_add and not check_triangle_intersection(new_triangle, triangles_visited, points)
                if can_add:
                    plot_triangle(plt,*points[new_triangle])
                    triangles = np.vstack((triangles, new_triangle))
                    break
        if triangles_visited is not None:
            triangles_visited = np.vstack((triangles_visited, triangles[0]))
        else:
            triangles_visited = np.array([triangles[0]])
        triangles = triangles[1:]

def connect_graph2(G):
    points = np.array(G._vertex)
    initial_point = 0
    initial_triangle = order_indexes(*neighborhood_k(initial_point, points, 3))
    # plot_triangle(plt,*points[np.array(initial_triangle)])
    triangles = np.array([ initial_triangle ])
    i = 0
    while i < len(triangles):
        edges = np.array( triangles[i,((0,1),(0,2), (1,2))])
        edge_oposing_points = triangles[i, (2,1,0)]
        for edge,edge_oposing_point in zip(edges, edge_oposing_points):
            candidate_points = get_oposition_points_by_distance(edge, edge_oposing_point, points)
            for candidate_point in candidate_points:
                new_triangle = np.array(order_indexes(*[*edge, candidate_point]))
                if not check_triangle_intersection(new_triangle, triangles, points):
                    # plot_triangle(plt,*points[new_triangle])
                    triangles = np.vstack((triangles, new_triangle))
                    break       
        i+=1

def edge_in_more_than_one_triangle(edge, triangles):
    outer_counter = 0
    for triangle in triangles:
        inner_counter = 0
        for point in triangle:
            if point == edge[0] or point == edge[1]:
                inner_counter += 1
                if inner_counter > 1:
                    outer_counter += 1
                    if outer_counter > 1:
                        return True
                    break
    return False

times0 = []
times1 = []
times11 = []
times2 = []
times3 = []
times4 = []
times5 = []

def connect_graph3(G):
    points = np.array(G._vertex)
    initial_point = 0
    initial_triangle = order_indexes(*neighborhood_k(initial_point, points, 3))
    # plot_triangle(plt,*points[np.array(initial_triangle)])
    triangles = np.array([ initial_triangle ])
    i = 0
    # candidate_triangle_plot, = plt.plot(0,0,color='red')
    # current_triangle_plot, = plt.plot(0,0,color='blue', marker='o')
    while i < len(triangles):
        time0 = timing.time()
        edges = np.array( triangles[i,((0,1),(0,2), (1,2))])
        edge_oposing_points = triangles[i, (2,1,0)]
        # current_triangle_draw = points[triangles[i][[0,1,2,0]]].T
        # current_triangle_plot.set_xdata(current_triangle_draw[0])
        # current_triangle_plot.set_ydata(current_triangle_draw[1])
        for edge,edge_oposing_point in zip(edges, edge_oposing_points):
            if not edge_in_more_than_one_triangle(edge, triangles):
                # print('Edge in more than one triangle? No')
                time1 = timing.time()
                candidate_points = get_oposition_points_by_distance(edge, edge_oposing_point, points)
                times1.append(timing.time()-time1)
                # timing.log('Candidate points search', timing.time()-time1)
                time11 = timing.time()
                triangles_to_look = get_triangles_to_look(edge, edge_oposing_point, triangles, points)
                times11.append(timing.time()-time11)
                # timing.log('Filtering triangles to look', timing.time()-time11)                
                time2 = timing.time()
                for candidate_point in candidate_points:
                    time3 = timing.time()
                    new_triangle = np.array(order_indexes(*[*edge, candidate_point]))
                    times3.append(timing.time()-time3)
                    # timing.log('Get new triangle', timing.time()-time3)
                    
                    # new_triangle_draw = points[new_triangle[[0,1,2,0]]].T
                    # candidate_triangle_plot.set_xdata(new_triangle_draw[0])
                    # candidate_triangle_plot.set_ydata(new_triangle_draw[1])
                    # plt.waitforbuttonpress()
                    time4 = timing.time()
                    value = not check_triangle_intersection(new_triangle, triangles_to_look, points)
                    times4.append(timing.time()-time4)
                    # timing.log('Check triangle intersection', timing.time()-time4)
                    if value:
                        # plot_triangle(plt,*points[new_triangle])
                        # plt.waitforbuttonpress()
                        time5 = timing.time()
                        triangles = np.vstack((triangles, new_triangle))
                        times5.append(timing.time()-time5)
                        # timing.log('Stacking triangles', timing.time()-time5)
                        break
                times2.append(timing.time()-time2)
                # timing.log('Candidate points investigation '+str(len(candidate_points)), timing.time()-time2)                
            # else:
            #     print('Edge in more than one triangle? Yes')
        times0.append(timing.time()-time0)
        # timing.log('While loop', timing.time()-time0)
        i+=1
        # candidate_triangle_plot.set_xdata(0)
        # candidate_triangle_plot.set_ydata(0)

if __name__ == "__main__":
    import timing
    G = Roadmap()
    G.init()
    for i in range(50):
        # G.add_vertex(alpha_decoy(i))
        v_candidate = alpha(i)
        while G.near(v_candidate, 100):
            v_candidate = alpha(i)
        G.add_vertex(v_candidate)
    print(G._vertex)
    # plt.ion()
    # fig, ax = plt.subplots()
    # plt.axis([0, 800, 0, 800])
    # print(G._vertex[3])
    # print(G._vertex[9])
    # print(G._vertex[23])
    # for g in G._vertex:
    #     ax.plot(*g, 'xk')
    from timeit import default_timer as timer
    from timeit import gc
    total = list()
    iterations = 10
    # for i in range(iterations):
    #     start = timer()
    #     gc.enable()
    #     connect_graph2(G)
    #     end = timer()
    #     total.append((end - start))
    # print('connect graph: ',np.mean(total), np.std(total))
    # total = list()
    for i in range(iterations):
    #     start = timer()
    #     gc.enable()
        timing.log('Connect graph started')
        time = timing.time()
        connect_graph3(G)
        timing.log('Connect graph ended', timing.time()-time)
    # plt.plot(times0)
    # plt.plot(times1)
    # plt.plot(times11)
    # plt.plot(times2)
    # plt.plot(times3)
    # plt.plot(times4)
    # plt.plot(times5)
    print('complete while loop ocurred ', len(times0), ' with mean ',  np.mean(times0),   ' total cost ', len(times0)*np.mean(times0))
    print('get_oposition_points_by_distance ocurred ', len(times1), ' with mean ',  np.mean(times1),   ' total cost ', len(times1)*np.mean(times1))
    print('get_triangles_to_look ocurred ', len(times11), ' with mean ', np.mean(times11), ' total cost ', len(times11)*np.mean(times11))
    print('for candidate loop ocurred ', len(times2), ' with mean ',  np.mean(times2),   ' total cost ', len(times2)*np.mean(times2))
    print('create new_triangle ocurred ', len(times3), ' with mean ',  np.mean(times3),   ' total cost ', len(times3)*np.mean(times3))
    print('check_triangle_intersection ocurred ', len(times4), ' with mean ',  np.mean(times4),   ' total cost ', len(times4)*np.mean(times4))
    print('np.vstack ocurred ', len(times5), ' with mean ',  np.mean(times5),   ' total cost ', len(times5)*np.mean(times5))
    #     end = timer()
    #     total.append((end - start))
    # print('connect graph 3: ',np.mean(total), np.std(total))
    
    # plt.ioff()
    # plt.show()
    

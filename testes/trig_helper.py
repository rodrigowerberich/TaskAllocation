import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

def plot_polygon(ax ,polygon):
    ax.plot(*np.array(polygon).T, marker='x')

def plot_triangle(ax, a, b, c):
    plot_polygon(ax, [a, b, c, a])

def colinear_on_segment(p1, p, p2):
    if (p[0] <= max(p1[0], p2[0]) and p[0] >= min(p1[0], p2[0]) and 
        p[1] <= max(p1[1], p2[1]) and p[1] >= min(p1[1], p2[1])):
       return True 
    return False

def triangle_area(a, b, c):
    v1 = b-a
    v2 = c-a
    return np.abs(np.cross(v1,v2)/2)

def points_orientation(p1, p2, p3):
    val = (p2[1] - p1[1]) * (p3[0] - p2[0]) - (p2[0] - p1[0]) * (p3[1] - p2[1])
  
    if val == 0:
        return 0 
  
    return  1 if val > 0 else 2 

def segments_do_intersect(p1, q1, p2, q2): 
    o1 = points_orientation(p1, q1, p2)
    o2 = points_orientation(p1, q1, q2) 
    o3 = points_orientation(p2, q2, p1) 
    o4 = points_orientation(p2, q2, q1) 
  
    # general case
    if (o1 != o2 and o3 != o4):
        return True
  
    # p1, q1 and p2 are colinear and p2 lies on segment p1q1 
    if (o1 == 0 and colinear_on_segment(p1, p2, q1)):
        return True
  
    # p1, q1 and q2 are colinear and q2 lies on segment p1q1 
    if (o2 == 0 and colinear_on_segment(p1, q2, q1)):
        return True
  
    # p2, q2 and p1 are colinear and p1 lies on segment p2q2 
    if (o3 == 0 and colinear_on_segment(p2, p1, q2)):
        return True 
  
    # p2, q2 and q1 are colinear and q1 lies on segment p2q2 
    if (o4 == 0 and colinear_on_segment(p2, q1, q2)):
        return True 
  
    return False # Doesn't fall in any of the above cases 

def point_inside_triangle(a, b, c, p):
    total_area = triangle_area(a, b, c)
    p1_area = triangle_area(a, b, p)
    p2_area = triangle_area(a, p, c)
    p3_area = triangle_area(p, b, c)
    if np.abs(total_area - (p1_area+p2_area+p3_area)) < 0.000001:
        return True
    return False

def triangles_do_intersect(a1, b1, c1, a2, b2, c2):
    segments_to_verify = [ [ a1, b1, a2, b2],
                            [a1, b1, a2, c2],
                            [a1, b1, b2, c2],
                            [a1, c1, a2, b2],
                            [a1, c1, a2, c2],
                            [a1, c1, b2, c2],
                            [b1, c1, a2, b2],
                            [b1, c1, a2, c2],
                            [b1, c1, b2, c2] ]
    for segments in segments_to_verify:
        if segments_do_intersect(*segments):
            return True

    for triangle_point in [a1, b1, c1]:
        if point_inside_triangle(a2,b2,c2, triangle_point):
            return True
        
    for triangle_point in [a2, b2, c2]:
        if point_inside_triangle(a1,b1,c1, triangle_point):
            return True

    return False

def check_angle_between(a1, b, a2):
    a1, a2 = (a1, a2) if a2>a1 else (a2, a1) 
    if abs(a2-a1) > np.pi:
        return b >= a2 or b <= a1
    else:
        return a1 <= b and b <= a2

def triangles_do_intersect_loose(a1, b1, c1, a2, b2, c2):
    t1 = [a1, b1, c1]
    t2 = [a2, b2, c2]
    # print(t1)
    # print(t2)
    matches = [[ all(v1==v2) for v2 in t2] for v1 in t1]
    matches_count = list(map(lambda x: any(x), matches))
    number_of_matching_vertex = matches_count.count(True)
    if number_of_matching_vertex == 0:
        return triangles_do_intersect(*t1,*t2)
    elif number_of_matching_vertex == 1:
        t1_match = matches_count.index(True)
        t2_match = matches[t1_match].index(True)
        common_vertex = t1[t1_match]
        del t1[t1_match]
        del t2[t2_match]
        angs1 = [ np.arctan2(v[1]-common_vertex[1],v[0]-common_vertex[0]) for v in t1 ]
        angs2 = [ np.arctan2(v[1]-common_vertex[1],v[0]-common_vertex[0]) for v in t2 ]
        for ang in angs2:
            if check_angle_between(angs1[0], ang, angs1[1]):
                return True
        for ang in angs1:
            if check_angle_between(angs2[0], ang, angs2[1]):
                return True
        return False
    elif number_of_matching_vertex == 2:
        t1_first_match = matches_count.index(True)
        t2_first_match = matches[t1_first_match].index(True)
        t1_second_match = matches_count.index(True, t1_first_match+1)
        t2_second_match = matches[t1_second_match].index(True)
        common_vertex1 = t1[t1_first_match]
        common_vertex2 = t1[t1_second_match]
        t1_first_match, t1_second_match = (t1_first_match, t1_second_match) if t1_second_match > t1_first_match else (t1_second_match, t1_first_match)
        t2_first_match, t2_second_match = (t2_first_match, t2_second_match) if t2_second_match > t2_first_match else (t2_second_match, t2_first_match)
        del t1[t1_second_match]
        del t2[t2_second_match]
        del t1[t1_first_match]
        del t2[t2_first_match]
        # print(t1, t2, common_vertex1, common_vertex2)
        if points_orientation(common_vertex1, common_vertex2, t1[0]) == points_orientation(common_vertex1, common_vertex2, t2[0]):
            return True
        return False 
    elif number_of_matching_vertex == 3:
        return True
    else:
        return True

if __name__ == "__main__":
    a = np.array([0, 0])
    b = np.array([2, 0])
    c = np.array([0, 2])
    print(triangle_area(a,b,c))

    a = np.array([0, 0])
    b = np.array([0, 2])
    c = np.array([2, 2])
    print(points_orientation(a,b,c))

    p1 = np.array([1,1])
    p2 = np.array([1,1.5])
    p3 = np.array([3,3])
    p4 = np.array([4,3])
    p5 = np.array([4,0])
    p5 = np.array([1,0.5])
    print(colinear_on_segment(a, p1, c))
    print(colinear_on_segment(a, p2, c))
    print(colinear_on_segment(a, p3, c))
    print(colinear_on_segment(a, p4, c))
    print(colinear_on_segment(a, p5, c))

    s1 = np.array([0, 3])
    s2 = np.array([2, 0])
    s1_1 = s1+ 1
    s2_1 = s2+1
    print(segments_do_intersect(a,c, s1,s2))
    print(segments_do_intersect(a,c, s1_1,s2_1))
    p1 = np.array([1, 0.5])
    p2 = np.array([0.5, 1])
    print(point_inside_triangle(a,b,c,p1))
    print(point_inside_triangle(a,b,c,p2))

    a = np.array([0, 0])
    b = np.array([0, 2])
    c = np.array([2, 2])
    plot_triangle(plt, a, b, c)
    triangles = np.array([  [[2,2],       [3,3],       [4,0]],
                            [[2,2],       [-1, -3],    [-0.5,0.5]],
                            [[2,2],       [2, 0],      [3,0]],
                            [[0,3],       [2,0],       [1,0]],
                            [[0.25, 1.5], [0.25, 0.5], [1.6, 1.8]],
                            [[-2,0],      [0,4],       [6,0]],
                            [[0,0],       [0,2],       [-2,-2]],
                            [[1,3],       [0,2],       [2,2]],
                            [[1,1.5],       [0,2],       [2,2]],
                            [[1,-3],       [0,2],       [2,2]],
                            [[0, 0],       [0,2],       [2,2]],
                            [[-2,-3],     [-1,-2],     [-2,-2]] ] )
    legend = ['0']
    for i in range(triangles.shape[0]):
        plot_triangle(plt ,*triangles[i])
        print('Collision 0 and '+ str(i+1)+': ', triangles_do_intersect(a,b,c,*triangles[i]))
        print('Loose Collision 0 and '+ str(i+1)+': ', triangles_do_intersect_loose(a,b,c,*triangles[i]))
        legend += [str(i+1)]
    plt.legend(legend)
    plt.show()
    

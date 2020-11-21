import numpy as np
import networkx as nx
from drawfuncs import *
from math import sqrt
import cv2 as cv

'''The below function forms coordiantes (in numpy array) for many lattice points, more than we need.
this is inputs the lattice vectors and the neigh parameter which is the user inputed nearest neighbours.'''

def createpoints(neigh, lattice_vectors) :
    dx_cell = max(abs(lattice_vectors[0][0]), abs(lattice_vectors[1][0]))
    dy_cell = max(abs(lattice_vectors[0][1]), abs(lattice_vectors[1][1]))
    nx = neigh//dx_cell
    ny = neigh//dy_cell
    '''Above is the difference (integer) of the known vectors, the output shape is divided by this number.'''
    x_sq = np.arange(-nx, nx, dtype=float)
    y_sq = np.arange(-ny, nx, dtype=float)
    x_sq.shape = x_sq.shape + (1,)
    y_sq.shape = (1,) + y_sq.shape
    x_lattice = lattice_vectors[0][0]*x_sq + lattice_vectors[1][0]*y_sq
    y_lattice = lattice_vectors[0][1]*x_sq + lattice_vectors[1][1]*y_sq
    '''The below mask reshapes the lattice to form a linear x and y coordinate list.'''
    mask = ((x_lattice < neigh/2.0)
             & (x_lattice > -neigh/2.0))
    mask = mask & ((y_lattice < neigh/2.0)
                    & (y_lattice > -neigh/2.0))
    x_lattice = x_lattice[mask]
    y_lattice = y_lattice[mask]
    '''variable is returned upon calling of function. Note the lattice is still larger than needed
    this will be fixed later.'''
    latt = np.empty((len(x_lattice), 2), dtype=float)
    latt[:, 0] = y_lattice
    latt[:, 1] = x_lattice
    return latt

X=nx.Graph()

'''Here the lattice vectors are inputed. '''
lattice_vectors = [
    np.array([1., 0.]),
    np.array([ 0.5, round(sqrt((3)/2,), 1)])]

'''Here the "i_s" variable will contain the amount of nearest neighbours that the user will input, this will
then be placed into the function seen from before.
'''

i_s = int(input("How may nearest neighbours?")) + 1
points = createpoints((i_s), lattice_vectors)
'''Previous function is called'''

'''here dictionaries are made for the coordinates'''
d = {}
for k,v in enumerate(points):
    d[k] = v

'''Here length of points (from origin) are calculated and placed in dictionary '''
lengthdict = {}
for i in d.keys():
    lengthdict[i] = np.linalg.norm(d[i])

''' Below the dictionary is reordered based on the length seen previously. Then the result is trimmed
based on user input, i_s '''
sorted_dict = {k: v for k, v in sorted(lengthdict.items(), key=lambda item: item[1])}
orderlist = [list(sorted_dict.keys())][0]
reordered_dict = {k: d[k] for k in orderlist}
reindexeddict = {i: v for i, v in enumerate(reordered_dict.values())}
reindexeddict = dict(list(reindexeddict.items())[:i_s])


X.add_nodes_from(reindexeddict)

'''nodes are then placed on graph with position'''
for n, p in reindexeddict.items():
    X.nodes[n]['pos'] = p

'''Below the function forms the edges in network x for the graph. Here the angles are found, this is done
to check if vectors are parallel to the original vectors and if so an edge is drawn'''

def angle_between(v1, v2):
    v1_u = v1 / np.linalg.norm(v1)
    v2_u = v2 / np.linalg.norm(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


lst_of_drawn_lines = []
'''two for loops are used. The first is done and assigned as the center. Then the neighbouring points are subtraced from this and assigned
as the difference vector.'''

for i in range(i_s):
    center  = reindexeddict[i]
    #print("--------------------------")
    #print("center is: {}".format(center))
    #print("--------------------------")
    for k in range(i_s):
        if i !=k:
            diff_vect = np.subtract(center , reindexeddict[k])
            diff_vect[0], diff_vect[1] = diff_vect[1], diff_vect[0]
            #print("difference is : {}".format(diff_vect))
            size1 = abs(np.divide(diff_vect, lattice_vectors[0]))
            size2 = abs(np.divide(diff_vect, lattice_vectors[1]))
            angle1 = angle_between(diff_vect, lattice_vectors[0])
            angle2 = angle_between(diff_vect, lattice_vectors[1])
            angle1 = round(angle1,1)
            angle2 = round(angle2,1)
            '''Below is the most efficient method to form lattice edges. Length is used inorder to make sure no incorrect lines are drawn that
            also happen to be paralell with the vector'''
            if angle1 == 0 and np.any(size1 == 1):
                X.add_edge(i,k)
                lst_of_drawn_lines.append([center, reindexeddict[k]])
            elif angle2 == 0 and np.any(size2 == 1):
                X.add_edge(i,k)
                lst_of_drawn_lines.append([center, reindexeddict[k]])

####################################################################################################################
'''Below the code is used for the opencv library.
As you can see the process is arduous as the opencv library requires whole integers and in the tuple form (no array)
the points that we used before are turned into whole numbers by *10 and the +40 inorder to make the values positive.
'''
nodedict = reindexeddict.copy()

max_size = 80
'''Here the canvas of pixels is made'''
img = make_canvas(max_size)
 
for i in reindexeddict.keys():
    reindexeddict[i] = np.multiply(reindexeddict[i], 10)
    reindexeddict[i] = np.int64(reindexeddict[i])
    reindexeddict[i] =  np.add(reindexeddict[i], 40)
    reindexeddict[i] = tuple(reindexeddict[i])

for i in range(len(lst_of_drawn_lines)):
    lst_of_drawn_lines[i][0] = np.multiply(lst_of_drawn_lines[i][0], 10)
    lst_of_drawn_lines[i][1] = np.multiply(lst_of_drawn_lines[i][1], 10)
    lst_of_drawn_lines[i][0] = np.int64(lst_of_drawn_lines[i][0])
    lst_of_drawn_lines[i][1] = np.int64(lst_of_drawn_lines[i][1])
    lst_of_drawn_lines[i][0] = np.add(lst_of_drawn_lines[i][0], 40)
    lst_of_drawn_lines[i][1] = np.add(lst_of_drawn_lines[i][1], 40)
    lst_of_drawn_lines[i][0] = tuple(lst_of_drawn_lines[i][0])
    lst_of_drawn_lines[i][1] = tuple(lst_of_drawn_lines[i][1])

native_tuple = tuple(tuple(x) for x in reindexeddict.values())

'''Again above the code turns data in away that opencv prefers. Places values into native_tuple and 
lst_of_drawn_line lists.'''
#print("native tuple is: {}".format(lst_of_drawn_lines))

print(reindexeddict)
origin = (40,40)
for i in reindexeddict.keys():
    make_spots(native_tuple[i], img)

#########################
#Here the code make the lines for the lattice.
for i in range(len(lst_of_drawn_lines)):
    make_lines(lst_of_drawn_lines[i], img)

###########################
#Here the code makes the lines for the d_1 etc. distances from the origin.
# note: you can't run this code and the above for loop at the same time.    
for i in reindexeddict.keys():
    make_d_lines(origin, reindexeddict[i], img)


save_img("lattice.png", img)

###########################################################################################################


import matplotlib.pyplot as plt
nx.draw(X, nodedict, with_labels=True, font_weight='bold')
plt.show()
#plt.savefig('latticenodes.png')

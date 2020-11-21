from finallattice import nodedict
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
print("imports successfully")

'''below the list "pointsofconsid", contains the points that we will need to consider i.e. the points 
that I visually could see from the previous exercise that are around the (0.4, 0.3) point, and will cause 
this site to bind in a polygon.
'''
pointsofconsid = [0,1,2,3,5,9]
points =[nodedict[i] for i in pointsofconsid]

'''As you can see I imported the node dictionary from the main python document to save some time. I then selected 
the points that I will consider by the dictionaries keys.
The rest is standard and taken directly from the scipy documentation.'''

points.append(np.array([0.4, 0.3]))

vor = Voronoi(points)
print("point list is : {}".format(points))


fig = voronoi_plot_2d(vor)
plt.show()
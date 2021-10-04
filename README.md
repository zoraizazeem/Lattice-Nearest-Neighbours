# LatticeNearestNeighbours
This project explores the various science python libraries, such as networkx, opencv and scipy.spatial.Voronoi.

I chose to code my programs in python as I have more fluency in this.

The exercises can be mostly found in the finallattice file.
The drawfuncs file has the opencv library, and the exercise3 has the voronoi portion of the problem.
I have made notes (in the following form '''NOTES''') to clarify the process I used to solve the problem.

A small portion of the code (def createpoints) is modified from user kiyo on https://stackoverflow.com/questions/6141955/efficiently-generate-a-lattice-of-points-in-python
All other code is my own.

My code allows for any input of nearest neighbours and the resultant planar graph is draw.
Any vector coordinates can be placed in the code and the lattice will be generated.
With the nature of the code the program struggles with unreasonable vectors, i.e. one much larger
than the other.
I also chose to make the background of the opencv diagram black, as the nodes and edges would be 
easier to see.

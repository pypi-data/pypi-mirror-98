This package creates Fractal networks.

The steps for installation are as follows:

1) pip install fractal-network-generator
2) from fractal_network import NetworkGenerator
3) NetworkGenerator.graph(num_of_levels,num_of_nodes_in_a_clique)

OUTPUT:
A file will be created in the current working directory having the name num_of_nodes_in_a_clique-num_of_levels.dat.
Example: If NetworkGenerator.graph(4,3) is entered then a dat file with name "3-4.dat" will be created.

Column 1: node number

Column 2: label

Column 3: Degree 

The next columns indicate the neighbour and the level of connection between the node and neighbour alternately.
For example:

12 10110 3 10 2 13 1 14 1

12 is the node numer, 10110 is the label, 3 is the degree.

10 2 indicates a connection between 12 and 10 having level 2.

13 1 indicates a connection between 12 and 13 having level 1.

14 1 indicates a connection between 12 and 14 having level 1.

 

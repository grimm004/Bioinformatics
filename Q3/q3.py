import matplotlib.pyplot as plt
import networkx as nx
import random


def WPGMA(filename):
    text_matrix = []
    with open(filename, 'rt') as file:
        text_matrix = file.readlines()
    
    species = []
    matrix = []
    # Load matrix and species into memory
    for i in range(1, len(text_matrix)):
        text_row = text_matrix[i].replace('\n', '')
        row = []
        elements = text_row.split(' ')
        species.append(elements[0])
        for j in range(1, len(elements)):
            row.append(float(elements[j]))
        matrix.append(row)

    print(species)
    print_matrix(matrix)
    print()
    g = nx.Graph()

    while len(matrix) > 1:
        # Find two species with smallest distance
        smallest_distance = matrix[1][0]
        i_, j_ = 1, 0
        for i in range(len(matrix)):
            for j in range(i + 1, len(matrix[i])):
                if matrix[i][j] < smallest_distance:
                    smallest_distance = matrix[i][j]
                    i_, j_ = i, j

        # Merge species
        matrix.append([(matrix[i_][k] + matrix[j_][k]) / 2 for k in range(len(species))])
        # Add row for new species (copying above column claculated above)
        for k in range(len(species)):
            matrix[k].append(matrix[-1][k])
        matrix[-1].append(0.0)

        # Ensure j_ is greater than i_ (so that j_ can be safely deleted first followed by i_)
        i_, j_ = min(i_, j_), max(i_, j_)
        # Update species list with new merged species
        species_i = species[i_]
        species_j = species[j_]
        new_species = '%s,%s' % (species_i, species_j)
        species.append(new_species)
        g.add_edge(new_species, species_i)
        g.add_edge(new_species, species_j)
        del species[j_]
        del species[i_]

        # Delete i_-th and j_-th column from matrix
        for k in range(len(matrix)):
            del matrix[k][j_]
            del matrix[k][i_]
        
        # Delete i_-th and j_-th row from matrix
        del matrix[j_]
        del matrix[i_]

        print(species)
        print_matrix(matrix)
        print()

    # Draw graph
    pos = hierarchy_pos(g, species[0])
    nx.draw(g, pos=pos, with_labels=True)
    plt.savefig('.'.join(filename.split('.')[:-1]) + '.png')
    plt.close()


def print_matrix(m):
    print('[%s]' % ',\n '.join(', '.join(str(e) for e in r) for r in m) if len(m) > 0 else 'NaM')


def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):

    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.  
    Licensed under Creative Commons Attribution-Share Alike 

    If the graph is a tree this will return the positions to plot this in a 
    hierarchical layout.

    G: the graph (must be a tree)

    root: the root node of current branch 
    - if the tree is directed and this is not given, 
      the root will be found and used
    - if the tree is directed and this is given, then 
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given, 
      then a random choice will be used.

    width: horizontal space allocated for this branch - avoids overlap with other branches

    vert_gap: gap between levels of hierarchy

    vert_loc: vertical location of root

    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
        '''
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        '''

        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)  
        if len(children)!=0:
            dx = width/len(children) 
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap, 
                                    vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos


    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)


if __name__ == '__main__':
    WPGMA('matrix1.txt')
    WPGMA('matrix2.txt')
    WPGMA('matrix3.txt')
    WPGMA('matrix4.txt')

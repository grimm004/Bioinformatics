import matplotlib.pyplot as plt
import networkx as nx


def WPGMA(filename):
    text_matrix = []
    with open(filename, 'rt') as file:
        text_matrix = file.readlines()
    
    species = []
    matrix = []
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
        new_species = species_i + species_j
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
    nx.draw(g, with_labels=True)
    plt.savefig('.'.join(filename.split('.')[:-1]) + '.png')
    plt.close()


def print_matrix(m):
    print('[%s]' % ',\n '.join(', '.join(str(e) for e in r) for r in m) if len(m) > 0 else 'NaM')


if __name__ == '__main__':
    WPGMA('matrix1.txt')
    WPGMA('matrix2.txt')

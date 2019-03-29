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
            row.append(elements[j])
        matrix.append(row)
    
    print(species)
    print_matrix(matrix)


def print_matrix(m):
    print('[%s]' % ',\n '.join((', '.join(r) for r in m)) if len(m) > 0 else 'NaM')


if __name__ == '__main__':
    WPGMA('matrix1.txt')
    WPGMA('matrix2.txt')

#!/usr/bin/python
import time
import sys


# YOUR FUNCTIONS GO HERE -------------------------------------
BASE_SCORES = { 'A': 4, 'C': 3, 'G': 2, 'T': 1 }
MISSMATCH_SCORE = -3
GAP_SCORE = -2


def print_matrix(m):
    print('[%s]' % ',\n '.join(', '.join(str(e) for e in r) for r in m) if len(m) > 0 else 'NaM')


def align(a, b):
    if len(a) == 0 or len(b) == 0:
        return ('', '', 0)

    # Initialise empty score and backtrack matrices
    score = [[None for _ in range(len(a) + 1)] for _ in range(len(b) + 1)]
    backtrack = [[' ' for _ in range(len(a) + 1)] for _ in range(len(b) + 1)]

    # i references row, j references column
    # a is along columns, b is along rows
    # e.g.
    #   j 0 1 2 3 4 5 6
    # i   A A A A A A A
    # 0 B . . . . . . .
    # 1 B . . . . . . .
    # 2 B . . . . . . .
    # 3 B . . . . . . .

    # Function to calculate the score for a diagonal (match or missmatch)
    def c(i, j):
        return BASE_SCORES[a[j - 1]] if a[j - 1] == b[i - 1] else MISSMATCH_SCORE


    # Calculate score and backtrack matrices
    score[0][0] = 0

    for i in range(1, len(b) + 1):
        score[i][0] = -2 * i
        backtrack[i][0] = 'U'

    for j in range(1, len(a) + 1):
        score[0][j] = -2 * j
        backtrack[0][j] = 'L'

    for i in range(1, len(b) + 1):
        for j in range(1, len(a) + 1):
            scores = {
                'D': score[i - 1][j - 1] + c(i, j),
                'U': score[i - 1][j] + GAP_SCORE,
                'L': score[i][j - 1] + GAP_SCORE
            }
            backtrack[i][j] = max(scores, key=scores.get)
            score[i][j] = scores[backtrack[i][j]]

    # Use backtrack matrix to find optimal alignment
    alignment = ['', '']
    i, j = len(score) - 1, len(score[0]) - 1
    while (i, j) != (0, 0):
        direction = backtrack[i][j]
        if direction == 'D':
            alignment[0] = a[j - 1] + alignment[0]
            alignment[1] = b[i - 1] + alignment[1]
            i -= 1
            j -= 1
        elif direction == 'U':
            alignment[0] = '-' + alignment[0]
            alignment[1] = b[i - 1] + alignment[1]
            i -= 1
        elif direction == 'L':
            alignment[0] = a[j - 1] + alignment[0]
            alignment[1] = '-' + alignment[1]
            j -= 1
    return (alignment[0], alignment[1]), score[-1][-1]

# ------------------------------------------------------------

# DO NOT EDIT ------------------------------------------------
# Given an alignment, which is two strings, display it

def displayAlignment(alignment):
    string1 = alignment[0]
    string2 = alignment[1]
    string3 = ''
    for i in range(min(len(string1),len(string2))):
        if string1[i]==string2[i]:
            string3=string3+"|"
        else:
            string3=string3+" "
    print('Alignment ')
    print('String1: '+string1)
    print('         '+string3)
    print('String2: '+string2+'\n\n')

# ------------------------------------------------------------


# DO NOT EDIT ------------------------------------------------
# This opens the files, loads the sequences and starts the timer
file1 = open(sys.argv[1], 'r')
seq1=file1.read()
file1.close()
file2 = open(sys.argv[2], 'r')
seq2=file2.read()
file2.close()
start = time.time()

#-------------------------------------------------------------


# YOUR CODE GOES HERE ----------------------------------------
# The sequences are contained in the variables seq1 and seq2 from the code above.
# Intialise the scoring matrix and backtracking matrix and call the function to populate them
# Use the backtracking matrix to find the optimal alignment 
# To work with the printing functions below the best alignment should be called best_alignment and its score should be called best_score. 

best_alignment, best_score = align(seq1, seq2)

#-------------------------------------------------------------


# DO NOT EDIT (unless you want to turn off displaying alignments for large sequences)------------------
# This calculates the time taken and will print out useful information 
stop = time.time()
time_taken=stop-start

# Print out the best
print('Time taken: '+str(time_taken))
print('Best (score '+str(best_score)+'):')
displayAlignment(best_alignment)

#-------------------------------------------------------------


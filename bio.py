MATCH_REWARD = 2
MISSMATCH_PENALTY = -1
GAP_PENALTY = -2
D = 'D'
U = 'U'
L = 'L'


def c(a, b, i, j):
    return MATCH_REWARD if a[i - 1] == b[j - 1] else MISSMATCH_PENALTY


def s(score, a, b, i, j):
    if score[i][j] is not None:
        return D, score[i][j]
    d = c(a, b, i, j) + s(score, a, b, i - 1, j - 1)[1]
    u = s(score, a, b, i - 1, j)[1] - 2
    l = s(score, a, b, i, j - 1)[1] - 2
    s_ = max(d, u, l)
    score[i][j] = s_
    if d == s_:
        return D, s_
    elif u == s_:
        return U, s_
    else:
        return L, s_


def align(a, b):
    score = [[None for _ in range(len(b) + 1)].copy() for _ in range(len(a) + 1)]
    backtrack = [['' for _ in range(len(b) + 1)].copy() for _ in range(len(a) + 1)]

    for i in range(len(a) + 1):
        score[i][0] = GAP_PENALTY * i
        backtrack[i][0] = U
    for i in range(len(b) + 1):
        score[0][i] = GAP_PENALTY * i
        backtrack[0][i] = L

    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            back, s_ = s(score, a, b, i, j)
            backtrack[i][j] = back

    return score, backtrack


if __name__ == '__main__':
    print(align("ACG", "AGT"))

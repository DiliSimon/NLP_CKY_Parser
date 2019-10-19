import util
from collections import Set


def CKY(sent:str, gr:dict):
    # initialize matrix
    words = sent.split()
    matrix = list()
    for n in words:
        col = list()
        for m in range(len(words)):
            new_list = list()
            col.append(new_list)
        matrix.append(col)

    for j, w in enumerate(words):
        initial = util.find_parent_terminal(w, gr)
        for t in initial:
            matrix[j][j].append(t)
        for i in range(j - 1, -1, -1):
            # print('i: ' + str(i))
            # print('j: ' + str(j))
            # print('\n')
            for k in range(1, j-i+1):
                # print('\n')
                parents = util.find_parent(matrix[i][j-k], matrix[j+1-k][j], gr)
                # if i == 2 and j == 3:
                #     # print('k: ' + str(k))
                #     # print('i: ' + str(i))
                #     # print('j: ' + str(j))
                #     # print(matrix[i][j-k])
                #     # print(matrix[j+1-k][j])
                #     # print(parents)
                for p in parents:
                    matrix[i][j].append(p)
            # matrix[i][j] = list(dict.fromkeys(matrix[i][j]))
    return matrix


if __name__ == '__main__':
    gr = util.load_grammar('flight.gr')

    # test_list_first = ['S', 'VP', 'NP', 'Nominal', 'Noun', 'Verb']
    # test_list_second = ['Det']
    # print(util.find_parent(test_list_first, test_list_second, gr))

    rslt = CKY('book the dinner flight .', gr)
    print(rslt[1][3])
    #print(rslt[0][0])

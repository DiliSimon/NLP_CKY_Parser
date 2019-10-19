import util
from collections import Set, defaultdict
import math
import argparse


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
                parents = util.find_parent(matrix[i][j-k], matrix[j+1-k][j], gr, k)
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


def reverse_CKY(rslt:list):

    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", type=str,
                        help="type in mode")
    parser.add_argument("filename", type=str,
                        help="type in the grammar filepath")
    parser.add_argument("sentence", type=str, help="filepath that contains sentences")
    args = parser.parse_args()

    gr = util.load_grammar(args.filename)

    if args.mode == 'RECOGNIZER':
        sent = util.load_sentence(args.sentence)
        for s in sent:
            length = len(s.split())
            rslt = CKY(s, gr)
            if len(rslt[0][length-1]) != 0:
                print('True')
                continue
            print('False')
        exit()

    if args.mode == 'BEST-PARSE':
        sent = util.load_sentence(args.sentence)
        for s in sent:
            length = len(s.split())
            rslt = CKY(s, gr)
            if len(rslt[0][length - 1]) != 0:
                k = 0
                max = 0
                for root in rslt[0][length - 1]: # find the most probable root
                    if root[1] > max:
                        k = root[-1]


                continue
            print('False')
        exit()


    # test_list_first = ['S', 'VP', 'NP', 'Nominal', 'Noun', 'Verb']
    # test_list_second = ['Det']
    # print(util.find_parent(test_list_first, test_list_second, gr))

    rslt = CKY('book the dinner flight .', gr)
    print(rslt[2][2])
    print(rslt[0][4])
    print(-math.log(rslt[0][4][1][1])/math.log(2))
    #print(rslt[0][0])

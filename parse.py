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


def reverse_CKY(current_info:list, i, j, rslt:list):
    # prepare children's indices
    first_child_i = i
    first_child_j = j - current_info[-3]
    second_child_i = j + 1 - current_info[-3]
    second_child_j = j

    # find first child
    first_potential_rules = rslt[first_child_i][first_child_j]
    for r in first_potential_rules:
        if r[1] == current_info[-2]:
            first_child_info = r
    print('(' ,end = '')
    print(first_child_info[0], end=' ')
    if len(first_child_info) != 3:
        reverse_CKY(first_child_info, first_child_i, first_child_j, rslt)
        print(')', end=' ')
    else:
        print(first_child_info[2], end='')
        print(')', end=' ')
    #print(')', end = ' ')

    # find second child
    second_potential_rules = rslt[second_child_i][second_child_j]
    for r in second_potential_rules:
        if r[1] == current_info[-1]:
            second_child_info = r
    print('(', end = '')
    print(second_child_info[0], end=' ')
    if len(second_child_info) != 3:
        reverse_CKY(second_child_info, second_child_i, second_child_j, rslt)
        print(')', end='')
    else:
        print(second_child_info[2], end='')
        print(')', end='')
    #print(')', end='')

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
            ifroot = False
            for r in rslt[0][length - 1]:
                if r[0] == 'ROOT':
                    ifroot = True
            if len(rslt[0][length-1]) != 0 and ifroot:
                print('True')
                continue
            print('False')
        exit()

    if args.mode == 'BEST-PARSE':
        sent = util.load_sentence(args.sentence)
        for s in sent:
            length = len(s.split())
            rslt = CKY(s, gr)
            ifroot = False
            for r in rslt[0][length-1]:
                if r[0] == 'ROOT':
                    ifroot = True
            if len(rslt[0][length - 1]) != 0 and ifroot:
                current_info = list()
                k = 0
                max = 0
                for root in rslt[0][length - 1]: # find the most probable root
                    if root[1] > max:
                        current_info = root
                        max = root[1]
                prob = current_info[1]
                weight = -math.log(prob)/math.log(2)
                print(round(weight, 3), end='\t')
                print('(', end='')
                print(current_info[0], end=' ')
                reverse_CKY(current_info, 0, length - 1, rslt)
                print(')')
            else:
                print('-\tNOPARSE')
        exit()

    if args.mode == 'TOTAL-WEIGHT':
        sent = util.load_sentence(args.sentence)
        for s in sent:
            length = len(s.split())
            rslt = CKY(s, gr)
            if len(rslt[0][length - 1]) != 0:
                total_prob = 0
                for r in rslt[0][length - 1]:
                    total_prob += r[1]
                total_weight = -math.log(total_prob) / math.log(2)
                print(round(total_weight, 3))
            else:
                print('-')
        exit()

    rslt = CKY('book the dinner flight', gr)
    # print(rslt[2][2])
    # print(rslt)
    # print(round(-math.log(rslt[0][4][1][1])/math.log(2), 3))

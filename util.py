from collections import defaultdict, Set
import random
import time


def random_number(num):
    random.seed(time.clock())
    rand = random.randint(0, num - 1)
    return rand


def load_sentence(filename):
    with open(filename) as f:
        lines = f.readlines()
        return lines


def load_grammar(filename):
    grammar = defaultdict(list)
    with open(filename) as f:
        text = f.read()
        for line in text.splitlines():
            if not line.startswith('#'):
                words = line.split()
                if len(words) == 0:
                    continue
                LHS = ''
                RHS = list()
                for idx, w in enumerate(words):
                    if idx == 0:
                        weight = float(w)
                        RHS.append(weight)
                        continue
                    if idx == 1:
                        LHS = w
                    else:
                        if w == '#':
                            break
                        RHS.append(w)
                grammar[LHS].append(RHS)
    g = dict(grammar)
    return g


def find_parent(children_first: list, children_second:list, gr:dict, k_value):
    parents = list()
    for f_list in children_first:
        f = f_list[0]
        for s_list in children_second:
            s = s_list[0]
            for k in gr.keys():
                for rule in gr[k]:
                    if len(rule) != 3:
                        continue
                    if rule[1] == f and rule[2] == s:
                        p = f_list[1] * s_list[1] * rule[0]
                        rslt = list()
                        rslt.append(k)
                        for r in rule:
                            rslt.append(r)
                        rslt[1] = p
                        rslt.append(k_value)
                        parents.append(rslt)
    return parents


def find_parent_terminal(child:str, gr:dict):
    parents = list()
    for k in gr.keys():
        for rule in gr[k]:
            if len(rule) == 2 and rule[1] == child:
                rslt = list()
                rslt.append(k)
                for r in rule:
                    rslt.append(r)
                parents.append(rslt)
                break
    return parents

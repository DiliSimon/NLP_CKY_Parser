from collections import defaultdict, Set
import random
import time


def random_number(num):
    random.seed(time.clock())
    rand = random.randint(0, num - 1)
    return rand


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


def find_parent(children_first: list, children_second:list, gr:dict):
    parents = list()
    for f in children_first:
        for s in children_second:
            for k in gr.keys():
                for rule in gr[k]:
                    if len(rule) != 3:
                        continue
                    if rule[1] == f and rule[2] == s:
                        parents.append(k)
    return parents


def find_parent_terminal(child:str, gr:dict):
    parents = list()
    for k in gr.keys():
        for rule in gr[k]:
            if len(rule) == 2 and rule[1] == child:
                parents.append(k)
                break
    return parents

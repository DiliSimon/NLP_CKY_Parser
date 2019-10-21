import util
import time


def remove_unit(non_terminals, new_grammar):
    for idx, k in enumerate(new_grammar.keys()):
        for r in new_grammar[k]:
            if len(r) == 2 and (r[1] in non_terminals):
                B_rules = new_grammar[r[1]]
                new_grammar[k].remove(r)
                new_grammar[k] = new_grammar[k] + B_rules
    return new_grammar


def binarize(gr:dict):
    new_grammar = gr
    non_terminals = list(new_grammar.keys())
    terminals = list()
    for k in non_terminals:
        for r in gr[k]:
            for t in r[1:]:
                if t not in non_terminals:
                    terminals.append(t)
    terminals = list(dict.fromkeys(terminals))

    # remove unit productions
    new_grammar = remove_unit(non_terminals, new_grammar)

    # remove RHS that has more than two elements
    i = 0
    unfinished = True
    while unfinished:
        unfinished = False
        for k in non_terminals:
            for r in new_grammar[k]:
                if len(r) > 3:
                    unfinished = True
                    new_terminal = 'ARTIFICIAL' + str(i)
                    i += 1
                    p = r[0]
                    B_1 = r[1]
                    new_rule = list()
                    new_rule.append(p)
                    new_rule.append(B_1)
                    new_rule.append(new_terminal)
                    new_grammar[k].remove(r)
                    new_grammar[k].append(new_rule)
                    new_grammar[new_terminal] = list()
                    new_terminal_rule = list()
                    new_terminal_rule.append(1)
                    for e in r[3:]:
                        new_terminal_rule.append(e)
                    new_grammar[new_terminal].append(new_terminal_rule)
                    non_terminals.append(new_terminal)

    # remove RHS that has the form A->aB
    for k in non_terminals:
        for r in new_grammar[k]:
            if len(r) == 3:
                if r[1] in non_terminals and r[2] in terminals:
                    new_terminal = 'ARTIFICIAL' + str(i)
                    i += 1
                    new_grammar[k].remove(r)
                    new_rule = [r[0], new_terminal, r[2]]
                    new_grammar[k].append(new_rule)
                    new_grammar[new_terminal] = list()
                    new_grammar[new_terminal].append([1, r[1]])
                    non_terminals.append(new_terminal)
                elif r[2] in terminals and r[1] in non_terminals:
                    new_terminal = 'ARTIFICIAL' + str(i)
                    i += 1
                    new_grammar[k].remove(r)
                    new_rule = [r[0], r[1], new_terminal]
                    new_grammar[k].append(new_rule)
                    new_grammar[new_terminal] = list()
                    new_grammar[new_terminal].append([1, r[2]])
                    non_terminals.append(new_terminal)

    return new_grammar


if __name__ == '__main__':
    start_time = time.time()
    gr = util.load_grammar('wallstreet.gr')
    new_grammar = binarize(gr)
    util.write_grammar(new_grammar, 'wallstreet.grb')
    print("--- %s seconds ---" % (time.time() - start_time))

import argparse
from automata import post_to_NFA, epsilonclosure, learn_alphabet, re2post
from graphviz import Digraph


LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
NUMBERS = '0123456789'

def main():
    args = parse_args()
    alphabet = learn_alphabet(args.input_file)
    postfix = re2post(args.RegEx)
    # converted_regex = explicit_concat(args.RegEx)
    # postfix = convert_postfix(converted_regex)
    nfa = post_to_NFA(postfix)
    print (postfix)
    print (nfa.c)
    print (nfa.out.c)
    print (nfa.out.out.c)

    
    NFA_DOT = Digraph(comment = "NFA", graph_attr={'rankdir' : 'LR'}, node_attr={'shape' : 'circle'})
    



    queue = []
    visited = set()
    i = 0
    state = nfa
    queue.append(state)
    known_states = {}
    visited = set()

    while queue:
        state = queue.pop()
        print (state.c)        
        known_states[state] = 's'+str(i)
        i = i + 1
        if state.c is -2:
            NFA_DOT.node(known_states[state], shape = 'doublecircle')
        else:
            NFA_DOT.node(known_states[state])
        if state.out is not None and state.out not in known_states:
            queue.append(state.out)
            known_states[state.out] = 's'+str(i)
            i = i + 1
            if state.c is -1:
                NFA_DOT.edge(known_states[state], known_states[state.out], '~e~')
                NFA_DOT.edge(known_states[state], known_states.get(state.out1, 's'+str(i)), '~e~')
            else:
                NFA_DOT.edge(known_states[state],known_states[state.out], state.c)
                i = i - 1
        elif state.out1 is not None and state.out1 not in known_states:
            queue.append(state.out1)
            known_states[state.out1] = 's'+str(i)
            i = i + 1
            if state.c is -1:
                NFA_DOT.edge(known_states[state], known_states.get(state.out, 's'+str(i)), state.out.c)
                NFA_DOT.edge(known_states[state], known_states[state.out1], '~e~')
            else:
                NFA_DOT.edge(known_states[state],known_states[state.out1], state.c)
                i = i - 1

    print(NFA_DOT.source)
    NFA_DOT.render("test", view=True)

def parse_args():
    parser = argparse.ArgumentParser(description='search regex pattern in file.')
    parser.add_argument('RegEx', metavar='REGEX-PATTERN', type=str,
                        help="the regular expression pattern to search"+
                        "input file with")
    parser.add_argument('input_file', metavar='INPUT-FILE', type=argparse.FileType('r'),
                        help="the file to test regex against")
    parser.add_argument("-n", type=argparse.FileType('rw'),
                        help="enable NFA output to specified file")
    parser.add_argument("-d", type=argparse.FileType('rw'),
                        help="enable DFA output to specified file")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()
    
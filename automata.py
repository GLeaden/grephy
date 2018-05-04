from graphviz import Digraph
def post_to_NFA(postfix_pattern):
    ''' Thank you Russ Cox of https://swtch.com/~rsc/regexp/regexp1.html fame for teaching me how Thompson's Construction works '''
    class state():
        def __init__(self, c):
            self.c = c
            self.out = None
            self.out1 = None

    class nfa_fragment():
        def __init__(self, start, incomplete_transitions):
            self.start = start
            self.out = incomplete_transitions
    
    def patch(incomplete_transitions, out):
        for state in incomplete_transitions:
            if state.c == -1:
                state.out1 = out
            else:
                state.out = out

    def nonterminal(token, nfa_fragments):
        s = state(token)
        nfa_fragments.append(nfa_fragment(s, [s]))

    def catenation(nfa_fragments):
        e2 = nfa_fragments.pop()
        e1 = nfa_fragments.pop()
        patch(e1.out, e2.start)
        e1.out = e2.out
        nfa_fragments.append(e1)

    def alternation(nfa_fragments):
        e2 = nfa_fragments.pop()
        e1 = nfa_fragments.pop()
        s = state(-1)
        s.out = e2.start
        s.out1 = e1.start
        e1.start = s
        e1.out = e1.out + e2.out
        nfa_fragments.append(e1)
    
    def zero_or_more(nfa_fragments):
        e = nfa_fragments.pop()
        s = state(-1)
        s.out = e.start
        patch(e.out, s)
        e.out = [s]
        e.start = s
        nfa_fragments.append(e)
    
    nfa_fragments = []

    for char in postfix_pattern:
        if char == '.':
            catenation(nfa_fragments)
        elif char == '*':
            zero_or_more(nfa_fragments)
        elif char == '+':
            alternation(nfa_fragments)
        else:
            nonterminal(char, nfa_fragments)
    if nfa_fragments:
        e = nfa_fragments.pop()
        patch(e.out, state(-2))
        return e.start
    return state(-2)

def learn_alphabet(input_file):
    alphabet = set()
    operators = '+()*'
    with input_file as file:
        line = file.readlines()
        for i in line:
            i = i.replace("\n", "")
            i = i.replace("\r", "")
            for c in i:
                alphabet.add(c)
            for o in operators:
                alphabet.add(o)
    return alphabet

def NFA_to_DFA(nfa):
    class dfa_state():
        def __init__(self, states):
            self.states = states  #Subset Construction (set of nfa states that this state represents)
            self.transitions = {} #Dictionary of [char]:[next state] 
            self.end_state = False
    
    class dfa():
        def __init__(self):
            self.Q = set()
            self.start = None

        def get_dfa_state(self, nfa_states):

            if not self.start:
                result = dfa_state(nfa_states)
                self.start = result
                self.Q.add(result)
                for state in nfa_states:
                    if state.c is -1:
                        self.get_dfa_state(set(state.out,state.out1))
                    elif state.c is -2:
                        result.end_state = True
                    else:
                        result.transitions[state.c] = self.get_dfa_state(set([state.out]))
                return result

            for state in self.Q:
                if state.states == nfa_states:
                    return state

            result = dfa_state(nfa_states)
            self.Q.add(result)
            for state in nfa_states:
                if state.c is -1:
                    self.get_dfa_state(set([state.out,state.out1]))
                elif state.c is -2:
                    result.end_state = True
                else:
                    result.transitions[state.c] = self.get_dfa_state(set([state.out]))
                    print ("transition " + str(result) + " to " + str(result.transitions[state.c]) + str(len(nfa_states)))
            return result
        
    dfa = dfa()
    queue = []
    state = nfa
    queue.append(state)
    visited = set()
    while queue:
        state = queue.pop()
        if state.out is not None and state.out not in visited:
            queue.append(state.out)
            visited.add(state.out)
        if state.out1 is not None and state.out1 not in visited:
            queue.append(state.out1)
            visited.add(state.out1)
        if state.c is -1:
            dfa.get_dfa_state(set([state.out,state.out1]))
        else:
            dfa.get_dfa_state(set([state]))
    return dfa

def compute_DFA(dfa):
    pass

def pretty_print_DFA(dfa, outfile):
    DFA_DOT = Digraph(comment = "DFA", graph_attr={'rankdir' : 'LR'}, node_attr={'shape' : 'circle'})
    DFA_DOT.node(str(dfa.start), 's0', shape = 'square')
    i = 1
    for state in dfa.Q:
        if state.end_state is True:
            DFA_DOT.node(str(state), 's'+str(i), shape = 'doublecircle')
        else:
            DFA_DOT.node(str(state), 's'+str(i))
        i = i + 1
        if state.transitions:
            for char in state.transitions:
                DFA_DOT.edge(str(state), str(state.transitions[char]), char)
    print(DFA_DOT.source)
    DFA_DOT.render("dtest", view=True)
    
def pretty_print_NFA(nfa, outfile):
    i = 0
    queue = []
    state = nfa
    queue.append(state)
    known_states = {}
    known_states[state] = 's'+str(i)
    NFA_DOT = Digraph(comment = "NFA", graph_attr={'rankdir' : 'LR'}, node_attr={'shape' : 'circle'})


    while queue:
        state = queue.pop()
        if state.out is not None and state.out not in known_states:
            i = i + 1
            queue.append(state.out)
            known_states[state.out] = 's'+str(i)
        if state.out1 is not None and state.out1 not in known_states:
            i = i + 1
            queue.append(state.out1)
            known_states[state.out1] = 's'+str(i)
        if state.c is -2:
            NFA_DOT.node(known_states[state], shape = 'doublecircle')
        elif state.c is not -1:
            NFA_DOT.node(known_states[state])
            NFA_DOT.edge(known_states[state], known_states[state.out], state.c)
        elif state.c is -1:
            NFA_DOT.edge(known_states[state], known_states[state.out], 'ε')
            NFA_DOT.edge(known_states[state], known_states[state.out1], 'ε')
    print(NFA_DOT.source)
    NFA_DOT.render("test", view=True)

def re_to_post(expression, alphabet):
    '''
    Converts Regex to PostFix Expression, adding '.' characters to explicity
    represent concatenation. 
    '''
    tempstack = []
    atomic_chars = 0
    alternation = 0
    result = []
    for char in expression:
        if char not in alphabet:
            print ("ERROR: character " + char + " not found in alphabet of input file.")
            exit()
        if char == '(':
            if atomic_chars == 2:
                result.append('.')
                atomic_chars = 1
            tempstack.append((atomic_chars, alternation))
            atomic_chars = 0
            alternation = 0
        elif char == ')':
            if atomic_chars == 2: 
                result.append('.')
            if alternation: 
                result.append('+'*alternation)
            atomic_chars,alternation = tempstack.pop()
            atomic_chars = atomic_chars + 1
        elif char == '*': 
            result.append(char)
        elif char == '+':
            if atomic_chars == 2: 
                result.append('.')
            atomic_chars = 0
            alternation = alternation + 1
        else:
            if atomic_chars == 2: 
                result.append('.')
                atomic_chars = atomic_chars - 1
            result.append(char)
            atomic_chars = atomic_chars + 1
    
    if atomic_chars == 2: 
        result.append('.')
    if alternation: 
        result.append('+'*alternation)

    return result
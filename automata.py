from graphviz import Digraph
def post_to_NFA(postfix_pattern):
    ''' 
    Utilizes Thompson's Construction/Algorithim
    converts a postfix regex with explicit concatenations (ab -> a.b)
    to an NFA state with 'out' pointers to other NFA states 
    '''
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
        # Combine an incomplete transition with specified out state
        for state in incomplete_transitions:
            if state.c == -1:
                state.out1 = out
            else:
                state.out = out

    def nonterminal(token, nfa_fragments):
        s = state(token)
        nfa_fragments.append(nfa_fragment(s, [s]))

    def catenation(nfa_fragments):
        # Combine the two most recent NFA fragments
        e2 = nfa_fragments.pop()
        e1 = nfa_fragments.pop()
        patch(e1.out, e2.start)
        e1.out = e2.out
        nfa_fragments.append(e1)

    def alternation(nfa_fragments):
        # Create an incomplete transition as one of the output
        e2 = nfa_fragments.pop()
        e1 = nfa_fragments.pop()
        s = state(-1)
        s.out = e2.start
        s.out1 = e1.start
        e1.start = s
        e1.out = e1.out + e2.out
        nfa_fragments.append(e1)
    
    def zero_or_more(nfa_fragments):
        # Create a loopback on the previous fragment, and split 
        # with an incomplete transition
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
    ''' 
    Scans the input file and compiles a set of all unique characters
    sans line endings.
    '''
    alphabet = set()
    file = open(input_file,"r")
    line = file.readlines()
    for i in line:
        i = i.replace("\n", "")
        i = i.replace("\r", "")
        for c in i:
            alphabet.add(c)
    file.close()
    return alphabet

def NFA_to_DFA(nfa, alphabet):
    ''' 
    Converts a given NFA to a DFA using subset construction.
    '''
    class dfa_state():
        def __init__(self, states, accept=False):
            self.states = states  # Subset Construction (set of nfa_states that this state represents)
            self.transitions = {} # Dictionary of [char]:[next state] 
            self.accept = accept    

    class dfa():
        def __init__(self):
            self.Q = set() # Set of dfa_states that comprise the DFA
            self.start = None # dfa_state that started it all...

        def move(self, char, states):
            ''' 
            Takes a dfa_state and character and returns set of all 
            possible nfa_states reachable with 1 transition of that character from that state.
            '''
            result = set()
            for state in states:
                if state.c == char:
                    result.add(state.out)
            return result

        def get_dfa_state(self, nfa_states):
            ''' 
            Performs ε-closure on each nfa state given. 
            Returns 1 dfa_state that represents all nfa_states 
            reachable with ε-transitions.
            '''
            tovisit = set()
            accept = False
            for state in nfa_states.copy():
                if state.c is -1:
                    tovisit.add(state.out)
                    tovisit.add(state.out1)
                    nfa_states.add(state)
                while tovisit:
                    current = tovisit.pop()
                    if current.c is -1:
                        tovisit.add(current.out)
                        tovisit.add(current.out1)
                    else:
                        nfa_states.add(current)
            for dstate in self.Q:
                if dstate.states == nfa_states:
                    return dstate
            # The finish states of the DFA are those which contain 
            # any of the finish states of the NFA.
            for state in nfa_states:
                if state.c == -2:
                    accept = True
            result = dfa_state(nfa_states,accept)
            return result
        
    dfa = dfa()
    queue = []
    # Create the start state of the DFA by taking the 
    # ε-closure of the start state of the NFA.
    new_dfa_state = dfa.get_dfa_state(set([nfa]))
    queue.append(new_dfa_state)
    dfa.Q.add(new_dfa_state)
    dfa.start = new_dfa_state
    # Each time we generate a new DFA state, we must apply step 2 to it. 
    # The process is complete when applying step 2 does not make new states.
    while queue:
        current_state = queue.pop()
        # For each possible input symbol:
        #     Apply move to the newly-created state and the input symbol; 
        #     this will return a set of states.
        #     Apply the ε-closure to this set of states, possibly resulting in a new set.
        for char in alphabet:
            next_nfa_states = dfa.move(char, current_state.states)
            if next_nfa_states:
                new_dfa_state = dfa.get_dfa_state(next_nfa_states)
                current_state.transitions[char] = new_dfa_state
                if new_dfa_state not in dfa.Q:
                    queue.append(new_dfa_state)
                    dfa.Q.add(new_dfa_state)
    return dfa

def pretty_print_DFA(dfa, outfile):
    ''' 
    Takes a dfa and creates a directed graph of transitions between states.
    Accepting state is dileniated with a doublecircle.
    Starting state is ALWAYS s0. (I could not find a 
    reliable way to have an arrow from nothing)
    '''
    DFA_DOT = Digraph(comment = "DFA", graph_attr={'rankdir' : 'LR'}, node_attr={'shape' : 'circle'})
    i = 1
    for dstate in dfa.Q:
        if dstate.accept is True:
            DFA_DOT.node(str(dstate), 's'+str(i), shape = 'doublecircle')
            i = i + 1
        elif dstate is dfa.start:
            DFA_DOT.node(str(dfa.start), 's0')
        else:
            DFA_DOT.node(str(dstate), 's'+str(i))
            i = i + 1
        if dstate.transitions:
            for char in dstate.transitions:
                DFA_DOT.edge(str(dstate), str(dstate.transitions[char]), char)

    file = open(outfile, "w")
    file.write(DFA_DOT.source)
    file.close()
    DFA_DOT.render(outfile, view=True)
    
def pretty_print_NFA(nfa, outfile):
    ''' 
    Takes an nfa and creates a directed graph of transitions between states.
    Accepting state is dileniated with a doublecircle.
    Starting state is ALWAYS s0. (I could not find a 
    reliable way to have an arrow from nothing)
    '''
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
    file = open(outfile, "w")
    file.write(NFA_DOT.source)
    file.close()
    NFA_DOT.render(outfile, view=True)

def re_to_post(expression, alphabet):
    '''
    Converts Regex to PostFix Expression, adding '.' characters to explicity
    represent concatenation. 

    REGEX ACCEPTED:
    *  ----  Zero or More
    +  ----  Alternation (OR)
    () ----  Parens (grouping)
    _________________________________
    .  ----  Concatenation (explicit)
    '''
    tempstack = []
    atomic_chars = 0
    alternation = 0
    result = []
    for char in expression:
        if char not in alphabet and char not in '+()*':
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

def compute_DFA(dfa, infile):
    f = open(infile,"r")
    lines = f.read().splitlines()
    f.close()
    for line in lines:
        current_state = dfa.start
        for char in line:
            if char in current_state.transitions:
                current_state = current_state.transitions[char]
            else:
                current_state = None
                break
        if current_state and current_state.accept == True:
            print(line)

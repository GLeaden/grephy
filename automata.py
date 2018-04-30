def post_to_NFA(postfix_pattern):
    ''' Thank you Russ Cox of https://swtch.com/~rsc/regexp/regexp1.html fame for teaching me how Thompson's Construction works '''
    class state():
        def __init__(self, c):
            self.c = c
            self.name = c
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

    def one_or_more(nfa_fragments):
        e = nfa_fragments.pop()
        print (e.start.c + "one or more")
        s = state(-1)
        s.out = e.start
        patch(e.out, s)
        e.out = [s]
        nfa_fragments.append(e)
    
    nfa_fragments = []

    for char in postfix_pattern:
        for i in nfa_fragments:
            print (i.start.c+" hey")
        print(char)
        if char == '.':
            catenation(nfa_fragments)
        elif char == '*':
            zero_or_more(nfa_fragments)
        elif char == '|':
            alternation(nfa_fragments)
        elif char == '+':
            one_or_more(nfa_fragments)
        else:
            nonterminal(char, nfa_fragments)
    if nfa_fragments:
        e = nfa_fragments.pop()
        patch(e.out, state(-2))
        return e.start
    return state(-2)

def learn_alphabet(input_file):
    alphabet = set()
    with input_file as file:
        line = file.readlines()
        for i in line:
            i = i.replace("\n", "")
            i = i.replace("\r", "")
            for c in i:
                alphabet.add(c)
    return alphabet

class DFA():
    def __init__(self, language=set()):
        self.valid_states = set() # Set of valid states.
        self.language = language # Set of valid characters.
        self.transitions = {} # Dictionary of transition functions.
        self.start_state = None # Starting state.
        self.accept_states = set() # Set of accepting states. Subset of valid_states.

    def set_start_state(self, state):
        """Sets the given state as the start_state, adds to valid_states"""
        self.start_state = state
        self.valid_states.add(state)
    
    def add_state(self, state):
        self.valid_states.add(state)

    def add_accept_state(self, state):
        """Adds the given state to the set of Accept_states"""
        if state in self.valid_states:
          self.accept_states.add(state)
        else:
          print ("accept state is not contained in valid_states!")

    def add_transition(self, begin_state, end_state, symbol):
            """Adds a new transition function to the transitions dictionary.

            Keyword Arguments:
            begin_state -- the state in which you begin transition
            end_state -- the state in which you are in when transition ends
            symbol -- the symbol which triggers this transition
            """
            self.valid_states.add(begin_state)
            self.valid_states.add(end_state)
            if begin_state in self.transitions:
              if end_state in self.transitions[begin_state]:
                self.transitions[begin_state][end_state] = symbol
            else:
              self.transitions[begin_state] = {end_state: symbol}

class NFA(DFA):

    def __init__(self, language=set()):
        self.valid_states = set() # Set of valid states.
        self.language = language # Set of valid characters.
        self.transitions = {} # Dictionary of transition functions.
        self.start_state = None # Starting state.
        self.accept_states = set() # Set of accepting states. Subset of valid_states.

    def add_transition(self, begin_state, end_state, symbols):
        """Adds a new transition function to the transitions dictionary.

        Keyword Arguments:
        begin_state -- the state in which you begin transition
        end_state -- the state in which you are in when transition ends
        symbols -- the symbols which trigger this transition
        """
        self.valid_states.add(begin_state)
        self.valid_states.add(end_state)
        if begin_state in self.transitions:
            if end_state in self.transitions[begin_state]:
                self.transitions[begin_state][end_state] = symbols
        else:
            self.transitions[begin_state] = {end_state: symbols}

def re2post(expression):
    '''Heavily influcenced by Ken Thompson's work on re -> nfa''''
    tempstack = []
    atomic_chars = 0
    pipes = 0
    result = []
    for char in expression:
        if char == '(':
            if atomic_chars == 2:
                result.append('.')
                atomic_chars = 1
            tempstack.append((atomic_chars, pipes))
            atomic_chars = 0
            pipes = 0
        elif char == ')':
            if atomic_chars == 2: 
                result.append('.')
            if pipes: 
                result.append('|'*pipes)
            atomic_chars,pipes = tempstack.pop()
            atomic_chars = atomic_chars + 1
        elif char == '*' or char == '?' or char == '+': 
            result.append(char)
        elif char == '|':
            if atomic_chars == 2: 
                result.append('.')
            atomic_chars = 0
            pipes = pipes + 1
        else:
            if atomic_chars == 2: 
                result.append('.')
                atomic_chars = atomic_chars - 1
            result.append(char)
            atomic_chars = atomic_chars + 1
    
    if atomic_chars == 2: 
        result.append('.')
    if pipes: 
        result.append('|'*pipes)

    return result
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

    def add_accept_state(self, state):
        """Adds the given state to the set of Accept_states"""
        if state in self.valid_states:
          self.accept_states.add(state)
        else:
          print "accept state is not contained in valid_states!"

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
    """Adds a new transition function to the transitions dictionary.

    Keyword Arguments:
    begin_state -- the state in which you begin transition
    end_state -- the state in which you are in when transition ends
    symbols -- the symbols which trigger this transition
    """
    def add_transition(self, begin_state, end_state, symbols):
        self.valid_states.add(begin_state)
        self.valid_states.add(end_state)
        if begin_state in self.transitions:
            if end_state in self.transitions[begin_state]:
                self.transitions[begin_state][end_state] = symbols
        else:
            self.transitions[begin_state] = {end_state: symbols}

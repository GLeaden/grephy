class DFA():
  def __init__(self, language=set()):
    self.validStates = set() # Set of valid states.
    self.language = language # Set of valid characters.
    self.transitions = {} # Dictionary of transition functions.
    self.startState = None # Starting state.
    self.acceptStates = set() # Set of accepting states. Subset of validStates. DFAs will have one.

  def setStartState(self, state):
    """Sets the given state as the startState, adds to validStates"""
    self.startState = state
    self.validStates.add(state)

  def addAcceptState(self, state):
    """Adds the given state to the set of AcceptStates"""
    if state in self.validStates:
      self.acceptStates.add(state)
    else:
      print("accept state is not contained in validStates!")

  def addTransition(self, beginState, endState, symbol):
    """Adds a new transition function to the transitions dictionary.

    Keyword Arguments:
    beginState -- the state in which you begin transition
    endState -- the state in which you are in when transition ends
    symbol -- the symbol which triggers this transition
    """
    self.validStates.add(beginState)
    self.validStates.add(endState)
    if beginState in transitions:
      if endState in transitions[beginState]:
        transitions[beginState][endState] = symbol
    else:
      transitions[beginState] = {endState: symbol}

class NFA(DFA):
  """Adds a new transition function to the transitions dictionary.

    Keyword Arguments:
    beginState -- the state in which you begin transition
    endState -- the state in which you are in when transition ends
    symbols -- the symbols which trigger this transition
    """
  def addTransition(self, beginState, endState, symbols):
    self.validStates.add(beginState)
    self.validStates.add(endState)
    if beginState in transitions:
      if endState in transitions[beginState]:
        transitions[beginState][endState] = symbols
    else:
      transitions[beginState] = {endState: symbols}
class Agent:
  """
  An agent must define a getAction method, but may also define the
  following methods which will be called if they exist:

  def registerInitialState(self, state): # inspects the starting state
  """
  def __init__(self, index=0):
    self.index = index

  def getAction(self, state):
    """
    The Agent will receive a GameState (from either {pacman, capture, sonar}.py) and
    must return an action from Directions.{North, South, East, West, Stop}
    """
    raiseNotDefined()

class KeyboardAgent(Agent):

  def getAction(self, state):
    actions = state.getLegalActions(self.index)
    print '===========STATE BEGIN===========\n',state,'\n===========STATE END============='
    while True:
      print 'Please enter the number of action from the following list: '
      for a, i in enumerate(actions):
        print '(%d): %s' % (i+1, str(a))
      action = raw_input()
      if action <= len(actions):
        return actions[action-1]
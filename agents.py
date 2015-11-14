from actions import *
import random

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
    if len(actions) == 1:
      print "Agent %d takes %s: %s" % (self.index, state.nextActionType, str(actions[0]))
      return actions[0]
    print '===========STATE BEGIN===========\n',state,'\n===========STATE END============='
    while True:
      print 'Please enter the number of action from the following list: '
      for i, a in enumerate(actions):
        print '(%d): %s' % (i+1, str(a))
      try:
        action = int(raw_input())
        if action <= len(actions):
          return actions[action-1]
      except:
        print 'Invalid number, try again...'

class RandomAgent(Agent):

  def getAction(self, state):
    actions = state.getLegalActions(self.index)
    actions = [x for x in actions if not isinstance(x, Challenge)]
    a = random.choice(actions)
    print "Agent %d takes %s: %s" % (self.index, state.nextActionType, str(a))
    return a

class ReflexAgent(Agent):

  def evaluationFunction(self, state):
    selfState = state.players[self.index]
    otherStates = [x for x in state.players if x.playerIndex != self.index]
    
    ownInfluences = len(selfState.influences)
    otherInfluences = sum([len(x.influences) for x in otherStates])

    return ownInfluences - otherInfluences

  def getAction(self, state):
    actionList = state.getBluffActions(self.index)
    return max([(self.evaluationFunction(state.generateSuccessor(a)), a) for a in actionList])[1]

class LookaheadAgent(Agent):

  def evaluationFunction(self, state):
    score = 0
    playerState = state.players[self.index]
    score += len(playerState.influences) * 100
    score += playerState.coins
    for i, p in enumerate(state.players):
      if i != self.index:
        score -= 10 * len(p.influences)
    print 'score', score
    return score

  def getAction(self, state):

    def vopt(s, d):
      print 'vopt called'
      if d == 0:
        return self.evaluationFunction(s), None
      possibleActions = []
      print s.detailedStr()
      print s.playersCanAct
      for player in s.playersCanAct:
        for action in s.getAllActions(player):
          print player, action
          newStates = s.generateSuccessorStates(action, player)
          for s in newStates:
            print 'calling vopt from depth %d' % d
            possibleActions.append((vopt(s, d - 1)[0], action))
      return max(possibleActions)

    v, a = vopt(state, 1)
    return a
















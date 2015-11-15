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

  def printAction(self, a, state):
    print "Agent %d takes %s: %s" % (self.index, state.nextActionType, str(a))

class KeyboardAgent(Agent):

  def getAction(self, state):
    actions = state.getLegalActions(self.index)
    if len(actions) == 1:
      print "Agent %d takes %s: %s" % (self.index, state.nextActionType, str(actions[0]))
      return actions[0]
    print '===========STATE BEGIN===========\n',state.detailedStr(),'\n===========STATE END============='
    while True:
      print 'Please enter the number of action from the following list: '
      for i, a in enumerate(actions):
        print '(%d): %s' % (i+1, str(a))
      try:
        action = int(raw_input())
        if action <= len(actions):
          self.printAction(action, state)
          return actions[action-1]
      except:
        print 'Invalid number, try again...'

class RandomAgent(Agent):

  def getAction(self, state):
    actions = state.getLegalActions(self.index)
    a = random.choice(actions)
    self.printAction(a, state)
    return a

class RandomAgentExcludeChallenge(Agent):

  def getAction(self, state):
    actions = state.getLegalActions(self.index)
    actions = [x for x in actions if not isinstance(x, Challenge)]
    a = random.choice(actions)
    self.printAction(a, state)
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
    a = max([(self.evaluationFunction(state.generateSuccessor(a)), a) for a in actionList])[1]
    self.printAction(a, state)
    return a

class LookaheadAgent(Agent):

  def evaluationFunction(self, state):
    score = 0
    playerState = state.players[self.index]
    score += len(playerState.influences) * 100
    score += playerState.coins
    for i, p in enumerate(state.players):
      if i != self.index:
        score -= 10 * len(p.influences)
    score += sum([-100 if x == self.index else +10 for x in state.punishedPlayers ])
    print 'score', score
    return score

  def getAction(self, state):

    def vopt(s, d):
      if s.isOver():
        return 10000, [None]
      print 'vopt called: depth %d' %d
      if d == 0:
        print s.detailedStr()
        return self.evaluationFunction(s), None
      possibleActions = []
      print s.playersCanAct
      for player in s.playersCanAct:
        for action in s.getAllActions(player):
          # print 'THIS IS S', s.detailedStr()
          newStates = s.generateSuccessorStates(action, player)
          # print 'THIS IS NEWSTATES[0] at d=%d performing action %s' %(d, action), newStates[0].detailedStr()
          # print 'Player %d has %d states from action %s' % (player, len(newStates), action)
          for successorState in newStates:
            print 'calling vopt from depth %d' % d
            possibleActions.append((vopt(successorState, d - 1)[0], action))
      return max(possibleActions)

    v, a = vopt(state.deepCopy(), 5)
    self.printAction(a, state)
    return a

class OracleAgent(Agent):

  def evaluationFunction(self, state):
    score = 0
    playerState = state.players[self.index]
    score += len(playerState.influences) * 100
    score += playerState.coins
    for i, p in enumerate(state.players):
      if i != self.index:
        score -= 10 * len(p.influences)
    score += sum([-100 if x == self.index else +10 for x in state.punishedPlayers ])
    return score

  def getAction(self, state):
    def vopt(s, d):
      if s.isOver():
        if len(state.players[self.index].influences) >0:
          return 99999999, [None]
        return -9999999, [None]
      if d == 0:
        return self.evaluationFunction(s), None
      possibleActions = []
      for player in s.playersCanAct:
        tempActions = []
        for action in s.getLegalActions(player):
          # print 'THIS IS S', s.detailedStr()
          newStates = s.generateSuccessorStates(action, player)
          # print 'THIS IS NEWSTATES[0] at d=%d performing action %s' %(d, action), newStates[0].detailedStr()
          # print 'Player %d has %d states from action %s' % (player, len(newStates), action)
          for successorState in newStates:
            tempActions.append((vopt(successorState, d - 1)[0], action))
        if player == self.index:
          possibleActions.append(max(tempActions))
        else:
          possibleActions.append(min(tempActions))
      return max(possibleActions)

    v, a = vopt(state.deepCopy(), 5)
    self.printAction(a, state)
    return a

class ExpectimaxAgent(Agent):

  def evaluationFunction(self, state):
    score = 0
    playerState = state.players[self.index]
    score += len(playerState.influences) * 100
    score += playerState.coins
    for i, p in enumerate(state.players):
      if i != self.index:
        score -= 10 * len(p.influences)
    score += sum([-100 if x == self.index else +10 for x in state.punishedPlayers ])
    return score

  def getAction(self, state):
    def vopt(s, d, requirePlayerAction=None):
      if s.isOver():
        if len(state.players[self.index].influences) >0:
          return 10000, [None]
        return -10000, [None]
      if d == 0:
        return self.evaluationFunction(s), None
      voptForSelf = ()
      voptForEachOpponent = []
      for player in s.playersCanAct:
        voptForActionProbability = []
        for action in (s.getAllActions(player) if player != self.index else s.getLegalActions(player)):
          newStates = s.generateSuccessorStates(action, player)
          for successorState in newStates:
            requiredInfluences = s.requiredInfluencesForState(successorState)
            probability = 1
            for p in requiredInfluences:
              possibleInfluences = s.players[p].possibleInfluences
              normalization = sum([possibleInfluences[i] for i in possibleInfluences])
              influenceList, hasInfluence = requiredInfluences[p]
              influenceSum = sum([possibleInfluences[x] for x in influenceList])
              product = ((normalization - influenceSum) / normalization) ** len(s.players[p].influences)
              probability *= 1 - product if hasInfluence else product
            nextVopt = vopt(successorState, d - 1)
            voptForActionProbability.append((nextVopt[0], action, probability))
        if player == self.index:
          actionToValueProb = {}
          for value, action, probability in voptForActionProbability:
            if action in actionToValueProb:
              actionToValueProb[action].append((value, probability))
            else:
              actionToValueProb[action] = [(value, probability)]
          actionToValue = {a: sum([v * p for v, p in actionToValueProb[a]]) for a in actionToValueProb}
          for a in actionToValue:
            n = sum([p for v, p in actionToValueProb[a]])
            actionToValue[a] = actionToValue[a] if n != 0 else 0
          maxAction = max(actionToValue, key=lambda x : actionToValue[x])
          maxValue = actionToValue[maxAction]
          voptForSelf = (maxValue, maxAction)
        else:
          expectedVopt = 0
          normalizationConstant = 0
          for value, action, probability in voptForActionProbability:
            expectedVopt += value * probability
            normalizationConstant += probability
          expectedVopt = expectedVopt/float(normalizationConstant) if normalizationConstant != 0 else 0
          voptForEachOpponent.append(expectedVopt)
      opponentVopt = min(voptForEachOpponent) if len(voptForEachOpponent) > 0 else None
      # raw_input()
      # print 'voptForSelf:', voptForSelf, 'd=', d, '\nvoptForEachOpponent:', voptForEachOpponent
      if opponentVopt is None:
        return voptForSelf
      elif len(voptForSelf) == 0:
        return opponentVopt, None
      else:
        return max([opponentVopt, voptForSelf])

    v, a = vopt(state.deepCopy(), 5, self.index)
    self.printAction(a, state)
    return a

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

class LyingRandomAgent(Agent):

  def getAction(self, state):
    actions = state.getAllActions(self.index)     
    a = random.choice(actions)
    self.printAction(a, state)
    return a

class LyingRandomAgentExcludeChallenge(Agent):

  def getAction(self, state):
    actions = state.getAllActions(self.index)
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
    a = max([(self.evaluationFunction(state.generateSuccessors(a)), a) for a in actionList])[1]
    self.printAction(a, state)
    return a

class LyingKillAgent(Agent):

  def findAction(self, actionList, query):
    for action in actionList:
      if action and action.type == query:
        return action
    return None

  def getAction(self, state):
    selfState = state.players[self.index]
    actionList = state.getAllActions(self.index)
    random.shuffle(actionList)
    actionList = [x for x in actionList if x is None or  x.type != 'challenge']
    a = self.findAction(actionList, 'block')
    if a:
      self.printAction(a, state)
      return a
    if random.random() > 0.5:
      a = self.findAction(actionList, 'assassinate')
      if a:
        self.printAction(a, state)
        return a
    else:
      a = self.findAction(actionList, 'coup')
      if a:
        print actionList
        self.printAction(a, state)
        return a
    a = self.findAction(actionList, 'tax')
    if a:
      self.printAction(a, state)
      return a
    a = random.choice(actionList)
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

# does this do what we think it does?? ....
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
          newStates = s.generateSuccessorStates(action, player)
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

# doesn't know anybody's cards when looking at probability
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

  def getActions(self, player, s):
    return s.getAllActions(player) if player != self.index else s.getLegalActions(player)

  def findProbability(self, state, successorState):
    requiredInfluences = state.requiredInfluencesForState(successorState)
    probability = 1
    for p in requiredInfluences:
      possibleInfluences = state.players[p].possibleInfluences
      normalization = sum([possibleInfluences[i] for i in possibleInfluences])
      influenceList, hasInfluence = requiredInfluences[p]
      influenceSum = sum([possibleInfluences[x] for x in influenceList])
      product = ((normalization - influenceSum) / normalization) ** len(state.players[p].influences)
      probability *= 1 - product if hasInfluence else product
      # new addition: know our own influences
      if p == self.index:
        influenceList, hasInfluence = requiredInfluences[p]
        hasAny = False
        selfInfluences = state.players[p].influences
        for influence in influenceList:
          if influence in selfInfluences:
            hasAny = True
        if hasInfluence:
          probability = 1 if hasAny else 0 
        else:
          probability = 0 if hasAny else 1
    return probability

  def getAction(self, state):
    def vopt(s, d ):
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
        for action in self.getActions(player, s):
          newStates = s.generateSuccessorStates(action, player)
          for successorState in newStates:
            nextVopt = vopt(successorState, d - 1)
            probability = self.findProbability(s, successorState)
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
      if opponentVopt is None:
        return voptForSelf
      elif len(voptForSelf) == 0:
        return opponentVopt, None
      else:
        return max([opponentVopt, voptForSelf])

    v, a = vopt(state.deepCopy(), 5)
    self.printAction(a, state)
    return a

class LyingExpectimaxAgent(ExpectimaxAgent):

  def getActions(self, player, s):
    return s.getAllActions(player)

class OracleExpectimaxAgent(ExpectimaxAgent):
  
  def findProbability(self, state, successorState):
    requiredInfluences = state.requiredInfluencesForState(successorState)
    probability = 1
    for p in requiredInfluences:
      if p == self.index:
        influenceList, hasInfluence = requiredInfluences[p]
        hasAny = False
        selfInfluences = state.players[p].influences
        for influence in influenceList:
          if influence in selfInfluences:
            hasAny = True
        if hasInfluence:
          probability = 1 if hasAny else 0 
        else:
          probability = 0 if hasAny else 1
    return probability

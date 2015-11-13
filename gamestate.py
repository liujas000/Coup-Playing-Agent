import collections
import random
from actions import *
import util

class GameState:

  def __init__( self, prevState = None ):
    """
    Generates a new state by copying information from its predecessor.
    """
    if prevState is None:
      self.players = []
      self.numPlayers = 0
      self.playerTurn = 0
      self.currentAction = None
      self.playerExchange = None
      self.playerChallenge = None
      self.playerBlock = None
      self.playerTarget = None
      self.punishedPlayers = []
      self.deck = []
      self.inactiveInfluences = collections.Counter()
      self.pastActions = [] #list of counters, one for each player
      self.nextActionType = None # can be 'action', 'block', 'challenge', 'discard'
      self.challengeSuccess = None
    else:
      self.players = list(prevState.players)
      self.numPlayers = prevState.numPlayers
      self.playerTurn = prevState.playerTurn
      self.currentAction = prevState.currentAction
      self.playerExchange = prevState.playerExchange
      self.playerChallenge = prevState.playerChallenge
      self.playerBlock = prevState.playerBlock
      self.playerTarget = prevState.playerTarget
      self.punishedPlayers = list(prevState.punishedPlayers)
      self.deck = list(prevState.deck)
      self.inactiveInfluences = collections.Counter(prevState.inactiveInfluences)
      self.pastActions = list(prevState.pastActions)
      self.nextActionType = prevState.nextActionType
      self.challengeSuccess = prevState.challengeSuccess
    
  def __eq__( self, other ):
    """
    Allows two states to be compared.
    """

  # def __hash__( self ):
  #   """
  #   Allows states to be keys of dictionaries.
  #   """

  def __str__( self ):
    return """
      Players: %r
      Number Players: %r
      Player Turn: %r
      Current Action: %r
      Next Action Type: %r
      Player Block: %r
      Player Challenge: %r
      Challenge Success: %r
      Player Target: %r
      Player Exchange: %r
      Punished Players: %r
      Past Actions: %r
      Deck: %r
      Inactive Influences: %r
    """ % ([str(player) for player in self.players], self.numPlayers, self.playerTurn, self.currentAction, \
      self.nextActionType, self.playerBlock, self.playerChallenge, self.challengeSuccess, self.playerTarget, \
      self.playerExchange, self.punishedPlayers, self.pastActions, self.deck, self.inactiveInfluences)

  def initialize( self, numPlayers=4 ):
    """
    Creates an initial game state given a number of players.
    """
    self.numPlayers = numPlayers
    self.deck = ['ambassador', 'assassin', 'captain', 'contessa', 'duke'] * 3
    random.shuffle(self.deck)
    for i in range(numPlayers):
      nextInfluences = self.deck[0:2]
      self.deck = self.deck[2:]
      s = PlayerState(i, nextInfluences) #initalizes player state with index number and two cards to have
      self.players.append(s)
    self.activePlayers = range(numPlayers)

  def getLegalActions( self, playerIndex=0 ):
    playerState = self.players[playerIndex]
    if len(playerState.influences) == 0:
      return [None]
    if self.nextActionType == 'action':
      indexList = [x.playerIndex for x in self.players if len(x.influences) > 0 and x.playerIndex != playerIndex]
      if self.playerTurn != playerIndex:
        return []
      result = ['income', 'foreign aid']
      if playerState.coins >= 10:
        return util.ActionGenerator(['coup'], playerIndex=playerIndex, otherPlayers=indexList)
      if playerState.coins >= 7:
        result += ['coup']
      #now, we look at Influences
      for influence in playerState.influences:
        if influence in util.influenceToAction:
          if influence != 'assassin' or playerState.coins >= 3:
            result.append(util.influenceToAction[influence])
      return util.ActionGenerator(result, playerIndex=playerIndex, otherPlayers=indexList)
    elif self.nextActionType == 'block':
      #if the action is steal or assassination, then only the target can block
      #if action is foreign aid, anyone can block
      if self.playerTurn == playerIndex:
        return [None]
      if self.currentAction == 'foreign aid' or (self.currentAction in ['steal', 'assassinate'] and playerIndex == self.playerTarget):
        for influence in playerState.influences:
          if self.currentAction in util.blockToInfluence and influence in util.blockToInfluence[self.currentAction]:
            return util.ActionGenerator(['block'], playerIndex=playerIndex) + [None]
      return [None]
    elif self.nextActionType == 'challenge':
      if self.currentAction not in util.basicActions and ((self.playerBlock is not None and playerIndex != self.playerBlock) \
        or (self.playerBlock is None and playerIndex != self.playerTurn)):
        return util.ActionGenerator(['challenge'], playerIndex=playerIndex) + [None]
      else:
        return [None]
    elif self.nextActionType == 'discard':
      return util.ActionGenerator(['discard'], playerIndex=playerIndex, numInfluences=len(self.players[playerIndex].influences))

  def getBluffActions( self, playerIndex=0 ):
    playerState = self.players[playerIndex]
    if len(playerState.influences) == 0:
      return []
    if self.nextActionType == 'action':
      indexList = [x.playerIndex for x in self.players if len(x.influences) > 0 and x.playerIndex != playerIndex]
      if self.playerTurn != playerIndex:
        return []
      if playerState.coins >= 10:
        return []
      for influence in util.influenceList:
        if influence not in playerState.influences:
          if influence in util.influenceToAction:
            if influence != 'assassin' or playerState.coins >= 3:
              result.append(util.influenceToAction[influence])
      return util.ActionGenerator(result, playerIndex=playerIndex, otherPlayers=indexList)
    elif self.nextActionType == 'block':
      if self.playerTurn == playerIndex:
        return []
      if self.currentAction == 'foreign aid' or (self.currentAction in ['steal', 'assassinate'] and playerIndex == self.playerTarget):
        canBlock = False
        for influence in self.characters:
          if influence in util.blockToInfluence[self.currentAction]
            canBlock = True
        if canBlock:
          return []
        else:
          return util.ActionGenerator(['block'], playerIndex=playerIndex)
      else:
        return []
    elif self.nextActionType == 'challenge':
      return []
    elif self.nextActionType == 'discard':
      return []

  def finishTurn(self):
    self.currentAction = None
    self.playerChallenge = None
    self.playerBlock = None
    self.playerTarget = None
    self.playerExchange = None
    self.punishedPlayers = []
    self.challengeSuccess = None
    while True:
      self.playerTurn = (self.playerTurn + 1) % self.numPlayers
      if len(self.players[self.playerTurn].influences) > 0:
        break

  # Returns:
  #   Dictionary{ Player -> ([list of influences], boolean hasInfluence}
  #   nextState can follow self if:
  #     if hasInfluence: Player must have at least one influence in list
  #     if not hasInfluence: Player must not have any influences in list
  def requiredInfluencesForState(self, nextState):
    requiredInfluences = {}
    if self.nextActionType == 'action':
      requiredInfluences[self.playerTurn] = (util.actionToInfluence[nextState.currentAction], True)
    elif self.nextActionType == 'block' and nextState.playerBlock is not None:
      requiredInfluences[nextState.playerBlock] = (util.blockToInfluence[self.currentAction], True)
    elif self.nextActionType == 'challenge' and nextState.playerChallenge is not None:
      if self.playerBlock == None:
        requiredInfluences[self.playerTurn] = (util.actionToInfluence[self.currentAction], not nextState.challengeSuccess)
      else:
        requiredInfluences[self.playerBlock] = (util.blockToInfluence[self.currentAction], not nextState.challengeSuccess)
    # discard?
    return requiredInfluences

  def isOver( self ):
    activePlayers = [1 for player in self.players if len(player.influences) > 0]
    return sum(activePlayers) <= 1

  def printState(self):
    print self

  def deepCopy( self ):
    return GameState(self)


class PlayerState:
  """
  PlayerStates hold the state of a player (index, Influences etc).
  """

  def __init__( self, index, influences ):
    
    self.playerIndex = index
    self.influences = influences
    self.coins = 2
    self.inactiveInfluences = []
    self.revealedInfluences = []
    self.possibleInfluences = collections.Counter()

  def __str__( self ):
    return str(self.playerIndex) + ': ' + str(self.influences) + ' (%d coins)' % self.coins

  # def __eq__( self, other ):

  # def __hash__(self):

  # def copy( self ):


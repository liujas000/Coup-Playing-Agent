import collections
from actions import *

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
      self.inactiveCharacters = collections.Counter()
      self.pastActions = [] #list of counters, one for each player
      self.nextActionType = None # can be 'action', 'block', 'challenge', 'discard'
    else:
      self.players = list(prevState.players)
      self.numPlayers = prevState.numPlayers
      self.playerTurn = prevState.playerTurn
      self.currentAction = prevState.currentAction
      self.playerExchange = prevState.playerExchange
      self.playerBlock = prevState.playerBlock
      self.playerTarget = prevState.playerTarget
      self.punishedPlayers = list(prevState.punishedPlayers)
      self.deck = list(prevState.deck)
      self.inactiveCharacters = collections.Counter(prevState.inactiveCharacters)
      self.pastActions = list(prevState.pastActions)
      self.nextActionType = prevState.nextActionType
    
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
      Active Players: %r
      Number Players: %r
      Player Turn: %r
      Current Action: %r
      Next Action Type: %r
      Player Block: %r
      Player Challenge: %r
      Player Target: %r
      Player Exchange: %r
      Punished Players: %r
      Past Actions: %r
      Deck: %r
      Inactive Characters: %r
    """ % (self.players, self.activePlayers, self.numPlayers, self.playerTurn, self.currentAction, \
      self.nextActionType, self.playerBlock, self.playerChallenge, self.playerTarget, self.playerExchange, \
      self.punishedPlayers, self.pastActions, self.deck, self.inactiveCharacters)

  def initialize( self, numPlayers=4 ):
    """
    Creates an initial game state given a number of players.
    """
    self.deck = random.shuffle(['ambassador', 'assassin', 'captain', 'contessa', 'duke'] * 3)
    for i in range(numPlayers):
      nextCharacters = self.deck[0:2]
      self.deck = self.deck[2:]
      s = playerState(i, nextCharacters) #initalizes player state with index number and two cards to have
      self.players.append(s)
    self.activePlayers = range(numPlayers)

  def getLegalActions( self, playerIndex=0 ):
    playerState = self.players[playerIndex]
    if self.nextActionType == 'action':
      indexList = [x.playerIndex for x in self.players if x.playerIndex != playerIndex]
      if self.playerTurn != playerIndex:
        return []
      result = ['income', 'foreign aid']
      if playerState.coins >= 10:
        return ActionGenerator(['coup'], playerIndex=playerIndex, indexList=indexList)
      if playerState.coins >= 7:
        result += ['coup']
        # coupActions = [Coup(x.playerIndex) for x in self.players if len(x.characters) > 0 and x.playerIndex != playerIndex]
      #now, we look at characters
      for character in playerState.characters:
        if character in util.characterToAction:
          result.append(util.characterToAction[character])
      return ActionGenerator(result, playerIndex=playerIndex, indexList=indexList)
    elif self.nextActionType == 'block':
      if self.playerTurn == playerIndex:
        return [None]
      for character in playerState.characters:
        if character in blockToCharacter[self.currentAction]:
          return ActionGenerator(['block'], playerIndex=playerIndex) + [None]
      return [None]
    elif self.nextActionType == 'challenge':
      return ActionGenerator(['challenge'], playerIndex=playerIndex) + [None]
    elif self.nextActionType == 'discard':
      return ActionGenerator(['discard'], playerIndex=playerIndex, numCharacters=len(self.players[playerIndex].characters))

  def finishTurn(self):
    self.currentAction = None
    self.playerChallenge = None
    slef.playerBlock = None
    self.playerTarget = None
    self.playerExchange = None
    self.punishedPlayers = []

  def isOver( self ):
    len(self.activePlayers) <= 1

  def printState(self):
    print self

  def deepCopy( self ):
    return GameState(self)

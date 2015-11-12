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
    self.deck = ['ambassador', 'assassin', 'captain', 'contessa', 'duke'] * 3
    random.shuffle(self.deck)
    for i in range(numPlayers):
      nextCharacters = self.deck[0:2]
      self.deck = self.deck[2:]
      s = PlayerState(i, nextCharacters) #initalizes player state with index number and two cards to have
      self.players.append(s)
    self.activePlayers = range(numPlayers)

  def getLegalActions( self, playerIndex=0 ):
    playerState = self.players[playerIndex]
    if self.nextActionType == 'action':
      indexList = [x.playerIndex for x in self.players if len(x.characters) > 0 and x.playerIndex != playerIndex]
      if self.playerTurn != playerIndex:
        return []
      result = ['income', 'foreign aid']
      if playerState.coins >= 10:
        return util.ActionGenerator(['coup'], playerIndex=playerIndex, otherPlayers=indexList)
      if playerState.coins >= 7:
        result += ['coup']
        # coupActions = [Coup(x.playerIndex) for x in self.players if len(x.characters) > 0 and x.playerIndex != playerIndex]
      #now, we look at characters
      for character in playerState.characters:
        if character in util.characterToAction:
          result.append(util.characterToAction[character])
      return util.ActionGenerator(result, playerIndex=playerIndex, otherPlayers=indexList)
    elif self.nextActionType == 'block':
      if self.playerTurn == playerIndex:
        return [None]
      for character in playerState.characters:
        if character in blockToCharacter[self.currentAction]:
          return util.ActionGenerator(['block'], playerIndex=playerIndex) + [None]
      return [None]
    elif self.nextActionType == 'challenge':
      return util.ActionGenerator(['challenge'], playerIndex=playerIndex) + [None]
    elif self.nextActionType == 'discard':
      return util.ActionGenerator(['discard'], playerIndex=playerIndex, numCharacters=len(self.players[playerIndex].characters))

  def finishTurn(self):
    self.currentAction = None
    self.playerChallenge = None
    slef.playerBlock = None
    self.playerTarget = None
    self.playerExchange = None
    self.punishedPlayers = []

  def isOver( self ):
    all([len(player.characters) == 0 for player in self.players])

  def printState(self):
    print self

  def deepCopy( self ):
    return GameState(self)


class PlayerState:
  """
  PlayerStates hold the state of a player (index, characters etc).
  """

  def __init__( self, index, characters ):
    
    self.playerIndex = index
    self.characters = characters
    self.coins = 2
    self.inactiveCharacters = []
    self.revealedCharacters = []

  def __str__( self ):
    return str(self.index)

  # def __eq__( self, other ):

  # def __hash__(self):

  # def copy( self ):


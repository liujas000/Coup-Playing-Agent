import collections

class GameState:

  def getLegalActions( self, playerIndex=0 ):
    playerState = self.players[playerIndex]
    if self.nextActionType == 'action':
      if self.playerTurn != playerIndex:
        return []
      result = ['income', 'foreign aid']
      if playerState.coins >= 10:
        return ['coup']
      elif playerState.coins >= 7:
        result.append('coup')
      #now, we look at characters
      for character in playerState.characters:
        if character in util.characterToAction:
          result.append(util.characterToAction[character])
      return result
    elif self.nextActionType == 'block':
      if self.playerTurn == playerIndex:
        return [None]
      for character in playerState.characters:
        if character in blockToCharacter[self.currentAction]:
          return ['block', None]
      return [None]
    elif self.nextActionType == 'challenge':
      return ['challenge', None]
    elif self.nextActionType == 'discard':
      result = []
      for character, index in enumerate(playerState.characters):
        result.append('discard '+index)
      return result

  def isOver( self ):
    len(self.activePlayers) <= 1

  def printState(self):
    print """
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
    """
    % (self.players, self.activePlayers, self.numPlayers, self.playerTurn, self.currentAction, \
      self.nextActionType, self.playerBlock, self.playerChallenge, self.playerTarget, self.playerExchange, \
      self.punishedPlayers, self.pastActions, self.deck, self.inactiveCharacters)


  #############################################
  #             Helper methods:               #
  # You shouldn't need to call these directly #
  #############################################

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
      self.activePlayers = []
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
      self.activePlayers = list(prevState.activePlayers)
      self.inactiveCharacters = collections.Counter(prevState.inactiveCharacters)
      self.pastActions = list(prevState.pastActions)
      self.nextActionType = prevState.nextActionType
    
  
  def finishTurn(self):
    self.currentAction = None
    self.playerChallenge = None
    slef.playerBlock = None
    self.playerTarget = None
    self.playerExchange = None
    self.punishedPlayers = []
    #punished player


  def deepCopy( self ):
    return GameState(self)


  def __eq__( self, other ):
    """
    Allows two states to be compared.
    """

  # def __hash__( self ):
  #   """
  #   Allows states to be keys of dictionaries.
  #   """

  def __str__( self ):
    out = ''
    for player in self.players:
      out += str(player) + "\n"
    out += 'Current turn:', self.playerTurn
    # out += 



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




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
      self.nextActionType = 'action' # can be 'action', 'block', 'challenge', 'discard'

      # has an action been chosen and by who
      # has a block been chosen and by who
      # has a challenge been chosen and by who
  
  def finishTurn(self):
    self.currentAction = None
    self.playerChallenge = None
    slef.playerBlock = None
    self.playerTarget = None
    #punished player


  def deepCopy( self ):

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




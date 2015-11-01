class GameState:

  def getLegalActions( self, agentIndex=0 ):

  def generateSuccessor( self, action):

  def getPlayerState( self ):

  def getNumAgents( self ):

  def getScore( self ):

  def isLose( self ):

  def isWin( self ):

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
      self.playerChallenge = None
      self.playerBlock = None
      self.playerTarget = None
      self.punishedPlayer = None
      self.deck = []
      self.activePlayers = []
      self.inactiveCharacters = collections.Counter()
      self.pastActions = [] #list of counters, one for each player

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




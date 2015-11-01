from util import *
from util import raiseNotDefined

#######################
# Parts worth reading #
#######################

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

class PlayerState:
  """
  PlayerStates hold the state of a player (index, characters etc).
  """

  def __init__( self, index, characters ):
    
    self.index = index
    self.characters = characters
    self.coins = 2
    self.inactiveCharacters = []
    self.revealedCharacters = []

  def __str__( self ):

  def __eq__( self, other ):

  def __hash__(self):

  def copy( self ):

class Actions:

  def getPossibleActions(config, walls):
    return None
  getPossibleActions = staticmethod(getPossibleActions)

class Game:
  """
  The Game manages the control flow, soliciting actions from agents.
  """

  def __init__( self ):

  def run( self ):
    """
    Main control loop for game play.
    """
    self.display.initialize(self.state.data)
    self.numMoves = 0

    ###self.display.initialize(self.state.makeObservation(1).data)
    # inform learning agents of the game start
    for i in range(len(self.agents)):
      agent = self.agents[i]
      agent.registerInitialState(self.state.deepCopy())

    numAgents = len( self.agents )

    while not self.gameOver:
      # Fetch the next agent
      agent = self.agents[self.state.agentTurn]
      # Generate an observation of the state

      # observation = agent.observationFunction(self.state.deepCopy())
      # observation = self.state.deepCopy()

      def getBlock():
        for agent in self.agents:
          block = agent.getAction(self.state.deepCopy())
          if block:
            return block, agent
        return None, None

      def getChallenge():
        for agent in self.agents:
          challenge = agent.getAction(self.state.deepCopy())
          if challenge:
            return challenge, agent
        return None, None

      def resolveChallenge(challengedPlayer, challengingPlayer, action):
        punished = challengingPlayer if action.isLegal() else challengedPlayer
        if punished == challengingPlayer:
          self.state = action.resolve(self.state)
        else:
          self.state = action.cancel(self.state)
        punishAction = Actions.punish(punished)
        self.state = punishAction.resolve(self.state) #punish is a general Actions method 


      # Solicit an action
      action = agent.getAction(self.state.deepCopy())
      # Execute the action
      # self.state = self.state.generateSuccessor( action )
      self.state = action.choose(self.state)
      block, b_player = getBlock()
      if block:
        challenge, c_player = getChallenge()
        if challenge:
          challenge.resolve(b_player, c_player, block)
        else:
          self.state = action.cancel(self.state) # resolve block?
      else:
        challenge, c_player = getChallenge()
        if challenge:
          challenge.resolve(agent, c_player, action)
        else:
          self.state = action.resolve(self.state)

      #scan gamestate, punish any players necessary, and reset some vars to None
      if self.state.punishedPlayer is not None:
        punishAction = self.agents[punishedPlayer].getAction(self.state.deepCopy())

      self.state.finishTurn()      

      # Allow for game specific conditions (winning, losing, etc.)
      self.rules.process(self.state, self)

      # Next agent
      agentIndex = ( agentIndex + 1 ) % numAgents

    # inform a learning agent of the game result
    for agent in self.agents:
      if "final" in dir( agent ) :
        agent.final( self.state )

    self.display.finish()







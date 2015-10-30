from util import *
from util import raiseNotDefined
import time, os
import traceback

try:
  import boinc
  _BOINC_ENABLED = True
except:
  _BOINC_ENABLED = False

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

class AgentState:
  """
  AgentStates hold the state of an agent (configuration, speed, scared, etc).
  """

  def __init__( self ):

  def __str__( self ):

  def __eq__( self, other ):

  def __hash__(self):

  def copy( self ):

####################################
# Parts you shouldn't have to read #
####################################

class Actions:

  def getPossibleActions(config, walls):
    return None
  getPossibleActions = staticmethod(getPossibleActions)

class GameStateData:
  def __init__( self, prevState = None ):

  def deepCopy( self ):

  def copyAgentStates( self, agentStates ):
    copiedStates = []
    for agentState in agentStates:
      copiedStates.append( agentState.copy() )
    return copiedStates

  def __eq__( self, other ):
    """
    Allows two states to be compared.
    """
    if other == None: return False
    if not self.agentStates == other.agentStates: return False
    return True

  def __hash__( self ):
    """
    Allows states to be keys of dictionaries.
    """
    for i, state in enumerate( self.agentStates ):
      try:
        int(hash(state))
      except TypeError, e:
        print e
        #hash(state)
    # return int((hash(tuple(self.agentStates)) + 13*hash(self.food) + 113* hash(tuple(self.capsules)) + 7 * hash(self.score)) % 1048575 )
    return 0

  def __str__( self ):
    return ''

  def initialize( self, numPlayers):

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

    agentIndex = self.startingIndex
    numAgents = len( self.agents )

    while not self.gameOver:
      # Fetch the next agent
      agent = self.agents[agentIndex]
      move_time = 0
      skip_action = False
      # Generate an observation of the state
      observation = agent.observationFunction(self.state.deepCopy())

      # Solicit an action
      action = None
      action = agent.getAction(observation)

      # Execute the action
      self.moveHistory.append( (agentIndex, action) )
      self.state = self.state.generateSuccessor( agentIndex, action )

      # Change the display
      self.display.update( self.state.data )

      # Allow for game specific conditions (winning, losing, etc.)
      self.rules.process(self.state, self)
      # Track progress
      if agentIndex == numAgents + 1: self.numMoves += 1
      # Next agent
      agentIndex = ( agentIndex + 1 ) % numAgents

      if _BOINC_ENABLED:
        boinc.set_fraction_done(self.getProgress())

    # inform a learning agent of the game result
    for agent in self.agents:
      if "final" in dir( agent ) :
        agent.final( self.state )

    self.display.finish()







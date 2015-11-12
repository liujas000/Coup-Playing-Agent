from util import *
from gamestate import GameState


class Game:
  """
  The Game manages the control flow, soliciting actions from agents.
  """

  def __init__(self, agents = []):
    self.gameOver = False
    state = GameState()
    state.initialize(len(agents))
    self.state = state
    self.agents = agents

  def getBlockOrChallenge(self):
    for agent in self.agents:
      block = agent.getAction(self.state.deepCopy())
      if block is not None:
        return block, agent
    return None, None

  def run( self ):
    """
    Main control loop for game play.
    """
    # for i in range(len(self.agents)):
    #   agent = self.agents[i]
      # agent.registerInitialState(self.state.deepCopy())

    numAgents = len( self.agents )

    while not self.gameOver:
      # Fetch the next agent
      agent = self.agents[self.state.playerTurn]
      # Solicit an action
      self.state.nextActionType = 'action'
      action = agent.getAction(self.state.deepCopy())
      # Execute the action
      # self.state = self.state.generateSuccessor( action )
      self.state = action.choose(self.state)
      self.state.nextActionType = 'block'
      block, b_player = self.getBlockOrChallenge()
      if block is not None:
        self.state = block.choose(self.state)
        self.state.nextActionType = 'challenge'
        challenge, c_player = self.getBlockOrChallenge()
        if challenge is not None:
          challenge.resolve(b_player, c_player, block)
          # resolve initial action?
      else:
        self.state.nextActionType = 'challenge'
        challenge, c_player = self.getBlockOrChallenge()
        if challenge is not None:
          challenge.resolve(agent, c_player, action)
        else:
          self.state = action.resolve(self.state)

      #scan gamestate, punish any players necessary, and reset some vars to None
      if self.state.punishedPlayer is not None:
        punishAction = self.agents[punishedPlayer].getAction(self.state.deepCopy())

      self.state.nextActionType = 'discard'
      for player in self.state.punishedPlayers:
        discardAction = player.getAction(self.state)
        self.state = discardAction.resolve()

      self.state.finishTurn() #resets the vars in gameState to None

      # Allow for game specific conditions (winning, losing, etc.)
      self.rules.process(self.state, self)

      # Next agent
      agentIndex = ( agentIndex + 1 ) % numAgents

    # inform a learning agent of the game result
    for agent in self.agents:
      if "final" in dir( agent ) :
        agent.final( self.state )








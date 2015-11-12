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
        return block
    return None

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
      self.state.nextActionType = 'challenge'
      challenge = self.getBlockOrChallenge()
      if challenge is not None:
        self.state = challenge.choose(self.state)
        self.state = challenge.resolve(self.state)
      if challenge is None or not self.state.challengeSuccess:
        self.state.nextActionType = 'block'
        block = self.getBlockOrChallenge()
        if block is not None:
          self.state = block.choose(self.state)
          self.state.nextActionType = 'challenge'
          challenge = self.getBlockOrChallenge()
          if challenge is not None:
            self.state = challenge.choose(self.state)
            self.state = challenge.resolve(self.state)
            if self.state.challengeSuccess:
              self.state = action.resolve(self.state)
        else:
          self.state = action.resolve(self.state)

      self.state.nextActionType = 'discard'
      for player in self.state.punishedPlayers:
        discardAction = self.agents[player].getAction(self.state)
        self.state = discardAction.resolve(self.state)

      self.state.finishTurn() #resets the vars in gameState to None

      self.gameOver = self.state.isOver()

    # inform a learning agent of the game result
    for agent in self.agents:
      if "final" in dir( agent ) :
        agent.final( self.state )








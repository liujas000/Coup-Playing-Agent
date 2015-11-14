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

  def run( self ):
    """
    Main control loop for game play.
    """
    numAgents = len( self.agents )

    while not self.state.isOver():
      for player in self.state.playersCanAct:
        action = self.agents[player].getAction(self.state)
        if action is not None:
          self.state = action.choose(self.state)
          break
      self.state = self.state.continueTurn()

    print "Game over! Final state: \n", self.state








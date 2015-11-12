from game import Game
from agents import *
import util 
import sys, time, random, os # which ones of these do we need?


# class GameRules:
#   def __init__(self, timeout=30):
#     self.timeout = timeout

#   def newGame(self):
#     game = Game()
#     return game

#   def process(self, state, game):
#     """
#     Checks to see whether it is time to end the game.
#     """
#     if state.isOver(): self.end(state, game)

#   def end( self, state, game ):
#     print "Game over!", state
#     game.gameOver = True

# class PlayerRules:

#   def getLegalActions( state ):
#     """
#     Returns a list of possible actions.
#     """
#     return Actions.getPossibleActions()

#   def applyAction( state, action ):
#     """
#     Edits the state to reflect the results of the action.
#     """
#     legal = PacmanRules.getLegalActions( state )
#     if action not in legal:
#       raise Exception("Illegal action " + str(action))
#     # do something
#   applyAction = staticmethod( applyAction )

def default(str):
  return str + ' [Default: %default]'

def readCommand( argv ):
  """
  Processes the command used to run pacman from the command line.
  """
  from optparse import OptionParser
  usageStr = """
  USAGE:      python pacman.py <options>
  EXAMPLES:   (1) python pacman.py
                  - starts an interactive game
              (2) python pacman.py --layout smallClassic --zoom 2
              OR  python pacman.py -l smallClassic -z 2
                  - starts an interactive game on a smaller board, zoomed in
  """
  parser = OptionParser(usageStr)

  parser.add_option('-n', '--numGames', dest='numGames', type='int',
                    help=default('the number of GAMES to play'), metavar='GAMES', default=1)

  options, otherjunk = parser.parse_args(argv)
  if len(otherjunk) != 0:
    raise Exception('Command line input not understood: ' + str(otherjunk))
  args = dict()

  args['numGames'] = options.numGames

  return args

def runGames(numGames=1):
  agents = [KeyboardAgent(x) for x in range(3)]
  game = Game(agents) 
  game.run()

if __name__ == '__main__':

  args = readCommand( sys.argv[1:] ) # Get game components based on input
  runGames( **args )

  # import cProfile
  # cProfile.run("runGames( **args )")
  pass

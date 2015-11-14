from game import Game
from agents import *
import util 
import sys, time, random, os # which ones of these do we need?

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
  # agents = [RandomAgent(x) for x in range(2)]
  # agents.append(KeyboardAgent(2))
  agents = [LookaheadAgent(x) for x in range(1)]
  agents.append(KeyboardAgent(1))
  game = Game(agents) 
  game.run()

if __name__ == '__main__':

  args = readCommand( sys.argv[1:] ) # Get game components based on input
  runGames( **args )

  # import cProfile
  # cProfile.run("runGames( **args )")
  pass

from game import Game
from agents import *
import util 
import sys, time, random, os # which ones of these do we need?
import collections

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

def runGames(numGames=50):
  # agents = [RandomAgent(x) for x in range(2)]
  # agents.append(KeyboardAgent(2))
  #agents = [LookaheadAgent(x) for x in range(3)]
  #agents.append(KeyboardAgent(1))
  # agents = [ExpectimaxAgent(x) for x in range(3)]
  wins = collections.Counter()
  for i in range(numGames):
    agents = [RandomAgent(0), RandomAgent(1), ExpectimaxAgent(2)]
    game = Game(agents) 
    winner = game.run()
    wins[winner] += 1
    print 'Current score:', wins

if __name__ == '__main__':

  args = readCommand( sys.argv[1:] ) # Get game components based on input
  runGames( **args )
  runGames()

  pass

from game import Game
from agents import *
import sys
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

def runGames(numGames=100):
  wins = collections.Counter()
  numGames = 20
  for i in range(numGames):
    agents = [RandomAgentExcludeChallenge(0), RandomAgentExcludeChallenge(1), LyingKillAgent(2)]
    game = Game(agents) 
    winner = game.run()
    wins[winner] += 1
    print 'Current score:', wins

if __name__ == '__main__':

  args = readCommand( sys.argv[1:] ) # Get game components based on input
  runGames( **args )
  runGames()

  pass

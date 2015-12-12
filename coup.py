from game import Game
from agents import *
import sys
import collections
import signal

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

def runAllMatchups():
  signal.signal(signal.SIGALRM, signal_handler)
  names = ['random', 'modified', 'aggressive', 'expectimax', 'liar', 'oracle']
  agents0 = {'random': RandomAgent(0), 'modified': LyingRandomAgentExcludeChallenge(0), \
    'aggressive': LyingKillAgent(0), 'expectimax': ExpectimaxAgent(0), \
    'liar': LyingExpectimaxAgent(0), 'oracle': OracleExpectimaxAgent(0)}
  agents1 = {'random': RandomAgent(1), 'modified': LyingRandomAgentExcludeChallenge(1), \
    'aggressive': LyingKillAgent(1), 'expectimax': ExpectimaxAgent(1), \
    'liar': LyingExpectimaxAgent(1), 'oracle': OracleExpectimaxAgent(1)}
  for i0, n0 in enumerate(names):
    for i1, n1 in enumerate(names):
      if i0 < i1:
        agents = [agents0[n0], agents1[n1]]
        for _ in range(5):
          signal.alarm(10)
          try:
            scoreFile = open('score-count-%s-%s.txt' % (n0, n1), 'a')
            runGames(agents=agents, scoreFile=scoreFile)
            scoreFile.close()
          except Exception, msg:
            print "Timed out!"
            scoreFile.close()


def runGames(numGames=100, agents=[], scoreFile = None):
  wins = collections.Counter()
  numGames = 20
  for i in range(numGames):
    game = Game(agents) 
    winner = game.run()
    wins[winner] += 1
    print 'winner is %r' % winner
    if scoreFile is not None:
      scoreFile.write( str(winner))
      scoreFile.write('\n')
    print 'Current score:', wins

def signal_handler(signum, frame):
  raise Exception("Timed out!")   

if __name__ == '__main__':
  args = readCommand( sys.argv[1:] ) # Get game components based on input
  #runGames( **args )
  runAllMatchups()

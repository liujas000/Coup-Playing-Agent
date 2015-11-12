from actions import *

characterList = ['ambassador', 'assassin', 'captain', 'contessa', 'duke']

characterToAction = {
	'ambassador': 'exchange',
	'assassin': 'assassinate',
	'captain' : 'steal',
	'duke': 'tax'
}

#actionToCharacter
actionToCharacter = {
	'exchange': ['ambassador'],
	'assassinate': ['assassin'],
	'steal': ['captain'],
	'tax': ['duke']
}
#blockToCharacter

blockToCharacter = {
	'steal': ['ambassador', 'captain'],
	'assassinate': ['contessa'],
	'foreign aid': ['duke']
}

characterToBlock = {
	'ambassador' : 'steal',
	'captain' : 'steal',
	'contessa' : 'assassinate',
	'duke:' : 'foreign aid'
}

basicActions = ['income', 'foreign aid', 'coup']
specialActions = ['steal', 'assassinate', 'exchange', 'tax']
blocks = ['steal', 'assassinate', 'foreign aid']

def ActionGenerator(actionList, playerIndex=0, otherPlayers=[], numCharacters=0):
	result = []
	for action in actionList:
		if action == 'income':
			result += [Income()]
		elif action == 'foreign aid':
			result += [ForeignAid()]
		elif action == 'coup':
			result += [Coup(x) for x in otherPlayers]
		elif action == 'block':
			result += [Block(playerIndex)]
		elif action == 'challenge':
			result += [Challenge(playerIndex)]
		elif action == 'tax':
			result += [Tax()]
		elif action == 'assassinate':
			result += [Assassinate(x) for x in otherPlayers]
		elif action == 'exchange':
			result += [Exchange()]
		elif action == 'steal':
			result += [Steal(x) for x in otherPlayers]
		elif action == 'discard':
			result += [Discard(playerIndex, x) for x in range(numCharacters)]


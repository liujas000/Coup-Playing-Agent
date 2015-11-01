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
	
	'steal': ['ambassador', 'captain']
	'assassinate': ['contessa']
	'foreign aid': ['duke']
}

characterToBlock = {
	
	'ambassador' : 'steal',
	'captain' : 'steal',
	'contessa' : 'assassinate',
	'duke:' : 'foreignAid'
}

basicActions = ['income', 'foreign aid', 'coup']
specialActions = ['steal', 'assassinate', 'exchange', 'tax']
blocks = ['steal', 'assassinate', 'foreign aid']



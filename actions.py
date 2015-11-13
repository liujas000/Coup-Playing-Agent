import util

class Action:
  def __init__( self ):
    pass

  def choose(self,gameState):
    pass

  def resolve(self,gameState):
    pass

class Challenge(Action):
  
  def __init__(self, playerChallenge):
    self.playerChallenge = playerChallenge

  def choose(self,gameState):
    gameState.playerChallenge = self.playerChallenge
    return gameState

  def resolve(self,gameState):
    actionIsBlock = gameState.playerBlock is not None
    lastPlayer = gameState.playerBlock if actionIsBlock else gameState.playerTurn
    if not actionIsBlock:
      influences = util.actionToInfluence[gameState.currentAction] #Influence is a list
      #want to see if playerTurn has that Influence
      result = any([True for x in influences if x in gameState.players[gameState.playerTurn].influences] )
      self.punishedPlayer = self.playerChallenge if result else playerTurn 
      self.challengeSuccess = not result
    else:
      influences = util.blockToInfluence[gameState.currentAction] #Influence is a list
      #want to see if playerTurn has that Influence
      result = any([True for x in influences if x in gameState.players[gameState.playerBlock].influences] )
      self.punishedPlayer = self.playerChallenge if result else playerBlock 
      self.challengeSuccess = not result
      gameState.blockSuccess = not self.challengeSuccess 

    gameState.challengeSuccess = self.challengeSuccess
    gameState.punishedPlayers.append(self.punishedPlayer)
    return gameState

  def __str__(self):
    return 'Challenge by  %r' %(self.playerChallenge)

class Tax(Action):

  def choose(self,gameState):
    gameState.currentAction = 'tax'
    gameState.players[gameState.playerTurn].possibleInfluences['duke'] += 1 
    return gameState

  def resolve(self,gameState):
    #Current player's coin amount += 3
    gameState.players[gameState.playerTurn].coins += 3
    return gameState

  def __str__(self):
    return 'Tax'

class Assassinate(Action):

  def __init__(self, target):
    self.target = target

  def choose(self,gameState):
    gameState.currentAction = 'assassinate'
    gameState.players[gameState.playerTurn].possibleInfluences['assassin'] += 1 
    gameState.players[gameState.playerTurn].coins -= 3
    gameState.playerTarget = self.target
    return gameState

  def resolve(self,gameState):
    gameState.punishedPlayers.append(self.target)
    return gameState

  def __str__(self):
    return 'Assassination of: %r' %(self.target)



class Exchange(Action):

  def choose(self,gameState):
    gameState.currentAction = 'exchange'
    gameState.players[gameState.playerTurn].possibleInfluences['ambassador'] += 1 
    return gameState

  def resolve(self,gameState):
    # add 2 cards to players hand
    # TODO: these cards need to be distinguised from punished cards, put back in deck
    gameState.playerExchange = gameState.playerTurn
    addCards = gameState.deck[0:2]
    gameState.deck = gameState.deck[2:]
    gameState.players[gameState.playerTurn].influences += addCards
    gameState.punishedPlayers += [gameState.playerTurn, gameState.playerTurn]
    return gameState

  def __str__(self):
    return 'Exchange'


class Steal(Action):

  def __init__(self, target):
    self.target = target

  def choose(self,gameState):
    gameState.currentAction = 'steal'
    gameState.players[gameState.playerTurn].possibleInfluences['captain'] += 1 
    gameState.playerTarget = self.target
    return gameState

  def resolve(self,gameState):
    stolenCoins = min(gameState.players[self.target].coins, 2)
    gameState.players[self.target].coins -= stolenCoins
    gameState.players[gameState.playerTurn].coins += stolenCoins
    return gameState

  def __str__(self):
    return 'Steal from: %r' %(self.target)


class Income(Action):

  def choose(self,gameState):
    gameState.currentAction = 'income'
    return gameState

  def resolve(self,gameState):
    #Current player's coin amount += 1
    gameState.players[gameState.playerTurn].coins += 1
    return gameState

  def __str__(self):
    return 'Income'

class ForeignAid(Action):

  def choose(self,gameState):
    gameState.currentAction = 'foreign aid'
    return gameState

  def resolve(self,gameState):
    #Current player's coin amount += 2
    gameState.players[gameState.playerTurn].coins += 2
    return gameState

  def __str__(self):
    return 'Foreign Aid'

class Coup(Action):

  def __init__(self, target):
    self.target = target

  def choose(self, gameState):
    gameState.currentAction = 'coup'
    return gameState

  def resolve(self, gameState):
    gameState.players[gameState.playerTurn].coins -= 7
    gameState.punishedPlayers.append(self.target)
    return gameState

  def __str__(self):
    return 'Coup on: %r' % (self.target)

class Block(Action):

  def __init__(self, playerBlock):
    self.playerBlock = playerBlock

  def choose(self, gameState):
    gameState.playerBlock = self.playerBlock
    if gameState.currentAction == 'foreign aid':
      gameState.players[gameState.playerTurn].possibleInfluences['duke'] += 1 
    elif gameState.currentAction == 'assassinate':
      gameState.players[gameState.playerTurn].possibleInfluences['contessa'] += 1 
    elif gameState.currentAction == 'steal':
      gameState.players[gameState.playerTurn].possibleInfluences['captain'] += 0.5
      gameState.players[gameState.playerTurn].possibleInfluences['ambassador'] += 0.5 
    return gameState

  def resolve(self, gameState):
    gameState.blockSuccess = True
    return gameState

  def __str__(self):
    return 'Block by: %r' % (self.playerBlock)

class Discard(Action):

  def __init__(self, player, InfluenceIndex):
    self.influenceIndex = InfluenceIndex
    self.player = player

  def resolve(self, gameState):
    #if the player played ambassador card
    if self.player == gameState.playerExchange:
      gameState.deck.append(gameState.players[self.player].influences[self.influenceIndex])
    else:
      gameState.inactiveInfluences[gameState.players[self.player].influences[self.influenceIndex]] += 1

    del gameState.players[self.player].influences[self.influenceIndex]
    return gameState

  def __str__(self):
    return 'Discard by: %r of: %r' %(self.player, self.influenceIndex)
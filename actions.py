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
    actionIsBlock = gameState.playerBlock is not None
    lastPlayer = gameState.playerBlock if actionIsBlock else gameState.playerTurn
    if not actionIsBlock:
      characters = util.actionToCharacter[gameState.currentAction] #character is a list
      #want to see if playerTurn has that character
      result = any([True for x in characters if x in gameState.players[gameState.playerTurn]] )
      self.punishedPlayer = self.playerChallenge if result else playerTurn 
    else:
      characters = util.blockToCharacter[gameState.currentAction] #character is a list
      #want to see if playerTurn has that character
      result = any([True for x in characters if x in gameState.players[gameState.playerBlock]] )
      self.punishedPlayer = self.playerChallenge if result else playerBlock 
    return gameState

  def resolve(self,gameState):
    gameState.punishedPlayer.append(self.punishedPlayer)
    return gameState

class Tax(Action):

  def choose(self,gameState):
    gameState.currentAction = 'tax'
    return gameState

  def resolve(self,gameState):
    #Current player's coin amount += 3
    gameState.players[gameState.playerTurn].coins += 3
    return gameState

class Assassinate(Action):

  def __init__(self, target):
    self.target = target

  def choose(self,gameState):
    gameState.currentAction = 'assassinate'
    gameState.players[gameState.playerTurn].coins -= 3
    gameState.playerTarget = self.target
    return gameState

  def resolve(gameState):
    gameState.punishedPlayer.append(self.target)
    return gameState



class Exchange(Action):

  def choose(self,gameState):
    gameState.currentAction = 'exchange'
    return gameState

  def resolve(self,gameState):
    # add 2 cards to players hand
    # TODO: these cards need to be distinguised from punished cards, put back in deck
    gameState.playerExchange = gameState.playerTurn
    addCards = gameState.deck[0:2]
    gameState.deck = gameState.deck[2:]
    gameState.punishedPlayer += [self.gameState.playerTurn, self.gameState.playerTurn]
    return gameState


class Steal(Action):

  def __init__(self, target):
    self.target = target

  def choose(self,gameState):
    gameState.currentAction = 'steal'
    gameState.playerTarget = self.target
    return gameState


  def resolve(self,gameState):
    stolenCoins = min(gameState.players[self.target].coins, 2)
    gameState.players[self.target].coins -= stolenCoins
    gameState.players[gameState.playerTurn].coins += stolenCoins
    return gameState

class Income(Action):

  def choose(self,gameState):
    gameState.currentAction = 'income'
    return gameState

  def resolve(self,gameState):
    #Current player's coin amount += 1
    gameState.players[gameState.playerTurn].coins += 1
    return gameState

class ForeignAid(Action):

  def choose(self,gameState):
    gameState.currentAction = 'foreign aid'
    return gameState

  def resolve(self,gameState):
    #Current player's coin amount += 2
    gameState.players[gameState.playerTurn].coins += 2
    return gameState

class Coup(Action):

  def __init__(self, target):
    self.target = target

  def choose(self, gameState):
    gameState.currentAction = 'coup'
    return gameState

  def resolve(self, gameState):
    gameState.punishedPlayer.append(self.target)
    return gameState

class Block(Action):

  def __init__(self, playerBlock):
    self.playerBlock = playerBlock

  def choose(self, gameState):
    gameState.playerBlock = self.playerBlock
    return gameState

  def resolve(self, gameState):
    gameState.playerBlock = None
    return gameState

class Discard(Action):

  def __init__(self, player, characterIndex):
    self.characterIndex = characterIndex
    self.player = player

  def resolve(self, gameState):
    #if the player played ambassador card
    if self.player == gameState.playerExchange:
      gameState.deck.append(gameState.players[self.player].characters[self.characterIndex])

    del gameState.players[self.player].characters[self.characterIndex]
    return gameState
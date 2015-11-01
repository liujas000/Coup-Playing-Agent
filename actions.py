class Action:
  def __init__( self ):
    pass

  def choose(gameState):
    pass

  def resolve(gameState):
    pass

class Challenge(Action):
  
  def __init__(playerChallenge):
    self.playerChallenge = playerChallenge

  def choose(gameState):
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

  def resolve(gameState):
    gameState.punishedPlayer = self.punishedPlayer


class Tax(Action):

  def choose(gameState):
    gameState.currentAction = 'tax'
    return gameState

  def resolve(gameState):
    #Current player's coin amount += 3
    gameState.players[gameState.playerTurn].coins += 3
    return gameState

class Assassinate(Action):

  def __init__(target):
    self.target = target

  def choose(gameState):
    gameState.currentAction = 'assassinate'
    gameState.players[gameState.playerTurn].coins -= 3
    gameState.playerTarget = self.target
    return gameState

  def resolve(gameState):
    gameState.punishedPlayer = self.target
    return gameState



class Exchange(Action):

  def choose(gameState):
    gameState.currentAction = 'exchange'
    return gameState

  def resolve(gameState):
    pass


class Steal(Action):

  def __init__(target):
    self.target = target

  def choose(gameState):
    gameState.currentAction = 'steal'
    gameState.playerTarget = self.target
    return gameState


  def resolve(gameState):
    stolenCoins = min(gameState.players[self.target].coins, 2)
    gameState.players[self.target].coins -= stolenCoins
    gameState.players[gameState.playerTurn].coins += stolenCoins
    return gameState

class Income(Action):

  def choose(gameState):
    gameState.currentAction = 'income'
    return gameState

  def resolve(gameState):
    #Current player's coin amount += 1
    gameState.players[gameState.playerTurn].coins += 1
    return gameState

class ForeignAid(Action):

  def choose(gameState):
    gameState.currentAction = 'foreign aid'
    return gameState

  def resolve(gameState):
    #Current player's coin amount += 2
    gameState.players[gameState.playerTurn].coins += 2
    return gameState

class Coup(Action):

  def __init__(target):
    self.target = target

  def choose(gameState):
    gameState.currentAction = 'coup'
    return gameState

  def resolve(gameState):
    gameState.punishedPlayer = self.target
    return gameState



class Block(Action):

  def choose(gameState):
    gameState.currentAction = 'tax'
    return gameState

  def resolve(gameState):
    #Current player's coin amount += 3
    gameState.players[gameState.playerTurn].coins += 3
    return gameState

class Punish(Action):

    def __init__(gameState, characterIndex):
      self.characterIndex = characterIndex

    def resolve(gameState):
       del gameState.players[gameState.punishedPlayer].characters[characterIndex]
       return gameState
# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
# Amy Eisenmenger (u1209324@utah.edu)


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        # print("bestScores: ", str(scores))
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        currFood = currentGameState.getFood().asList()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        score = successorGameState.getScore()
        # penalize staying put
        if action == 'Stop':
          score -= 5

        # minimize steps to next food
        foodScore = 0
        if len(newFood) < len(currFood):
          foodScore += 50 #we found one, probs should go here
        else:
          closestFood = min([util.manhattanDistance(newPos,foodPos) for foodPos in newFood])
          foodScore += (closestFood**(-1))*10 #take reciprocal to prioritize closest first
        score += foodScore
      
        # maximize distance to closest ghost and how often they are scared
        ghostScore = 0
        oldGhostStates = currentGameState.getGhostStates()
        oldScaredTimes = [ghostState.scaredTimer for ghostState in oldGhostStates]
        if sum(oldScaredTimes) == 0:
          # only avoid if not scared
          ghostDistances = [util.manhattanDistance(newPos,ghostPos.getPosition()) for ghostPos in newGhostStates]
          closestGhost = min(ghostDistances)
          ghostScore += closestGhost
          # avgGhostDistance = sum(ghostDistances)/len(ghostDistances)
          score += ghostScore
          avgScaredTimes = sum(newScaredTimes)/len(newScaredTimes)
          minScaredTime = min(newScaredTimes)
          ghostScore += avgScaredTimes

        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        # get pacman's best action/move
        # returns value, action tuple
        move = self.maxValueAction(gameState, self.depth)[1]
        return move

    def maxValueAction(self, gameState, depth):
        """
          Returns the max value and action from the current gameState searched to 
          specified depth
        """
        # init default return vals
        v = float("-inf")
        maxAct = 'Stop'
        # if we have reached terminal state (max allowed depth or won/lost), return eval function value
        if depth == 0 or gameState.isWin() or gameState.isLose():
          v = self.evaluationFunction(gameState)
        else:
            # for each of pacman's actions
            # check the mins for a full round of all ghost agent moves
            actions = gameState.getLegalActions(0)
            for action in actions:
                successor = gameState.generateSuccessor(0, action)
                newV = self.minValue(successor, depth, 1)
                # find the max of the mins for value and associated action
                if newV > v:
                    v = newV
                    maxAct = action
        # return the value and action
        return v, maxAct
        

    def minValue(self, gameState, depth, agentNum):
        """
          Returns the min value from the current ghost gameState searched to 
          specified depth
        """
        v = float("inf")
        # if we're at a terminal state (depth zero/win/lost) return evaluationFunction value
        if depth == 0 or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState)
        # find the min value for each of the ghost's legal moves
        actions = gameState.getLegalActions(agentNum)
        for action in actions:
            successor = gameState.generateSuccessor(agentNum, action)
            if  agentNum == gameState.getNumAgents() - 1:
                # if this is the last ghost, loop back to Pacman and decrement the depth
                newV = self.maxValueAction(successor, depth - 1)[0]
            else:
                # get the value of the next ghost's move
                newV = self.minValue(successor, depth, agentNum + 1)
            v = min(v, newV)
        return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        alpha = float("-inf")
        beta = float("inf")
        move = self.maxPrunedValueAction(gameState, self.depth, alpha, beta)[1]
        return move

    def maxPrunedValueAction(self, gameState, depth, alpha, beta):
        """
          Returns the max value and action from the current gameState searched to 
          specified depth
        """
        # init default return vals
        v = float("-inf")
        maxAct = 'Stop'
        # if we have reached terminal state (max allowed depth or won/lost), return eval function value
        if depth == 0 or gameState.isWin() or gameState.isLose():
          v = self.evaluationFunction(gameState)
        else:
            # for each of pacman's actions
            # check the mins for a full round of all ghost agent moves
            actions = gameState.getLegalActions(0)
            for action in actions:
                successor = gameState.generateSuccessor(0, action)
                newV = self.minValue(successor, depth, 1, alpha, beta)
                # find the max of the mins for value and associated action
                if newV > v:
                    v = newV
                    maxAct = action
                if v > beta:
                  return v, maxAct
                alpha = max(alpha, v)
        # return the value and action
        return v, maxAct
        

    def minValue(self, gameState, depth, agentNum, alpha, beta):
        """
          Returns the min value from the current ghost gameState searched to 
          specified depth
        """
        v = float("inf")
        # if we're at a terminal state (depth zero/win/lost) return evaluationFunction value
        if depth == 0 or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState)
        # find the min value for each of the ghost's legal moves
        actions = gameState.getLegalActions(agentNum)
        for action in actions:
            successor = gameState.generateSuccessor(agentNum, action)
            if  agentNum == gameState.getNumAgents() - 1:
                # if this is the last ghost, loop back to Pacman and decrement the depth
                newV = self.maxPrunedValueAction(successor, depth - 1, alpha, beta)[0]
            else:
                # get the value of the next ghost's move
                newV = self.minValue(successor, depth, agentNum + 1, alpha, beta)
            v = min(v, newV)
            if v < alpha:
              return v
            beta = min(beta, v)
        return v
        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        move = self.maxValueAction(gameState, self.depth)[1]
        return move

    def maxValueAction(self, gameState, depth):
        """
          Returns the max value and action from the current gameState searched to 
          specified depth
        """
        # init default return vals
        v = float("-inf")
        maxAct = 'Stop'
        # if we have reached terminal state (max allowed depth or won/lost), return eval function value
        if depth == 0 or gameState.isWin() or gameState.isLose():
          v = self.evaluationFunction(gameState)
        else:
            # for each of pacman's actions
            # check the mins for a full round of all ghost agent moves
            actions = gameState.getLegalActions(0)
            for action in actions:
                successor = gameState.generateSuccessor(0, action)
                newV = self.expetiValue(successor, depth, 1)
                # find the max of the mins for value and associated action
                if newV > v:
                    v = newV
                    maxAct = action
        # return the value and action
        return v, maxAct
        

    def expetiValue(self, gameState, depth, agentNum):
        """
          Returns the min value from the current ghost gameState searched to 
          specified depth
        """
        # v = float("inf")
        # if we're at a terminal state (depth zero/win/lost) return evaluationFunction value
        if depth == 0 or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState)
        # find the min value for each of the ghost's legal moves
        actions = gameState.getLegalActions(agentNum)
        avgVal = 0
        for action in actions:
            successor = gameState.generateSuccessor(agentNum, action)
            if  agentNum == gameState.getNumAgents() - 1:
                # if this is the last ghost, loop back to Pacman and decrement the depth
                newV = self.maxValueAction(successor, depth - 1)[0]
            else:
                # get the value of the next ghost's move
                newV = self.expetiValue(successor, depth, agentNum + 1)
            avgVal += newV
        avgVal /= float(len(actions))
        return avgVal

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: Evaluates game state based on weighted score, distance to closest food, 
      average distance to food, number of foods remaining, distance to closest ghost, and 
      min time the ghosts will be scared
    """
    if currentGameState.isWin():
      return float("inf")
    elif currentGameState.isLose():
      return float("-inf")

    position = currentGameState.getPacmanPosition()
    food = currentGameState.getFood().asList()
    
    oldGhostStates = currentGameState.getGhostStates()
    oldScaredTimes = [ghostState.scaredTimer for ghostState in oldGhostStates]

    score = currentGameState.getScore()

    # minimize steps to next food and average food
    if len(food) > 0:
        foodDistances = [util.manhattanDistance(position,foodPos) for foodPos in food]
        foodScore = 0
        closestFood = min(foodDistances)
        foodScore += (closestFood**(-1))*10 #take reciprocal to prioritize closest first
        avgFood  = sum(foodDistances)/len(food)
        foodScore += (avgFood**(-1))*3
        score += foodScore

    # incentivize pacman to eat more food
    score -= len(food)*3

    ghostScore = 0
    # maximize distance to closest ghost
    ghostDistances = [util.manhattanDistance(position,ghostPos.getPosition()) for ghostPos in oldGhostStates]
    closestGhost = min(ghostDistances)
    ghostScore += closestGhost*2
    # these are the same because there is only one ghost
    # avgScaredTimes = sum(oldScaredTimes)/len(oldScaredTimes)
    minScaredTime = min(oldScaredTimes)
    ghostScore += minScaredTime
    score += ghostScore

    return score

# Abbreviation
better = betterEvaluationFunction


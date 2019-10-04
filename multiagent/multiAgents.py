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
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # print successorGameState
        # print newFood
        # print newPos
        # print newGhostStates
        # print newScaredTimes
        # print currentGameState
        # print action
        food_list = currentGameState.getFood().asList()
        distance = -99999

        # Calculate the diatance between the current position of pacman and the position of a food
        # Set distance if the calculated result is larger than the initial distance
        for food in food_list:
              distance_ = -(manhattanDistance(newPos, food))
              if(distance_ > distance):
                    distance = distance_

        # If the pacman reaches a ghost, set distance to its inital value
        for ghost_state in newGhostStates:
              if(ghost_state.getPosition() == newPos):
                    distance = -99999
        
        if action == 'Stop':
              distance = -99999

        return distance
        # return successorGameState.getScore()

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
        "*** YOUR CODE HERE ***"
        def miniMax(gameState, depth, agentIndex):
              '''If is the last ghost to evaluate'''
              if(gameState.getNumAgents() == agentIndex):
                    if(self.depth != depth):
                          '''If the depth is not the max depth, start a new layer'''
                          # depth+=1
                          # agentIndex = 0
                          return miniMax(gameState, depth+1, 0)
                    else:
                          '''Else evaluate the current state'''
                          return self.evaluationFunction(gameState)
              else:
                    '''Get all the legal moves of the agent'''
                    action_list = gameState.getLegalActions(agentIndex)
                    '''No legal move can be made, evaluate the current state'''
                    if(len(action_list) == 0):
                          return self.evaluationFunction(gameState)
                    else:
                          list_of_possible_result = []
                          '''for each legal move, calculate the correspond miniMax and store it in a list'''
                          for action in action_list:
                                newState = gameState.generateSuccessor(agentIndex, action)
                                # agentIndex++
                                i = miniMax(newState, depth, agentIndex + 1)
                                list_of_possible_result.append(i)
                          if agentIndex == 0:
                                '''return max when processing pacman'''
                                return max(list_of_possible_result)
                          else:
                                '''return min when processing ghost'''
                                return min(list_of_possible_result)

        pacman_legal_actions = gameState.getLegalActions(0)
        mini_value = -99999
        action_res = ''
        '''return action with the max miniMax'''
        for action in pacman_legal_actions:
              successor = gameState.generateSuccessor(0, action)
              temp = miniMax(successor, 1, 1)
              if(temp > mini_value):
                    mini_value = temp
                    action_res = action                   
        return action_res
        # util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def max_value(gameState, depth, agentIndex, alpha, beta):
            value = -999
            if(self.depth >= depth):
                  for action in gameState.getLegalActions(agentIndex):
                        successor = gameState.generateSuccessor(agentIndex, action)
                        min_successor = min_value(successor, depth, agentIndex + 1, alpha, beta)
                        value = max(value, min_successor)
                        alpha = max(alpha, value)
                        if(beta < value):
                              if(beta != 999):
                                    return value
                  if(value != -999):
                        return value
                  else:
                        return self.evaluationFunction(gameState)
            else:
                  return self.evaluationFunction(gameState)
                             
        def min_value(gameState, depth, agentIndex, alpha, beta):
            value = 999
            if(agentIndex == gameState.getNumAgents()):
                  return max_value(gameState, depth + 1, 0, alpha, beta)
            else: 
                  for action in gameState.getLegalActions(agentIndex):
                        successor = gameState.generateSuccessor(agentIndex, action)
                        min_successor = min_value(successor, depth, agentIndex + 1, alpha, beta)
                        value = min_successor if(value == 999) else min(value, min_successor)
                        beta = value if(beta == 999) else min(value, beta)
                        if(alpha > value):
                              if(alpha != -999):
                                    return value
                  if(value != 999):
                        return value
                  else:
                        return self.evaluationFunction(gameState)

        def alpha_beta(gameState):
            alpha = -999
            beta = 999
            value = -999
            res_action = ''

            for action in gameState.getLegalActions(0):
                successor = gameState.generateSuccessor(0, action)
                _minValue = min_value(successor, 1, 1, alpha, beta)
                value = max(_minValue, value)
                if alpha == -999:
                    res_action = action
                    alpha = value
                else:
                    if value > alpha:
                          alpha = max(value, alpha)
                          res_action = action
                    else:
                          res_action = res_action
            return res_action
        return alpha_beta(gameState)
        # util.raiseNotDefined()

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
        "*** YOUR CODE HERE ***"
        def expectimax(gameState, depth, agentIndex):
            if(agentIndex == gameState.getNumAgents()):
                if depth != self.depth:
                    return expectimax(gameState, depth + 1, 0)
                else:
                    return self.evaluationFunction(gameState)
            else:
                action_list = gameState.getLegalActions(agentIndex)
                if(len(action_list) == 0):
                    return self.evaluationFunction(gameState)
                else:
                    list_of_possible_result = []
                    for action in action_list:
                          successor = gameState.generateSuccessor(agentIndex, action)
                          exp_max = expectimax(successor, depth, agentIndex + 1)
                          list_of_possible_result.append(exp_max)
                    if agentIndex == 0:
                        return max(list_of_possible_result)
                    else:
                        # return min(list_of_possible_result)
                        return sum(list_of_possible_result) / len(list_of_possible_result)
        pacman_legal_actions = gameState.getLegalActions(0)
        action_res = ''
        expect_max = -99999
        for action in pacman_legal_actions:
              successor = gameState.generateSuccessor(0, action)
              temp = expectimax(successor, 1, 1)
              if(temp > expect_max):
                    expect_max = temp
                    action_res = action
        return action_res
        # util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    food_list = currentGameState.getFood().asList()
    # distance = -99999
    distance_list = []
    score = currentGameState.getScore()
    newPos = currentGameState.getPacmanPosition()
    for food in food_list:
          temp = -(manhattanDistance(newPos, food))
          # if(temp > distance):
          #       distance = temp
          distance_list.append(temp)
    if(len(distance_list) == 0):
          distance_list.append(0)
    
    return max(distance_list) + score
    # util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction


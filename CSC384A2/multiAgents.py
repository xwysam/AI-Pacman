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

        gamescore = successorGameState.getScore()
        ghostdistence = []
        foodsdistence =[]
        foods = newFood.asList()

        for i in newGhostStates:
            dis = manhattanDistance(newPos,i.getPosition())
            ghostdistence.append(dis)

        for i in foods:
            dis = manhattanDistance(newPos,i)
            foodsdistence.append(dis)

        if min(ghostdistence) > 0 and len(foodsdistence) != 0:
            gamescore = gamescore + 10/min(foodsdistence) - 10/min(ghostdistence)

        return gamescore


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

        value = float('-Inf')
        best_move = None
        cur_depth = 0
        agentIndex = 1
        action = gameState.getLegalActions(0)

        for a in action:
            next_step = gameState.generateSuccessor(0, a)
            next_value = self.MIN(next_step, cur_depth, agentIndex)

            if next_value > value:
                value = next_value
                best_move = a

        return best_move

    def MAX(self, state, cur_depth):

        value = float('-Inf')
        actions = state.getLegalActions(0)
        cur_depth += 1

        if state.isWin() or state.isLose()or cur_depth == self.depth:
            return self.evaluationFunction(state)

        for a in actions:
            next_step = state.generateSuccessor(0,a)
            next_value = self.MIN(next_step,cur_depth,1)

            if next_value > value:
                value = next_value

        return value

    def MIN(self, state, cur_depth, agentIndex):

        value = float('Inf')
        actions = state.getLegalActions(agentIndex)

        if state.isWin() or state.isLose()or cur_depth == self.depth:
            return self.evaluationFunction(state)

        for a in actions:
            next_step = state.generateSuccessor(agentIndex,a)

            if agentIndex == state.getNumAgents()-1:
                next_value = self.MAX(next_step,cur_depth)

                if next_value < value:
                    value = next_value
            else:
                next_value = self.MIN(next_step,cur_depth,agentIndex+1)

                if next_value < value:
                    value = next_value
        return value


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        value = float('-Inf')
        best_move = None
        cur_depth = 0
        agentIndex = 1
        alpha = float('-Inf')
        beta = float('Inf')
        action = gameState.getLegalActions(0)

        for a in action:
            next_step = gameState.generateSuccessor(0, a)
            next_value = self.MIN(next_step, cur_depth, agentIndex,alpha,beta)

            if next_value > value:
                value = next_value
                best_move = a

            if value > alpha:
                alpha = value

        return best_move

    def MAX(self, state, cur_depth, alpha, beta):

        cur_depth += 1
        value = float('-Inf')
        actions = state.getLegalActions(0)

        if state.isWin() or state.isLose() or cur_depth == self.depth:
            return self.evaluationFunction(state)

        for a in actions:
            next_step = state.generateSuccessor(0,a)
            next_value = self.MIN(next_step,cur_depth,1,alpha,beta)

            if next_value > value:
                value = next_value

            if value >= beta:
                return value

            if value >= alpha:
                alpha = value

        return value

    def MIN(self, state, cur_depth, agentIndex, alpha, beta):

        value = float('Inf')
        actions = state.getLegalActions(agentIndex)

        if state.isWin() or state.isLose()or cur_depth == self.depth:
            return self.evaluationFunction(state)

        for a in actions:
            next_step = state.generateSuccessor(agentIndex,a)

            if agentIndex == state.getNumAgents() - 1:
                next_value = self.MAX(next_step,cur_depth,alpha,beta)

                if next_value < value:
                    value = next_value
            else:
                next_value = self.MIN(next_step,cur_depth,agentIndex+1,alpha,beta)

                if next_value < value:
                    value = next_value

            if value <= alpha:
                return value

            if value < beta:
                beta = value

        return value



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
        # util.raiseNotDefined()

        value = float('-Inf')
        best_move = None
        cur_depth = 0
        agentIndex = 1
        action = gameState.getLegalActions(0)

        for a in action:
            next_step = gameState.generateSuccessor(0, a)
            next_value = self.EXP(next_step, cur_depth, agentIndex)

            if next_value > value:
                value = next_value
                best_move = a

        return best_move

    def MAX(self, state, cur_depth):

        value = float('-Inf')
        actions = state.getLegalActions(0)
        cur_depth += 1

        if state.isWin() or state.isLose()or cur_depth == self.depth:
            return self.evaluationFunction(state)

        for a in actions:
            next_step = state.generateSuccessor(0,a)
            next_value = self.EXP(next_step,cur_depth,1)

            if next_value > value:
                value = next_value

        return value

    def EXP(self, state, cur_depth, agentIndex):

        value = 0
        actions = state.getLegalActions(agentIndex)

        if state.isWin() or state.isLose()or cur_depth == self.depth:
            return self.evaluationFunction(state)

        probility = 1.0/len(state.getLegalActions(agentIndex))

        for a in actions:
            next_step = state.generateSuccessor(agentIndex,a)

            if agentIndex == state.getNumAgents()-1:
                next_value = self.MAX(next_step,cur_depth)
                value += next_value * probility

            else:
                next_value = self.EXP(next_step,cur_depth,agentIndex+1)
                value += next_value * probility
        return value

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <first we calculate the distence from the pacman to the food dots, and add the distence in to a list.
       second we count the distence from the pacman to the ghost and also add in to a list and we split the ghost in two
       way one is ghost in scared and second is in normal. in the final we count the score based on the game score and
       if there are foods we add the minimum distence as the food score and the ghost distence is what we need to minus,
       also add the scared ghost distence then we count the final score.>
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    score = currentGameState.getScore()
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    food_list = newFood.asList()
    food_dis_list = []
    scar_gs_list = []
    gs_list =[]

    for food in food_list:
        food_dis = manhattanDistance(newPos,food)
        food_dis_list.append(food_dis)

    for gs in newGhostStates:
        ghostPos = newGhostStates[0].getPosition()
        gs_dis = manhattanDistance(newPos,ghostPos)
        if gs_dis > 0 and newScaredTimes[0] > 0:
            scar_gs_list.append(gs_dis)
        elif gs_dis > 0 and newScaredTimes[0] == 0:
            gs_list.append(gs_dis)

    if len(food_dis_list) > 0:

        if len(gs_list) > 0 :

            if len(scar_gs_list) > 0:
                score = score + 10/min(food_dis_list) + 100/min(scar_gs_list)
            else:
                score = score + 10/min(food_dis_list) - 10/min(gs_list)
        else:
            score += 10/min(food_dis_list)

    return score

# Abbreviation
better = betterEvaluationFunction


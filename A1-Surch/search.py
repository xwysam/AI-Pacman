# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def d_b_s_helper(problem, theStack):
    """
    Return a list of the action that reaches the goal, a helper function of the
    depthFirstSearch and breadthFirstSearch.
    """
    visited = []

    theStack.push((problem.getStartState(), []))

    while not theStack.isEmpty():
        cur_state, action_list = theStack.pop()

        if cur_state not in visited:

            if problem.isGoalState(cur_state):
                return action_list

            else:
                visited.append(cur_state)
                successors = problem.getSuccessors(cur_state)

                for i in successors:
                    child_state = i[0]
                    child_list = []
                    child_list.append(i[1])

                    if child_state not in visited:
                        final_list = action_list + child_list
                        theStack.push((child_state, final_list))



def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()

    theStack = util.Stack()

    return d_b_s_helper(problem, theStack)


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()

    theStack = util.Queue()

    return d_b_s_helper(problem, theStack)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()

    visited = []
    thePQueue = util.PriorityQueue()
    action_list = []
    final_list = []
    thePQueue.push((problem.getStartState(),action_list),0)

    while not thePQueue.isEmpty():
        cur_state, actions = thePQueue.pop()

        if cur_state not in visited:

            if problem.isGoalState(cur_state):
                return actions

            else:
                visited.append(cur_state)
                successors = problem.getSuccessors(cur_state)

                for i in successors:
                    child_state = i[0]
                    child_action = i[1]
                    child_action_list = [child_action]
                    action_list = actions + child_action_list
                    cost = problem.getCostOfActions(action_list)

                    if child_state not in visited:
                        thePQueue.push((child_state,action_list),cost)



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    action_list = []
    visited =[]
    thePQueue = util.PriorityQueue()
    thePQueue.push((problem.getStartState(),action_list),0)

    while not thePQueue.isEmpty():
        cur_state, actions = thePQueue.pop()

        if cur_state not in visited:

            if problem.isGoalState(cur_state):
                return actions
            else:
                visited.append(cur_state)
                successors = problem.getSuccessors(cur_state)

                for i in successors:
                    child_state = i[0]
                    child_action = i[1]
                    child_action_list = [child_action]
                    action_list = actions + child_action_list
                    cost = heuristic(child_state, problem) + problem.getCostOfActions(action_list)

                    if child_state not in visited:
                        thePQueue.push((child_state,action_list),cost)





# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

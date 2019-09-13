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
    # print "Start:", problem.getStartState()
    # print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    # print "Start's successors:", problem.getSuccessors(problem.getStartState())

    forward_stack = util.Stack()
    '''Elements are stored as ((state_to_expand), [actions_list]).'''
    forward_stack.push((problem.getStartState(), []))
    visited_nodes = []
    # visited_nodes.append(problem.getStartState())

    while forward_stack.isEmpty() == 0:
        current_position, actions = forward_stack.pop()     
        if problem.isGoalState(current_position):
            # actions.append(next_action)
            break
        else:
            if current_position not in visited_nodes:
                visited_nodes.append(current_position)
                next = problem.getSuccessors(current_position)
                for i in next:
                    next_position, next_action, next_cost = i
                    # print next_action, next_position
                    # actions.append(next_action)
                    forward_stack.push((next_position, actions+[next_action]))
    return actions

    # ac = ['South'];
    # print forward_stack.pop()
    # print visited_nodes
    # print problem.getSuccessors(problem.getStartState())
    # print problem.getCostOfActions(ac)
    # util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    '''Use a queue instead of a stack'''
    forward_stack = util.Queue()
    forward_stack.push((problem.getStartState(), [])) 
    visited_nodes = []
    # visited_nodes.append(problem.getStartState())

    while forward_stack.isEmpty() == 0:
        current_position, actions = forward_stack.pop()   
        if problem.isGoalState(current_position):
            # actions.append(next_action)
            break
        else:
            if current_position not in visited_nodes:
                visited_nodes.append(current_position)
                next = problem.getSuccessors(current_position)
                for i in next:
                    next_position, next_action, next_cost = i
                    # print next_action, next_position
                    # actions.append(next_action)
                    forward_stack.push((next_position, actions+[next_action]))
    return actions

    # util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    '''Use a priority queue instead of a queue'''
    forward_stack = util.PriorityQueue()
    '''A sum of total cost should also be stored now and used as the priority, a low cost solution should be considered first'''
    forward_stack.push((problem.getStartState(), [], 0), 0) 
    visited_nodes = []
    # visited_nodes.append(problem.getStartState())

    while forward_stack.isEmpty() == 0:
        current_position, actions, cost = forward_stack.pop()   
        if problem.isGoalState(current_position):
            # actions.append(next_action)
            break
        else:
            if current_position not in visited_nodes:
                visited_nodes.append(current_position)
                next = problem.getSuccessors(current_position)
                for i in next:
                    next_position, next_action, next_cost = i
                    # print next_action, next_position
                    # actions.append(next_action)
                    forward_stack.push((next_position, actions+[next_action], cost+next_cost), cost+next_cost)
    return actions
    # util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    '''Use a priority queue instead of a queue'''
    forward_stack = util.PriorityQueue()
    '''A sum of total cost should also be stored now and used as the priority, a low cost solution should be considered first'''
    forward_stack.push((problem.getStartState(), [], 0), 0) 
    visited_nodes = []
    # visited_nodes.append(problem.getStartState())

    while forward_stack.isEmpty() == 0:
        current_position, actions, cost = forward_stack.pop()   
        if problem.isGoalState(current_position):
            # actions.append(next_action)
            break
        else:
            if current_position not in visited_nodes:
                visited_nodes.append(current_position)
                next = problem.getSuccessors(current_position)
                for i in next:
                    next_position, next_action, next_cost = i
                    # print next_action, next_position
                    # actions.append(next_action)
                    '''When pushing next state, add the heuristic value to the priority value'''
                    forward_stack.push((next_position, actions+[next_action], cost+next_cost), cost+next_cost+heuristic(next_position, problem))
    return actions
    # util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

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
    # use Last-In-First-Out Stack to search nodes of 
    frontier = util.Stack()
    # use generic tree search to find actions needed to get to the goal
    actions = treeSearch(problem, frontier)
    return actions

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    # use First-In-First-Out Queue to search nodes of same depth
    frontier = util.Queue()
    # use generic tree search to find actions needed to get to the goal
    actions = treeSearch(problem, frontier)
    return actions

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    # use priority queue with default null heuristic that returns same cost
    frontier = util.PriorityQueue()
    # use generic tree search to find actions needed to get to the goal
    actions = treeSearch(problem, frontier)
    return actions

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    # use priority queue with specified heuristic to determine which node to pop from the frontier
    frontier = util.PriorityQueue()
    # use generic tree search to find actions needed to get to the goal
    actions = treeSearch(problem, frontier, heuristic)
    return actions


# Helper Methods
def treeSearch(problem, frontier, heuristic=nullHeuristic):
    """Search the fringe nodes in the search tree for given problem and data structure."""
    # track exclusive set of explored nodes
    explored = []
    # track path actions of each node
    path = []
    # check type of frontier for modified behavior later
    isPriorityQueue = isinstance(frontier, util.PriorityQueue)
    start_location = problem.getStartState()
    # if priority is applicable, keep a running_cost as the third value of node tuple
    # otherwise just track current location and path actions to get there
    # add node to frontier
    if isPriorityQueue == True:
        node = (start_location, path, 0)
        frontier.push(node, heuristic(start_location, problem))
    else:
        node = (start_location,path)
        frontier.push(node)
    # current_state = problem.getStartState()

    goalFound = False
    # keep checking until we have no nodes left to expand
    while not frontier.isEmpty():
        # get next node
        node = frontier.pop()
        current_location = node[0]
        path = node[1]
        # if already explored, don't expand it again
        if current_location in explored:
            continue
        # add current location to closed list so don't re-expand
        explored.append(current_location)
        # check goal reached
        if problem.isGoalState(current_location):
            goalFound = True
            break
        # add unseen children/successors of current state to frontier
        for scsr in problem.getSuccessors(current_location):
            if not scsr[0] in explored:
                # append current coordinates so we know where this node came form
                node_path = path + [scsr[1]]
                # if type is priority queue, calculate cost
                if isPriorityQueue:
                    cost = scsr[2];
                    running_cost = node[2] + cost
                    priority_cost = running_cost + heuristic(scsr[0], problem);
                    frontier.push((scsr[0], node_path,running_cost),priority_cost)
                    # frontier.push((scsr[0], node_path), cost)
                else:
                    frontier.push((scsr[0], node_path))
    # return no solution if goal not reached
    if not goalFound:
        print "Goal Not Reached."
        return []
        
    return path

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

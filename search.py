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
import game
from pprint import pprint

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
    
    Code written by: 
        Nike Lambooy
        Nicky Lenaers

    DFS takes O(b^m) time with
        b = maximum branching factor
        m = maximum depth of the state space (in this case finite)
    
    DFS takes O(b*m) space because 'black' nodes are removed, resulting in linear space.
    """
    
    # Initialize Stack() instances for LIFO datastructure (Source: College 2, Slide 38)
    fringe = util.Stack()
    visited = util.Stack()
    parents = util.Stack()
    actions = util.Queue()
    
    # Initialize the fringe
    fringe.push([problem.getStartState()])

    while not problem.isGoalState(fringe.list[-1][0]):

        successors = problem.getSuccessors(fringe.list[-1][0])
        
        # Current node is visited, because it will soon be expanded...
        visited.push(fringe.list[-1][0])
        
        parent = fringe.list[-1][0]
        
        # Use pop BEFORE adding items to the fringe, because it removes the last item
        fringe.pop()
        
        # Loop over successors using xrange loading lazingly
        for index in reversed(xrange(len(successors))):

            if successors[index][0] not in visited.list:
                
                # Push successors to the fringe if not visited
                fringe.push([successors[index][0], parent, successors[index][1]])

        parents.push(fringe.list[-1])
    
    # Assign goal item as first state (actions is build backwards)
    state = fringe.list[-1][0]
    
    # Build actions
    while state != problem.getStartState():
        
        for index in xrange(len(parents.list)):
            
            if state == parents.list[index][0]:
                
                actions.push(parents.list[index][2])
                state = parents.list[index][1]
    
    # Return the actions Pacman will take
    return actions.list

def breadthFirstSearch(problem):
    
    """ 
    Search the shallowest nodes in the search tree first.
    
    Code written by:
        Nike Lambooy
        Nicky Lenaers
        
    BFS takes O(b^d+1) time with
        b = maximum branching factor
        d = depth of the least-cost solution
        1 = the frist node (root node)

    BFS takes O(b^d+1) space, keeping every node in memory.
    """
    
    # Initialize Queue() instances for FIFO datastructure (Source: College 2, Slide 32)
    fringe = util.Queue()
    visited = util.Queue()
    parents = util.Queue()
    actions = util.Queue()

    # Initialize the fringe
    fringe.push(problem.getStartState())

    while not problem.isGoalState(fringe.list[-1]):
        
        successors = problem.getSuccessors(fringe.list[-1])
        
        # Current node is visited, because it will soon be expanded...
        visited.push(fringe.list[-1])

        # Add item to be expanded as the current parent
        parent = fringe.list[-1]
        
        # Loop over successors using xrange loading lazingly
        for index in reversed(xrange(len(successors))):
            
            if successors[index][0] not in visited.list:
                
                fringe.push(successors[index][0])
                visited.push(successors[index][0])
                parents.push([successors[index][0], parent, successors[index][1]])
        
        fringe.pop()
    
    # Assign goal item as first state (actions is build backwards)
    state = fringe.list[-1]
    
    # Build actions
    while state != problem.getStartState():
        
        for index in xrange(len(parents.list)):
            
            if state == parents.list[index][0]:
                
                actions.push(parents.list[index][2])
                state = parents.list[index][1]
    
    return actions.list

def uniformCostSearch(problem):
    
    """
    Search the node of least total cost first.
    
    Code written by: 
        Nike Lambooy
        Nicky Lenaers
        
    UCS takes O(b^(C*/e)) time with
        b  = maximum branching factor
        C* = cost of optimal solution
        e  = some positive bound

    UCS takes O(b^(C*/e)) space.
    """
    
    # Initialize PriorityQueue() instance for fringe (Source: College 2, Slide 37)
    fringe = util.PriorityQueue() # Step cost / Total Cost / State Coordinates
    visited = util.Stack()
    parents = util.Queue()
    actions = util.Queue()
    
    # Push first state with priority zero
    fringe.push(problem.getStartState(), 0)
    smallest = fringe.pop()
    # TEMP
    count = 0
    
    while not problem.isGoalState(smallest):
        
        #smallest = fringe.pop()
        
        # First item is lowerst-cost item in the heap
        successors = problem.getSuccessors(smallest)
        
        visited.push(smallest)
        
        #if count > 10:
        #    break
        
        # Loop over successors using xrange loading lazingly
        for index in reversed(xrange(len(successors))):

            if successors[index][0] not in visited.list:
                
                # Addition of cost-so-far and cost of successor being pushed to the fringe heap
                fringe.push(successors[index][0], successors[index][2])                
                visited.push(successors[index][0])
                parents.push([successors[index][0], smallest, successors[index][1]])

        #count += 1
        
        smallest = fringe.pop()
        
    state = smallest
    
    # Build actions
    while state != problem.getStartState():
        
        for index in xrange(len(parents.list)):
            
            if state == parents.list[index][0]:
                
                actions.push(parents.list[index][2])
                state = parents.list[index][1]

    return actions.list

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

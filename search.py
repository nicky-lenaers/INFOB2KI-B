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
    
    """
    Initialize the fringe with following indeces:
    [0] = state (or node) to be expanded
    [1] = list of actions up to this node
    """
    
    fringe.push([problem.getStartState(), []])

    while not fringe.isEmpty():
        
        # Extract deepest node from the fringe
        state, actions = fringe.pop()
        
        # Goal test
        if problem.isGoalState(state):
            return actions
        
        # Get successors of current state
        successors = problem.getSuccessors(state)

        # Loop over successors
        for index in reversed(range(0, len(successors))):

            # Successors can't be visited, so check
            if successors[index][0] not in visited.list:
                
                # Push successors' state and actions to the fringe if not visited
                fringe.push([successors[index][0], actions + [successors[index][1]]])
                
        # Current node is visited
        visited.push(state)

    return []

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
    fringe = util.PriorityQueue()
    visited = util.Stack()
    parents = util.Queue()
    actions = util.Queue()
    
    # Push first state with priority zero
    fringe.push(problem.getStartState(), 0)
    priority = fringe.pop()
    
    while not problem.isGoalState(priority):

        # First item is lowerst-cost item in the heap
        successors = problem.getSuccessors(priority)
        
        # Got successors, so mark as visited
        visited.push(priority)

        # Get cost-so-far
        totalcost = problem.getCostOfActions(actions.list)
        
        # Loop over successors using xrange loading lazingly
        for index in reversed(xrange(len(successors))):

            stepcost = 0
            unseen = True
            
            # If successor is already seen
            for j in range(len(fringe.heap)):
                if successors[index][0] in fringe.heap[j]:
                    stepcost = fringe.heap[j][0] - totalcost
                    unseen = False
            
            if successors[index][0] not in visited.list and (successors[index][2] < stepcost or unseen):
                
                # Addition of cost-so-far and cost of successor being pushed to the fringe heap
                fringe.push(successors[index][0], totalcost + successors[index][2])
                parents.push([successors[index][0], priority, successors[index][1]])
        
        # Get the highest priority item from the priority queueu
        state = priority = fringe.pop()
        
        # Build actions
        del actions.list[:]
        
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
    """
    Search the node of least total cost first.
    
    Code written by: 
        Nike Lambooy
        Nicky Lenaers
        
    """
    
    # Initialize PriorityQueue() instance for fringe (Source: College 2, Slide 37)
    fringe = util.PriorityQueue()
    visited = util.Stack()
    parents = util.Queue()
    actions = util.Queue()
    
    # Push first state with priority zero
    fringe.push(problem.getStartState(), 0)
    priority = fringe.pop()
    
    while not problem.isGoalState(priority):

        #print "HEURISTIEK: ", heuristic(priority, problem)
        
        # First item is lowerst-cost item in the heap
        successors = problem.getSuccessors(priority)
        
        # Got successors, so mark as visited
        visited.push(priority)

        # Get cost-so-far
        totalcost = problem.getCostOfActions(actions.list)
        
        # Loop over successors using xrange loading lazingly
        for index in reversed(xrange(len(successors))):

            stepcost = 0
            unseen = True
            
            # If successor is already seen
            for j in range(len(fringe.heap)):
                if successors[index][0] in fringe.heap[j]:
                    # Set cost to sp
                    stepcost = fringe.heap[j][0] - totalcost - heuristic(priority, problem)
                    unseen = False
            
            if successors[index][0] not in visited.list and (successors[index][2] < stepcost or unseen):
                
                # Addition of cost-so-far, cost of successor and heuristic cost of successor being pushed to the fringe heap
                fringe.push(successors[index][0], heuristic(successors[index][0], problem) + totalcost + successors[index][2])
                parents.push([successors[index][0], priority, successors[index][1]])
        
        # Get the highest priority item from the priority queueu
        state = priority = fringe.pop()
        
        # Build actions
        del actions.list[:]
        
        while state != problem.getStartState():

            for index in xrange(len(parents.list)):

                if state == parents.list[index][0]:

                    actions.push(parents.list[index][2])
                    state = parents.list[index][1]
    
    return actions.list
    
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
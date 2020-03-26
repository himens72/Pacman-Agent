"""
REFERENCES:
[1] http://ai.berkeley.edu/project_overview.html
[2] A* Search Algorithm: https://www.geeksforgeeks.org/a-search-algorithm/
[3] AI Search Algorithm: https://www.tutorialspoint.com/artificial_intelligence/artificial_intelligence_popular_search_algorithms.htm
[4] Heuristic Search Algorithm: https://data-flair.training/blogs/heuristic-search-ai/
[5] Suboptimal search: https://intellipaat.com/community/26159/the-suboptimal-solution-is-given-by-a-search
[6] Teaching Introductory AI with Pac-Man: https://www.aaai.org/ocs/index.php/EAAI/EAAI10/paper/viewFile/1954/2331
"""
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
from util import Stack
from util import Queue
from util import PriorityQueue

"""
A Node in a tree
"""
class Node:

    def __init__(self, state, parent, direction, priority=0):
        self.state = state
        self.parent = parent
        self.direction = direction
        self.priority = priority

    def getPath(self):
        path, node = list(), self
        while node.direction != 'none':
            path.append(node.direction)
            node = node.parent
        path.reverse()
        return path

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

# To do (least cost solution if needed!)
def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # create a stack for DFS
    stack = Stack()
    # create a set to keep track of explored/visited nodes
    visited = set()
    stack.push(Node(problem.getStartState(), 'none', 'none'))
    
    while not stack.isEmpty():
        # pop a node from stack
        current = stack.pop()
        # if current node is Goal state then return the path
        if problem.isGoalState(current.state):
            path = current.getPath()
            return path

        """ 
        visit current node if is not explored before and find its
        children (push those into the stack) 
        """
        if current.state not in visited:
            visited.add(current.state)
            all_successor = problem.getSuccessors(current.state)
            for successor in all_successor:
                if successor not in visited:
                    child = Node(successor[0], current, successor[1])
                    stack.push(child)

    return list()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    que = Queue()
    visited = set()
    que.push(Node(problem.getStartState(), 'none', 'none'))

    while not que.isEmpty():
        # Dequeue first element from queue
        current = que.pop()

        # if current node is Goal state then return the path
        if problem.isGoalState(current.state):
            path = current.getPath()
            return path

        # find all adjacent nodes of dequeued node current.
        # if adjacent nodes are not visited, then 
        # mark it as visited and add into queue.
        if current.state not in visited:
            visited.add(current.state)
            all_successor = problem.getSuccessors(current.state)
            for successor in all_successor:
                if successor not in visited:
                    child = Node(successor[0], current, successor[1])
                    que.push(child)
            
    return list()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # Uniform Cost Search requires PriorityQueue 
    pque = PriorityQueue()
    visited = set()
    pque.update(Node(problem.getStartState(), 'none', 'none'), 0)

    while not pque.isEmpty():
        # Dequeue first element from queue
        current = pque.pop()

        # if current node is Goal state then return the path
        if problem.isGoalState(current.state):
            path = current.getPath()
            return path
        
        # find all adjacent nodes of dequeued node current.
        # if adjacent nodes are not visited, then 
        # mark it as visited and add into queue.
        if current.state not in visited:
            visited.add(current.state)
            all_successor = problem.getSuccessors(current.state)
            for successor in all_successor:
                child = Node(successor[0], current, successor[1], successor[2]+current.priority)
                pque.update(child, child.priority)
        
    return list()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    queue = PriorityQueue()

    # get current state of Pacman
    # State of current problem, parent, direction and cost of node -> parameters of Node constructor
    current_node = Node(problem.getStartState(), 'none', 'none', 0)
    queue.update(current_node, 0)

    path = []
    visited = []
    while not queue.isEmpty():
        current_node = queue.pop()
        # returns path if Pacman has reached final destination state
        if problem.isGoalState(current_node.state):
            path = current_node.getPath()
            return path

        # Search the node that has the lowest combined cost and heuristic first.
        if current_node.state not in visited:
            visited.append(current_node.state)
            for successor in problem.getSuccessors(current_node.state):
                # successor[0] = state of new node
                # succesor[1] = direction of new node
                # successor[2] = cost of new node
                total_cost = current_node.priority + successor[2]
                next_node = Node(successor[0], current_node, successor[1], total_cost)
                queue.update(next_node, total_cost + heuristic(successor[0], problem))
    return path

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

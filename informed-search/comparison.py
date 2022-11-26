import os
import sys
import copy
import math
import heapq
import time
import timeout_decorator

import utils
import cube

# For following test cases
def wrap_test(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f'FAILED, reason: {str(e)}'
    return inner

def bfs_tree_search(num_mis, num_can):
    r"""
    Breadth First Search (BFS) finds the solution to reach the goal from the 
    initial. By default, fail is True and returns False

    Tree search builds a child node for every reachable state, and push them 
    all into the froniter to be explored in the future. In every iteration, 
    agent explores a state with least priority (path cost). At the beginning 
    of search, agent can only explore from the initial state, and makes it as 
    the root node in the search tree.

    Solution should be the action taken from the root node (initial state) to 
    the leaf node (goal state) in the search tree.

    Args:
        num_mis: the number of the Missionaries 
        num_can: the number of the Cannibals

    Returns:
        solution (List): the action sequence
    """
    
    fail = True
    solution = []
    
    """ YOUR CODE HERE """
    # Need to track 2 things
    # - state tuple (m, c, boat), where m is missionary on start bank, c is cannibal on start bank,
    # and boat = 0 when boat at start and = 1 when boat at end
    # - action tuple (m, c), where m is missionary on boat, and c is cannibal on boat
    start_state_tuple = (num_mis, num_can, 0)
    goal_state = (0, 0, 1)
    # Generate all possible action tuples, regardless of m and c constraints
    # Boat can only hold 1 or 2 people
    possible_action_tuples = [[0, 1], [0, 2], [1, 0], [2, 0], [1, 1]]

    # frontier contains nodes --> tuples of state and solution to reach there
    start_node = utils.Node(None, None, start_state_tuple, 0, 0)
    frontier = utils.PriorityQueue()
    frontier.push(start_node.g_n, start_node)
    while len(frontier) != 0:
        curr_node = frontier.pop()
        curr_state = curr_node.state
        # Check if state is goal state
        if curr_state == goal_state:
            trace_act = curr_node.act
            while trace_act != None:
                solution.append(trace_act)
                curr_node = curr_node.parent
                trace_act = curr_node.act
            fail = False
            solution.reverse()
            break
        multiplier = -1 if curr_node.state[2] == 0 else 1
        next_boat_pos = 1 if curr_node.state[2] == 0 else 0
        # Calculate all possible actions from this state
        for action in possible_action_tuples:
            # Calculate m and c on start side of river
            next_mis = curr_state[0] + action[0] * multiplier
            next_can = curr_state[1] + action[1] * multiplier
            if ((next_can > next_mis and next_mis > 0)
            or next_can < 0 or next_mis < 0
            or next_can > num_can or next_mis > num_mis):
                continue

            # Calculate m and c on other side of the river
            next_mis_other_bank = num_mis - next_mis
            next_can_other_bank = num_can - next_can
            if ((next_can_other_bank > next_mis_other_bank and next_mis_other_bank > 0)
            or next_can_other_bank < 0 or next_mis_other_bank < 0
            or next_can_other_bank > num_can or next_mis_other_bank > num_mis):
                continue

            # State falls within m and c constraints
            next_state = (next_mis, next_can, next_boat_pos)
            next_node = utils.Node(curr_node, action, next_state, curr_node.g_n + 1, 0)
            frontier.push(next_node.g_n, next_node)
    """ END YOUR CODE HERE """
    
    if fail:
        return False
    return solution

def dfs_tree_search(num_mis, num_can):
    r"""Deep First Search (DFS) finds the solution to reach the goal from the 
    initial. By default, fail is True and returns False

    DFS proceeds immediately to the deepest level of the search tree, where the 
    nodes have no successors. The search then “backs up” to the next deepest 
    node that still has unexpanded successors.
    
    Tree search builds a child node for every reachable state, and push them 
    all into a stack to be explored in the future. In every iteration, 
    agent explores the latest pushed state. At the beginning of search, agent 
    can only explore from the initial state, and makes it as the root node in 
    the search tree.

    Solution should be the action taken from the root node (initial state) to 
    the leaf node (goal state) in the search tree.

    Args:
        num_mis: the number of the Missionaries 
        num_can: the number of the Cannibals

    Returns:
        solution (List): the action sequence
    """

    fail = True
    solution = []
    
    """ YOUR CODE HERE """
    # Need to track 2 things
    # - state tuple (m, c, boat), where m is missionary on start bank, c is cannibal on start bank,
    # and boat = 0 when boat at start and = 1 when boat at end
    # - action tuple (m, c), where m is missionary on boat, and c is cannibal on boat
    start_state_tuple = (num_mis, num_can, 0)
    goal_state = (0, 0, 1)
    # Generate all possible action tuples, regardless of m and c constraints
    # Boat can only hold 1 or 2 people
    possible_action_tuples = [[0, 1], [0, 2], [1, 0], [2, 0], [1, 1]]

    # frontier contains nodes --> tuples of state and solution to reach there
    start_node = utils.Node(None, None, start_state_tuple, 0, 0)
    stack = utils.Stack()
    stack.push(start_node)
    
    while not stack.is_empty():
        curr_node = stack.pop()
        curr_state = curr_node.state
        # Check if state is goal state
        if curr_state == goal_state:
            trace_act = curr_node.act
            while trace_act != None:
                solution.append(trace_act)
                curr_node = curr_node.parent
                trace_act = curr_node.act
            fail = False
            solution.reverse()
            break
        multiplier = -1 if curr_node.state[2] == 0 else 1
        next_boat_pos = 1 if curr_node.state[2] == 0 else 0
        # Calculate all possible actions from this state and add to stack
        for action in possible_action_tuples:
            # Calculate m and c on start side of river
            next_mis = curr_state[0] + action[0] * multiplier
            next_can = curr_state[1] + action[1] * multiplier
            if ((next_can > next_mis and next_mis > 0)
            or next_can < 0 or next_mis < 0
            or next_can > num_can or next_mis > num_mis):
                continue

            # Calculate m and c on other side of the river
            next_mis_other_bank = num_mis - next_mis
            next_can_other_bank = num_can - next_can
            if ((next_can_other_bank > next_mis_other_bank and next_mis_other_bank > 0)
            or next_can_other_bank < 0 or next_mis_other_bank < 0
            or next_can_other_bank > num_can or next_mis_other_bank > num_mis):
                continue

            # State falls within m and c constraints
            next_state = (next_mis, next_can, next_boat_pos)
            next_node = utils.Node(curr_node, action, next_state, curr_node.g_n + 1, 0)
            stack.push(next_node)
    """ END YOUR CODE HERE """
    
    if fail:
        return False
    return solution

def bfs_graph_search(num_mis, num_can):
    r"""
    Breadth First Search finds the solution to reach the goal from the initial.
    By default, fail is True and returns False.

    Graph search requires to deal with the redundant path: cycle or loopy path.
    Modify the above implemented tree search algorithm to acceralate your AI.

    ***IMPORTANT***: make comments in the code you change and explain it.

    Args:
        num_mis: the number of the Missionaries 
        num_can: the number of the Cannibals

    Returns:
        solution (List): the action sequence
    """
    fail = True
    solution = []
    
    """ YOUR CODE HERE """
        # Need to track 2 things
    # - state tuple (m, c, boat), where m is missionary on start bank, c is cannibal on start bank,
    # and boat = 0 when boat at start and = 1 when boat at end
    # - action tuple (m, c), where m is missionary on boat, and c is cannibal on boat
    start_state_tuple = (num_mis, num_can, 0)
    goal_state = (0, 0, 1)
    # Generate all possible action tuples, regardless of m and c constraints
    # Boat can only hold 1 or 2 people
    possible_action_tuples = [[0, 1], [0, 2], [1, 0], [2, 0], [1, 1]]

    # frontier contains nodes --> tuples of state and solution to reach there
    start_node = utils.Node(None, None, start_state_tuple, 0, 0)
    frontier = utils.PriorityQueue()
    frontier.push(start_node.g_n, start_node)
    # ADDITION: Array to track visited nodes
    visited = set()
    visited.add(start_node)
    while len(frontier) != 0:
        curr_node = frontier.pop()
        curr_state = curr_node.state
        # Check if state is goal state
        if curr_state == goal_state:
            trace_act = curr_node.act
            while trace_act != None:
                solution.append(trace_act)
                curr_node = curr_node.parent
                trace_act = curr_node.act
            fail = False
            solution.reverse()
            break
        multiplier = -1 if curr_node.state[2] == 0 else 1
        next_boat_pos = 1 if curr_node.state[2] == 0 else 0
        # Calculate all possible actions from this state
        for action in possible_action_tuples:
            # Calculate m and c on start side of river
            next_mis = curr_state[0] + action[0] * multiplier
            next_can = curr_state[1] + action[1] * multiplier
            if ((next_can > next_mis and next_mis > 0)
            or next_can < 0 or next_mis < 0
            or next_can > num_can or next_mis > num_mis):
                continue

            # Calculate m and c on other side of the river
            next_mis_other_bank = num_mis - next_mis
            next_can_other_bank = num_can - next_can
            if ((next_can_other_bank > next_mis_other_bank and next_mis_other_bank > 0)
            or next_can_other_bank < 0 or next_mis_other_bank < 0
            or next_can_other_bank > num_can or next_mis_other_bank > num_mis):
                continue

            # State falls within m and c constraints
            next_state = (next_mis, next_can, next_boat_pos)
            # ADDITION: Check if this state has been visited
            next_visited = False
            for visited_node in visited:
                if next_state == visited_node.state:
                    next_visited = True
                    break
            
            # ADDITION: If state is visited, do not add it to frontier, else do add it to frontier
            if next_visited:
                continue
            next_node = utils.Node(curr_node, action, next_state, curr_node.g_n + 1, 0)
            frontier.push(next_node.g_n, next_node)
        # ADDITION: Add every processed node to the visited array for tracking purpose
        visited.add(curr_node)
    """ END YOUR CODE HERE """
    
    if fail:
        return False
    return solution

# Test Task 1
@wrap_test
def test_bfs_tree_search(case):
    input_dict = case['input_dict']
    answer = case['answer']
    
    m, c = input_dict['initial']
    start = time.time()
    solution = bfs_tree_search(m, c)
    print(f"Time lapsed: {time.time() - start}")

    if solution is False:
        assert answer["solution"] is False, "Solution is not False"
    else:
        correctness = solution == answer["solution"]
        cost = len(solution)
        assert correctness, f"Fail to reach goal state with solution {solution}"
        assert cost <= answer['cost'], f"Cost is not optimal."
    return "PASSED"

# Test Task 2
@wrap_test
def test_dfs_tree_search(case):
    input_dict = case['input_dict']
    answer = case['answer']
    
    m, c = input_dict['initial']
    start = time.time()
    solution = dfs_tree_search(m, c)
    print(f"Time lapsed: {time.time() - start}")

    if solution is False:
        assert answer["solution"] is False, "Solution is not False"
    else:
        correctness = solution == answer["solution"]
        cost = len(solution)
        assert correctness, f"Fail to reach goal state with solution {solution}"
    return "PASSED"

# Test Task 3
@wrap_test
def test_bfs_graph_search(case):
    input_dict = case['input_dict']
    answer = case['answer']
    
    m, c = input_dict['initial']
    start = time.time()
    solution = bfs_graph_search(m, c)
    print(f"Time lapsed: {time.time() - start}")

    if solution is False:
        assert answer["solution"] is False, "Solution is not False"
    else:
        correctness = solution == answer["solution"]
        cost = len(solution)
        assert correctness, f"Fail to reach goal state with solution {solution}"
        assert cost <= answer['cost'], f"Cost is not optimal."
    return "PASSED"

def test_three_mnc(m, c, rounds):
    for r in range(1, rounds + 1):
        print(f"ROUND {r}")
        start = time.time()
        # solution = bfs_tree_search(m, c)
        # print(f"BFS TREE - Time lapsed: {time.time() - start}")
        start = time.time()
        solution = dfs_tree_search(m, c)
        print(f"DFS TREE - Time lapsed: {time.time() - start}")
        start = time.time()
        # solution = bfs_graph_search(m, c)
        # print(f"BFS GRAPH - Time lapsed: {time.time() - start}")

print("TEST 1")
# test_three_mnc(5, 3, 5)

print("\nTEST 2")
test_three_mnc(4, 3, 5)

print("\nTEST 3")
test_three_mnc(4, 4, 5)

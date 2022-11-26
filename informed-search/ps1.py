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
    # TODO: Change to prio queue
    frontier = utils.PriorityQueue()
    frontier.push(start_node.g_n, start_node)
    while len(frontier) != 0:
        print(len(frontier))
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
            print(next_state)
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
        print(curr_state)
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

# Test cases for Task 1
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

# Test cases for Task 2
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

def heuristic_func(problem: cube.Cube, state) -> float:
    r"""
    Computes the heuristic value of a state
    
    Args:
        problem (cube.Cube): the problem to compute
        state (cube.State): the state to be evaluated
        
    Returns:
        h_n (float): the heuristic value 
    """
    h_n = 0.0
    goals = problem.goal

    """ YOUR CODE HERE """
    # Calculate how many tiles are not in the right place, and divide
    # that number by the max(rows, columns)
    shape = goals.shape
    max_dim = max(shape)

    for i in range(len(goals.layout)):
        if goals.layout[i] == state.layout[i]:
            continue
        h_n += 1

    h_n /= max_dim
    """ END YOUR CODE HERE """

    return h_n

def astar_search(problem: cube.Cube):
    r"""
    A* Search finds the solution to reach the goal from the initial.
    By default, fail is True and returns False.
    
    Args:
        problem (cube.Cube): Cube instance

    Returns:
        solution (List[Action]): the action sequence
    """
    fail = True
    solution = []
    
    """ YOUR CODE HERE """
    start_node = utils.Node(None, None, problem.initial, 0, heuristic_func(problem, problem.initial))
    frontier = utils.PriorityQueue()
    frontier.push(start_node.get_fn(), start_node)
    visited = set()
    visited.add(start_node)
    while len(frontier) != 0:
        curr_node = frontier.pop()
        curr_state = curr_node.state
        # Check if state is goal state
        if problem.goal_test(curr_state):
            trace_act = curr_node.act
            while trace_act != None:
                solution.append(trace_act)
                curr_node = curr_node.parent
                trace_act = curr_node.act
            fail = False
            solution.reverse()
            break
        # Calculate all possible actions from this state
        for action in problem.actions(curr_state):
            next_state = problem.result(curr_state, action)
            if next_state in visited:
                continue
            next_node = utils.Node(curr_node, action, next_state,
                problem.path_cost(curr_node.g_n, curr_state, action, next_state), heuristic_func(problem, next_state))
            frontier.push(next_node.get_fn(), next_node)
        visited.add(curr_node)
    """ END YOUR CODE HERE """
    
    if fail:
        return False
    return solution

# Test cases for Task 6
@wrap_test
def test_astar(case):

    input_dict = case['input_dict']
    answer = case['answer']
    problem = cube.Cube(input_dict = input_dict)
    
    start = time.time()
    solution = astar_search(problem)
    print(f"Time lapsed: {time.time() - start}")

    if solution is False:
        assert answer["solution"] is False, "Solution is not False"
    else:
        correctness, cost = problem.verify_solution(solution, _print=False)
        assert correctness, f"Fail to reach goal state with solution {solution}"
        assert cost <= answer['cost'], f"Cost is not optimal."
    return "PASSED"

cube1 = {'input_dict': {"initial": {'shape': [3, 3], 'layout': ['N', 'U',   
    'S', 'N','U', 'S', 'N', 'U', 'S']}, "goal": {'shape': [3, 3], 'layout': 
    ['N', 'U', 'S', 'N', 'U', 'S', 'N', 'U', 'S']}}, 'answer': {"solution": 
    [], "cost": 0}}

cube2 = {'input_dict': {"initial": {'shape': [3, 3], 'layout': ['S', 'O', 
    'C', 'S', 'O', 'C', 'S', 'O', 'C']}, "goal": {'shape': [3, 3], 
    'layout': ['S', 'S', 'S', 'O', 'O', 'O', 'C', 'C', 'C']}}, 'answer': 
    {"solution": [[2, 'right'], [1, 'left'], [1, 'down'], 
    [2, 'up']], "cost": 4}}

cube3 = {'input_dict': {"initial": {'shape': [3, 3], 'layout': ['N', 'U',   
    'S', 'N','U', 'S', 'N', 'U', 'S']}, "goal": {'shape': [3, 3], 'layout': 
    ['S', 'U', 'N', 'S', 'U', 'N', 'S', 'U', 'N']}}, 'answer': {"solution": 
    [[0, 'right'], [2, 'left'], [2, 'down'], [1, 'up'], [1, 'left'], 
    [2, 'right']], "cost": 6}}

cube4 = {'input_dict':{"initial": {'shape': [3, 4], 'layout': [1, 1, 9, 0,
    2, 2, 0, 2, 9, 0, 1, 9]}, "goal": {'shape': [3, 4], 'layout': [2, 1, 0,
    9, 2, 1, 0, 9, 2, 1, 0, 9]}}, 'answer': {"solution": [[3, "up"], 
    [1, "down"], [2, "left"], [0, "right"]], "cost": 4}}

print('cube1: ' + test_astar(cube1))
print('cube2: ' + test_astar(cube2))
print('cube3: ' + test_astar(cube3))
print('cube4: ' + test_astar(cube4))
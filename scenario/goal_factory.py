import random
from config import DEFAULT_EXEC_STEPS
from scenario.env import CellType


class Goal:
    def __init__(self, pos, executing_steps=DEFAULT_EXEC_STEPS):
        self.pos = pos
        self.executing_steps = executing_steps

    def is_satisfied(self, agent):
        return agent.pos == self.pos


# --------------------------
# Goal Chains
# --------------------------

# for both finite and infinite simulation
# a goal chain = a list of Goal objects (pos, executing_steps)

INIT_GOAL_CHAIN = {
    "worker_default": [
        ([CellType.WORKSHOP], 5)],

    "vehicle_default": [
        ([CellType.DEPOT], 5),
        ([CellType.WORKSHOP], 5),
        ([CellType.PARKING], 10)],

    # --> add various chains here <--
    # ......

}

# for infinite simulation --> new goal generation strategy
ACTIVE_GOAL_CHAIN = {

    "worker_default": [
        ([CellType.WORKSHOP], 5)],
    
    "vehicle_default": [
        ([CellType.DEPOT], 5),
        ([CellType.WORKSHOP], 5),
        ([CellType.PARKING], 10)],

    # --> add various chains here <--
    # ......

}


# ----------------
# Goal Generation
# ----------------

def sample_goal(grid, cell_types, executing_steps):
    """
    return a Goal object
    --> specify a target cell from all valid cells as the goal pas
    """
    rows, cols = grid.shape
    valid_cells = [
        (x, y) 
        for x in range(rows) 
        for y in range(cols) 
        if grid[x, y] in cell_types
    ]

    if not valid_cells:
        return None

    pos = random.choice(valid_cells)
    return Goal(pos, executing_steps)


def build_init_goal(agent, chain_name):
    chain = INIT_GOAL_CHAIN.get(chain_name, [])
    goals = []

    for cell_types, steps in chain:
        goal = sample_goal(agent.map, cell_types, steps)
        if goal:
            goals.append(goal)

    return goals

def build_active_goal(agent, chain_name):
    chain = ACTIVE_GOAL_CHAIN.get(chain_name, [])
    goals = []

    for cell_types, steps in chain:
        goal = sample_goal(agent.map, cell_types, steps)
        if goal:
            goals.append(goal)

    return goals
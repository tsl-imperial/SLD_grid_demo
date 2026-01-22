import random
from scenario.env import CellType
from config import DEFAULT_EXEC_STEPS


class Goal:
    def __init__(self, pos, executing_steps=2):
        self.pos = pos
        self.executing_steps = executing_steps

    def is_satisfied(self, agent):
        return agent.pos == self.pos
    

def generate_goals_by_type(map, cell_types, default_executing_steps=DEFAULT_EXEC_STEPS):
    goals = []
    rows, cols = map.shape
    print(0)
    for ctype in cell_types:
        valid_cells = [(x, y) for x in range(rows) for y in range(cols) if map[x, y] == ctype]
        print(valid_cells)
        if valid_cells:
            pos = random.choice(valid_cells)
            goals.append(Goal(pos, executing_steps=default_executing_steps))
    return goals

def generate_new_goal(map, cell_types, default_executing_steps=DEFAULT_EXEC_STEPS):
    rows, cols = map.shape
    valid_cells = []

    for ctype in cell_types:
        valid_cells.extend(
            [(x, y) for x in range(rows) for y in range(cols) if map[x, y] == ctype]
        )
    
    if not valid_cells:
        return None
    
    pos = random.choice(valid_cells)
    return Goal(pos, executing_steps=default_executing_steps)


def get_goals(agent, default_executing_steps=DEFAULT_EXEC_STEPS):
    """
    return list of Goal objects
    """
    if agent.agent_type == "worker":
        return generate_goals_by_type(agent.map, [CellType.WORKSHOP], default_executing_steps)
    elif agent.agent_type == "vehicle":
        return generate_goals_by_type(agent.map, [CellType.DEPOT, CellType.WORKSHOP, CellType.PARKING], default_executing_steps)
    else:
        return []

def append_new_goal(agent):
    """
    for infinite simulation
    """
    if agent.agent_type == "worker":
        cell_types = [CellType.WORKSHOP, CellType.DEPOT]     # define potential goals
        new_goal = generate_new_goal(agent.map, cell_types, DEFAULT_EXEC_STEPS)
        print(new_goal.pos)
    if agent.agent_type == "vehicle":
        cell_types = [CellType.DEPOT, CellType.WORKSHOP, CellType.PARKING]
        new_goal = generate_new_goal(agent.map, cell_types, DEFAULT_EXEC_STEPS)
    
    return new_goal
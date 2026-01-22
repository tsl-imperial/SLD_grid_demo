from scenario.goal_factory import Goal

def move_towards_goal(agent):
    """
    simple deterministic movement towards goal
    (prioritize x movement first, then y)
    """
    x, y = agent.pos
    gx, gy = agent.goals[agent.current_goal_idx].pos

    if x < gx:
        return (1, 0)
    elif x > gx:
        return (-1, 0)
    elif y < gy:
        return (0, 1)
    elif y > gy:
        return (0, -1)
    else:
        return (0, 0)
    
# -----------------
# various policies
# -----------------

from scenario.goal_factory import Goal

MOVING_POLICY = {}

def register_policy(name):
    def decorator(func):
        MOVING_POLICY[name] = func
        return func
    return decorator


# --------------------------
# Moving Policies
# --------------------------

# function(agent)
# calculate and return (dx,dy)

@register_policy("move_towards_goal")
def move_towards_goal(agent):
    """
    simple deterministic movement towards goal
    (prioritize x movement first, then y)
    """
    x, y = agent.pos
    gx, gy = agent.current_goal.pos

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
    
# --> add various moving policies here <--
# e.g., 
# @register_policy("policy name"):
# def ......


# ------------------
# Policy Generation
# ------------------
    
def build_policy(policy_name):
    if policy_name not in MOVING_POLICY:
        raise ValueError(f"Unknown policy: {policy_name}")
    return MOVING_POLICY[policy_name]

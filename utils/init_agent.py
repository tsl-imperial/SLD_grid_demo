import numpy as np
from scenario.env import CellType
from scenario.agent import Agent

# --------------------------
# agents
# --------------------------

def parse_agent_spec(spec):
    """
    return:
        count: int
        extra: dict, other parameters for Agents
    """
    if isinstance(spec, int):
        # e.g., 
        # agent_specs = {
        # "worker": 3,
        # "vehicle": 2
        # }
        extra = {}
        return spec, extra

    if isinstance(spec, dict):
        # e.g., 
        # agent_specs = {
        # "worker": {"count": 3},
        # "vehicle": {"count": 2, "pos": [(0, 0),(1, 1)], "policy": "move_towards_goal"}
        # }
        count = spec.get("count", 1)
        extra = spec.copy()
        extra.pop("count", None)  

        return count, extra

    raise TypeError(f"Invalid agent spec: {spec}")


def generate_random_agents(map, agent_specs):
    """
    generate random agent population, supporting optional position, policy (, and etc. like speed)
    """
    if agent_specs is None:
        agent_specs = {"worker": 1, "vehicle": 1}
    
    h, w = map.shape
    agents = []
    type_counters = {a:0 for a in agent_specs.keys()}
    occupied = set()

    for agent_type, specs in agent_specs.items():
        # for heterogeneous groups
        # e.g., 
        # agent_specs = {
        #     "worker": [
        #         {"count": 2, "policy": ["move_towards_goal", "..."]},
        #         {"count": 1, "speed": 3}  # 1 worker with a speed of 3
        #     ],
        #     "vehicle": [
        #         2,  # 2 vehicles with default params 
        #         {"count": 1, "pos": [(5,5)], "speed": 6}
        #     ]
        # }
        if not isinstance(specs, list):
            specs = [specs]

        for spec in specs:

            n_agents, extra_kwargs = parse_agent_spec(spec)

            # convert all single values into lists of length n_agents
            for k, v in extra_kwargs.items():
                if not isinstance(v, list):
                    extra_kwargs[k] = [v] * n_agents
                elif len(v) != n_agents:
                    raise ValueError(f"Length of {k} ({len(v)}) != count {n_agents}")

            for i in range(n_agents):
                # if pos is not specified, generate it randomly
                # ------------------------------------------
                # TO DO: 
                # extended to other params (policy, spd, ...)
                # ------------------------------------------
                if "pos" not in extra_kwargs or extra_kwargs["pos"][i] is None:
                    placed = False
                    while not placed:
                        x = np.random.randint(0, h)
                        y = np.random.randint(0, w)
                        if map[x, y] == CellType.EMPTY and (x, y) not in occupied:
                            extra_kwargs.setdefault("pos", [None]*n_agents)[i] = (x, y)
                            placed = True
                else:
                    # --- if pos is specified, ignore occupancy conflicts --- #
                    x, y = extra_kwargs["pos"][i]
                    # if map[x, y] != CellType.EMPTY or (x, y) in occupied:
                    #    raise ValueError(f"Specified pos {(x, y)} for {agent_type} is not empty")

                name = f"{agent_type}_{type_counters[agent_type]}"
                type_counters[agent_type] += 1

                agent_params = {k: extra_kwargs[k][i] for k in extra_kwargs}
                agent_params["agent_type"] = agent_type
                agent_params["map"] = map
                agent_params["name"] = name

                agent = Agent(**agent_params)
                agents.append(agent)
                occupied.add(agent.pos)

    return agents




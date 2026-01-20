
from agent import Agent

class SimulationEvaluator:
    def __init__(self, env, agents):
        self.env = env
        self.agents = agents
        # initialisation
        # agent.name required!
        self.agent_paths = {agent.name: [agent.pos] for agent in agents}
        self.num_collisions = 0
        self.prev_collisions = {}   # pair -> last_position
        # self.counted_collisions = set()

    def eval_metrics(self):

        positions = {}        # dict: key - pos(x,y); value - agent.name
        current_collisions = {}   # pair -> position

        for agent in self.agents:
            self.agent_paths[agent.name].append(agent.pos)

            # --------------------------------------------------------
            # TO DO: collision check in entities
            # Currently: collision +1 even agents meet within entities, and

            # only save (agent 1, agent 2) -->+1

            # if agent.pos in positions: 
            #     self.num_collisions += 1 
            # positions[agent.pos] = agent.name

            if agent.pos in positions:
                other = positions[agent.pos]
                pair = frozenset([agent.name, other])
                current_collisions[pair] = agent.pos

            positions[agent.pos] = agent.name

            for pair, pos in current_collisions.items():
                if pair not in self.prev_collisions:
                    # case 1: meet for the first time
                    self.num_collisions += 1
                else:
                    prev_pos = self.prev_collisions[pair]
                    if pos != prev_pos:
                        # case 2: move together
                        self.num_collisions += 1
                    # else:
                    # case 3: meet and then both keep static

        self.prev_collisions = current_collisions


        path_lengths = {}
        for name, path in self.agent_paths.items():
            length = 0
            for (x0, y0), (x1, y1) in zip(path[:-1], path[1:]):
                length += abs(x1 - x0) + abs(y1 - y0)
            path_lengths[name] = length

        goal_achieved = {agent.name: agent.current_goal is None for agent in self.agents}

        return {
            # overall metrics
            "num_collisions": self.num_collisions,

            # agent metrics
            "path_lengths": path_lengths,
            "goal_achieved": goal_achieved
        }
    
    # -----------------------------
    # TO DO: def eval_summary(self)
    # -----------------------------
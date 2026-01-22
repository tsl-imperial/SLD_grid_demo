
from scenario.agent import Agent

class SimulationEvaluator:
    """
    evaluate simulation metrics at each timestep

    metrics:
    num_collisions
    path_lengths : dict
    goal_achieved : dict {agent|bool}
    """
    def __init__(self, env, agents):
        self.env = env
        self.agents = agents

        # initialisation
        # agent.name required!
        self.agent_paths = {agent.name: [agent.pos] for agent in agents}

        self.num_collisions = 0
        self.prev_collisions = {}   # pair: last_position

    # ---------------
    # collision
    # ---------------
    def collision_record(self):
        """
        return dict
            key   : frozenset({agent_name_1, agent_name_2})
            value : collision position (x, y)
        """
        positions = {}     # pos -> agent.name
        collisions = {}    # pair -> pos

        for agent in self.agents:
            pos = agent.pos

            if pos in positions:
                other = positions[pos]
                pair = frozenset([agent.name, other])
                collisions[pair] = pos

            positions[pos] = agent.name

        return collisions
    
    def compute_collision(self, current_collisions):
        for pair, pos in current_collisions.items():
            # rule1: first-time meeting -> +1
            if pair not in self.prev_collisions:
                self.num_collisions += 1
            else:
                prev_pos = self.prev_collisions[pair]
                # rule2: move together to new cell -> +1
                if pos != prev_pos:
                    self.num_collisions += 1
                # else:
                #     rule3: stay together -> +0

        # update prev_collisions for next timestep
        self.prev_collisions = current_collisions

    # ---------------
    # path length
    # ---------------
    def compute_path_length(self):
        path_lengths = {}

        for name, path in self.agent_paths.items():
            length = 0
            for (x0, y0), (x1, y1) in zip(path[:-1], path[1:]):
                length += abs(x1 - x0) + abs(y1 - y0)
            path_lengths[name] = length

        return path_lengths
    
    # -----------------
    # goal achievement
    # -----------------
    def compute_goal_achievement(self):
        return {
            agent.name: agent.current_goal is None
            for agent in self.agents
        }
    
    # -------------------
    # full eval metrics
    # -------------------
    def eval_metrics(self):
        """
        evaluate all metrics at the current timestep
        """

        for agent in self.agents:
            self.agent_paths[agent.name].append(agent.pos)

        current_collisions = self.collision_record()
        self.compute_collision(current_collisions)

        path_lengths = self.compute_path_length()
        goal_achieved = self.compute_goal_achievement()

        return {
            "num_collisions": self.num_collisions,
            "path_lengths": path_lengths,
            "goal_achieved": goal_achieved
        }
    
    
    # -----------------------------
    # TO DO: def eval_summary(self)
    # -----------------------------
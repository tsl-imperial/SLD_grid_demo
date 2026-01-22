import random
from enum import Enum

from scenario.goal_factory import get_goals, append_new_goal
from scenario.moving_policy_factory import move_towards_goal

from config import SIM_TYPE

class AgentStatus(Enum):
    MOVING = 0        # move to the next goal ( <-- policy )
    EXECUTING = 1     # execute the task in a certain entity (keep current position)
    DONE = 2          # complete all goals (keep current position)

class Agent:
    def __init__(self, agent_type, pos, map, name=None, policy=move_towards_goal):
        """
        agent_type: "worker" or "vehicle"
        pos: tuple (x, y)
        map: static_map --> 2d array
        """
        self.agent_type = agent_type

        self.pos = pos
        self.map = map

        self.goals = get_goals(self)     # ultimate goals for finite sim/initial goals for infinite sim
        self.current_goal_idx = 0
        self.status = AgentStatus.MOVING
        self.execute_timer = 0  # record the duration at executing phase

        self.name = name        # required for evaluation and rendering
        self.policy = policy
    
    def __repr__(self):
        return f"{self.name}, pos={self.pos}, policy={self.policy.__name__}"
    
    @property
    def current_goal(self):       # check the progress of the objectives
        # return an objective of Goal
        if self.current_goal_idx < len(self.goals):
            return self.goals[self.current_goal_idx]
        else:
            return None  

    def act(self):
        
        # status = Done
        if self.status == AgentStatus.DONE:
            return (0, 0)        # all objectives achieved (dx, dy) = (0, 0)
        
        # status = Moving
        if self.status == AgentStatus.MOVING:
            # current goal achieved: status --> Executing
            if self.current_goal.is_satisfied(self):
                self.status = AgentStatus.EXECUTING
                self.execute_timer = 0
                return (0, 0)

            return self.policy(self)
        
        # status = Executing
        if self.status == AgentStatus.EXECUTING:
            self.execute_timer += 1

            # if reach executing_steps, status --> Done / Moving (to the next goal)
            if self.execute_timer >= self.current_goal.executing_steps:
                self.current_goal_idx += 1
            
                if self.current_goal is None:
                    if SIM_TYPE == "INFINITE":
                        # generate additional goals and append to initial goals
                        new_goal = append_new_goal(self)
                        self.goals.append(new_goal)

                        self.status = AgentStatus.MOVING

                    else:
                        self.status = AgentStatus.DONE      # mark DONE
                else:
                    self.status = AgentStatus.MOVING

            return (0, 0)



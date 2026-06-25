import sys
import copy
from algorithms.base_solver import BaseSolver
sys.setrecursionlimit(5000)

class AndOrGraphSolver(BaseSolver):
    def __init__(self):
        self.memo = {}

    def or_search(self, state, path, total_visited):
        state_key = state.state_key()
        if state.is_goal():
            return [], total_visited
        if state_key in path:
            return "failure", total_visited
        
        if state_key in self.memo:
            return self.memo[state_key], total_visited

        for name, step in state.get_valid_moves():
            total_visited[0] += 1
            child_state = state.move_vehicle(name, step)
            result_states = [child_state]
            sign = 1 if step > 0 else -1
            over_step = step + sign
            if (name, over_step) in state.get_valid_moves():
                result_states.append(state.move_vehicle(name, over_step))
            plan, total_visited = self.and_search(result_states, path | {state_key}, total_visited)
            if plan != "failure":
                main_plan = plan[child_state.state_key()]
                final_plan = [(name, step)] + main_plan
                self.memo[state_key] = final_plan
                return final_plan, total_visited
        self.memo[state_key] = "failure"
        return "failure", total_visited

    def and_search(self, states, path, total_visited):
        plans = {}
        for s in states:
            plan_s, total_visited = self.or_search(s, path, total_visited)
            if plan_s == "failure":
                return "failure", total_visited
            plans[s.state_key()] = plan_s
        return plans, total_visited

    def solve(self, initial_board):
        self.memo = {}
        total_visited = [0]
        result, total_visited = self.or_search(initial_board, set(), total_visited)
        if result == "failure" or not result:
            return None 
        return {"path": result, "visited": total_visited[0]}
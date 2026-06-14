from algorithms.base_solver import BaseSolver
from algorithms.search_framework import Frontier, Node


class BeliefGoalSolver(BaseSolver):
    def solve(self, initial_board):
        reached = set()
        result = self.BGS(initial_board, reached)
        if result == "Không thể giải được":
            return None
        path = []
        current = result
        while current.parent is not None:
            path.append(current.action)
            current = current.parent
        path.reverse()
        return {"path": path, "visited" : len(reached)}
    
    def BGS(self, problem, reached):
        def check_goal(state): #belief goal la xe nam o 2 dau mut cua hang 
            return state.vehicles["X"].col == 4 or state.vehicles["X"].col == 0
        
        node = Node(problem, None, None, 0)
        if check_goal(node.state) == True:
            return node
        frontier = Frontier(is_fifo=True)
        frontier.enqueue(node)
        reached.add(node.state.state_key())
        while frontier.is_empty() == False:
            node  = frontier.dequeue()
            for v, action in node.state.get_valid_moves():
                new_state = node.state.move_vehicle(v, action)
                child = Node(new_state, node, (v, action), node.path_cost + 1)
                if check_goal(child.state) == True:
                    return child
                if child.state.state_key() not in reached and frontier.is_contain(child) == False:
                    frontier.enqueue(child)
                    reached.add(child.state.state_key())
        return "Không thể giải được"

        
from algorithms.base_solver import BaseSolver
from algorithms.search_framework import Node, hn
import random

class SHCSolver(BaseSolver):
    def SHC(self, initial_board, reached):
        current_node = Node(initial_board, None, None, hn(initial_board))
        reached.add(current_node.state.state_key())
        while True:
            if current_node.state.is_goal():
                return current_node
            better_neighbors = []
            for name, step in current_node.state.get_valid_moves():
                child_state = current_node.state.move_vehicle(name, step)
                child = Node(child_state, current_node, (name, step), hn(child_state))
                reached.add(child.state.state_key())
                if child.path_cost < current_node.path_cost:
                    better_neighbors.append(child)

            if len(better_neighbors) == 0:
                return current_node
            
            current_node = random.choice(better_neighbors)

    def solve(self, initial_board):
        reached = set()
        result = self.SHC(initial_board, reached)
        current = result
        path = []
        while current.parent is not None:
            path.append(current.action)
            current = current.parent
        path.reverse()
        if not result.state.is_goal():
            return {"path": path, "visited": "Chỉ đạt tới trạng thái tối ưu cục bộ, không thể giải"}
        return {"path": path, "visited": len(reached)}
import random
from algorithms.base_solver import BaseSolver
from algorithms.search_framework import Node, hn


class LBSSolver(BaseSolver):
    def __init__(self, k=3):
        self.k = k

    def LBS(self, initial_board, reached):
        node = Node(initial_board, None, None, hn(initial_board))
        if node.state.is_goal():
            return node
        current_node_set = []
        for name, step in node.state.get_valid_moves():
            child_state = node.state.move_vehicle(name, step)
            child = Node(child_state, node, (name, step), hn(child_state))
            current_node_set.append(child)
        if len(current_node_set) > 3:
            current_node_set = random.sample(current_node_set, self.k)
        while True:
            neighbors = []
            for n in current_node_set:
                for name, step in n.state.get_valid_moves():
                    child_state = n.state.move_vehicle(name, step)
                    child = Node(child_state, n, (name, step),hn(child_state))
                    key = child_state.state_key()
                    if key not in reached:
                        neighbors.append(child)
                        reached.add(key)

            if len(neighbors) == 0:
                current_node_set.sort()
                return current_node_set[0]

            for neighbor in neighbors:
                if neighbor.state.is_goal():
                    return neighbor

            neighbors.sort()

            if len(neighbors) <= self.k:
                current_node_set = neighbors.copy()
            else:
                current_node_set = neighbors[:self.k]

    def solve(self, initial_board):
        reached = set()
        result = self.LBS(initial_board, reached)
        current = result
        path = []
        while current.parent is not None:
            path.append(current.action)
            current = current.parent
        path.reverse()
        if not result.state.is_goal():
            return {
                "path": path,
                "visited": "Chỉ đạt tới trạng thái tối ưu cục bộ, không thể giải"
            }
        return {
            "path": path,
            "visited": len(reached)
        }
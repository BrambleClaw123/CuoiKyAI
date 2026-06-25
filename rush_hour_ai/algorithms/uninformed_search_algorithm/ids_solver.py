from algorithms.base_solver import BaseSolver
from algorithms.search_framework import Frontier, Node

class IDSSolver(BaseSolver):
    def IDS(self, initial_board):
        def DLS(initial_board, depth, reached):
            node = Node(initial_board, None, None, 0)

            if node.state.is_goal():
                return node
            result = "Không thể giải được"
            frontier = Frontier(is_fifo=False)
            frontier.enqueue(node)
            reached.add(node.state.state_key())
            while not frontier.is_empty():
                node = frontier.dequeue()
                if node.path_cost >= depth:
                    result = "cutoff"
                    continue
                for name, step in node.state.get_valid_moves():
                    child_state = node.state.move_vehicle(name, step)
                    child = Node(child_state, node, (name, step), node.path_cost + 1)
                    if child.state.is_goal():
                        return child
                    key = child.state.state_key()
                    if key not in reached:
                        reached.add(key)
                        frontier.enqueue(child)

            return result
        depth = 0
        total_visited = 0
        while True:
            reached = set()
            result = DLS(initial_board, depth, reached)
            total_visited += len(reached)
            if result != "cutoff":
                return result, total_visited
            depth += 1
    def solve(self, initial_board):
        result, visited = self.IDS(initial_board)
        if result == "Không thể giải được":
            return None
        path = []
        current = result
        while current.parent is not None:
            path.append(current.action)
            current = current.parent
        path.reverse()
        return {"path": path, "visited": visited}
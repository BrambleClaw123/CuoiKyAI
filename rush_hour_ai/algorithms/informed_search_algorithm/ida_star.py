from algorithms.base_solver import BaseSolver
from algorithms.search_framework import Frontier, Node, hn


class IDAStarSolver(BaseSolver):
    def IDA_star(self, initial_board):
        def search(initial_board, bound, reached):
            node = Node(initial_board, None, None, 0 + hn(initial_board))
            frontier = Frontier(is_fifo=False)
            frontier.enqueue(node)
            reached.add(node.state.state_key())
            minimum = float('inf')
            while not frontier.is_empty():
                node = frontier.dequeue()
                if node.path_cost > bound:
                    minimum = min(minimum, node.path_cost)
                    continue
                if node.state.is_goal():
                    return node, bound
                for name, step in node.state.get_valid_moves():
                    child_state = node.state.move_vehicle(name, step)
                    child = Node(child_state, node, (name, step), node.path_cost - hn(node.state) + hn(child_state) + 1)
                    key = child.state.state_key()
                    if key not in reached:
                        reached.add(key)
                        frontier.enqueue(child)
            return "cutoff", minimum

        bound = hn(initial_board)
        total_visited = 0
        while True:
            reached = set()
            result, new_bound = search(initial_board, bound, reached)
            total_visited += len(reached)
            if result != "cutoff":
                return result, total_visited
            if new_bound == float('inf'):
                return "Không thể giải được", total_visited
            bound = new_bound

    def solve(self, initial_board):
        result, visited = self.IDA_star(initial_board)
        if result == "Không thể giải được":
            return None
        path = []
        current = result
        while current.parent is not None:
            path.append(current.action)
            current = current.parent
        path.reverse()
        return {"path": path, "visited": visited}
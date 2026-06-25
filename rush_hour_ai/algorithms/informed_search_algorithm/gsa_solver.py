from algorithms.base_solver import BaseSolver
import heapq

from algorithms.search_framework import Node, hn


class GSASolver(BaseSolver):
    def solve(self, initial_board):
        reached = {}
        result = self.GSA(initial_board, reached)
        if result == "Không thể giải được":
            return None
        path = []
        current = result
        while current.parent is not None:
            path.append(current.action)
            current = current.parent
        path.reverse()
        return {
            "path": path,
            "visited": len(reached)
        }

    def GSA(self, problem, reached):
        node = Node(problem, None, None, hn(problem))
        if node.state.is_goal():
            return node
        frontier = []
        heapq.heappush(frontier, node)
        while len(frontier) != 0:
            node = heapq.heappop(frontier)
            reached[node.state.state_key()] = node.path_cost
            if node.path_cost > reached[node.state.state_key()]:
                continue
            if node.state.is_goal():
                return node
            for v, action in node.state.get_valid_moves():
                new_state = node.state.move_vehicle(v, action)
                child = Node(
                    new_state, node, (v, action), hn(new_state))
                if (new_state.state_key() not in reached or
                        child.path_cost < reached[new_state.state_key()]):
                    heapq.heappush(frontier, child)
        return "Không thể giải được"
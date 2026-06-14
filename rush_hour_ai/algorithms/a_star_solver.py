from algorithms.base_solver import BaseSolver
import heapq

from algorithms.search_framework import Node, hn

class AStarSolver(BaseSolver) :
    def solve(self, initial_board):
        reached = {}
        result = self.a_star(initial_board, reached)
        if result == "Không thể giải được":
            return None
        path = []
        current = result
        while current.parent is not None:
            path.append(current.action)
            current = current.parent
        path.reverse()
        return {"path" : path, "visited" : len(reached)}

    
    def a_star(self, problem, reached):
        node = Node(problem, None, None, 0 + hn(problem))
        if node.state.is_goal() == True:
            return node
        frontier = []
        heapq.heappush(frontier, node)
        while len(frontier) != 0:
            node = heapq.heappop(frontier)
            reached[node.state.state_key()] = node.path_cost

            if node.path_cost > reached[node.state.state_key()]:
                continue
            if node.state.is_goal() == True:
                return node
            for v, action in node.state.get_valid_moves():
                new_state = node.state.move_vehicle(v, action)
                child = Node(new_state, node, (v, action), node.path_cost - hn(node.state) + hn(new_state) + 1)
                if new_state.state_key() not in reached or child.path_cost < reached[new_state.state_key()]:
                    heapq.heappush(frontier, child)
        return "Không thể giải được"
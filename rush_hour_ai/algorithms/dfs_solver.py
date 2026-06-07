from algorithms.base_solver import BaseSolver
from algorithms.search_framework import Frontier, Node


class DFSSolver(BaseSolver):

    def DFS(self, problem, reached):
        node = Node(problem, None, None, 0)
        if node.state.is_goal() == True :
            return node
        frontier = Frontier(is_fifo=False)
        frontier.enqueue(node)
        reached.add(node.state.state_key())
        while frontier.is_empty() == False:
            node = frontier.dequeue()
            for name, step in node.state.get_valid_moves():
                child_state = node.state.move_vehicle(name, step)
                child = Node(child_state, node, (name, step), node.path_cost + 1)
                if child.state.is_goal():
                    return child
                if child_state.state_key() not in reached and frontier.is_contain(child) == False:
                    reached.add(child.state.state_key())
                    frontier.enqueue(child)
        return "Không thể giải được"

    def solve(self, initial_board):
        reached = set()
        result = self.DFS(initial_board, reached)
        if result == "Không thể giải được":
            return None
        path = []
        current = result
        while current.parent is not None:
            path.append(current.action)
            current = current.parent
        path.reverse()
        return {"path": path, "visited" : len(reached)}
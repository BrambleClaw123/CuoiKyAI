from algorithms.base_solver import BaseSolver
from algorithms.search_framework import Node, Frontier

class BFSSolver(BaseSolver):
    def solve(self, initial_board):
        reached = set()
        result_node = self.BFS(initial_board, reached)
        if result_node == "Không thể giải được":
            return None
        path = []
        curr = result_node
        while curr.parent is not None:
            path.append(curr.action)
            curr = curr.parent
        path.reverse()
        return {"path": path, "visited": len(reached)}
    
    def BFS(self, problem, reached):
        node = Node(problem, None, None, 0)
        if node.state.is_goal() == True:
            return node
        frontier = Frontier(is_fifo=True) 
        frontier.enqueue(node)
        reached.add(node.state.state_key())
        while frontier.is_empty() == False:
            node = frontier.dequeue()
            for name, step in node.state.get_valid_moves():
                child_state = node.state.move_vehicle(name, step)
                child = Node(child_state, node, (name, step), node.path_cost + 1)
                if child.state.is_goal() == True:
                    return child
                state_key = child.state.state_key()
                if state_key not in reached and frontier.is_contain(child) == False:
                    reached.add(state_key)
                    frontier.enqueue(child)  
        return "Không thể giải được"
from algorithms.base_solver import BaseSolver
from algorithms.search_framework import Frontier, Node

class BeliefStateWrapper:
    """Class bọc giúp Frontier gọi được .state_key() trên một cụm nhiều bàn cờ"""
    def __init__(self, boards):
        self.boards = tuple(boards)
        
    def state_key(self):
        # Nối state_key của tất cả các kịch bản lại thành 1 khóa duy nhất
        return tuple(b.state_key() for b in self.boards)
        
    def __iter__(self):
        # Cho phép vòng lặp for state in node.state hoạt động
        return iter(self.boards)

class PartialStartSolver(BaseSolver):
    def solve(self, initial_beliefs):
        reached = set()
        result = self.PSS(initial_beliefs, reached)
        
        if result == "Không thể giải được":
            return None
            
        path = []
        current = result
        while current.parent is not None:
            path.append(current.action)
            current = current.parent
        path.reverse()
        
        return {"path": path, "visited": len(reached)}
    
    def PSS(self, initial_beliefs, reached):
        def check_goal(belief_wrapper):
            # Thành công khi TẤT CẢ các kịch bản đều đã đến đích
            return all(state.is_goal() for state in belief_wrapper)
            
        # Khởi tạo node gốc với class bọc
        start_state = BeliefStateWrapper(initial_beliefs)
        node = Node(start_state, None, None, 0)
        
        if check_goal(node.state):
            return node
            
        frontier = Frontier(is_fifo=True) # Dùng BFS để tìm số bước ngắn nhất
        frontier.enqueue(node)
        reached.add(node.state.state_key())
        
        while not frontier.is_empty():
            node = frontier.dequeue()
            
            # Gom tất cả các nước đi có thể thực hiện từ các kịch bản CHƯA đến đích
            possible_actions = set()
            for state in node.state:
                if not state.is_goal():
                    for act in state.get_valid_moves():
                        possible_actions.add(act)
                        
            # Thử từng hành động lên toàn bộ belief state
            for action in possible_actions:
                new_belief = []
                changed = False
                
                for state in node.state:
                    if state.is_goal():
                        # Đã đến đích thì nằm im không nhận lệnh nữa
                        new_belief.append(state)
                    else:
                        # Áp dụng hành động nếu hợp lệ với kịch bản này
                        if action in state.get_valid_moves():
                            new_belief.append(state.move_vehicle(action[0], action[1]))
                            changed = True
                        else:
                            # Không hợp lệ thì xe kẹt lại, kịch bản này đứng im
                            new_belief.append(state)
                            
                # Nếu hành động này vô dụng với tất cả kịch bản, bỏ qua
                if not changed:
                    continue
                    
                # Bọc trạng thái mới lại trước khi đưa vào Node
                child_state = BeliefStateWrapper(new_belief)
                child = Node(child_state, node, action, node.path_cost + 1)
                
                if check_goal(child.state):
                    return child
                    
                b_key = child.state.state_key()
                if b_key not in reached and not frontier.is_contain(child):
                    frontier.enqueue(child)
                    reached.add(b_key)
                    
        return "Không thể giải được"
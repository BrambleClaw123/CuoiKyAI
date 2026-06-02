from collections import deque
from algorithms.base_solver import BaseSolver

class BFS(BaseSolver):
    def __init__(self):
        super().__init__("Breadth First Search (BFS)")

    def solve(self, initial_state):
        # Nếu trạng thái đầu đã là đích thì xong luôn
        if initial_state.is_goal():
            return [initial_state]

        # Hàng đợi (Queue) lưu trữ các tuple: (Trạng_thái_hiện_tại, Đường_đi_đến_đó)
        queue = deque([(initial_state, [initial_state])])
        
        # Tập hợp (Set) lưu các trạng thái đã đi qua để tránh lặp vòng vô hạn
        visited = set([initial_state])

        while queue:
            current_state, path = queue.popleft()

            # Lấy tất cả các nước đi tiếp theo hợp lệ (nhờ "động cơ" đã viết)
            for next_state in current_state.get_successors():
                if next_state not in visited:
                    # Tạo đường đi mới bằng cách nối đường đi cũ với trạng thái mới
                    new_path = path + [next_state]
                    
                    # Kiểm tra xem đã win chưa?
                    if next_state.is_goal():
                        print(f"-> BFS đã duyệt qua tổng cộng {len(visited)} trạng thái bàn cờ khác nhau!")
                        return new_path
                    
                    visited.add(next_state)
                    queue.append((next_state, new_path))
        
        # Chạy hết vòng lặp mà không thấy lối ra
        return []
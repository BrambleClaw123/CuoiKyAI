from algorithms.base_solver import BaseSolver
import math

class MinimaxSolver(BaseSolver):
    def __init__(self):
        # Định nghĩa các phe phái (dựa vào tên xe)
        self.MAX_FACTION = ['X', 'A', 'B'] # Phe Tẩu thoát
        self.MIN_FACTION = ['C', 'D', 'E'] # Phe Cảnh sát
        self.max_turns = 20
        self.visited_states = 0

    def solve(self, initial_board):
        self.visited_states = 0
        path = []
        current_state = initial_board
        
        # Cho AI tự chơi cờ với nhau tối đa 20 lượt
        for turn in range(self.max_turns):
            if current_state.is_goal():
                break # Max đã thoát thành công
                
            is_max = (turn % 2 == 0) # Lượt chẵn là Max, lẻ là Min
            
            # Gọi hàm ra quyết định Minimax (độ sâu = 3)
            best_move = self.minimax_decision(current_state, depth=3, is_max_turn=is_max)
            
            if not best_move:
                break # Phe đến lượt bị kẹt cứng (không có nước đi hợp lệ)
                
            path.append(best_move)
            current_state = current_state.move_vehicle(best_move[0], best_move[1])

        return {"path": path, "visited": self.visited_states}

    # ==========================================
    # CÁC HÀM THÀNH PHẦN THEO MÃ GIẢ (PSEUDO-CODE)
    # ==========================================

    def minimax_decision(self, state, depth, is_max_turn):
        """Tương đương hàm MINIMAX-DECISION(state): Tìm nước đi tốt nhất ban đầu"""
        best_move = None
        
        if is_max_turn:
            max_eval = -math.inf
            for move in self.get_faction_moves(state, is_max=True):
                child = state.move_vehicle(move[0], move[1])
                # Max đi xong thì gọi min_value để xem Min sẽ phản đòn thế nào
                eval_score = self.min_value(child, depth - 1)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
        else:
            min_eval = math.inf
            for move in self.get_faction_moves(state, is_max=False):
                child = state.move_vehicle(move[0], move[1])
                # Min đi xong thì gọi max_value để xem Max sẽ phản đòn thế nào
                eval_score = self.max_value(child, depth - 1)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                    
        return best_move

    def max_value(self, state, depth):
        """Tương đương hàm MAX-VALUE(state): Tìm giá trị lớn nhất cho Max"""
        self.visited_states += 1
        
        if state.is_goal():
            return 1000 + depth # Cộng depth để AI ưu tiên thắng càng nhanh càng tốt
        if depth == 0:
            return self.evaluate(state)
            
        valid_moves = self.get_faction_moves(state, is_max=True)
        if not valid_moves:
            return -1000 # Max hết nước đi -> Max thua -> Trả về giá trị cực nhỏ
            
        v = -math.inf
        for move in valid_moves:
            child = state.move_vehicle(move[0], move[1])
            v = max(v, self.min_value(child, depth - 1))
        return v

    def min_value(self, state, depth):
        """Tương đương hàm MIN-VALUE(state): Tìm giá trị nhỏ nhất cho Min"""
        self.visited_states += 1
        
        if state.is_goal():
            return 1000 + depth # Nếu bàn cờ là đích (Max đã thoát) -> Min thất bại toàn tập
        if depth == 0:
            return self.evaluate(state)
            
        valid_moves = self.get_faction_moves(state, is_max=False)
        if not valid_moves:
            return 1000 # Min hết nước đi -> Min thua -> Trả về giá trị cực lớn có lợi cho Max
            
        v = math.inf
        for move in valid_moves:
            child = state.move_vehicle(move[0], move[1])
            v = min(v, self.max_value(child, depth - 1))
        return v

    # ==========================================
    # CÁC HÀM TIỆN ÍCH (HEURISTIC & LOGIC GAME)
    # ==========================================

    def get_faction_moves(self, state, is_max):
        """Lọc các nước đi hợp lệ theo Phe"""
        moves = state.get_valid_moves()
        if is_max:
            # Max đi được X, A, B và xe Trung lập (Cấm đụng vào xe Cảnh sát)
            return [m for m in moves if m[0] not in self.MIN_FACTION]
        else:
            # Min đi được C, D, E và xe Trung lập (Cấm đụng vào X và đồng minh Max)
            return [m for m in moves if m[0] not in self.MAX_FACTION]

    def evaluate(self, state):
        """Hàm đánh giá Heuristic quyết định độ ngon của bàn cờ"""
        if state.is_goal():
            return 1000 # MAX thắng tuyệt đối
            
        v_x = state.vehicles['X']
        distance = 4 - v_x.col # Khoảng cách tới đích
        
        blocking_cars = 0
        occupied = state.get_occupied_cells()
        # Duyệt các ô phía trước mũi xe X xem có ai cản không
        for c in range(v_x.col + v_x.size, 6):
            if (v_x.row, c) in occupied:
                name = occupied[(v_x.row, c)]
                if name != 'BRICK':
                    # Xe cảnh sát chặn đường bị trừ điểm nặng gấp đôi xe thường
                    weight = 2 if name in self.MIN_FACTION else 1
                    blocking_cars += weight
                    
        max_moves = len(self.get_faction_moves(state, is_max=True))
        min_moves = len(self.get_faction_moves(state, is_max=False))
        
        # Công thức: Khả năng di chuyển - Khoảng cách - Mức độ bị chặn
        return (max_moves - min_moves) - (distance * 10) - (blocking_cars * 20)
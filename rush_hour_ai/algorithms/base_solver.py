class BaseSolver:
    def __init__(self, name="Base Solver"):
        self.name = name

    def solve(self, initial_state):
        """
        Hàm này nhận vào trạng thái đầu và trả về một list các GameState 
        từ lúc bắt đầu đến khi xe mục tiêu thoát ra.
        Nếu không có lời giải, trả về mảng rỗng [].
        """
        raise NotImplementedError("Các thuật toán con phải tự viết lại hàm này!")
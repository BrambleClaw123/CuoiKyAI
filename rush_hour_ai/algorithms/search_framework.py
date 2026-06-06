from collections import deque

class Node:
    """Lớp Node học thuật dùng chung cho mọi thuật toán tìm kiếm dựa trên trạng thái"""
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state        # Trạng thái hiện tại (Đối tượng Board)
        self.parent = parent      # Node cha dẫn đến node này
        self.action = action      # Nước đi dẫn đến node này (Tên_xe, số_bước)
        self.path_cost = path_cost # Tổng số bước đi từ gốc

class Frontier:
    """Hàng đợi FIFO/LIFO cơ bản phục vụ làm hàng đợi tìm kiếm"""
    def __init__(self, is_fifo=True):
        self.queue = deque()
        self.states_in_frontier = set()
        self.is_fifo = is_fifo # True: BFS (FIFO), False: DFS (LIFO)

    def enqueue(self, node):
        self.queue.append(node)
        self.states_in_frontier.add(node.state.state_key())

    def dequeue(self):
        # FIFO thì bốc đầu (.popleft()), LIFO thì bốc đuôi (.pop())
        node = self.queue.popleft() if self.is_fifo else self.queue.pop()
        self.states_in_frontier.remove(node.state.state_key())
        return node

    def is_empty(self):
        return len(self.queue) == 0

    def is_contain(self, node):
        return node.state.state_key() in self.states_in_frontier
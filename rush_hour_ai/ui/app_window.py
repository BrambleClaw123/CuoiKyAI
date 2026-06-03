import customtkinter as ctk
from core.board import Board
from core.vehicle import Vehicle
from algorithms.bfs_solver import BFSSolver

BG_COLOR = "#0D1117"
PANEL_COLOR = "#161B22"
TEXT_COLOR = "#C9D1D9"
CYAN_NEON = "#58A6FF"
CELL_SIZE = 60 

class RushHourApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("RUSHOUR.AI - Gridlock Alpha")
        self.geometry("1100x650")
        self.configure(fg_color=BG_COLOR)
        
        self.initial_board = self.load_level_1()
        self.current_board = self.load_level_1()
        
        self.solvers = {
            "Breadth-First Search (BFS)": BFSSolver()
        }

        # Biến phục vụ kéo thả realtime
        self.selected_vehicle_name = None
        self.drag_data = {"x": 0, "y": 0} # Lưu tọa độ chuột lúc vừa click
        self.ghost_cell = None            # Ô lưới dự kiến sẽ đáp xuống nếu thả chuột

        self.setup_ui()
        self.draw_board()
        self.bind_mouse_events() 

    def load_level_1(self):
        vehicles = [
            Vehicle('A', 0, 0, 2, 'H'), Vehicle('B', 0, 2, 3, 'V'), Vehicle('C', 0, 3, 2, 'H'),
            Vehicle('D', 1, 0, 2, 'H'), Vehicle('E', 1, 3, 2, 'V'),
            Vehicle('X', 2, 0, 2, 'H'), 
            Vehicle('F', 3, 2, 2, 'H'), Vehicle('H', 4, 0, 2, 'V'),
            Vehicle('I', 5, 1, 2, 'H'), Vehicle('G', 3, 4, 3, 'V')
        ]
        return Board(vehicles)

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1, minsize=250)
        self.grid_columnconfigure(1, weight=2, minsize=450)
        self.grid_columnconfigure(2, weight=1, minsize=300)
        self.grid_rowconfigure(0, weight=1)

        # --- CỘT TRÁI ---
        left_panel = ctk.CTkFrame(self, fg_color=PANEL_COLOR, corner_radius=12, border_color="#30363D", border_width=1)
        left_panel.grid(row=0, column=0, padx=15, pady=20, sticky="nsew")
        
        lbl_alg = ctk.CTkLabel(left_panel, text="SELECT ALGORITHM", font=("Segoe UI", 14, "bold"), text_color=CYAN_NEON)
        lbl_alg.pack(padx=15, pady=(20, 10), anchor="w")
        
        self.alg_selector = ctk.CTkComboBox(left_panel, values=list(self.solvers.keys()), width=200, fg_color=BG_COLOR, button_color=CYAN_NEON)
        self.alg_selector.pack(padx=15, pady=5, fill="x")

        btn_solve = ctk.CTkButton(left_panel, text="GỌI AI GIẢI (RUN AI)", font=("Segoe UI", 12, "bold"), fg_color=CYAN_NEON, text_color="#000000", command=self.run_ai)
        btn_solve.pack(padx=15, pady=20, fill="x")

        # --- CỘT GIỮA ---
        center_panel = ctk.CTkFrame(self, fg_color="transparent")
        center_panel.grid(row=0, column=1, padx=10, pady=20, sticky="nsew")
        
        lbl_title = ctk.CTkLabel(center_panel, text="LEVEL 1: GRIDLOCK ALPHA", font=("Segoe UI", 18, "bold"), text_color=TEXT_COLOR)
        lbl_title.pack(pady=(0, 15))

        self.board_canvas = ctk.CTkCanvas(center_panel, width=360, height=360, bg="#21262D", highlightthickness=1, highlightbackground="#30363D")
        self.board_canvas.pack()

        lbl_hint = ctk.CTkLabel(center_panel, text="Kéo xe để di chuyển • Nhấn AI để giải tự động", font=("Segoe UI", 12), text_color="#8B949E")
        lbl_hint.pack(pady=5)

        btn_reset = ctk.CTkButton(center_panel, text="Reset Level", fg_color="#21262D", text_color=TEXT_COLOR, hover_color="#30363D", command=self.reset_game)
        btn_reset.pack(pady=10)

        # --- CỘT PHẢI ---
        right_panel = ctk.CTkFrame(self, fg_color=PANEL_COLOR, corner_radius=12, border_color="#30363D", border_width=1)
        right_panel.grid(row=0, column=2, padx=15, pady=20, sticky="nsew")
        
        lbl_log = ctk.CTkLabel(right_panel, text="MOVE LOG", font=("Segoe UI", 14, "bold"), text_color=CYAN_NEON)
        lbl_log.pack(padx=15, pady=(20, 10), anchor="w")
        
        self.log_box = ctk.CTkTextbox(right_panel, fg_color=BG_COLOR, text_color="#8B949E", font=("Consolas", 12), corner_radius=8)
        self.log_box.pack(padx=15, pady=10, fill="both", expand=True)
        self.log_box.insert("end", "Log cleared.\nSẵn sàng - Kéo xe hoặc gọi AI.\n")

    def draw_board(self):
        self.board_canvas.delete("all")
        
        # Vẽ lưới nền 6x6
        for r in range(6):
            for c in range(6):
                x1, y1 = c * CELL_SIZE, r * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                self.board_canvas.create_rectangle(x1, y1, x2, y2, outline="#30363D", width=1)
        
        # Vẽ EXIT
        self.board_canvas.create_rectangle(356, 2*CELL_SIZE, 360, 3*CELL_SIZE, fill="#FF7B72", outline="")

        # Vẽ các xe
        for name, v in self.current_board.vehicles.items():
            if name == 'X':
                color = "#FF7B72"
            else:
                color = "#7EE787" if ord(name) % 2 == 0 else "#D2A8FF"

            x1 = v.col * CELL_SIZE + 4
            y1 = v.row * CELL_SIZE + 4
            
            if v.orientation == 'H':
                x2 = (v.col + v.size) * CELL_SIZE - 4
                y2 = (v.row + 1) * CELL_SIZE - 4
            else:
                x2 = (v.col + 1) * CELL_SIZE - 4
                y2 = (v.row + v.size) * CELL_SIZE - 4
                
            # Tạo khối xe với tag độc nhất chính là tên xe
            self.board_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#30363D", width=1, tags=(name, "vehicle"))
            self.board_canvas.create_text((x1+x2)/2, (y1+y2)/2, text=name, fill="#000000", font=("Segoe UI", 12, "bold"), tags=(name, "text"))

    def bind_mouse_events(self):
        self.board_canvas.bind("<Button-1>", self.on_mouse_click)
        self.board_canvas.bind("<B1-Motion>", self.on_mouse_drag) # Thêm sự kiện bắt chuyển động chuột realtime
        self.board_canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

    def on_mouse_click(self, event):
        click_col = event.x // CELL_SIZE
        click_row = event.y // CELL_SIZE

        self.selected_vehicle_name = None
        for name, v in self.current_board.vehicles.items():
            for i in range(v.size):
                r = v.row + (i if v.orientation == 'V' else 0)
                c = v.col + (i if v.orientation == 'H' else 0)
                if r == click_row and c == click_col:
                    self.selected_vehicle_name = name
                    # Lưu vị trí chuột ban đầu để tính khoảng cách lệch (delta)
                    self.drag_data["x"] = event.x
                    self.drag_data["y"] = event.y
                    self.start_col = v.col
                    self.start_row = v.row
                    self.ghost_cell = (v.row, v.col)
                    return

    def on_mouse_drag(self, event):
        """Xử lý di chuyển khối xe mượt mà và hiển thị vị trí đích dự kiến."""
        if not self.selected_vehicle_name:
            return

        v = self.current_board.vehicles[self.selected_vehicle_name]
        
        # Tính khoảng cách chuột đã di chuyển so với điểm click ban đầu
        delta_x = event.x - self.drag_data["x"]
        delta_y = event.y - self.drag_data["y"]

        # 1. DI CHUYỂN KHỐI XE REALTIME TRÊN MÀN HÌNH
        if v.orientation == 'H':
            # Di chuyển các thành phần thuộc xe theo trục X
            self.board_canvas.move(self.selected_vehicle_name, delta_x, 0)
            self.drag_data["x"] = event.x # Cập nhật lại mốc chuột
            
            # Tính toán xem đầu xe đang ghé sát vào ô lưới nào nhất
            coords = self.board_canvas.coords(self.selected_vehicle_name)
            if coords:
                current_pixel_x = coords[0] - 4
                estimated_col = round(current_pixel_x / CELL_SIZE)
                # Giới hạn không cho kéo lố ra ngoài bàn cờ
                estimated_col = max(0, min(estimated_col, 6 - v.size))
                self.ghost_cell = (v.row, estimated_col)
        else:
            # Di chuyển các thành phần thuộc xe theo trục Y
            self.board_canvas.move(self.selected_vehicle_name, 0, delta_y)
            self.drag_data["y"] = event.y
            
            coords = self.board_canvas.coords(self.selected_vehicle_name)
            if coords:
                current_pixel_y = coords[1] - 4
                estimated_row = round(current_pixel_y / CELL_SIZE)
                estimated_row = max(0, min(estimated_row, 6 - v.size))
                self.ghost_cell = (estimated_row, v.col)

        # 2. VẼ KHUNG GỢI Ý Ô ĐÁP XUỐNG (GHOST BOX)
        self.board_canvas.delete("ghost")
        g_row, g_col = self.ghost_cell
        gx1 = g_col * CELL_SIZE + 2
        gy1 = g_row * CELL_SIZE + 2
        gx2 = (g_col + (v.size if v.orientation == 'H' else 1)) * CELL_SIZE - 2
        gy2 = (g_row + (1 if v.orientation == 'H' else v.size)) * CELL_SIZE - 2
        
        # Vẽ một khung viền nét đứt màu Cyan Neon để người dùng biết xe sẽ đáp vào đâu
        self.board_canvas.create_rectangle(gx1, gy1, gx2, gy2, outline=CYAN_NEON, width=2, dash=(4, 4), tags="ghost")

    def on_mouse_release(self, event):
        if not self.selected_vehicle_name:
            return

        self.board_canvas.delete("ghost")
        v = self.current_board.vehicles[self.selected_vehicle_name]
        g_row, g_col = self.ghost_cell

        # Tính số ô cần di chuyển thực tế từ vị trí xuất phát ban đầu tới ô gợi ý
        if v.orientation == 'H':
            steps = g_col - self.start_col
        else:
            steps = g_row - self.start_row

        if steps != 0:
            sign = 1 if steps > 0 else -1
            valid_total_steps = 0
            temp_board = self.current_board

            # Kiểm tra va chạm vật lý từng ô một
            for _ in range(abs(steps)):
                valid_moves = temp_board.get_valid_moves()
                if (self.selected_vehicle_name, sign) in valid_moves:
                    temp_board = temp_board.move_vehicle(self.selected_vehicle_name, sign)
                    valid_total_steps += sign
                else:
                    break 

            if valid_total_steps != 0:
                self.current_board = self.current_board.move_vehicle(self.selected_vehicle_name, valid_total_steps)
                direction_text = "Phải" if v.orientation == 'H' and valid_total_steps > 0 else "Trái" if v.orientation == 'H' else "Xuống" if valid_total_steps > 0 else "Lên"
                self.log_box.insert("end", f"[User]: Xe {self.selected_vehicle_name} di chuyển {direction_text} {abs(valid_total_steps)} ô.\n")
                self.log_box.see("end")

        # Vẽ lại toàn bộ bàn cờ để đưa các xe về đúng khấc lưới chuẩn xác (snap-to-grid)
        self.draw_board()
        
        if self.current_board.is_goal():
            self.log_box.insert("end", "🎉 XUẤT SẮC! Bạn đã giải thành công màn chơi này!\n")
            self.log_box.see("end")

        self.selected_vehicle_name = None

    def run_ai(self):
        selected_alg_name = self.alg_selector.get()
        solver = self.solvers[selected_alg_name]
        
        self.log_box.insert("end", f"\n> Đang tìm đường đi bằng {selected_alg_name}...\n")
        self.log_box.see("end")
        
        path = solver.solve(self.current_board)
        
        if path:
            self.log_box.insert("end", f"> Thành công! AI tìm ra chuỗi {len(path)} bước đi tối ưu nhất:\n")
            temp_board = self.current_board
            for idx, (name, steps) in enumerate(path, 1):
                v = temp_board.vehicles[name]
                direction = "Phải" if v.orientation == 'H' and steps > 0 else "Trái" if v.orientation == 'H' else "Xuống" if steps > 0 else "Lên"
                self.log_box.insert("end", f"   • Bước {idx}: Xe {name} -> {direction} {abs(steps)} ô\n")
                temp_board = temp_board.move_vehicle(name, steps)
            
            self.current_board = temp_board
            self.draw_board()
            self.log_box.insert("end", "🏁 AI đã đưa xe X thoát hiểm an toàn!\n")
            self.log_box.see("end")
        else:
            self.log_box.insert("end", "> Thất bại: Trạng thái hiện tại kẹt cứng, không có đường ra.\n")
            self.log_box.see("end")

    def reset_game(self):
        self.current_board = self.load_level_1()
        self.draw_board()
        self.log_box.delete("1.0", "end")
        self.log_box.insert("end", "Log cleared.\nLevel 1 đã được đặt lại ban đầu.\n")
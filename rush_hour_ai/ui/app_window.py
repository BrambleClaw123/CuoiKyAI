import customtkinter as ctk
import tkinter as tk
from core.board import Board
# Import toàn bộ hằng số hệ màu và map từ file cấu hình vừa tạo ở Bước 1
from core.level_config import (
    BG_COLOR, PANEL_COLOR, PANEL2_COLOR, BORDER_COLOR,
    ACCENT_CYAN, ACCENT_ORANGE, GREEN_NEON, RED_NEON,
    TEXT_MAIN, TEXT_MUTED, CELL_SIZE, CAR_COLORS, LEVEL_DATA
)

class RushHourAIApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Rush Hour AI")
        self.geometry("1150x680")
        self.configure(fg_color=BG_COLOR)

        # Trạng thái Game ban đầu
        self.current_level_id = 1
        self.initial_board = self.load_level(1)
        self.current_board = self.load_level(1)
        self.move_count = 0
        
        # Quản lý thuật toán
        self.current_algo_key = "BFS"
        self.algo_buttons = {}  

        # Chuột kéo thả
        self.selected_vehicle_name = None
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.orig_v_col = 0
        self.orig_v_row = 0
        self.ghost_cell = None

        self.setup_ui()
        self.switch_level(1) 

    def load_level(self, level_id):
        self.current_level_id = level_id
        data = LEVEL_DATA[level_id]
        cloned_vehicles = [v.clone() for v in data["vehicles"]]
        return Board(cloned_vehicles, data["bricks"])

    def setup_ui(self):
        # ═══════════════════════════════════════════════════
        # HEADER BAR
        # ═══════════════════════════════════════════════════
        header = ctk.CTkFrame(self, height=60, fg_color=PANEL_COLOR, corner_radius=0, border_color=BORDER_COLOR, border_width=1)
        header.pack(fill="x", side="top")

        logo_label = ctk.CTkLabel(header, text="RUSHHOUR.AI", font=("Space Mono", 20, "bold"), text_color=ACCENT_CYAN)
        logo_label.pack(side="left", padx=28, pady=14)

        self.pill_algo = ctk.CTkLabel(header, text="ALGO: BFS", font=("Space Mono", 11), fg_color=BG_COLOR, text_color=ACCENT_CYAN, corner_radius=20, width=110, height=25)
        self.pill_algo.pack(side="right", padx=(0, 28), pady=14)

        self.pill_moves = ctk.CTkLabel(header, text="MOVES: 0", font=("Space Mono", 11), fg_color=BG_COLOR, text_color=TEXT_MAIN, corner_radius=20, width=90, height=25)
        self.pill_moves.pack(side="right", padx=15, pady=14)

        self.pill_level = ctk.CTkLabel(header, text="LEVEL: 1", font=("Space Mono", 11), fg_color=BG_COLOR, text_color=TEXT_MUTED, corner_radius=20, width=90, height=25)
        self.pill_level.pack(side="right", padx=0, pady=14)

        main_layout = ctk.CTkFrame(self, fg_color="transparent")
        main_layout.pack(fill="both", expand=True, side="top")

        # ═══════════════════════════════════════════════════
        # LEFT SIDEBAR
        # ═══════════════════════════════════════════════════
        sidebar_left = ctk.CTkFrame(main_layout, width=220, fg_color=PANEL_COLOR, corner_radius=0, border_color=BORDER_COLOR, border_width=1)
        sidebar_left.pack(side="left", fill="y")
        sidebar_left.pack_propagate(False)

        lbl_sec_lvl = ctk.CTkLabel(sidebar_left, text="--- LEVELS ---", font=("Space Mono", 10, "bold"), text_color=BORDER_COLOR, anchor="w")
        lbl_sec_lvl.pack(fill="x", padx=16, pady=(20, 5))

        self.btn_lvl1 = ctk.CTkButton(sidebar_left, text="Gridlock Alpha   [1]", font=("Rajdhani", 14, "bold"), fg_color="#0B1A22", text_color=ACCENT_CYAN, border_color=ACCENT_CYAN, border_width=1, hover_color="#0B2531", anchor="w", command=lambda: self.switch_level(1))
        self.btn_lvl1.pack(fill="x", padx=16, pady=4)

        self.btn_lvl2 = ctk.CTkButton(sidebar_left, text="Beta Block       [2]", font=("Rajdhani", 14, "bold"), fg_color="transparent", text_color=TEXT_MAIN, border_color=BORDER_COLOR, border_width=1, hover_color="#1F2937", anchor="w", command=lambda: self.switch_level(2))
        self.btn_lvl2.pack(fill="x", padx=16, pady=4)

        for dummy_lvl in ["Gamma Trap   [3]", "Delta Hard   [4]"]:
            btn_lock = ctk.CTkButton(sidebar_left, text=dummy_lvl, font=("Rajdhani", 14, "bold"), fg_color="transparent", text_color="#475569", state="disabled", anchor="w")
            btn_lock.pack(fill="x", padx=16, pady=4)

        lbl_sec_alg = ctk.CTkLabel(sidebar_left, text="--- ALGORITHM ---", font=("Space Mono", 10, "bold"), text_color=BORDER_COLOR, anchor="w")
        lbl_sec_alg.pack(fill="x", padx=16, pady=(25, 5))

        self.algo_container = ctk.CTkFrame(sidebar_left, fg_color="transparent")
        self.algo_container.pack(fill="x", padx=16, pady=5)

        desc_frame = ctk.CTkFrame(sidebar_left, fg_color="transparent")
        desc_frame.pack(fill="x", padx=16, side="bottom", pady=30)
        self.lbl_desc_t = ctk.CTkLabel(desc_frame, text="Agent Solver", font=("Rajdhani", 13, "bold"), text_color=ACCENT_CYAN, anchor="w")
        self.lbl_desc_t.pack(fill="x")
        self.lbl_desc_b = ctk.CTkLabel(desc_frame, text="", font=("Rajdhani", 12), text_color=TEXT_MUTED, anchor="w", justify="left", wraplength=185)
        self.lbl_desc_b.pack(fill="x", pady=2)

        # ═══════════════════════════════════════════════════
        # RIGHT PANEL
        # ═══════════════════════════════════════════════════
        sidebar_right = ctk.CTkFrame(main_layout, width=260, fg_color=PANEL_COLOR, corner_radius=0, border_color=BORDER_COLOR, border_width=1)
        sidebar_right.pack(side="right", fill="y")
        sidebar_right.pack_propagate(False)

        ai_card = ctk.CTkFrame(sidebar_right, fg_color=PANEL2_COLOR, border_color=BORDER_COLOR, border_width=1, corner_radius=10)
        ai_card.pack(fill="x", padx=16, pady=20)

        lbl_card_t = ctk.CTkLabel(ai_card, text="AI AGENT", font=("Space Mono", 11), text_color=TEXT_MUTED)
        lbl_card_t.pack(anchor="w", padx=14, pady=(10, 5))

        self.btn_ai = ctk.CTkButton(ai_card, text="▶ Gọi AI Giải", font=("Rajdhani", 15, "bold"), fg_color="#0B212B", text_color=ACCENT_CYAN, border_color="#0B3C4F", border_width=1, hover_color="#0C3848", command=self.run_ai)
        self.btn_ai.pack(fill="x", padx=14, pady=6)

        btn_reset = ctk.CTkButton(ai_card, text="↺ Reset Level", font=("Rajdhani", 14), fg_color="transparent", text_color=TEXT_MUTED, border_color=BORDER_COLOR, border_width=1, hover_color="#1F2937", command=self.reset_game)
        btn_reset.pack(fill="x", padx=14, pady=(4, 14))

        log_card = ctk.CTkFrame(sidebar_right, fg_color=PANEL2_COLOR, border_color=BORDER_COLOR, border_width=1, corner_radius=10)
        log_card.pack(fill="both", expand=True, padx=16, pady=(0, 20))

        lbl_log_t = ctk.CTkLabel(log_card, text="MOVE LOG", font=("Space Mono", 11), text_color=TEXT_MUTED)
        lbl_log_t.pack(anchor="w", padx=14, pady=(10, 5))

        self.log_box = tk.Text(log_card, bg=BG_COLOR, fg=TEXT_MUTED, insertbackground=TEXT_MAIN, bd=0, highlightthickness=0, font=("Space Mono", 9), wrap="word")
        self.log_box.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        
        self.log_box.tag_config("info", foreground="#A78BFA")
        self.log_box.tag_config("current", foreground=ACCENT_CYAN)
        self.log_box.tag_config("success", foreground=GREEN_NEON)

        # ═══════════════════════════════════════════════════
        # CENTER GAME AREA
        # ═══════════════════════════════════════════════════
        center_area = ctk.CTkFrame(main_layout, fg_color="transparent")
        center_area.pack(side="left", fill="both", expand=True)

        board_outer = ctk.CTkFrame(center_area, fg_color=PANEL2_COLOR, border_color=BORDER_COLOR, border_width=2, corner_radius=12)
        board_outer.place(relx=0.5, rely=0.45, anchor="center")

        self.canvas = tk.Canvas(board_outer, width=CELL_SIZE*6, height=CELL_SIZE*6, bg="#0D1117", bd=0, highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)

        self.lbl_hint = ctk.CTkLabel(center_area, text="Kéo xe để di chuyển • Nhấn AI để giải tự động", font=("Rajdhani", 13, "normal"), text_color=TEXT_MUTED)
        self.lbl_hint.place(relx=0.5, rely=0.85, anchor="center")

        # ═══════════════════════════════════════════════════
        # STATUS BAR
        # ═══════════════════════════════════════════════════
        status_bar = ctk.CTkFrame(self, height=30, fg_color=PANEL_COLOR, corner_radius=0, border_color=BORDER_COLOR, border_width=1)
        status_bar.pack(fill="x", side="bottom")

        self.status_dot = ctk.CTkLabel(status_bar, text="●", font=("Space Mono", 14), text_color=GREEN_NEON)
        self.status_dot.pack(side="left", padx=(28, 5))

        self.status_text = ctk.CTkLabel(status_bar, text="Sẵn sàng — Kéo xe hoặc gọi AI", font=("Space Mono", 11), text_color="#475569")
        self.status_text.pack(side="left", padx=0)

    def update_algo_menu(self):
        for btn in self.algo_buttons.values():
            btn.destroy()
        self.algo_buttons.clear()

        algos = LEVEL_DATA[self.current_level_id]["algorithms"]
        self.current_algo_key = list(algos.keys())[0]

        for key, info in algos.items():
            btn = ctk.CTkButton(
                self.algo_container, 
                text=f"• {info['label']}" if key == self.current_algo_key else f"  {info['label']}", 
                font=("Rajdhani", 13, "bold"),
                fg_color="transparent", 
                text_color=ACCENT_CYAN if key == self.current_algo_key else TEXT_MUTED, 
                anchor="w", hover=False,
                command=lambda k=key: self.select_algorithm(k)
            )
            btn.pack(fill="x", pady=2)
            self.algo_buttons[key] = btn
        self.refresh_algo_display_texts()

    def select_algorithm(self, algo_key):
        self.current_algo_key = algo_key
        algos = LEVEL_DATA[self.current_level_id]["algorithms"]
        for key, btn in self.algo_buttons.items():
            if key == algo_key:
                btn.configure(text=f"• {algos[key]['label']}", text_color=ACCENT_CYAN)
            else:
                btn.configure(text=f"  {algos[key]['label']}", text_color=TEXT_MUTED)
        self.refresh_algo_display_texts()

    def refresh_algo_display_texts(self):
        algos = LEVEL_DATA[self.current_level_id]["algorithms"]
        current_info = algos[self.current_algo_key]
        self.pill_algo.configure(text=f"ALGO: {self.current_algo_key}")
        self.lbl_desc_t.configure(text=f"{self.current_algo_key} Agent")
        self.lbl_desc_b.configure(text=current_info["desc"])

    def switch_level(self, level_id):
        self.initial_board = self.load_level(level_id)
        self.current_board = self.load_level(level_id)
        self.move_count = 0
        self.pill_level.configure(text=f"LEVEL: {level_id}")
        self.pill_moves.configure(text="MOVES: 0")
        
        if level_id == 1:
            self.btn_lvl1.configure(fg_color="#0B1A22", text_color=ACCENT_CYAN, border_color=ACCENT_CYAN)
            self.btn_lvl2.configure(fg_color="transparent", text_color=TEXT_MAIN, border_color=BORDER_COLOR)
        elif level_id == 2:
            self.btn_lvl1.configure(fg_color="transparent", text_color=TEXT_MAIN, border_color=BORDER_COLOR)
            self.btn_lvl2.configure(fg_color="#0B1A22", text_color=ACCENT_CYAN, border_color=ACCENT_CYAN)

        self.update_algo_menu()
        self.draw_board()
        self.log_box.delete("1.0", "end")
        self.add_log("Log cleared.", "")
        self.add_log(f"Level {level_id}: {LEVEL_DATA[level_id]['name']} đã sẵn sàng.", "info")
        self.set_status("ready")

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(1, 6):
            pos = i * CELL_SIZE
            self.canvas.create_line(pos, 0, pos, CELL_SIZE*6, fill="#21262D", width=1)
            self.canvas.create_line(0, pos, CELL_SIZE*6, pos, fill="#21262D", width=1)

        exit_y1 = 2 * CELL_SIZE + 2
        exit_y2 = 3 * CELL_SIZE - 2
        self.canvas.create_rectangle(CELL_SIZE*6 - 6, exit_y1, CELL_SIZE*6, exit_y2, fill=RED_NEON, outline="")

        pad_brick = 5
        for (r, c) in self.current_board.bricks:
            bx1 = c * CELL_SIZE + pad_brick
            by1 = r * CELL_SIZE + pad_brick
            bx2 = (c + 1) * CELL_SIZE - pad_brick
            by2 = (r + 1) * CELL_SIZE - pad_brick
            self.canvas.create_rectangle(bx1, by1, bx2, by2, fill="#1F2226", outline="#2A2F3D", width=2)
            offset = 12
            screws = [
                (bx1 + offset, by1 + offset), (bx2 - offset, by1 + offset),
                (bx1 + offset, by2 - offset), (bx2 - offset, by2 - offset)
            ]
            for (sx, sy) in screws:
                self.canvas.create_oval(sx - 3, sy - 3, sx + 3, sy + 3, fill="#8A94A2", outline="")

        pad = 5
        for name, v in self.current_board.vehicles.items():
            color_cfg = CAR_COLORS.get(name, {"bg": "#1F2937", "border": "#4B5563", "text": "#FFFFFF"})
            x1 = v.col * CELL_SIZE + pad
            y1 = v.row * CELL_SIZE + pad
            if v.orientation == 'H':
                x2 = (v.col + v.size) * CELL_SIZE - pad
                y2 = (v.row + 1) * CELL_SIZE - pad
            else:
                x2 = (v.col + 1) * CELL_SIZE - pad
                y2 = (v.row + v.size) * CELL_SIZE - pad

            rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color_cfg["bg"], outline=color_cfg["border"], width=2, tags=(name, "vehicle"))
            text_id = self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=name, fill=color_cfg["text"], font=("Space Mono", 16, "bold"), tags=(name, "text"))

            for item_id in (rect_id, text_id):
                self.canvas.tag_bind(item_id, "<Button-1>", lambda e, n=name: self.on_vehicle_click(e, n))
                self.canvas.tag_bind(item_id, "<B1-Motion>", self.on_vehicle_drag)
                self.canvas.tag_bind(item_id, "<ButtonRelease-1>", self.on_vehicle_release)

    def on_vehicle_click(self, event, name):
        self.selected_vehicle_name = name
        v = self.current_board.vehicles[name]
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.orig_v_col = v.col
        self.orig_v_row = v.row
        self.ghost_cell = (v.row, v.col)
        self.show_move_hints(v)

    def on_vehicle_drag(self, event):
        if not self.selected_vehicle_name: return
        v = self.current_board.vehicles[self.selected_vehicle_name]
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y

        if v.orientation == 'H':
            self.canvas.move(self.selected_vehicle_name, dx, 0)
            self.drag_start_x = event.x
            coords = self.canvas.coords(self.selected_vehicle_name)
            if coords:
                current_pixel_x = coords[0] - 5
                estimated_col = round(current_pixel_x / CELL_SIZE)
                estimated_col = max(0, min(estimated_col, 6 - v.size))
                self.ghost_cell = (v.row, estimated_col)
        else:
            self.canvas.move(self.selected_vehicle_name, 0, dy)
            self.drag_start_y = event.y
            coords = self.canvas.coords(self.selected_vehicle_name)
            if coords:
                current_pixel_y = coords[1] - 5
                estimated_row = round(current_pixel_y / CELL_SIZE)
                estimated_row = max(0, min(estimated_row, 6 - v.size))
                self.ghost_cell = (estimated_row, v.col)
        self.update_ghost_box(v)

    def update_ghost_box(self, v):
        self.canvas.delete("ghost")
        g_row, g_col = self.ghost_cell
        gx1 = g_col * CELL_SIZE + 2
        gy1 = g_row * CELL_SIZE + 2
        gx2 = (g_col + (v.size if v.orientation == 'H' else 1)) * CELL_SIZE - 2
        gy2 = (g_row + (1 if v.orientation == 'H' else v.size)) * CELL_SIZE - 2
        self.canvas.create_rectangle(gx1, gy1, gx2, gy2, outline=ACCENT_CYAN, width=1.5, dash=(4, 4), tags="ghost")

    def on_vehicle_release(self, event):
        if not self.selected_vehicle_name: return
        self.canvas.delete("ghost")
        self.canvas.delete("hint")
        v = self.current_board.vehicles[self.selected_vehicle_name]
        g_row, g_col = self.ghost_cell
        steps = (g_col - self.orig_v_col) if v.orientation == 'H' else (g_row - self.orig_v_row)

        if steps != 0:
            sign = 1 if steps > 0 else -1
            valid_total_steps = 0
            temp_board = self.current_board
            for _ in range(abs(steps)):
                if (self.selected_vehicle_name, sign) in temp_board.get_valid_moves():
                    temp_board = temp_board.move_vehicle(self.selected_vehicle_name, sign)
                    valid_total_steps += sign
                else: break
            if valid_total_steps != 0:
                self.current_board = self.current_board.move_vehicle(self.selected_vehicle_name, valid_total_steps)
                self.move_count += 1
                self.pill_moves.configure(text=f"MOVES: {self.move_count}")
                dir_symbol = "→ phải" if v.orientation == 'H' and valid_total_steps > 0 else "← trái" if v.orientation == 'H' else "↓ xuống" if valid_total_steps > 0 else "↑ lên"
                self.add_log(f"Xe {self.selected_vehicle_name} {dir_symbol}", "current")

        self.draw_board()
        self.check_win()
        self.selected_vehicle_name = None

    def show_move_hints(self, v):
        self.canvas.delete("hint")
        board_cells = self.current_board.get_occupied_cells()
        if v.orientation == 'H':
            for c in range(v.col - 1, -1, -1):
                if (v.row, c) in board_cells: break
                self.draw_hint_tile(c, v.row)
            for c in range(v.col + v.size, 6):
                if (v.row, c) in board_cells: break
                self.draw_hint_tile(c, v.row)
        else:
            for r in range(v.row - 1, -1, -1):
                if (r, v.col) in board_cells: break
                self.draw_hint_tile(v.col, r)
            for r in range(v.row + v.size, 6):
                if (r, v.col) in board_cells: break
                self.draw_hint_tile(v.col, r)

    def draw_hint_tile(self, col, row):
        x1, y1 = col * CELL_SIZE + 3, row * CELL_SIZE + 3
        x2, y2 = x1 + CELL_SIZE - 6, y1 + CELL_SIZE - 6
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="", outline="#1A3A4A", width=1, dash=(2, 2), tags="hint")

    def add_log(self, text, tag=""):
        self.log_box.insert("end", text + "\n", tag)
        self.log_box.see("end")

    def set_status(self, mode, text=""):
        if mode == "thinking":
            self.status_dot.configure(text_color=ACCENT_ORANGE)
            self.status_text.configure(text="AI đang tính toán...")
        else:
            self.status_dot.configure(text_color=GREEN_NEON)
            self.status_text.configure(text=text if text else "Sẵn sàng — Kéo xe hoặc gọi AI")

    def run_ai(self):
        self.btn_ai.configure(state="disabled")
        self.set_status("thinking")
        self.add_log(f"[{self.current_algo_key}] Đang tính toán...", "info")

        algos = LEVEL_DATA[self.current_level_id]["algorithms"]
        solver = algos[self.current_algo_key]["solver"]
        
        result = solver.solve(self.current_board)

        if not result:
            self.add_log("Không tìm thấy lời giải!", "error")
            self.set_status("ready", "Kẹt cứng — Cần reset màn chơi")
            self.btn_ai.configure(state="normal")
            return

        self.add_log(f"[{self.current_algo_key}] Đã duyệt {result['visited']} trạng thái", "info")
        self.add_log(f"Tìm thấy lời giải {len(result['path'])} bước!", "success")
        self.animate_path(result["path"], 0)

    def animate_path(self, path, index):
        if index >= len(path):
            self.btn_ai.configure(state="normal")
            self.set_status("ready")
            return

        name, steps = path[index]
        v = self.current_board.vehicles[name]
        
        dir_text = ("→ phải" if steps > 0 else "← trái") if v.orientation == 'H' else ("↓ xuống" if steps > 0 else "↑ lên")

        self.current_board = self.current_board.move_vehicle(name, steps)
        self.move_count += 1
        self.pill_moves.configure(text=f"MOVES: {self.move_count}")
        
        is_last = (index == len(path) - 1)
        self.add_log(f"Bước {index + 1}: Xe {name} {dir_text} {abs(steps)} ô", "success" if is_last else "current")
        
        self.draw_board()
        self.check_win()
        self.after(480, lambda: self.animate_path(path, index + 1))

    def check_win(self):
        if self.current_board.is_goal():
            self.set_status("ready", "🎯 XE THOÁT RA! LEVEL HOÀN THÀNH!")
            self.add_log("🎯 XE THOÁT RA! LEVEL HOÀN THÀNH!", "success")
            self.show_win_popup()

    def show_win_popup(self):
        popup = tk.Toplevel(self)
        popup.title("SOLVED!")
        popup.geometry("380x220") 
        popup.configure(bg=PANEL_COLOR)
        popup.transient(self)
        popup.grab_set()
        
        x = self.winfo_x() + (self.winfo_width() // 2) - 190
        y = self.winfo_y() + (self.winfo_height() // 2) - 110
        popup.geometry(f"+{x}+{y}")

        lbl_win = ctk.CTkLabel(popup, text="SOLVED!", font=("Space Mono", 32, "bold"), text_color=GREEN_NEON)
        lbl_win.pack(pady=(30, 5))

        lbl_sub = ctk.CTkLabel(popup, text=f"Xe thoát ra ngoài trong {self.move_count} bước đi!", font=("Rajdhani", 15), text_color=TEXT_MAIN)
        lbl_sub.pack(pady=5)

        btn_close = ctk.CTkButton(popup, text="Tiếp tục", font=("Rajdhani", 14, "bold"), fg_color=GREEN_NEON, text_color="#0A0C10", hover_color="#16A34A", command=popup.destroy)
        btn_close.pack(pady=20)

    def reset_game(self):
        self.current_board = self.load_level(self.current_level_id)
        self.move_count = 0
        self.pill_moves.configure(text="MOVES: 0")
        self.update_algo_menu()
        self.draw_board()
        self.log_box.delete("1.0", "end")
        self.add_log("Log cleared.", "")
        self.add_log(f"Level {self.current_level_id} đã được đặt lại trạng thái ban đầu.", "info")
        self.set_status("ready")
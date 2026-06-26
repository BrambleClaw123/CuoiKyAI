import customtkinter as ctk
import tkinter as tk
from core.board import Board
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

        self.current_level_id = 1
        self.initial_board = self.load_level(1)
        self.current_board = self.load_level(1)
        self.move_count = 0
        
        # Mảng lưu kịch bản của Partial Start
        self.initial_beliefs = []
        self.current_beliefs = []
        
        self.current_algo_key = "BFS"
        self.algo_buttons = {}  
        self.level_buttons = {} 

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

        # Board chính
        cloned_vehicles = [v.clone() for v in data["vehicles"]]

        # Partial observe
        self.partial_board = None
        if "partial_view" in data:
            self.partial_board = Board(
                [v.clone() for v in data["partial_view"]],
                data.get("bricks", [])
            )

        # Belief states
        self.initial_beliefs = []
        self.current_beliefs = []

        if "belief_starts" in data:
            for belief in data["belief_starts"]:
                self.initial_beliefs.append(
                    Board(
                        [v.clone() for v in belief],
                        data.get("bricks", [])
                    )
                )

        return Board(cloned_vehicles, data.get("bricks", []))

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

        level_names = {
            1: "Gridlock Alpha", 2: "Beta Block", 3: "Gamma Trap",
            4: "Delta Hard", 5: "Epsilon CSP", 6: "Zeta Adver"
        }
        
        for i in range(1, 7):
            if i not in LEVEL_DATA: continue
            btn = ctk.CTkButton(
                sidebar_left, 
                text=f"{level_names[i]:<16} [{i}]", 
                font=("Rajdhani", 14, "bold"), 
                fg_color="transparent", 
                text_color=TEXT_MAIN, 
                border_color=BORDER_COLOR, 
                border_width=1, 
                hover_color="#1F2937", 
                anchor="w", 
                command=lambda lvl=i: self.switch_level(lvl)
            )
            btn.pack(fill="x", padx=16, pady=4)
            self.level_buttons[i] = btn

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
        self.log_box.tag_config("error", foreground=RED_NEON)

        # ═══════════════════════════════════════════════════
        # CENTER GAME AREA
        # ═══════════════════════════════════════════════════
        self.center_area = ctk.CTkFrame(main_layout, fg_color="transparent")
        self.center_area.pack(side="left", fill="both", expand=True)

        # KHUNG 1: BÀN CỜ CHÍNH (CHO CÁC THUẬT TOÁN BÌNH THƯỜNG)
        self.board_outer = ctk.CTkFrame(self.center_area, fg_color=PANEL2_COLOR, border_color=BORDER_COLOR, border_width=2, corner_radius=12)
        self.board_outer.place(relx=0.5, rely=0.42, anchor="center")
        self.canvas = tk.Canvas(self.board_outer, width=CELL_SIZE*6, height=CELL_SIZE*6, bg="#0D1117", bd=0, highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)

        # Panel 1: Hint Text
        self.lbl_hint = ctk.CTkLabel(self.center_area, text="Kéo xe để di chuyển • Nhấn AI để giải tự động", font=("Rajdhani", 13, "normal"), text_color=TEXT_MUTED)
        
        # Panel 2: Belief Goals (Level 4 - BGS)
        self.belief_panel = ctk.CTkFrame(self.center_area, fg_color="#451A03", corner_radius=8, border_color="#F59E0B", border_width=1)
        ctk.CTkLabel(self.belief_panel, text="🎯 TẬP ĐÍCH MÙ (BELIEF GOALS)", font=("Rajdhani", 14, "bold"), text_color="#FCD34D").pack(pady=(5, 0), padx=10)
        ctk.CTkLabel(self.belief_panel, text="Trạng thái 1: Xe Đỏ (X) ở cột 4 (thoát bên phải)\nTrạng thái 2: Xe Đỏ (X) ở cột 0 (thoát bên trái)", font=("Space Mono", 11), text_color=TEXT_MAIN).pack(pady=(0, 5), padx=15)

        # Panel 3: CSP (Level 5)
        self.inventory_panel = ctk.CTkFrame(self.center_area, fg_color=PANEL2_COLOR, corner_radius=8, border_color=BORDER_COLOR, border_width=1)

        # Panel 4: Adversarial (Level 6)
        self.adversarial_panel = ctk.CTkFrame(self.center_area, fg_color=PANEL2_COLOR, corner_radius=8, border_color=BORDER_COLOR, border_width=1)
        top_adv = ctk.CTkFrame(self.adversarial_panel, fg_color="transparent")
        top_adv.pack(fill="x", pady=(8, 2))
        self.lbl_max = ctk.CTkLabel(top_adv, text=" 🛡️ MAX (Đỏ/Xanh) ", font=("Rajdhani", 14, "bold"), corner_radius=6)
        self.lbl_max.pack(side="left", padx=(10, 5))
        self.lbl_vs = ctk.CTkLabel(top_adv, text="VS", font=("Space Mono", 14, "bold", "italic"), text_color=TEXT_MUTED)
        self.lbl_vs.pack(side="left", padx=5)
        self.lbl_min = ctk.CTkLabel(top_adv, text=" ⚔️ MIN (Cảnh sát) ", font=("Rajdhani", 14, "bold"), corner_radius=6)
        self.lbl_min.pack(side="left", padx=(5, 10))
        self.lbl_turn_counter = ctk.CTkLabel(self.adversarial_panel, text="Lượt: 0/20", font=("Space Mono", 12, "bold"), text_color=ACCENT_ORANGE)
        self.lbl_turn_counter.pack(side="bottom", pady=(0, 8))

        # KHUNG 5: PARTIAL START SEARCH (LEVEL 4 - PSS)
        self.pss_panel = ctk.CTkFrame(self.center_area, fg_color="transparent")
        
        # Góc nhìn Partial nhỏ gọn ở trên
        self.pss_top = ctk.CTkFrame(self.pss_panel, fg_color="transparent")
        self.pss_top.pack(pady=(0, 10))
        
        self.obs_frame = ctk.CTkFrame(self.pss_top, fg_color=PANEL2_COLOR, border_color=BORDER_COLOR, border_width=1, corner_radius=8)
        self.obs_frame.pack()
        ctk.CTkLabel(self.obs_frame, text="PARTIAL", font=("Rajdhani", 11, "bold"), text_color="#A78BFA").pack(pady=(2,0))
        # Kích thước siêu nhỏ (cell_size = 20)
        self.canvas_obs = tk.Canvas(self.obs_frame, width=20*6, height=20*6, bg="#0D1117", bd=0, highlightthickness=0)
        self.canvas_obs.pack(padx=8, pady=(2, 8))
        
        # 2 Belief States bự ở dưới
        self.pss_bottom = ctk.CTkFrame(self.pss_panel, fg_color="transparent")
        self.pss_bottom.pack()
        
        self.pss_b1_frame = ctk.CTkFrame(self.pss_bottom, fg_color=PANEL2_COLOR, border_color=BORDER_COLOR, border_width=2, corner_radius=10)
        self.pss_b1_frame.pack(side="left", padx=10)
        self.lbl_pss_b1 = ctk.CTkLabel(self.pss_b1_frame, text="BELIEF START 1", font=("Rajdhani", 13, "bold"), text_color=TEXT_MUTED)
        self.lbl_pss_b1.pack(pady=(5,0))
        # Kích thước to hơn (cell_size = 38)
        self.canvas_b1 = tk.Canvas(self.pss_b1_frame, width=38*6, height=38*6, bg="#0D1117", bd=0, highlightthickness=0)
        self.canvas_b1.pack(padx=10, pady=(5, 10))

        self.pss_b2_frame = ctk.CTkFrame(self.pss_bottom, fg_color=PANEL2_COLOR, border_color=BORDER_COLOR, border_width=2, corner_radius=10)
        self.pss_b2_frame.pack(side="left", padx=10)
        self.lbl_pss_b2 = ctk.CTkLabel(self.pss_b2_frame, text="BELIEF START 2", font=("Rajdhani", 13, "bold"), text_color=TEXT_MUTED)
        self.lbl_pss_b2.pack(pady=(5,0))
        self.canvas_b2 = tk.Canvas(self.pss_b2_frame, width=38*6, height=38*6, bg="#0D1117", bd=0, highlightthickness=0)
        self.canvas_b2.pack(padx=10, pady=(5, 10))

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
        for btn in self.algo_buttons.values(): btn.destroy()
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
            if key == algo_key: btn.configure(text=f"• {algos[key]['label']}", text_color=ACCENT_CYAN)
            else: btn.configure(text=f"  {algos[key]['label']}", text_color=TEXT_MUTED)
        self.refresh_algo_display_texts()

    def refresh_algo_display_texts(self):
        algos = LEVEL_DATA[self.current_level_id]["algorithms"]
        current_info = algos[self.current_algo_key]
        self.pill_algo.configure(text=f"ALGO: {self.current_algo_key}")
        self.lbl_desc_t.configure(text=f"{self.current_algo_key} Agent")
        self.lbl_desc_b.configure(text=current_info["desc"])

        # Ẩn tất cả Panels đi trước
        self.belief_panel.place_forget()
        self.inventory_panel.place_forget()
        self.adversarial_panel.place_forget()
        self.pss_panel.place_forget()
        self.board_outer.place_forget()
        self.lbl_hint.place_forget()

        # Hiện Panels theo Level & Thuật toán
        if self.current_level_id == 6:

            if self.current_algo_key == "EX":
                self.lbl_max.configure(
                    text=" 🛡️ MAX "
                )

                self.lbl_min.configure(
                    text=" 🎲 CHANCE "
                )

            else:
                self.lbl_max.configure(
                    text=" 🛡️ MAX "
                )

                self.lbl_min.configure(
                    text=" ⚔️ MIN "
                )
        if self.current_level_id == 4 and self.current_algo_key == "PSS":
            self.pss_panel.place(relx=0.5, rely=0.48, anchor="center")
        else:
            self.board_outer.place(relx=0.5, rely=0.42, anchor="center")
            
            if self.current_level_id == 4 and self.current_algo_key == "BGS":
                self.belief_panel.place(relx=0.5, rely=0.88, anchor="center")
            elif self.current_level_id == 5:
                self.inventory_panel.place(relx=0.5, rely=0.89, anchor="center")
            elif self.current_level_id == 6:
                self.adversarial_panel.place(relx=0.5, rely=0.88, anchor="center")
                self.lbl_max.configure(text_color=GREEN_NEON, fg_color="transparent")
                self.lbl_min.configure(text_color=RED_NEON, fg_color="transparent")
                self.lbl_turn_counter.configure(text="Lượt: 0/20")
            else:
                self.lbl_hint.place(relx=0.5, rely=0.86, anchor="center")
                self.lbl_hint.configure(text="Kéo xe để di chuyển • Nhấn AI để giải tự động")
            
        self.draw_board() 

    def switch_level(self, level_id):
        self.initial_board = self.load_level(level_id)
        self.current_board = self.load_level(level_id)
        
        self.current_beliefs = []
        if self.initial_beliefs:
            self.current_beliefs = [Board([v.clone() for v in b.vehicles.values()], b.bricks) for b in self.initial_beliefs]
            
        self.move_count = 0
        self.pill_level.configure(text=f"LEVEL: {level_id}")
        self.pill_moves.configure(text="MOVES: 0")
        
        for lvl, btn in self.level_buttons.items():
            if lvl == level_id: btn.configure(fg_color="#0B1A22", text_color=ACCENT_CYAN, border_color=ACCENT_CYAN)
            else: btn.configure(fg_color="transparent", text_color=TEXT_MAIN, border_color=BORDER_COLOR)

        self.update_algo_menu()
        self.draw_board()
        self.log_box.delete("1.0", "end")
        self.add_log("Log cleared.", "")
        self.add_log(f"Level {level_id}: {LEVEL_DATA[level_id]['name']} đã sẵn sàng.", "info")
        self.set_status("ready")

    # --- HÀM VẼ MA TRẬN TÙY CHỈNH KÍCH THƯỚC (CHO PSS) ---
    def draw_single_board(self, canvas, board, cell_size, is_observation=False):
        canvas.delete("all")
        for i in range(1, 6):
            pos = i * cell_size
            canvas.create_line(pos, 0, pos, cell_size*6, fill="#21262D", width=1)
            canvas.create_line(0, pos, cell_size*6, pos, fill="#21262D", width=1)

        exit_y1 = 2 * cell_size + 2; exit_y2 = 3 * cell_size - 2
        canvas.create_rectangle(cell_size*6 - 6, exit_y1, cell_size*6, exit_y2, fill=RED_NEON, outline="")

        pad_brick = max(2, cell_size // 10)
        for (r, c) in board.bricks:
            bx1 = c * cell_size + pad_brick; by1 = r * cell_size + pad_brick
            bx2 = (c + 1) * cell_size - pad_brick; by2 = (r + 1) * cell_size - pad_brick
            canvas.create_rectangle(bx1, by1, bx2, by2, fill="#1F2226", outline="#2A2F3D", width=2)

        pad = max(2, cell_size // 10)
        for name, v in board.vehicles.items():
            if v.row < 0 or v.col < 0: continue
            
            is_unknown = is_observation and name == 'U'
            color_cfg = CAR_COLORS.get(name, {"bg": "#1F2937", "border": "#4B5563", "text": "#FFFFFF"})
            
            if is_unknown:
                bg_color = "#1E1E24"; border_color = "#BE185D"; dash_style = (4, 4)
            else:
                bg_color = color_cfg["bg"]; border_color = color_cfg["border"]; dash_style = ()

            x1 = v.col * cell_size + pad; y1 = v.row * cell_size + pad
            if v.orientation == 'H': x2 = (v.col + v.size) * cell_size - pad; y2 = (v.row + 1) * cell_size - pad
            else: x2 = (v.col + 1) * cell_size - pad; y2 = (v.row + v.size) * cell_size - pad

            canvas.create_rectangle(x1, y1, x2, y2, fill=bg_color, outline=border_color, width=2, dash=dash_style, tags=(name, "vehicle"))
            font_size = max(8, cell_size // 3)
            canvas.create_text((x1+x2)/2, (y1+y2)/2, text="?" if is_unknown else name, fill="#BE185D" if is_unknown else color_cfg["text"], font=("Space Mono", font_size, "bold"), tags=(name, "text"))

    # --- HÀM VẼ CHÍNH ---
    def draw_board(self):
        if self.current_level_id == 4 and self.current_algo_key == "PSS":
            if self.partial_board:
                self.draw_single_board(
                    self.canvas_obs,
                    self.partial_board,
                    18
                )

            if len(self.current_beliefs) >= 1:
                self.draw_single_board(
                    self.canvas_b1,
                    self.current_beliefs[0],
                    38
                )

                self.lbl_pss_b1.configure(
                    text_color=GREEN_NEON
                    if self.current_beliefs[0].is_goal()
                    else TEXT_MUTED
                )

            if len(self.current_beliefs) >= 2:
                self.draw_single_board(
                    self.canvas_b2,
                    self.current_beliefs[1],
                    38
                )

                self.lbl_pss_b2.configure(
                    text_color=GREEN_NEON
                    if self.current_beliefs[1].is_goal()
                    else TEXT_MUTED
                )

            return

        # VẼ BÀN CỜ CHÍNH CHO CÁC THUẬT TOÁN KHÁC
        self.canvas.delete("all")
        for i in range(1, 6):
            pos = i * CELL_SIZE
            self.canvas.create_line(pos, 0, pos, CELL_SIZE*6, fill="#21262D", width=1)
            self.canvas.create_line(0, pos, CELL_SIZE*6, pos, fill="#21262D", width=1)

        if self.current_level_id == 5:
            rx1 = 0; ry1 = 2 * CELL_SIZE; rx2 = 6 * CELL_SIZE; ry2 = 3 * CELL_SIZE
            self.canvas.create_rectangle(rx1, ry1, rx2, ry2, fill="#3A1015", outline="#EF4444", width=2, dash=(4,4), tags="csp_zone")
            self.canvas.create_text(CELL_SIZE * 3, ry1 + CELL_SIZE/2, text="ĐƯỜNG CHẠY CỦA XE ĐỎ (CẤM XÂM PHẠM)", fill="#EF4444", font=("Rajdhani", 12, "bold"))

        exit_y1 = 2 * CELL_SIZE + 2
        exit_y2 = 3 * CELL_SIZE - 2
        if self.current_level_id != 5: self.canvas.create_rectangle(CELL_SIZE*6 - 6, exit_y1, CELL_SIZE*6, exit_y2, fill=RED_NEON, outline="")
        if self.current_level_id == 4 and self.current_algo_key == "BGS": self.canvas.create_rectangle(0, exit_y1, 6, exit_y2, fill=RED_NEON, outline="")

        pad_brick = 5
        for (r, c) in self.current_board.bricks:
            bx1 = c * CELL_SIZE + pad_brick; by1 = r * CELL_SIZE + pad_brick
            bx2 = (c + 1) * CELL_SIZE - pad_brick; by2 = (r + 1) * CELL_SIZE - pad_brick
            self.canvas.create_rectangle(bx1, by1, bx2, by2, fill="#1F2226", outline="#2A2F3D", width=2)
            offset = 12
            screws = [(bx1+offset, by1+offset), (bx2-offset, by1+offset), (bx1+offset, by2-offset), (bx2-offset, by2-offset)]
            for (sx, sy) in screws: self.canvas.create_oval(sx - 3, sy - 3, sx + 3, sy + 3, fill="#8A94A2", outline="")

        pad = 5
        for name, v in self.current_board.vehicles.items():
            if v.row < 0 or v.col < 0: continue
            color_cfg = CAR_COLORS.get(name, {"bg": "#1F2937", "border": "#4B5563", "text": "#FFFFFF"})
            x1 = v.col * CELL_SIZE + pad; y1 = v.row * CELL_SIZE + pad
            if v.orientation == 'H': x2 = (v.col + v.size) * CELL_SIZE - pad; y2 = (v.row + 1) * CELL_SIZE - pad
            else: x2 = (v.col + 1) * CELL_SIZE - pad; y2 = (v.row + v.size) * CELL_SIZE - pad

            rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color_cfg["bg"], outline=color_cfg["border"], width=2, tags=(name, "vehicle"))
            text_id = self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=name, fill=color_cfg["text"], font=("Space Mono", 16, "bold"), tags=(name, "text"))

            for item_id in (rect_id, text_id):
                self.canvas.tag_bind(item_id, "<Button-1>", lambda e, n=name: self.on_vehicle_click(e, n))
                self.canvas.tag_bind(item_id, "<B1-Motion>", self.on_vehicle_drag)
                self.canvas.tag_bind(item_id, "<ButtonRelease-1>", self.on_vehicle_release)

        if self.current_level_id == 5:
            for widget in self.inventory_panel.winfo_children(): widget.destroy()
            title = ctk.CTkLabel(self.inventory_panel, text="KHO XE CHỜ XẾP:", font=("Rajdhani", 12, "bold"), text_color=TEXT_MUTED)
            title.pack(side="left", padx=10, pady=8)
            unplaced = [v for v in self.current_board.vehicles.values() if v.name != 'X' and (v.row < 0 or v.col < 0)]
            if not unplaced:
                ctk.CTkLabel(self.inventory_panel, text="Đã xếp xong tất cả!", font=("Space Mono", 12, "bold"), text_color=GREEN_NEON).pack(side="left", padx=10)
            else:
                for v in unplaced:
                    color_cfg = CAR_COLORS.get(v.name, {"bg": "#1F2937", "border": "#4B5563", "text": "#FFFFFF"})
                    dir_txt = "Dọc" if v.orientation == 'V' else "Ngang"
                    badge = ctk.CTkLabel(self.inventory_panel, text=f" {v.name} ({dir_txt} {v.size}) ", font=("Space Mono", 11, "bold"), fg_color=color_cfg["bg"], text_color=color_cfg["text"], corner_radius=4)
                    badge.pack(side="left", padx=4, pady=8)

    def on_vehicle_click(self, event, name):
        if self.current_level_id == 5: return 
        self.selected_vehicle_name = name
        v = self.current_board.vehicles[name]
        self.drag_start_x = event.x; self.drag_start_y = event.y
        self.orig_v_col = v.col; self.orig_v_row = v.row
        self.ghost_cell = (v.row, v.col)
        self.show_move_hints(v)

    def on_vehicle_drag(self, event):
        if not self.selected_vehicle_name or self.current_level_id == 5: return
        v = self.current_board.vehicles[self.selected_vehicle_name]
        dx = event.x - self.drag_start_x; dy = event.y - self.drag_start_y

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
        gx1 = g_col * CELL_SIZE + 2; gy1 = g_row * CELL_SIZE + 2
        gx2 = (g_col + (v.size if v.orientation == 'H' else 1)) * CELL_SIZE - 2
        gy2 = (g_row + (1 if v.orientation == 'H' else v.size)) * CELL_SIZE - 2
        self.canvas.create_rectangle(gx1, gy1, gx2, gy2, outline=ACCENT_CYAN, width=1.5, dash=(4, 4), tags="ghost")

    def on_vehicle_release(self, event):
        if not self.selected_vehicle_name or self.current_level_id == 5: return
        self.canvas.delete("ghost"); self.canvas.delete("hint")
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
        colors = {
            "ready": GREEN_NEON, "thinking": ACCENT_ORANGE,
            "local_max": RED_NEON, "success": "#34D399"
        }
        self.status_dot.configure(text_color=colors.get(mode, GREEN_NEON))
        
        if mode == "thinking": self.status_text.configure(text="AI đang tính toán...")
        elif mode == "local_max": self.status_text.configure(text="⚠️ BẾ TẮC (LOCAL MAXIMUM)")
        elif mode == "success": self.status_text.configure(text="✅ ĐÃ TÌM THẤY LỜI GIẢI!")
        else: self.status_text.configure(text=text if text else "Sẵn sàng — Kéo xe hoặc gọi AI")

    def flash_canvas(self, color):
        original_bg = self.canvas.cget("bg")
        self.canvas.configure(bg=color)
        self.after(600, lambda: self.canvas.configure(bg=original_bg))

    def run_ai(self):
        self.btn_ai.configure(state="disabled")
        self.set_status("thinking")
        self.add_log(f"[{self.current_algo_key}] Đang tính toán...", "info")

        algos = LEVEL_DATA[self.current_level_id]["algorithms"]
        solver = algos[self.current_algo_key]["solver"]
        
        if self.current_level_id == 4 and self.current_algo_key == "PSS":
            if not self.initial_beliefs:
                self.add_log("Lỗi: Level không cấu hình belief_starts!", "error")
                self.btn_ai.configure(state="normal")
                return
            result = solver.solve(self.initial_beliefs)
        else:
            result = solver.solve(self.current_board)

        if result is None or not isinstance(result, dict) or not result.get("path"):
            self.add_log("Không tìm thấy lời giải (hoặc bị kẹt)!", "error")
            self.set_status("local_max", "Kẹt cứng — Không tìm thấy đường đi/cách xếp")
            self.btn_ai.configure(state="normal")
            return
        
        is_stuck = not result or not result.get("path") or (isinstance(result.get("visited"), str) and "không thể giải" in result["visited"])

        if is_stuck:
            self.add_log("❌ THẤT BẠI: AI đã rơi vào tối ưu cục bộ (Local Maximum)!", "error")
            if isinstance(result.get("visited"), str):
                self.add_log(f"Lý do: {result['visited']}", "error")
            self.set_status("local_max")
            self.btn_ai.configure(state="normal")
            if hasattr(self, 'flash_canvas'): self.flash_canvas("#450A0A")
            return

        self.add_log("✨ Tìm thấy đường đi!", "success")
        self.set_status("success")

        if self.current_level_id == 5:
            self.add_log(f"[{self.current_algo_key}] Đã duyệt {result['visited']} trạng thái gán", "info")
            if result.get("solution"): self.add_log("Tìm thấy cách xếp thỏa mãn!", "success")
            else: self.add_log("Không có cách xếp nào thỏa mãn!", "error")
            self.animate_path(result["path"], 0, is_csp=True, solution_found=(result.get("solution") is not None))
            return

        if isinstance(result['visited'], int):
            self.add_log(f"[{self.current_algo_key}] Đã duyệt {result['visited']} trạng thái", "info")
        else:
            self.add_log(f"{result['visited']}", "info")
            
        self.animate_path(result["path"], 0)

    def animate_path(self, path, index, is_csp=False, solution_found=False):

        if index >= len(path):
            self.btn_ai.configure(state="normal")

            if is_csp:
                if solution_found:
                    self.set_status("ready", "🎯 ĐÃ XẾP XONG TẤT CẢ CÁC XE!")
                    self.show_win_popup()
                else:
                    self.set_status("ready", "Không tìm thấy cách xếp hợp lệ!")

            else:
                if self.current_level_id == 6:

                    self.lbl_max.configure(
                        text_color=GREEN_NEON,
                        fg_color="transparent"
                    )

                    self.lbl_min.configure(
                        text_color=RED_NEON,
                        fg_color="transparent"
                    )

                    if self.current_board.is_goal():

                        self.set_status(
                            "ready",
                            "🛡️ MAX ĐÃ TẨU THOÁT THÀNH CÔNG!"
                        )

                        self.add_log(
                            "Trận đấu kết thúc: MAX THẮNG",
                            "success"
                        )

                        self.show_win_popup("MAX WINS!")

                    else:

                        if self.current_algo_key == "EX":
                            loser_text = "CHANCE KHÔNG NGĂN ĐƯỢC MAX"
                        else:
                            loser_text = "MIN ĐÃ BAO VÂY MAX"

                        self.set_status(
                            "ready",
                            "⚔️ MAX KHÔNG THỂ TẨU THOÁT!"
                        )

                        self.add_log(
                            f"Trận đấu kết thúc: {loser_text}",
                            "error"
                        )

                        self.show_win_popup("DEFENSE WINS!")

                elif self.current_level_id == 4 and self.current_algo_key == "PSS":

                    self.set_status(
                        "ready",
                        "🎯 TẤT CẢ CÁC KỊCH BẢN ĐỀU ĐẾN ĐÍCH!"
                    )

                    self.show_win_popup("ALL CLEARED!")

                else:
                    self.set_status("ready")

            return

        # ==================================================
        # CSP
        # ==================================================

        if is_csp:

            assignment = path[index]
            new_vehicles = []

            for v_init in self.initial_board.vehicles.values():

                v_clone = v_init.clone()

                if v_clone.name == 'X':
                    pass

                elif v_clone.name in assignment:
                    v_clone.row, v_clone.col = assignment[v_clone.name]

                else:
                    v_clone.row, v_clone.col = -1, -1

                new_vehicles.append(v_clone)

            self.current_board = Board(
                new_vehicles,
                self.initial_board.bricks
            )

            self.pill_moves.configure(
                text=f"STEPS: {index + 1}/{len(path)}"
            )

            assigned_str = ", ".join(
                [f"{k}:{v}" for k, v in assignment.items()]
            )

            self.add_log(
                f"Trạng thái {index + 1}: {assigned_str}",
                "current"
            )

            self.draw_board()

            self.after(
                150,
                lambda: self.animate_path(
                    path,
                    index + 1,
                    is_csp,
                    solution_found
                )
            )

            return

        # ==================================================
        # NORMAL
        # ==================================================

        name, steps = path[index]

        if self.current_level_id == 4 and self.current_algo_key == "PSS":

            self.add_log(
                f"Lệnh chung {index + 1}: Di chuyển xe {name} {abs(steps)} ô",
                "current"
            )

            for i in range(len(self.current_beliefs)):

                board = self.current_beliefs[i]

                if not board.is_goal():
                    if (name, steps) in board.get_valid_moves():
                        self.current_beliefs[i] = board.move_vehicle(
                            name,
                            steps
                        )
                        self.add_log(
                            f"  + Belief {i+1}: Xe {name} đi thành công",
                            "info"
                        )
                    else:
                        self.add_log(
                            f"  + Belief {i+1}: Xe {name} đứng im",
                            "error"
                        )
        else:
            v = self.current_board.vehicles[name]
            if v.orientation == 'H':
                dir_text = "→ phải" if steps > 0 else "← trái"
            else:
                dir_text = "↓ xuống" if steps > 0 else "↑ lên"
            self.current_board = self.current_board.move_vehicle(
                name,
                steps
            )
            is_last = (index == len(path) - 1)
            if self.current_level_id == 6:
                is_max_turn = (index % 2 == 0)
                self.lbl_turn_counter.configure(
                    text=f"Lượt: {index + 1}/20"
                )
                if is_max_turn:
                    self.lbl_max.configure(
                        text_color=BG_COLOR,
                        fg_color=GREEN_NEON
                    )
                    self.lbl_min.configure(
                        text_color=TEXT_MUTED,
                        fg_color="transparent"
                    )
                    turn_label = "[MAX]"
                    log_color = "success"
                else:
                    self.lbl_max.configure(
                        text_color=TEXT_MUTED,
                        fg_color="transparent"
                    )
                    self.lbl_min.configure(
                        text_color=BG_COLOR,
                        fg_color=RED_NEON
                    )
                    if self.current_algo_key == "EX":
                        turn_label = "[CHANCE]"
                    else:
                        turn_label = "[MIN]"
                    log_color = "error"
                self.add_log(
                    f"{turn_label} Xe {name} {dir_text} {abs(steps)} ô",
                    log_color
                )
            else:
                self.add_log(
                    f"Bước {index + 1}: Xe {name} {dir_text} {abs(steps)} ô",
                    "success" if is_last else "current"
                )
        self.move_count += 1
        self.pill_moves.configure(
            text=f"MOVES: {self.move_count}"
        )
        self.draw_board()
        if self.current_level_id == 4 and self.current_algo_key == "BGS":
            if (
                self.current_board.vehicles['X'].col == 4
                or
                self.current_board.vehicles['X'].col == 0
            ):
                self.set_status(
                    "ready",
                    "🎯 XE ĐÃ VÀO TRẠNG THÁI BELIEF GOAL!"
                )
                self.add_log(
                    "🎯 TÌM THẤY LỜI GIẢI ĐÍCH MÙ!",
                    "success"
                )
                self.show_win_popup()
                self.btn_ai.configure(state="normal")
                return
        elif self.current_level_id == 4 and self.current_algo_key == "PSS":
            pass
        else:
            self.check_win()
            if (
                self.current_board.is_goal()
                and
                self.current_level_id != 6
            ):
                self.btn_ai.configure(state="normal")
                return
        delay_speed = 800 if self.current_level_id == 6 else 480
        self.after(
            delay_speed,
            lambda: self.animate_path(
                path,
                index + 1
            )
        )

    def check_win(self):
        if self.current_board.is_goal() and self.current_level_id != 6:
            self.set_status("ready", "🎯 XE THOÁT RA! LEVEL HOÀN THÀNH!")
            self.add_log("🎯 XE THOÁT RA! LEVEL HOÀN THÀNH!", "success")
            self.show_win_popup()

    def show_win_popup(self, custom_title=None):
        popup = tk.Toplevel(self)
        if self.current_level_id == 4:
            popup.title("SOLVED!")
            win_text = "SOLVED!"
            sub_text = f"Hoàn thành trong {self.move_count} bước đi!"
            color = GREEN_NEON
        elif custom_title:
            popup.title(custom_title)
            win_text = custom_title
            sub_text = f"Trận đấu kết thúc ở lượt thứ {self.move_count}!"
            color = RED_NEON if "MIN" in custom_title else GREEN_NEON
        elif self.current_level_id == 5:
            popup.title("ARRANGED!")
            win_text = "SUCCESS!"
            sub_text = "Đã xếp xong xe không vi phạm ràng buộc!"
            color = GREEN_NEON
        else:
            popup.title("SOLVED!")
            win_text = "SOLVED!"
            sub_text = f"Hoàn thành trong {self.move_count} bước đi!"
            color = GREEN_NEON
            
        popup.geometry("380x220") 
        popup.configure(bg=PANEL_COLOR)
        popup.transient(self)
        popup.grab_set()
        
        x = self.winfo_x() + (self.winfo_width() // 2) - 190
        y = self.winfo_y() + (self.winfo_height() // 2) - 110
        popup.geometry(f"+{x}+{y}")

        lbl_win = ctk.CTkLabel(popup, text=win_text, font=("Space Mono", 32, "bold"), text_color=color)
        lbl_sub = ctk.CTkLabel(popup, text=sub_text, font=("Rajdhani", 15), text_color=TEXT_MAIN)

        lbl_win.pack(pady=(30, 5))
        lbl_sub.pack(pady=5)

        btn_close = ctk.CTkButton(popup, text="Tiếp tục", font=("Rajdhani", 14, "bold"), fg_color=color, text_color="#0A0C10", hover_color="#16A34A", command=popup.destroy)
        btn_close.pack(pady=20)

    def reset_game(self):
        self.current_board = self.load_level(self.current_level_id)
        
        # Reset state cho PSS
        self.current_beliefs = []
        if self.initial_beliefs:
            self.current_beliefs = [Board([v.clone() for v in b.vehicles.values()], b.bricks) for b in self.initial_beliefs]
            
        self.move_count = 0
        self.pill_moves.configure(text="MOVES: 0")
        self.update_algo_menu()
        self.draw_board()
        self.log_box.delete("1.0", "end")
        self.add_log("Log cleared.", "")
        self.add_log(f"Level {self.current_level_id} đã được đặt lại trạng thái ban đầu.", "info")
        self.set_status("ready")
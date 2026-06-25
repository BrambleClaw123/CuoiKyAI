import customtkinter as ctk
from ui.app_window import RushHourAIApp
import sys

sys.setrecursionlimit(100000)
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = RushHourAIApp()
    app.mainloop()
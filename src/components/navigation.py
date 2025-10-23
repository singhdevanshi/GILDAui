import tkinter as tk
from src.config import Config

class NavigationBar(tk.Frame):
    """Navigation bar component for page switching"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config = Config()
        
        self.configure(bg=self.config.SECONDARY_COLOR, height=60)
        self.pack_propagate(False)
        
        self.setup_navigation()
    
    def setup_navigation(self):
        """Setup navigation buttons"""
        # App title
        title = tk.Label(
            self,
            text="GILDA",
            font=(self.config.FONT_FAMILY, self.config.FONT_SIZE_TITLE, "bold"),
            bg=self.config.SECONDARY_COLOR,
            fg=self.config.TEXT_COLOR
        )
        title.pack(side="left", padx=20, pady=15)
        
        # Navigation buttons frame
        nav_frame = tk.Frame(self, bg=self.config.SECONDARY_COLOR)
        nav_frame.pack(side="right", padx=20, pady=10)
        
        # Create navigation buttons (will be enabled/disabled based on login state)
        self.radar_btn = tk.Button(
            nav_frame,
            text="Radar",
            command=lambda: self.controller.show_page("RadarPage"),
            font=(self.config.FONT_FAMILY, self.config.FONT_SIZE_MEDIUM),
            bg=self.config.ACCENT_COLOR,
            fg=self.config.TEXT_COLOR,
            relief="flat",
            padx=15,
            pady=5,
            state="disabled"
        )
        self.radar_btn.pack(side="left", padx=5)
        
        self.map_btn = tk.Button(
            nav_frame,
            text="Map",
            command=lambda: self.controller.show_page("MapPage"),
            font=(self.config.FONT_FAMILY, self.config.FONT_SIZE_MEDIUM),
            bg=self.config.ACCENT_COLOR,
            fg=self.config.TEXT_COLOR,
            relief="flat",
            padx=15,
            pady=5,
            state="disabled"
        )
        self.map_btn.pack(side="left", padx=5)
        
        self.logout_btn = tk.Button(
            nav_frame,
            text="Logout",
            command=self.handle_logout,
            font=(self.config.FONT_FAMILY, self.config.FONT_SIZE_MEDIUM),
            bg=self.config.ERROR_COLOR,
            fg=self.config.TEXT_COLOR,
            relief="flat",
            padx=15,
            pady=5,
            state="disabled"
        )
        self.logout_btn.pack(side="left", padx=5)
    
    def enable_navigation(self):
        """Enable navigation buttons after login"""
        self.radar_btn.config(state="normal")
        self.map_btn.config(state="normal")
        self.logout_btn.config(state="normal")
    
    def disable_navigation(self):
        """Disable navigation buttons after logout"""
        self.radar_btn.config(state="disabled")
        self.map_btn.config(state="disabled")
        self.logout_btn.config(state="disabled")
    
    def handle_logout(self):
        """Handle logout action"""
        self.disable_navigation()
        self.controller.show_page("LoginPage")
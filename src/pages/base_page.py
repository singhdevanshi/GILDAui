import tkinter as tk
from abc import ABC, abstractmethod
from src.config import Config

class BasePage(ABC, tk.Frame):
    """Base class for all pages in the application"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config = Config()
        
        # Configure the frame
        self.configure(bg=self.config.PRIMARY_COLOR)
        
        # Initialize the page
        self.setup_ui()
    
    @abstractmethod
    def setup_ui(self):
        """Setup the user interface for this page"""
        pass
    
    def show(self):
        """Show this page"""
        self.tkraise()
    
    def hide(self):
        """Hide this page"""
        pass
    
    def create_title_label(self, text, row=0, column=0, columnspan=1):
        """Create a standardized title label"""
        title = tk.Label(
            self,
            text=text,
            font=(self.config.FONT_FAMILY, self.config.FONT_SIZE_TITLE, "bold"),
            bg=self.config.PRIMARY_COLOR,
            fg=self.config.TEXT_COLOR
        )
        title.grid(row=row, column=column, columnspan=columnspan, pady=20, sticky="ew")
        return title
    
    def create_button(self, text, command, row, column, **kwargs):
        """Create a standardized button"""
        button = tk.Button(
            self,
            text=text,
            command=command,
            font=(self.config.FONT_FAMILY, self.config.FONT_SIZE_MEDIUM),
            bg=self.config.ACCENT_COLOR,
            fg=self.config.TEXT_COLOR,
            activebackground=self.config.SECONDARY_COLOR,
            activeforeground=self.config.TEXT_COLOR,
            relief="flat",
            padx=20,
            pady=10,
            **kwargs
        )
        button.grid(row=row, column=column, pady=10, padx=10, sticky="ew")
        return button
import tkinter as tk
from tkinter import ttk
from src.config import Config

class StatusIndicator(tk.Frame):
    """Status indicator widget with color-coded states"""
    
    def __init__(self, parent, label="Status"):
        super().__init__(parent)
        self.config = Config()
        self.configure(bg=self.config.SECONDARY_COLOR)
        
        self.label_text = label
        self.setup_widget()
    
    def setup_widget(self):
        """Setup the status indicator"""
        # Label
        self.label = tk.Label(
            self,
            text=f"{self.label_text}:",
            font=(self.config.FONT_FAMILY, self.config.FONT_SIZE_MEDIUM),
            bg=self.config.SECONDARY_COLOR,
            fg=self.config.TEXT_COLOR
        )
        self.label.pack(side="left", padx=(0, 10))
        
        # Status circle
        self.canvas = tk.Canvas(
            self,
            width=20,
            height=20,
            bg=self.config.SECONDARY_COLOR,
            highlightthickness=0
        )
        self.canvas.pack(side="left", padx=(0, 10))
        
        # Status text
        self.status_label = tk.Label(
            self,
            text="Unknown",
            font=(self.config.FONT_FAMILY, self.config.FONT_SIZE_MEDIUM, "bold"),
            bg=self.config.SECONDARY_COLOR,
            fg=self.config.TEXT_COLOR
        )
        self.status_label.pack(side="left")
        
        # Initial state
        self.set_status("unknown")
    
    def set_status(self, status, text=None):
        """Set the status indicator state"""
        colors = {
            "active": self.config.SUCCESS_COLOR,
            "warning": self.config.WARNING_COLOR,
            "error": self.config.ERROR_COLOR,
            "unknown": self.config.TEXT_COLOR
        }
        
        status_texts = {
            "active": "ACTIVE",
            "warning": "WARNING",
            "error": "ERROR",
            "unknown": "UNKNOWN"
        }
        
        color = colors.get(status.lower(), self.config.TEXT_COLOR)
        display_text = text or status_texts.get(status.lower(), status.upper())
        
        # Update circle
        self.canvas.delete("all")
        self.canvas.create_oval(2, 2, 18, 18, fill=color, outline=color)
        
        # Update text
        self.status_label.config(text=display_text, fg=color)

class AlertPanel(tk.Frame):
    """Alert panel for displaying notifications"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.config = Config()
        self.configure(bg=self.config.ERROR_COLOR, relief="raised", bd=2)
        
        self.alerts = []
        self.setup_widget()
        self.hide()  # Initially hidden
    
    def setup_widget(self):
        """Setup the alert panel"""
        # Alert title
        self.title_label = tk.Label(
            self,
            text="⚠ GUNSHOT DETECTED ⚠",
            font=(self.config.FONT_FAMILY, self.config.FONT_SIZE_LARGE, "bold"),
            bg=self.config.ERROR_COLOR,
            fg=self.config.TEXT_COLOR
        )
        self.title_label.pack(pady=10)
        
        # Alert details
        self.details_label = tk.Label(
            self,
            text="",
            font=(self.config.FONT_FAMILY, self.config.FONT_SIZE_MEDIUM),
            bg=self.config.ERROR_COLOR,
            fg=self.config.TEXT_COLOR,
            justify="center"
        )
        self.details_label.pack(pady=5)
        
        # Dismiss button
        self.dismiss_btn = tk.Button(
            self,
            text="Acknowledge",
            command=self.dismiss_alert,
            font=(self.config.FONT_FAMILY, self.config.FONT_SIZE_MEDIUM),
            bg=self.config.TEXT_COLOR,
            fg=self.config.ERROR_COLOR,
            relief="flat",
            padx=20,
            pady=5
        )
        self.dismiss_btn.pack(pady=10)
    
    def show_alert(self, message, details=""):
        """Show an alert with message and details"""
        self.title_label.config(text=message)
        self.details_label.config(text=details)
        self.pack(fill="x", padx=20, pady=10)
        
        # Auto-dismiss after 10 seconds
        self.after(10000, self.dismiss_alert)
    
    def dismiss_alert(self):
        """Dismiss the current alert"""
        self.pack_forget()
    
    def hide(self):
        """Hide the alert panel"""
        self.pack_forget()

class DataTable(tk.Frame):
    """Data table widget for displaying tabular information"""
    
    def __init__(self, parent, columns):
        super().__init__(parent)
        self.config = Config()
        self.configure(bg=self.config.SECONDARY_COLOR)
        
        self.columns = columns
        self.setup_widget()
    
    def setup_widget(self):
        """Setup the data table"""
        # Create treeview
        self.tree = ttk.Treeview(
            self,
            columns=self.columns,
            show="headings",
            height=10
        )
        
        # Configure columns
        for col in self.columns:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=100, anchor="center")
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack widgets
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def insert_row(self, values):
        """Insert a row into the table"""
        self.tree.insert("", "end", values=values)
    
    def clear_table(self):
        """Clear all rows from the table"""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def get_selected(self):
        """Get the selected row data"""
        selection = self.tree.selection()
        if selection:
            return self.tree.item(selection[0])["values"]
        return None
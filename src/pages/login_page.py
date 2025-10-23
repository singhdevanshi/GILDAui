import tkinter as tk
from tkinter import messagebox
import math
from src.pages.base_page import BasePage
from src.utils.auth import AuthManager

class LoginPage(BasePage):
    """Modern military-style login page for Indian Army application"""
    
    def __init__(self, parent, controller):
        self.auth_manager = AuthManager()
        self.animation_step = 0
        super().__init__(parent, controller)
    
    def setup_ui(self):
        """Setup the modern military login interface"""
        # Configure main grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=1)
        
        # Header section with military graphics
        self.create_header()
        
        # Main login card
        self.create_login_card()
        
        # Footer with system info
        self.create_footer()
        
        # Start subtle animations
        self.animate_elements()
    
    def create_header(self):
        """Create the header with military styling"""
        header_frame = tk.Frame(self, bg=self.config.PRIMARY_COLOR, height=120)
        header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=20, pady=20)
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Left military emblem (text-based)
        emblem_frame = tk.Frame(header_frame, bg=self.config.SECONDARY_COLOR, 
                               relief="raised", bd=3, width=80, height=80)
        emblem_frame.grid(row=0, column=0, padx=20, pady=20)
        emblem_frame.grid_propagate(False)
        
        # Create a star emblem using canvas
        emblem_canvas = tk.Canvas(emblem_frame, bg=self.config.SECONDARY_COLOR, 
                                 highlightthickness=0, width=76, height=76)
        emblem_canvas.pack(expand=True, fill="both", padx=2, pady=2)
        self.draw_military_star(emblem_canvas)
        
        # Center title
        title_frame = tk.Frame(header_frame, bg=self.config.PRIMARY_COLOR)
        title_frame.grid(row=0, column=1, sticky="ew", padx=20)
        
        main_title = tk.Label(
            title_frame,
            text="GILDA",
            font=(self.config.FONT_FAMILY, 32, "bold"),
            bg=self.config.PRIMARY_COLOR,
            fg=self.config.GOLD_COLOR
        )
        main_title.pack(pady=(10, 0))
        
        subtitle = tk.Label(
            title_frame,
            text="Gunshot Intelligence & Location Detection Array",
            font=(self.config.FONT_FAMILY, 12, "italic"),
            bg=self.config.PRIMARY_COLOR,
            fg=self.config.TEXT_COLOR
        )
        subtitle.pack()
        
        classification = tk.Label(
            title_frame,
            text="● RESTRICTED ACCESS ●",
            font=(self.config.FONT_FAMILY, 10, "bold"),
            bg=self.config.PRIMARY_COLOR,
            fg=self.config.ERROR_COLOR
        )
        classification.pack(pady=(5, 0))
        
        # Right status indicator
        status_frame = tk.Frame(header_frame, bg=self.config.SECONDARY_COLOR,
                               relief="raised", bd=2, width=100, height=80)
        status_frame.grid(row=0, column=2, padx=20, pady=20)
        status_frame.grid_propagate(False)
        
        tk.Label(
            status_frame,
            text="SYSTEM\nSTATUS",
            font=(self.config.FONT_FAMILY, 9, "bold"),
            bg=self.config.SECONDARY_COLOR,
            fg=self.config.TEXT_COLOR,
            justify="center"
        ).pack(pady=(10, 5))
        
        self.status_indicator = tk.Label(
            status_frame,
            text="● ONLINE",
            font=(self.config.FONT_FAMILY, 8, "bold"),
            bg=self.config.SECONDARY_COLOR,
            fg=self.config.SUCCESS_COLOR
        )
        self.status_indicator.pack()
    
    def create_login_card(self):
        """Create the main login card with modern styling"""
        # Main card container
        card_container = tk.Frame(self, bg=self.config.PRIMARY_COLOR)
        card_container.grid(row=1, column=1, sticky="nsew", padx=40, pady=20)
        card_container.grid_columnconfigure(0, weight=1)
        card_container.grid_rowconfigure(1, weight=1)
        
        # Card header
        card_header = tk.Frame(card_container, bg=self.config.SECONDARY_COLOR, 
                              relief="raised", bd=3, height=60)
        card_header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
        card_header.grid_propagate(False)
        
        tk.Label(
            card_header,
            text="🔐 SECURE LOGIN",
            font=(self.config.FONT_FAMILY, 16, "bold"),
            bg=self.config.SECONDARY_COLOR,
            fg=self.config.GOLD_COLOR
        ).pack(expand=True)
        
        # Main card body
        card_body = tk.Frame(card_container, bg=self.config.SECONDARY_COLOR,
                            relief="raised", bd=3)
        card_body.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        card_body.grid_columnconfigure(0, weight=1)
        
        # Login form
        form_frame = tk.Frame(card_body, bg=self.config.SECONDARY_COLOR)
        form_frame.pack(expand=True, fill="both", padx=40, pady=40)
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Service Number field
        tk.Label(
            form_frame,
            text="Service Number:",
            font=(self.config.FONT_FAMILY, self.config.FONT_SIZE_MEDIUM, "bold"),
            bg=self.config.SECONDARY_COLOR,
            fg=self.config.TEXT_COLOR
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.username_entry = tk.Entry(
            form_frame,
            font=(self.config.FONT_FAMILY, self.config.FONT_SIZE_MEDIUM),
            bg=self.config.TEXT_COLOR,
            fg=self.config.PRIMARY_COLOR,
            relief="flat",
            bd=5,
            insertbackground=self.config.PRIMARY_COLOR
        )
        self.username_entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        # Password field
        tk.Label(
            form_frame,
            text="Access Code:",
            font=(self.config.FONT_FAMILY, self.config.FONT_SIZE_MEDIUM, "bold"),
            bg=self.config.SECONDARY_COLOR,
            fg=self.config.TEXT_COLOR
        ).grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        self.password_entry = tk.Entry(
            form_frame,
            font=(self.config.FONT_FAMILY, self.config.FONT_SIZE_MEDIUM),
            show="●",
            bg=self.config.TEXT_COLOR,
            fg=self.config.PRIMARY_COLOR,
            relief="flat",
            bd=5,
            insertbackground=self.config.PRIMARY_COLOR
        )
        self.password_entry.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 30))
        
        # Login button with military styling
        self.login_btn = tk.Button(
            form_frame,
            text="🔓 AUTHENTICATE",
            command=self.handle_login,
            font=(self.config.FONT_FAMILY, self.config.FONT_SIZE_MEDIUM, "bold"),
            bg=self.config.SUCCESS_COLOR,
            fg=self.config.TEXT_COLOR,
            activebackground=self.config.ACCENT_COLOR,
            activeforeground=self.config.TEXT_COLOR,
            relief="raised",
            bd=3,
            padx=40,
            pady=15,
            cursor="hand2"
        )
        self.login_btn.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Security notice
        security_frame = tk.Frame(card_body, bg=self.config.BORDER_COLOR, height=40)
        security_frame.pack(fill="x", padx=10, pady=(0, 10))
        security_frame.pack_propagate(False)
        
        tk.Label(
            security_frame,
            text="⚠ Authorized Personnel Only • All Access Monitored ⚠",
            font=(self.config.FONT_FAMILY, 9, "bold"),
            bg=self.config.BORDER_COLOR,
            fg=self.config.WARNING_COLOR
        ).pack(expand=True)
        
        # Bind events
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.handle_login())
        self.username_entry.bind('<FocusIn>', self.on_entry_focus)
        self.password_entry.bind('<FocusIn>', self.on_entry_focus)
        
        # Focus on username field
        self.username_entry.focus()
    
    def create_footer(self):
        """Create footer with system information"""
        footer_frame = tk.Frame(self, bg=self.config.PRIMARY_COLOR, height=60)
        footer_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=20, pady=10)
        footer_frame.grid_propagate(False)
        footer_frame.grid_columnconfigure(1, weight=1)
        
        # Left info
        tk.Label(
            footer_frame,
            text="Indian Army • Defense Technology",
            font=(self.config.FONT_FAMILY, 9),
            bg=self.config.PRIMARY_COLOR,
            fg=self.config.TEXT_COLOR
        ).grid(row=0, column=0, sticky="w", padx=20)
        
        # Center info
        tk.Label(
            footer_frame,
            text="Version 1.0 • Secure Terminal",
            font=(self.config.FONT_FAMILY, 9),
            bg=self.config.PRIMARY_COLOR,
            fg=self.config.TEXT_COLOR
        ).grid(row=0, column=1)
        
        # Right info
        import datetime
        current_time = datetime.datetime.now().strftime("%d %b %Y • %H:%M IST")
        tk.Label(
            footer_frame,
            text=current_time,
            font=(self.config.FONT_FAMILY, 9),
            bg=self.config.PRIMARY_COLOR,
            fg=self.config.TEXT_COLOR
        ).grid(row=0, column=2, sticky="e", padx=20)
    
    def draw_military_star(self, canvas):
        """Draw a military star emblem"""
        center_x, center_y = 38, 38
        outer_radius = 30
        inner_radius = 12
        
        # Calculate star points
        points = []
        for i in range(10):
            angle = (i * math.pi) / 5
            if i % 2 == 0:
                # Outer point
                x = center_x + outer_radius * math.cos(angle - math.pi/2)
                y = center_y + outer_radius * math.sin(angle - math.pi/2)
            else:
                # Inner point
                x = center_x + inner_radius * math.cos(angle - math.pi/2)
                y = center_y + inner_radius * math.sin(angle - math.pi/2)
            points.extend([x, y])
        
        # Draw star
        canvas.create_polygon(points, fill=self.config.GOLD_COLOR, 
                            outline=self.config.TEXT_COLOR, width=2)
        
        # Add center circle
        canvas.create_oval(center_x-8, center_y-8, center_x+8, center_y+8,
                          fill=self.config.ERROR_COLOR, outline=self.config.TEXT_COLOR)
    
    def on_entry_focus(self, event):
        """Handle entry field focus events"""
        event.widget.configure(bg="#FFFFFF", relief="solid", bd=2)
        self.after(200, lambda: event.widget.configure(bg=self.config.TEXT_COLOR, relief="flat", bd=5))
    
    def animate_elements(self):
        """Subtle animation for status indicator"""
        colors = [self.config.SUCCESS_COLOR, self.config.ACCENT_COLOR]
        color = colors[self.animation_step % 2]
        
        if hasattr(self, 'status_indicator'):
            self.status_indicator.configure(fg=color)
        
        self.animation_step += 1
        self.after(2000, self.animate_elements)  # Animate every 2 seconds
    
    def handle_login(self):
        """Handle login attempt with enhanced feedback"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            self.show_error("Access Denied", "Service Number and Access Code required")
            return
        
        # Disable button during authentication
        self.login_btn.configure(state="disabled", text="🔄 AUTHENTICATING...")
        self.update()
        
        # Simulate authentication delay
        self.after(1000, lambda: self.complete_authentication(username, password))
    
    def complete_authentication(self, username, password):
        """Complete the authentication process"""
        if self.auth_manager.authenticate(username, password):
            self.login_btn.configure(text="✅ ACCESS GRANTED", bg=self.config.SUCCESS_COLOR)
            self.password_entry.delete(0, tk.END)
            
            # Navigate after brief delay
            self.after(1000, lambda: self.controller.show_page("RadarPage"))
        else:
            self.show_error("Access Denied", "Invalid credentials")
            self.login_btn.configure(state="normal", text="🔓 AUTHENTICATE", 
                                   bg=self.config.SUCCESS_COLOR)
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()
    
    def show_error(self, title, message):
        """Show error with military styling"""
        messagebox.showerror(title, message)
    
    def show(self):
        """Show the login page and reset form"""
        super().show()
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        if hasattr(self, 'login_btn'):
            self.login_btn.configure(state="normal", text="🔓 AUTHENTICATE", 
                                   bg=self.config.SUCCESS_COLOR)
        self.username_entry.focus()
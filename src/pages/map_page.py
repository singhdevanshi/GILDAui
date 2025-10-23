import tkinter as tk
from tkinter import ttk
import math
import random
from src.pages.base_page import BasePage
from src.utils.data_manager import DataManager

class MapPage(BasePage):
    """Military-grade map view page for tactical positioning"""
    
    def __init__(self, parent, controller):
        self.data_manager = DataManager()
        self.map_markers = []
        self.node_coords = {"lat": 28.6139, "lon": 77.2090}
        self.enemy_coords = {"lat": 28.6145, "lon": 77.2095}
        super().__init__(parent, controller)
    
    def setup_ui(self):
        """Setup the military map interface"""
        # Configure main grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Map
        self.grid_rowconfigure(2, weight=0)  # Coordinates
        self.grid_rowconfigure(3, weight=0)  # Tactical info
        
        # Header with title and navigation
        self.create_header()
        
        # Main map display
        self.create_map_display()
        
        # Coordinates display
        self.create_coordinates_display()
        
        # Tactical information box
        self.create_tactical_info()
    
    def create_header(self):
        """Create header with title and navigation"""
        header_frame = tk.Frame(self, bg=self.config.PRIMARY_COLOR, height=80)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Navigation buttons (left)
        nav_frame = tk.Frame(header_frame, bg=self.config.PRIMARY_COLOR)
        nav_frame.grid(row=0, column=0, sticky="w")
        
        radar_btn = tk.Button(
            nav_frame,
            text="RADAR VIEW",
            command=lambda: self.controller.show_page("RadarPage"),
            font=(self.config.FONT_FAMILY, 10, "bold"),
            bg=self.config.ACCENT_COLOR,
            fg=self.config.TEXT_COLOR,
            relief="raised",
            bd=2,
            padx=15,
            pady=8
        )
        radar_btn.pack(side="left", padx=5)
        
        logout_btn = tk.Button(
            nav_frame,
            text="LOGOUT",
            command=self.handle_logout,
            font=(self.config.FONT_FAMILY, 10, "bold"),
            bg=self.config.ERROR_COLOR,
            fg=self.config.TEXT_COLOR,
            relief="raised",
            bd=2,
            padx=15,
            pady=8
        )
        logout_btn.pack(side="left", padx=5)
        
        # Center title
        title = tk.Label(
            header_frame,
            text="MAP",
            font=(self.config.FONT_FAMILY, 36, "bold"),
            bg=self.config.PRIMARY_COLOR,
            fg=self.config.GOLD_COLOR
        )
        title.grid(row=0, column=1)
    
    def create_map_display(self):
        """Create the main map display with GIS styling"""
        map_frame = tk.Frame(self, bg=self.config.SECONDARY_COLOR, relief="raised", bd=3)
        map_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        map_frame.grid_rowconfigure(0, weight=1)
        map_frame.grid_columnconfigure(0, weight=1)
        
        # Map canvas
        self.map_canvas = tk.Canvas(
            map_frame,
            bg="#2F4F2F",  # Dark green for map background
            highlightthickness=0
        )
        self.map_canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Bind canvas events
        self.map_canvas.bind('<Configure>', self.on_canvas_resize)
        
        # Draw the GIS map
        self.after(100, self.draw_gis_map)
    
    def create_coordinates_display(self):
        """Create coordinates display below the map"""
        coords_frame = tk.Frame(self, bg=self.config.PRIMARY_COLOR, height=60)
        coords_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        coords_frame.grid_propagate(False)
        coords_frame.grid_columnconfigure(0, weight=1)
        coords_frame.grid_columnconfigure(1, weight=1)
        
        # Your coordinates (left)
        your_frame = tk.Frame(coords_frame, bg=self.config.SECONDARY_COLOR, relief="raised", bd=2)
        your_frame.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        tk.Label(
            your_frame,
            text="YOUR COORDINATES:",
            font=(self.config.FONT_FAMILY, 12, "bold"),
            bg=self.config.SECONDARY_COLOR,
            fg=self.config.SUCCESS_COLOR
        ).pack(pady=5)
        
        self.your_coords_label = tk.Label(
            your_frame,
            text=f"{self.node_coords['lat']:.4f}° N, {self.node_coords['lon']:.4f}° E",
            font=(self.config.FONT_FAMILY, 11, "bold"),
            bg=self.config.SECONDARY_COLOR,
            fg=self.config.TEXT_COLOR
        )
        self.your_coords_label.pack(pady=5)
        
        # Enemy coordinates (right)
        enemy_frame = tk.Frame(coords_frame, bg=self.config.SECONDARY_COLOR, relief="raised", bd=2)
        enemy_frame.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        
        tk.Label(
            enemy_frame,
            text="ENEMY COORDINATES:",
            font=(self.config.FONT_FAMILY, 12, "bold"),
            bg=self.config.SECONDARY_COLOR,
            fg=self.config.ERROR_COLOR
        ).pack(pady=5)
        
        self.enemy_coords_label = tk.Label(
            enemy_frame,
            text=f"{self.enemy_coords['lat']:.4f}° N, {self.enemy_coords['lon']:.4f}° E",
            font=(self.config.FONT_FAMILY, 11, "bold"),
            bg=self.config.SECONDARY_COLOR,
            fg=self.config.TEXT_COLOR
        )
        self.enemy_coords_label.pack(pady=5)
    
    def create_tactical_info(self):
        """Create tactical information box"""
        tactical_frame = tk.Frame(self, bg=self.config.BORDER_COLOR, relief="raised", bd=3, height=80)
        tactical_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        tactical_frame.grid_propagate(False)
        tactical_frame.grid_columnconfigure(0, weight=1)
        tactical_frame.grid_columnconfigure(1, weight=1)
        tactical_frame.grid_columnconfigure(2, weight=1)
        
        # Calculate tactical data
        self.calculate_tactical_data()
        
        # Elevation
        elev_frame = tk.Frame(tactical_frame, bg=self.config.BORDER_COLOR)
        elev_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        tk.Label(
            elev_frame,
            text="ELEVATION:",
            font=(self.config.FONT_FAMILY, 10, "bold"),
            bg=self.config.BORDER_COLOR,
            fg=self.config.TEXT_COLOR
        ).pack()
        
        self.elevation_label = tk.Label(
            elev_frame,
            text="+12.5°",
            font=(self.config.FONT_FAMILY, 14, "bold"),
            bg=self.config.BORDER_COLOR,
            fg=self.config.WARNING_COLOR
        )
        self.elevation_label.pack()
        
        # Range
        range_frame = tk.Frame(tactical_frame, bg=self.config.BORDER_COLOR)
        range_frame.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        
        tk.Label(
            range_frame,
            text="RANGE:",
            font=(self.config.FONT_FAMILY, 10, "bold"),
            bg=self.config.BORDER_COLOR,
            fg=self.config.TEXT_COLOR
        ).pack()
        
        self.range_label = tk.Label(
            range_frame,
            text="1,247 m",
            font=(self.config.FONT_FAMILY, 14, "bold"),
            bg=self.config.BORDER_COLOR,
            fg=self.config.WARNING_COLOR
        )
        self.range_label.pack()
        
        # Angle
        angle_frame = tk.Frame(tactical_frame, bg=self.config.BORDER_COLOR)
        angle_frame.grid(row=0, column=2, sticky="ew", padx=10, pady=10)
        
        tk.Label(
            angle_frame,
            text="ANGLE:",
            font=(self.config.FONT_FAMILY, 10, "bold"),
            bg=self.config.BORDER_COLOR,
            fg=self.config.TEXT_COLOR
        ).pack()
        
        self.angle_label = tk.Label(
            angle_frame,
            text="045°",
            font=(self.config.FONT_FAMILY, 14, "bold"),
            bg=self.config.BORDER_COLOR,
            fg=self.config.WARNING_COLOR
        )
        self.angle_label.pack()
    
    def draw_gis_map(self):
        """Draw a realistic GIS-style map"""
        self.map_canvas.delete("all")
        
        # Get canvas dimensions
        width = self.map_canvas.winfo_width()
        height = self.map_canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            self.after(100, self.draw_gis_map)
            return
        
        # Draw map background with terrain features
        self.draw_terrain_features(width, height)
        
        # Draw grid lines (UTM grid style)
        self.draw_grid_lines(width, height)
        
        # Draw scale and compass
        self.draw_map_elements(width, height)
        
        # Draw node and enemy positions
        self.draw_positions(width, height)
    
    def draw_terrain_features(self, width, height):
        """Draw terrain features like roads, buildings, etc."""
        # Draw some roads
        road_color = "#8B7355"  # Brown for roads
        
        # Horizontal road
        self.map_canvas.create_rectangle(
            0, height//2 - 10, width, height//2 + 10,
            fill=road_color, outline=road_color
        )
        
        # Vertical road
        self.map_canvas.create_rectangle(
            width//2 - 10, 0, width//2 + 10, height,
            fill=road_color, outline=road_color
        )
        
        # Draw some buildings
        building_color = "#696969"  # Dark gray for buildings
        
        buildings = [
            (width//4 - 20, height//4 - 15, width//4 + 20, height//4 + 15),
            (3*width//4 - 25, height//4 - 20, 3*width//4 + 25, height//4 + 20),
            (width//4 - 15, 3*height//4 - 25, width//4 + 15, 3*height//4 + 25),
            (3*width//4 - 30, 3*height//4 - 15, 3*width//4 + 30, 3*height//4 + 15),
        ]
        
        for x1, y1, x2, y2 in buildings:
            self.map_canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=building_color, outline="#FFFFFF", width=1
            )
    
    def draw_grid_lines(self, width, height):
        """Draw UTM-style grid lines"""
        grid_color = "#4F6F4F"  # Darker green for grid
        
        # Vertical lines
        for i in range(0, width, 50):
            self.map_canvas.create_line(
                i, 0, i, height,
                fill=grid_color, width=1, dash=(2, 4)
            )
        
        # Horizontal lines
        for i in range(0, height, 50):
            self.map_canvas.create_line(
                0, i, width, i,
                fill=grid_color, width=1, dash=(2, 4)
            )
    
    def draw_map_elements(self, width, height):
        """Draw scale, compass, and other map elements"""
        # Compass rose (top right)
        compass_x = width - 60
        compass_y = 60
        
        # Compass circle
        self.map_canvas.create_oval(
            compass_x - 25, compass_y - 25,
            compass_x + 25, compass_y + 25,
            outline=self.config.GOLD_COLOR, width=2
        )
        
        # North arrow
        self.map_canvas.create_line(
            compass_x, compass_y - 20,
            compass_x, compass_y + 20,
            fill=self.config.ERROR_COLOR, width=3, arrow=tk.FIRST
        )
        
        # N label
        self.map_canvas.create_text(
            compass_x, compass_y - 35,
            text="N", fill=self.config.TEXT_COLOR,
            font=(self.config.FONT_FAMILY, 12, "bold")
        )
        
        # Scale bar (bottom left)
        scale_x = 50
        scale_y = height - 30
        
        self.map_canvas.create_line(
            scale_x, scale_y, scale_x + 100, scale_y,
            fill=self.config.TEXT_COLOR, width=3
        )
        
        self.map_canvas.create_text(
            scale_x + 50, scale_y - 15,
            text="1 km", fill=self.config.TEXT_COLOR,
            font=(self.config.FONT_FAMILY, 10, "bold")
        )
    
    def draw_positions(self, width, height):
        """Draw node and enemy positions on the map"""
        center_x = width // 2
        center_y = height // 2
        
        # Node position (center)
        node_size = 12
        self.map_canvas.create_oval(
            center_x - node_size, center_y - node_size,
            center_x + node_size, center_y + node_size,
            fill=self.config.SUCCESS_COLOR,
            outline=self.config.TEXT_COLOR, width=3
        )
        
        # Node label
        self.map_canvas.create_text(
            center_x, center_y - 25,
            text="NODE", fill=self.config.TEXT_COLOR,
            font=(self.config.FONT_FAMILY, 10, "bold")
        )
        
        # Enemy position (offset from center)
        enemy_x = center_x + 80
        enemy_y = center_y - 60
        enemy_size = 10
        
        self.map_canvas.create_oval(
            enemy_x - enemy_size, enemy_y - enemy_size,
            enemy_x + enemy_size, enemy_y + enemy_size,
            fill=self.config.ERROR_COLOR,
            outline=self.config.TEXT_COLOR, width=3
        )
        
        # Enemy label
        self.map_canvas.create_text(
            enemy_x, enemy_y - 20,
            text="ENEMY LOC", fill=self.config.TEXT_COLOR,
            font=(self.config.FONT_FAMILY, 9, "bold")
        )
        
        # Draw line between positions
        self.map_canvas.create_line(
            center_x, center_y, enemy_x, enemy_y,
            fill=self.config.WARNING_COLOR, width=2, dash=(5, 5)
        )
        
        # Distance marker
        mid_x = (center_x + enemy_x) // 2
        mid_y = (center_y + enemy_y) // 2
        
        self.map_canvas.create_text(
            mid_x, mid_y - 10,
            text="1.2 km", fill=self.config.WARNING_COLOR,
            font=(self.config.FONT_FAMILY, 9, "bold")
        )
    
    def calculate_tactical_data(self):
        """Calculate and update tactical data"""
        # Generate realistic tactical data
        elevation = random.uniform(-5, 25)
        range_m = random.randint(800, 2500)
        angle = random.randint(0, 359)
        
        # Store for updates
        self.tactical_data = {
            "elevation": elevation,
            "range": range_m,
            "angle": angle
        }
    
    def update_tactical_display(self):
        """Update tactical information display"""
        if hasattr(self, 'tactical_data'):
            self.elevation_label.config(text=f"{self.tactical_data['elevation']:+.1f}°")
            self.range_label.config(text=f"{self.tactical_data['range']:,} m")
            self.angle_label.config(text=f"{self.tactical_data['angle']:03d}°")
        
        # Update enemy coordinates
        self.enemy_coords['lat'] += random.uniform(-0.0001, 0.0001)
        self.enemy_coords['lon'] += random.uniform(-0.0001, 0.0001)
        
        self.enemy_coords_label.config(
            text=f"{self.enemy_coords['lat']:.4f}° N, {self.enemy_coords['lon']:.4f}° E"
        )
        
        # Recalculate tactical data
        self.calculate_tactical_data()
        
        # Schedule next update
        self.after(2000, self.update_tactical_display)
    

    

    

    
    def on_canvas_resize(self, event):
        """Handle canvas resize and redraw map"""
        self.draw_gis_map()
    
    def handle_logout(self):
        """Handle logout"""
        self.controller.show_page("LoginPage")
    
    def show(self):
        """Show the map page and start updates"""
        super().show()
        self.after(100, self.draw_gis_map)
        self.update_tactical_display()
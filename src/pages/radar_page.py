import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import math
import time
import csv
import os
from datetime import datetime
from src.pages.base_page import BasePage
from src.utils.data_manager import DataManager

class RadarPage(BasePage):
    """Military-grade radar visualization page for gunshot detection"""
    
    def __init__(self, parent, controller):
        self.data_manager = DataManager()
        self.radar_points = []
        self.animation_id = None
        self.danger_detected = False
        self.blink_state = False
        super().__init__(parent, controller)
    
    def setup_ui(self):
        """Setup the military radar interface"""
        # Configure main grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=0)  # Node info
        self.grid_rowconfigure(2, weight=1)  # Main content
        self.grid_rowconfigure(3, weight=0)  # Footer
        
        # Header with title and danger indicator
        self.create_header()
        
        # Node coordinates and time
        self.create_node_info()
        
        # Main content area
        self.create_main_content()
        
        # Footer with CSV download
        self.create_footer()
        
        # Start blinking animation
        self.start_danger_blink()
    
    def create_header(self):
        """Create header with title and danger indicator"""
        header_frame = tk.Frame(self, bg=self.config.PRIMARY_COLOR, height=80)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Navigation buttons (left)
        nav_frame = tk.Frame(header_frame, bg=self.config.PRIMARY_COLOR)
        nav_frame.grid(row=0, column=0, sticky="w")
        
        map_btn = tk.Button(
            nav_frame,
            text="MAP VIEW",
            command=lambda: self.controller.show_page("MapPage"),
            font=(self.config.FONT_FAMILY, 10, "bold"),
            bg=self.config.ACCENT_COLOR,
            fg=self.config.TEXT_COLOR,
            relief="raised",
            bd=2,
            padx=15,
            pady=8
        )
        map_btn.pack(side="left", padx=5)
        
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
            text="RADAR",
            font=(self.config.FONT_FAMILY, 36, "bold"),
            bg=self.config.PRIMARY_COLOR,
            fg=self.config.GOLD_COLOR
        )
        title.grid(row=0, column=1)
        
        # Danger indicator (right)
        danger_frame = tk.Frame(header_frame, bg=self.config.PRIMARY_COLOR)
        danger_frame.grid(row=0, column=2, sticky="e", padx=20)
        
        tk.Label(
            danger_frame,
            text="THREAT STATUS",
            font=(self.config.FONT_FAMILY, 8, "bold"),
            bg=self.config.PRIMARY_COLOR,
            fg=self.config.TEXT_COLOR
        ).pack()
        
        self.danger_indicator = tk.Label(
            danger_frame,
            text="●",
            font=(self.config.FONT_FAMILY, 40, "bold"),
            bg=self.config.PRIMARY_COLOR,
            fg=self.config.SUCCESS_COLOR
        )
        self.danger_indicator.pack()
        
        # Toggle button for testing
        toggle_btn = tk.Button(
            danger_frame,
            text="TOGGLE",
            command=self.toggle_danger,
            font=(self.config.FONT_FAMILY, 8),
            bg=self.config.SECONDARY_COLOR,
            fg=self.config.TEXT_COLOR,
            relief="flat",
            padx=10,
            pady=2
        )
        toggle_btn.pack(pady=5)
    
    def create_node_info(self):
        """Create node coordinates and current time display"""
        info_frame = tk.Frame(self, bg=self.config.SECONDARY_COLOR, height=60)
        info_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        info_frame.grid_propagate(False)
        info_frame.grid_columnconfigure(0, weight=1)
        
        # Node coordinates
        coords_text = "NODE COORDINATES: 28.6139° N, 77.2090° E"
        coords_label = tk.Label(
            info_frame,
            text=coords_text,
            font=(self.config.FONT_FAMILY, 12, "bold"),
            bg=self.config.SECONDARY_COLOR,
            fg=self.config.TEXT_COLOR
        )
        coords_label.grid(row=0, column=0, sticky="w", padx=20, pady=5)
        
        # Current time
        self.time_label = tk.Label(
            info_frame,
            text="",
            font=(self.config.FONT_FAMILY, 12, "bold"),
            bg=self.config.SECONDARY_COLOR,
            fg=self.config.GOLD_COLOR
        )
        self.time_label.grid(row=1, column=0, sticky="w", padx=20, pady=5)
        
        # Update time
        self.update_time()
    
    def create_main_content(self):
        """Create main content area with radar and enemy coordinates"""
        content_frame = tk.Frame(self, bg=self.config.PRIMARY_COLOR)
        content_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Enemy coordinates box (left)
        self.create_enemy_coords_box(content_frame)
        
        # Radar display (right)
        self.setup_radar_canvas(content_frame)
    
    def create_enemy_coords_box(self, parent):
        """Create enemy coordinates display box"""
        coords_frame = tk.Frame(parent, bg=self.config.SECONDARY_COLOR, 
                               relief="raised", bd=3)
        coords_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        coords_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title = tk.Label(
            coords_frame,
            text="ENEMY COORDINATES",
            font=(self.config.FONT_FAMILY, 16, "bold"),
            bg=self.config.SECONDARY_COLOR,
            fg=self.config.ERROR_COLOR
        )
        title.pack(pady=20)
        
        # Coordinates data
        data_frame = tk.Frame(coords_frame, bg=self.config.SECONDARY_COLOR)
        data_frame.pack(expand=True, fill="both", padx=30, pady=20)
        
        # Create coordinate fields
        self.coord_fields = {}
        
        fields = [
            ("LATITUDE:", "28.6145° N"),
            ("LONGITUDE:", "77.2095° E"),
            ("RANGE:", "1,247 m"),
            ("ANGLE:", "045°"),
            ("ELEVATION:", "+12.5°")
        ]
        
        for i, (label, value) in enumerate(fields):
            # Label
            lbl = tk.Label(
                data_frame,
                text=label,
                font=(self.config.FONT_FAMILY, 12, "bold"),
                bg=self.config.SECONDARY_COLOR,
                fg=self.config.TEXT_COLOR,
                anchor="w"
            )
            lbl.grid(row=i, column=0, sticky="w", pady=8)
            
            # Value
            val = tk.Label(
                data_frame,
                text=value,
                font=(self.config.FONT_FAMILY, 14, "bold"),
                bg=self.config.SECONDARY_COLOR,
                fg=self.config.WARNING_COLOR,
                anchor="e"
            )
            val.grid(row=i, column=1, sticky="e", padx=(20, 0), pady=8)
            
            self.coord_fields[label] = val
        
        data_frame.grid_columnconfigure(1, weight=1)
        
        # Status indicator
        status_frame = tk.Frame(coords_frame, bg=self.config.BORDER_COLOR, height=40)
        status_frame.pack(fill="x", side="bottom")
        status_frame.pack_propagate(False)
        
        tk.Label(
            status_frame,
            text="⚠ LIVE TRACKING ACTIVE ⚠",
            font=(self.config.FONT_FAMILY, 10, "bold"),
            bg=self.config.BORDER_COLOR,
            fg=self.config.WARNING_COLOR
        ).pack(expand=True)
    
    def create_footer(self):
        """Create footer with CSV download option"""
        footer_frame = tk.Frame(self, bg=self.config.PRIMARY_COLOR, height=50)
        footer_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        footer_frame.grid_propagate(False)
        footer_frame.grid_columnconfigure(0, weight=1)
        
        # CSV download text and button
        csv_frame = tk.Frame(footer_frame, bg=self.config.PRIMARY_COLOR)
        csv_frame.pack(expand=True)
        
        csv_text = tk.Label(
            csv_frame,
            text="For detailed logs check ",
            font=(self.config.FONT_FAMILY, 12),
            bg=self.config.PRIMARY_COLOR,
            fg=self.config.TEXT_COLOR
        )
        csv_text.pack(side="left")
        
        csv_btn = tk.Button(
            csv_frame,
            text="CSV",
            command=self.download_csv,
            font=(self.config.FONT_FAMILY, 12, "bold", "underline"),
            bg=self.config.PRIMARY_COLOR,
            fg=self.config.ACCENT_COLOR,
            relief="flat",
            cursor="hand2",
            padx=5
        )
        csv_btn.pack(side="left")
    
    def toggle_danger(self):
        """Toggle danger detection status"""
        self.danger_detected = not self.danger_detected
        print(f"Danger status toggled: {self.danger_detected}")
    
    def start_danger_blink(self):
        """Start the danger indicator blinking animation"""
        if self.danger_detected:
            # Blink red when danger detected
            color = self.config.ERROR_COLOR if self.blink_state else self.config.PRIMARY_COLOR
            self.danger_indicator.configure(fg=color)
            self.blink_state = not self.blink_state
            self.after(500, self.start_danger_blink)  # Blink every 500ms
        else:
            # Solid green when no danger
            self.danger_indicator.configure(fg=self.config.SUCCESS_COLOR)
            self.after(1000, self.start_danger_blink)  # Check every 1000ms
    
    def update_time(self):
        """Update the current time display"""
        current_time = datetime.now().strftime("CURRENT TIME: %d %b %Y • %H:%M:%S IST")
        self.time_label.configure(text=current_time)
        self.after(1000, self.update_time)  # Update every second
    
    def download_csv(self):
        """Generate and download dummy CSV file"""
        try:
            # Generate dummy data
            csv_data = self.generate_dummy_csv_data()
            
            # Ask user where to save
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save Detection Log",
                initialname=f"gilda_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            
            if filename:
                # Write CSV file
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows(csv_data)
                
                messagebox.showinfo("Success", f"Detection log saved to:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save CSV file:\n{str(e)}")
    
    def generate_dummy_csv_data(self):
        """Generate dummy CSV data for download"""
        headers = ["Timestamp", "Gunshot Fired", "Enemy Latitude", "Enemy Longitude", 
                  "Range (m)", "Angle (°)", "Elevation (°)", "Confidence"]
        
        data = [headers]
        
        # Generate 50 dummy records
        import random
        base_time = datetime.now()
        
        for i in range(50):
            # Random time in last 24 hours
            time_offset = random.randint(0, 86400)
            record_time = base_time.timestamp() - time_offset
            timestamp = datetime.fromtimestamp(record_time).strftime("%Y-%m-%d %H:%M:%S")
            
            # Random detection data
            gunshot_fired = random.choice(["YES", "NO", "NO", "NO"])  # 25% chance of gunshot
            lat = 28.6139 + random.uniform(-0.01, 0.01)
            lon = 77.2090 + random.uniform(-0.01, 0.01)
            range_m = random.randint(500, 2000)
            angle = random.randint(0, 359)
            elevation = random.uniform(-10, 30)
            confidence = random.uniform(0.7, 0.99)
            
            row = [
                timestamp,
                gunshot_fired,
                f"{lat:.6f}° N",
                f"{lon:.6f}° E",
                range_m,
                angle,
                f"{elevation:.1f}",
                f"{confidence:.2f}"
            ]
            
            data.append(row)
        
        return data
    
    def setup_radar_canvas(self, parent):
        """Setup the radar visualization canvas"""
        radar_frame = tk.Frame(parent, bg=self.config.SECONDARY_COLOR, relief="raised", bd=3)
        radar_frame.grid(row=0, column=1, sticky="nsew")
        radar_frame.grid_rowconfigure(1, weight=1)
        radar_frame.grid_columnconfigure(0, weight=1)
        
        # Radar title
        radar_title = tk.Label(
            radar_frame,
            text="TACTICAL DISPLAY",
            font=(self.config.FONT_FAMILY, 14, "bold"),
            bg=self.config.SECONDARY_COLOR,
            fg=self.config.GOLD_COLOR
        )
        radar_title.grid(row=0, column=0, pady=10)
        
        self.radar_canvas = tk.Canvas(
            radar_frame,
            bg=self.config.PRIMARY_COLOR,
            highlightthickness=0
        )
        self.radar_canvas.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        
        # Bind canvas resize
        self.radar_canvas.bind('<Configure>', self.on_canvas_resize)
    

    
    def on_canvas_resize(self, event):
        """Handle canvas resize event"""
        self.draw_radar()
    
    def draw_radar(self):
        """Draw the radar display"""
        self.radar_canvas.delete("all")
        
        # Get canvas dimensions
        width = self.radar_canvas.winfo_width()
        height = self.radar_canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        # Calculate center and radius
        center_x = width // 2
        center_y = height // 2
        max_radius = min(center_x, center_y) - 20
        
        # Draw radar circles
        for i in range(1, 4):
            radius = (max_radius * i) // 3
            self.radar_canvas.create_oval(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                outline=self.config.ACCENT_COLOR,
                width=1
            )
        
        # Draw radar lines
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            end_x = center_x + max_radius * math.cos(rad)
            end_y = center_y + max_radius * math.sin(rad)
            
            self.radar_canvas.create_line(
                center_x, center_y, end_x, end_y,
                fill=self.config.ACCENT_COLOR,
                width=1
            )
        
        # Draw detection points
        for point in self.radar_points:
            self.draw_detection_point(point, center_x, center_y, max_radius)
    
    def draw_detection_point(self, point, center_x, center_y, max_radius):
        """Draw a detection point on the radar"""
        # Convert polar coordinates to cartesian
        angle_rad = math.radians(point['angle'])
        distance_ratio = point['distance'] / 100.0  # Normalize to 0-1
        
        x = center_x + (distance_ratio * max_radius * math.cos(angle_rad))
        y = center_y + (distance_ratio * max_radius * math.sin(angle_rad))
        
        # Draw point with intensity-based color
        intensity = point.get('intensity', 0.5)
        if intensity > 0.8:
            color = self.config.ERROR_COLOR
        elif intensity > 0.5:
            color = self.config.WARNING_COLOR
        else:
            color = self.config.SUCCESS_COLOR
        
        self.radar_canvas.create_oval(
            x - 5, y - 5, x + 5, y + 5,
            fill=color,
            outline=self.config.TEXT_COLOR,
            width=1
        )
    
    def handle_logout(self):
        """Handle logout"""
        self.stop_radar_updates()
        self.controller.show_page("LoginPage")
    
    def show(self):
        """Show the radar page and start updates"""
        super().show()
        self.start_radar_updates()
        self.after(100, self.draw_radar)  # Initial draw
    
    def hide(self):
        """Hide the radar page and stop updates"""
        super().hide()
        self.stop_radar_updates()
    
    def start_radar_updates(self):
        """Start radar data updates"""
        self.update_radar_data()
    
    def stop_radar_updates(self):
        """Stop radar data updates"""
        if self.animation_id:
            self.after_cancel(self.animation_id)
            self.animation_id = None
    
    def update_radar_data(self):
        """Update radar data and enemy coordinates"""
        # Get new detection data
        new_detections = self.data_manager.get_recent_detections()
        
        # Update radar points
        self.radar_points = new_detections
        
        # Update enemy coordinates with random data
        self.update_enemy_coordinates()
        
        # Redraw radar
        self.draw_radar()
        
        # Schedule next update
        self.animation_id = self.after(self.config.MAP_UPDATE_INTERVAL, self.update_radar_data)
    
    def update_enemy_coordinates(self):
        """Update enemy coordinates with live data"""
        import random
        
        # Generate realistic coordinates near Delhi
        base_lat = 28.6139
        base_lon = 77.2090
        
        lat = base_lat + random.uniform(-0.01, 0.01)
        lon = base_lon + random.uniform(-0.01, 0.01)
        range_m = random.randint(800, 2500)
        angle = random.randint(0, 359)
        elevation = random.uniform(-5, 25)
        
        # Update coordinate fields
        if hasattr(self, 'coord_fields'):
            self.coord_fields["LATITUDE:"].config(text=f"{lat:.4f}° N")
            self.coord_fields["LONGITUDE:"].config(text=f"{lon:.4f}° E")
            self.coord_fields["RANGE:"].config(text=f"{range_m:,} m")
            self.coord_fields["ANGLE:"].config(text=f"{angle:03d}°")
            self.coord_fields["ELEVATION:"].config(text=f"{elevation:+.1f}°")
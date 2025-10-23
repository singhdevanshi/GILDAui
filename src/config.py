# Configuration settings for GILDAui
import os

class Config:
    # Display settings for LCD screen
    WINDOW_WIDTH = 1024
    WINDOW_HEIGHT = 600
    FULLSCREEN = True
    
    # Application settings
    APP_TITLE = "GILDA - Gunshot Detection System"
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Authentication settings
    SESSION_TIMEOUT = 3600  # 1 hour in seconds
    
    # Data settings
    MAX_RADAR_POINTS = 100
    MAP_UPDATE_INTERVAL = 1000  # milliseconds
    
    # Colors and styling - Indian Army Theme
    PRIMARY_COLOR = "#1B2F1B"      # Dark Army Green
    SECONDARY_COLOR = "#2D4A2D"    # Medium Army Green
    ACCENT_COLOR = "#4A7C59"       # Lighter Army Green
    SUCCESS_COLOR = "#6B8E23"      # Olive Drab
    WARNING_COLOR = "#DAA520"      # Goldenrod
    ERROR_COLOR = "#8B0000"        # Dark Red
    TEXT_COLOR = "#F5F5DC"         # Beige/Cream
    GOLD_COLOR = "#FFD700"         # Gold for accents
    BORDER_COLOR = "#556B2F"       # Dark Olive Green
    
    # Font settings
    FONT_FAMILY = "Arial"
    FONT_SIZE_SMALL = 10
    FONT_SIZE_MEDIUM = 12
    FONT_SIZE_LARGE = 16
    FONT_SIZE_TITLE = 20
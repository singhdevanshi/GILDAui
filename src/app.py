import tkinter as tk
from src.config import Config
from src.pages.login_page import LoginPage
from src.pages.radar_page import RadarPage
from src.pages.map_page import MapPage
from src.utils.auth import AuthManager

class GILDAApp:
    """Main application class for GILDA gunshot detection system"""
    
    def __init__(self):
        self.config = Config()
        self.auth_manager = AuthManager()
        
        # Create main window
        self.root = tk.Tk()
        self.setup_window()
        
        # Initialize pages
        self.pages = {}
        self.current_page = None
        
        self.create_pages()
        self.show_page("LoginPage")
    
    def setup_window(self):
        """Setup the main application window"""
        self.root.title(self.config.APP_TITLE)
        self.root.geometry(f"{self.config.WINDOW_WIDTH}x{self.config.WINDOW_HEIGHT}")
        self.root.configure(bg=self.config.PRIMARY_COLOR)
        
        # Configure for fullscreen if specified
        if self.config.FULLSCREEN:
            self.root.attributes('-fullscreen', True)
            # Bind Escape key to exit fullscreen (for development)
            self.root.bind('<Escape>', self.toggle_fullscreen)
        
        # Configure window properties for Raspberry Pi LCD
        self.root.resizable(True, True)
        
        # Configure grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_pages(self):
        """Create all application pages"""
        # Create container frame for pages
        self.container = tk.Frame(self.root, bg=self.config.PRIMARY_COLOR)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Create pages
        page_classes = {
            "LoginPage": LoginPage,
            "RadarPage": RadarPage,
            "MapPage": MapPage
        }
        
        for page_name, page_class in page_classes.items():
            page = page_class(self.container, self)
            page.grid(row=0, column=0, sticky="nsew")
            self.pages[page_name] = page
    
    def show_page(self, page_name):
        """Show the specified page"""
        if page_name in self.pages:
            # Hide current page
            if self.current_page:
                self.pages[self.current_page].hide()
            
            # Show new page
            page = self.pages[page_name]
            page.show()
            self.current_page = page_name
            
            # Update window title
            titles = {
                "LoginPage": f"{self.config.APP_TITLE} - Login",
                "RadarPage": f"{self.config.APP_TITLE} - Radar View",
                "MapPage": f"{self.config.APP_TITLE} - Map View"
            }
            self.root.title(titles.get(page_name, self.config.APP_TITLE))
    
    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode"""
        current_state = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current_state)
    
    def on_closing(self):
        """Handle application closing"""
        # Save any pending data
        try:
            # Perform cleanup
            self.auth_manager.logout()
            
            # Stop any running updates
            for page in self.pages.values():
                if hasattr(page, 'stop_radar_updates'):
                    page.stop_radar_updates()
            
        except Exception as e:
            print(f"Error during cleanup: {e}")
        
        # Close application
        self.root.destroy()
    
    def run(self):
        """Start the application main loop"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Application interrupted by user")
        except Exception as e:
            print(f"Application error: {e}")
        finally:
            self.on_closing()
    
    def get_auth_manager(self):
        """Get the authentication manager"""
        return self.auth_manager
    
    def restart_application(self):
        """Restart the application"""
        self.root.quit()
        # In a real implementation, you might want to restart the process
#!/usr/bin/env python3
"""
GILDA - Gunshot Detection System Frontend
Main entry point for the application
"""

import sys
import os
import logging
from datetime import datetime

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.app import GILDAApp
from src.config import Config

def setup_logging():
    """Setup logging configuration"""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_filename = os.path.join(log_dir, f"gilda_{datetime.now().strftime('%Y%m%d')}.log")
    
    logging.basicConfig(
        level=logging.INFO if not Config.DEBUG else logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """Main application entry point"""
    try:
        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)
        
        logger.info("Starting GILDA Gunshot Detection System")
        logger.info(f"Python version: {sys.version}")
        logger.info(f"Platform: {sys.platform}")
        
        # Create and run application
        app = GILDAApp()
        
        logger.info("Application initialized successfully")
        logger.info("Starting main application loop")
        
        app.run()
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please ensure all required dependencies are installed.")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        print(f"Fatal error: {e}")
        logging.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
    
    finally:
        logging.info("Application shutdown complete")

if __name__ == "__main__":
    main()
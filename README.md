# GILDAui - Gunshot Detection System Frontend

A Python-based GUI application for gunshot detection systems, designed for Raspberry Pi with LCD displays.

## Features

- **Login System**: Secure authentication with multiple user levels
- **Radar View**: Real-time visualization of gunshot detections
- **Map View**: Geographic display of detection locations with filtering
- **Touch-Friendly Interface**: Optimized for LCD touchscreen displays
- **Raspberry Pi Optimized**: Lightweight and efficient for embedded systems

## Quick Start

### Prerequisites
- Python 3.7 or higher
- Tkinter (included with most Python installations)
- Raspberry Pi with LCD display (recommended)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd GILDAui
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python src/main.py
```

### Default Login Credentials
- **Admin**: username: `admin`, password: `admin123`
- **Operator**: username: `operator`, password: `operator123`
- **Guest**: username: `guest`, password: `guest123`

## Project Structure

```
GILDAui/
├── src/
│   ├── main.py              # Application entry point
│   ├── app.py               # Main application class
│   ├── config.py            # Configuration settings
│   ├── pages/               # UI pages
│   │   ├── login_page.py    # Login interface
│   │   ├── radar_page.py    # Radar visualization
│   │   └── map_page.py      # Map display
│   ├── components/          # Reusable UI components
│   ├── utils/               # Utility modules
│   └── assets/              # Images and styles
├── tests/                   # Test files
├── requirements.txt         # Python dependencies
└── setup.py                # Package setup
```

## Configuration

Edit `src/config.py` to customize:
- Display resolution and fullscreen settings
- Color scheme and fonts
- Authentication timeouts
- Data update intervals

## Development

### Running in Development Mode
```bash
# Enable debug mode
export DEBUG=true
python src/main.py
```

### Key Features for Customization
- **Modular Design**: Easy to add new pages or modify existing ones
- **Configuration-Driven**: Most settings in `config.py`
- **Mock Data**: Built-in sample data for testing without real sensors
- **Extensible**: Ready for integration with real gunshot detection hardware

## Raspberry Pi Deployment

### Auto-Start Setup
1. Create a desktop entry:
```bash
sudo nano /etc/xdg/autostart/gilda.desktop
```

2. Add content:
```ini
[Desktop Entry]
Type=Application
Name=GILDA UI
Exec=python3 /path/to/GILDAui/src/main.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
```

### Kiosk Mode
For full kiosk mode, set `FULLSCREEN = True` in `config.py` and configure your Raspberry Pi to auto-login and start X11.

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions, please create an issue in the repository.
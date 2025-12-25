Minimalist E-Paper Weather Station

A clean, high-contrast digital weather dashboard built for the **Raspberry Pi Zero v1.1** and the **Waveshare 2.13" E-Paper HAT+**. 
This project focuses on readable and glanceable data.

## Features
- Includes Date, highs and lows, current temperature, percipitation % and humidity %
- Uses the Erik Flowers Weather Icon font to map OpenWeatherMap IDs to clean graphics.
- Runs as a `systemd` service that starts on boot and handles network/API errors gracefully.

## Hardware Used
- **Raspberry Pi Zero** (v1.1)
- **Waveshare 2.13" E-Paper HAT+** (250x122 resolution)
- **MicroSD Card** with Raspberry Pi OS (Lite recommended)

## Setup & Installation

### 1. Enable Hardware Interfaces
The e-paper display uses SPI. Enable it via the configuration tool:

```
sudo raspi-config
Interface Options -> SPI -> Yes
```

### 2. Clone the repository and set up your Python environment:
```
git clone [https://github.com/jerem234/epaper-weather-display.git](https://github.com/jerem234/epaper-weather-display.git)
cd epaper-weather-display
python3 -m venv venv
source venv/bin/activate
pip install RPi.GPIO spidev Pillow requests python-dotenv
```
### 3. Drivers & Fonts
Ensure the waveshare_epd driver library is in the root folder. You will also need the following font files in the project root:  
```font.ttf```: For numeric and text data.  
```weathericons.ttf```: For weather condition graphics.  

### 4. Environment Variables
Create a .env file in the root directory and fill in your openweather api key and city/state.
Look at .env.example for reference. Make sure the actual file is named ```.env```

This script is designed to run as a background service.
1. Create the service file: ```sudo nano /etc/systemd/system/weather.service```
2. Configure it to use your virtual environment's Python path: ```ExecStart=/home/<USER>/weather_display/venv/bin/python3 weather.py```
3. Enable and start:
```
sudo systemctl daemon-reload
sudo systemctl enable weather.service
sudo systemctl start weather.service
```

## Acknowledgments
[OpenWeatherMap API](https://openweathermap.org/api) for the data.
[Waveshare](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT+) for the display drivers.
[Erik Flowers](https://github.com/erikflowers/weather-icons) for the weather icon font.

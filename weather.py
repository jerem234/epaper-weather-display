import os
import sys
import time
import requests
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd2in13_V4

# --- CONFIGURATION ---
API_KEY = "d89325250240d68432bb9a74e884f925"
CITY = "Nashville,TN,US"
UNITS = "imperial" 

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
FONT_FILE = os.path.join(SCRIPT_DIR, "font.ttf")
ICON_FILE = os.path.join(SCRIPT_DIR, "weathericons.ttf")

def get_weather():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units={UNITS}"
        res = requests.get(url, timeout=15)
        data = res.json()
        
        # OpenWeather returns 'cod' as 200 for success
        if data.get("cod") != 200:
            return {"error": True, "message": data.get("message", "Unknown Error")}

        return {
            "error": False,
            "temp": int(data['main']['temp']),
	    "temp_max": int(data['main']['temp_max']),
    	    "temp_min": int(data['main']['temp_min']),
            "id": data['weather'][0]['id'],
            "humidity": data['main']['humidity'],
            "rain": data.get('rain', {}).get('1h', 0),
            "snow": data.get('snow', {}).get('1h', 0)
        }
    except Exception as e:
        return {"error": True, "message": "Connection Failed"}

def draw_error(epd, message):
    """Simple screen to show when something goes wrong"""
    canvas = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(canvas)
    font_small = ImageFont.truetype(FONT_FILE, 16)
    
    draw.rectangle((0, 0, 250, 30), fill=0)
    draw.text((10, 5), "SYSTEM ERROR", font=font_small, fill=255)
    
    # Center the error message
    draw.text((10, 50), f"Status: {message.upper()}", font=font_small, fill=0)
    draw.text((10, 80), "Retrying in 15 mins...", font=font_small, fill=0)
    return canvas

def draw_screen(epd, data):
    """The minimalist dashboard for successful data"""
    canvas = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(canvas)
    
    font_city = ImageFont.truetype(FONT_FILE, 13)
    font_temp = ImageFont.truetype(FONT_FILE, 75) # Extra large minimalist temp
    font_small = ImageFont.truetype(FONT_FILE, 14)
    font_icon = ImageFont.truetype(ICON_FILE, 65)

# Header
    draw.text((10, 5), time.strftime("%b %d, %Y"), font=font_city, fill=0)
    # High/Low on the right
    	# Format: H: 75 L: 45
    hi_lo_text = f"H: {data['temp_max']}° L: {data['temp_min']}°"
    
    draw.text((10, 20), hi_lo_text, font=font_city, fill=0)
    # Big Temp
    draw.text((10, 30), f"{data['temp']}°", font=font_temp, fill=0)
# 3. Weather Icon (Right Side)
    # Mapping OWM IDs to WeatherIcon characters
    icon_map = {
        800: "\uf00d", # Clear/Sun
        801: "\uf002", # Clouds
        802: "\uf002",
        803: "\uf013", # Overcast
        804: "\uf013",
        500: "\uf019", # Rain
        600: "\uf01b", # Snow
    }
    
    # Find icon based on ID, default to a '?' icon (\uf03e) if not found
    icon_char = icon_map.get(data['id'], "\uf03e")
    
    # Position: X=165 (far right area), Y=35 (aligned with temp)
    draw.text((165, 30), icon_char, font=font_icon, fill=0)
    # Precipitation Text
    precip = "0%"
    if data['rain'] > 0 or data['snow'] > 0:
        precip = f"{data['rain'] or data['snow']}mm/h"
    
    draw.line((10, 105, 240, 105), fill=0, width=1)
    draw.text((10, 108), f"PRECIP: {precip}", font=font_small, fill=0)
    draw.text((125, 108), f"HUMIDITY: {data['humidity']}%", font=font_small, fill=0)

    return canvas

def main():
    try:
        epd = epd2in13_V4.EPD()
        while True:
            print("Contacting OpenWeather...")
            data = get_weather()
            
            epd.init()
            if data["error"]:
                print(f"Error encountered: {data['message']}")
                image = draw_error(epd, data["message"])
            else:
                print("Success! Rendering weather...")
                image = draw_screen(epd, data)
                
            epd.display(epd.getbuffer(image))
            epd.sleep()
            
            # Refresh every 15 minutes
            print(id)
            time.sleep(900)
    except KeyboardInterrupt:
        epd.init()
        epd.Clear()
        epd.sleep()

if __name__ == "__main__":
    main()

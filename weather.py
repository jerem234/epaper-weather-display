import os
import sys
import time
import requests
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd2in13_V4
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
API_KEY = os.getenv("API_KEY")
CITY = os.getenv("CITY")
UNITS = "imperial"

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
FONT_FILE = os.path.join(SCRIPT_DIR, "font.ttf")
ICON_FILE = os.path.join(SCRIPT_DIR, "weathericons.ttf")

def get_weather_forecast():
    """Fetches 5-day/3-hour forecast and extracts 24h data"""
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units={UNITS}"
        res = requests.get(url, timeout=15)
        data = res.json()

        if str(data.get("cod")) != "200":
            return {"error": True, "message": data.get("message", "API Error")}

        # Get the next 24 hours (8 blocks of 3 hours)
        next_24h = data['list'][:8]

        # Extract current and forecast data
        return {
            "error": False,
            "temp": int(next_24h[0]['main']['temp']),
            "high": int(max(item['main']['temp_max'] for item in next_24h)),
            "low": int(min(item['main']['temp_min'] for item in next_24h)),
            "pop": int(max(item.get('pop', 0) for item in next_24h) * 100),
            "id": next_24h[0]['weather'][0]['id'],
            "humidity": next_24h[0]['main']['humidity'],
            "rain": next_24h[0].get('rain', {}).get('3h', 0),
            "snow": next_24h[0].get('snow', {}).get('3h', 0)
        }
    except Exception as e:
        print(f"Connection error: {e}")
        return {"error": True, "message": "Connection Failed"}

def draw_error(epd, message):
    canvas = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(canvas)
    font_small = ImageFont.truetype(FONT_FILE, 16)
    draw.rectangle((0, 0, 250, 30), fill=0)
    draw.text((10, 5), "SYSTEM ERROR", font=font_small, fill=255)
    draw.text((10, 50), f"Status: {str(message).upper()}", font=font_small, fill=0)
    draw.text((10, 80), "Retrying in 15 mins...", font=font_small, fill=0)
    return canvas

def draw_screen(epd, data):
    canvas = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(canvas)

    font_city = ImageFont.truetype(FONT_FILE, 13)
    font_temp = ImageFont.truetype(FONT_FILE, 75)
    font_small = ImageFont.truetype(FONT_FILE, 14)
    font_icon = ImageFont.truetype(ICON_FILE, 60)
    font_bottom = ImageFont.truetype(FONT_FILE, 12)
    # Header Bar
    draw.text((10, 5), time.strftime("%b %d, %Y"), font=font_city, fill=0)
    hi_lo_text = f"H: {data['high']}° L: {data['low']}°"
    draw.text((10, 20), hi_lo_text, font=font_city, fill=0)

    # Big Temp
    draw.text((10, 25), f"{data['temp']}°", font=font_temp, fill=0)

    # Weather Icon
    icon_map = {800: "\uf00d", 801: "\uf002", 802: "\uf002", 803: "\uf013", 804: "\uf013", 500: "\uf019", 600: "\uf01b"}
    icon_char = icon_map.get(data['id'], "\uf03e")
    draw.text((165, 15), icon_char, font=font_icon, fill=0)

    # Bottom Stats
    draw.line((10, 105, 240, 105), fill=0, width=1)
    
    # Safe check for current rain volume vs forecast chance
    if data['rain'] > 0:
        precip_str = f"RAIN: {data['rain']}mm"
    else:
        precip_str = f"CHANCE: {data['pop']}%"
        
    draw.text((10, 108), precip_str, font=font_bottom, fill=0)
    draw.text((125, 108), f"HUMIDITY: {data['humidity']}%", font=font_bottom, fill=0)

    return canvas

def main():
    try:
        epd = epd2in13_V4.EPD()
        while True:
            print("Contacting OpenWeather...")
            data = get_weather_forecast()
            epd.init()
            if data["error"]:
                print(f"Error: {data['message']}")
                image = draw_error(epd, data["message"])
            else:
                print("Success! Rendering...")
                image = draw_screen(epd, data)

            epd.display(epd.getbuffer(image))
            epd.sleep()
            time.sleep(900)
    except KeyboardInterrupt:
        epd.init()
        epd.Clear()
        epd.sleep()

if __name__ == "__main__":
    main()

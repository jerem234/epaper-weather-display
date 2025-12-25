import os
import sys
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd2in13_V4  # Change to V3 or V2 if needed

def main():
    try:
        # 1. Initialize the display
        epd = epd2in13_V4.EPD()
        epd.init()
        epd.Clear()

        # 2. Create the canvas (Landscape mode)
        # The 2.13" is naturally 122x250, so we swap for landscape
        image = Image.new('1', (epd.height, epd.width), 255) 
        draw = ImageDraw.Draw(image)

        # 3. Draw a "Weather-style" layout
        draw.text((10, 10), "PI ZERO WEATHER", fill=0)
        draw.line((10, 30, 240, 30), fill=0, width=2)
        
        # Draw a big fake temperature
        draw.text((80, 50), "22*C", fill=0) 
        draw.text((10, 100), "Status: Practicing...", fill=0)

        # 4. Display it
        # epd.getbuffer(image) converts the Pillow image to hardware data
        epd.display(epd.getbuffer(image))

        # 5. Power down the screen
        epd.sleep()
        print("Success! Check your screen.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

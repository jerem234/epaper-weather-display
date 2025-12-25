from PIL import Image, ImageDraw, ImageFont

# 1. Create the canvas
# '1' means 1-bit color (black and white)
# (250, 122) is the resolution of your 2.13" HAT
canvas = Image.new('1', (250, 122), 255) # 255 is White
draw = ImageDraw.Draw(canvas)

# 2. Draw some shapes
# draw.rectangle([start_x, start_y, end_x, end_y], outline=0, fill=0)
draw.rectangle([5, 5, 245, 117], outline=0) # A thin border
draw.ellipse([190, 20, 230, 60], outline=0, fill=0) # A "Sun" circle

# 3. Add some text
# Note: For custom fonts, you'd load a .ttc or .ttf file
draw.text((20, 40), "Hello Pi!", fill=0)
draw.text((20, 70), "Weather: Sunny", fill=0)

# 4. Save it to view it
canvas.save("test_display.bmp")
print("Image saved as test_display.bmp")

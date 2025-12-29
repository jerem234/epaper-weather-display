import os
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd2in13_V4
import requests

epd = epd2in13_V4.EPD()

epd.init()
epd.Clear()


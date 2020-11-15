import time
from random import sample
from flask import Flask
from flask import request
from rpi_ws281x import PixelStrip, Color, ws
from utils.utils import color_wipe_rain
from ConfigParser import SafeConfigParser

app = Flask(__name__)

config = SafeConfigParser()
config.read('settings.conf')

# Create NeoPixel object with appropriate configuration.
strip = PixelStrip(
config.getint('ledstrip', 'LED_COUNT'),
config.getint('ledstrip', 'LED_PIN'),
config.getint('ledstrip', 'LED_FREQ_HZ'),
config.getint('ledstrip', 'LED_DMA'),
config.getboolean('ledstrip', 'LED_INVERT'),
config.getint('ledstrip', 'LED_BRIGHTNESS'),
config.getint('ledstrip', 'LED_CHANNEL'),
ws.WS2811_STRIP_RGB)

# Intialize the library (must be called once before other functions).
strip.begin()

# List of colors used by the pixels (GRB)
predefined_colors = {
'ssh': Color(0,0,255), # BLUE
'ssh-success': Color(0,255,0), # RED
'rdp': Color(20,255,147), # PINK
'smbd': Color(255,0,0), # GREEN
'bitcoin': Color(128,128,0), # GOLD ISH
'smtp': Color(128,128,0), # PURPLE
'adb': Color(242,64,224), # WHITE/BLUE
'elasticsearch': Color(255,0,162) # TEAL?
}

# Initial random list of pixels
available_pixels = sample([x for x in range(0, strip.numPixels())], strip.numPixels())

@app.route('/', methods=['POST'])
def honey_tree():
    global available_pixels

    try:
        proto = request.form['protocol']  # Get message from Logstash
        if proto is not None:
            if proto in predefined_colors.keys():  # If proto key exist in dict
                # Remove whitespace front and back
                proto = proto.strip()
                # Get a random pixel
                if len(available_pixels) < 1:  # No available pixels left
                    # Wait before wiping all pixels
                    time.sleep(0.5)
                    # Wipe all pixels
                    color_wipe_rain(strip)
                    # Generate random pixels and shuffle again
                    available_pixels = sample([x for x in range(0, strip.numPixels())], strip.numPixels())
                # Pop new index from list
                _index = available_pixels.pop()
                # Set new color based on preset
                strip.setPixelColor(_index, predefined_colors[proto])
                strip.show()
    except Exception:  # If something happens, ignore it
        pass
    return 'OK'  # Return something so Flask don't complain

if __name__ == '__main__':
    app.run()

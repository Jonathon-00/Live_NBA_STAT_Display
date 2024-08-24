import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import os
import time

WIDTH = 128
HEIGHT = 64 
BORDER = 3

i2c = board.I2C()  # uses board.SCL and board.SDA
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

# Display set up
oled.fill(0)
oled.show()

cwd = os.getcwd()

abbreviations = {
    'Atlanta': 'ATL',
    'Boston': 'BOS',
    'Brooklyn': 'BRK',
    'Charlotte': 'CHO',
    'Chicago': 'CHI',
    'Cleveland': 'CLE',
    'Dallas': 'DAL',
    'Denver': 'DEN',
    'Detroit': 'DET',
    'Golden State': 'GSW',
    'Houston': 'HOU',
    'Indiana': 'IND',
    'LA Clippers': 'LAC',
    'LA Lakers': 'LAL',
    'Memphis': 'MEM',
    'Miami': 'MIA',
    'Milwaukee': 'MIL',
    'Minnesota': 'MIN',
    'New Orleans': 'NOP',
    'New York': 'NYK',
    'Oklahoma City': 'OKC',
    'Orlando': 'ORL',
    'Philadelphia': 'PHI',
    'Phoenix': 'PHO',
    'Portland': 'POR',
    'Sacramento': 'SAC',
    'San Antonio': 'SAS',
    'Toronto': 'TOR',
    'Utah': 'UTA',
    'Washington': 'WAS'
}

for key in abbreviations:
    # Create a new blank image
    image = Image.new('1', (WIDTH, HEIGHT))
    
    # Load the image
    image_path = os.path.join(cwd, "logos", f"{key}.jpg")
    imageClip = Image.open(image_path)
    imageSize = imageClip.size
    print(f"Original size: {imageSize}")

    # Resize the image
    scale = min(WIDTH / imageSize[0], HEIGHT / imageSize[1])
    newSize = (int(imageSize[0] * scale), int(imageSize[1] * scale))
    imageClip = imageClip.resize(newSize)
    imageSize = imageClip.size
    print(f"Resized to: {imageSize}")

    # Convert image to 1-bit color
    imageClip = imageClip.convert('1')

    # Calculate center position
    cX = (WIDTH - imageSize[0]) // 2
    cY = (HEIGHT - imageSize[1]) // 2
    image.paste(imageClip, (cX, cY))

    # Display image
    oled.image(image)
    oled.show()
    print(f"Displayed: {key}")
    time.sleep(10)

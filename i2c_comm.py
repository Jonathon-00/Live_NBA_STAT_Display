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

half_width = 58


for key in abbreviations:
    # Create a new blank image
    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    
    # Load the image
    image_path = os.path.join(cwd, "logos", f"{key}.jpg")
    imageClip = Image.open(image_path)
    imageSize = imageClip.size

    cX_left = 0
    cY_left = (HEIGHT - imageSize[1]) // 2
    image.paste(imageClip, (cX_left, cY_left))

    cX_right = WIDTH-imageSize[0]
    cY_right = cY_left
    image.paste(imageClip, (cX_right, cY_right))
    
    text = "vs"

    font = ImageFont.load_default()
    bbox = font.getbbox(text)
    (text_width, text_height) = bbox[2] - bbox[0], bbox[3] - bbox[1]
    textX = (WIDTH - text_width) // 2
    textY = (HEIGHT - text_height) // 2

    draw.text((textX, textY), text, font=font, fill=255)


    # Display image
    oled.image(image)
    oled.show()
    print(f"Displayed: {key}")
    time.sleep(4)

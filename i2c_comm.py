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

# display set up
oled.fill(0)
oled.show()
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Draw a white background
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

# Draw a smaller inner rectangle
draw.rectangle(
    (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
    outline=0,
    fill=0,
)

# Load default font.
font = ImageFont.load_default()

# Draw Some Text
# text = "Hello World!"
# bbox = font.getbbox(text)
# (font_width, font_height) = bbox[2] - bbox[0], bbox[3] - bbox[1]
# draw.text(
#     (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
#     text,
#     font=font,
#     fill=255,
# )

# oled.image(image)
 # oled.show()





cwd = os.getcwd()

abbreviations =     {
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
    print(key)
    image_path = cwd + "/logos/" + key + ".jpg"
    image = Image.open(image_path)
    imageSize = image.size
    image = image.convert('1')
    cX = 10
    cY = 10
    image.paste(image, (cX, cY, cX+imageSize[0], cY+imageSize[1]))
    
    #Display image
    oled.image(image)
    oled.show()
    time.sleep(20)







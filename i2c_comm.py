import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


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

image = Image.open("oklahoma-city-thunder-logo.jpg")

# Display image
oled.image(image)
oled.show()

from PIL import Image, ImageDraw, ImageFont
import smbus
from time import sleep

ssd1306 = 0x3C  # OLED SSD1306's I2C address
d_mode_i = 0x00
d_mode_w = 0x40
d_init = b'\xAE\xD5\x80\x8D\x14\x20\x00\xDA\x12\x81\x00\xD9\xF1\xDB\x40\xA4\xA6\xAF'
d_home = b'\x21\x00\x7F\x22\x00\x07'

disp_land = [\
    '  Hello! RasPi  ', '    OLED Lib    ',\
    '  for CPython   ', '                ',\
    'https://git.boku', 'nimo.com/oled/  ',\
    '                ', 'by Wataru KUNINO',\
]

def create_font_bitmap(text, font_size=16):
    # Create an image with a white background
    image = Image.new('1', (128, 8), 1)  # Adjust size based on your display
    draw = ImageDraw.Draw(image)
    
    # Load a TTF font and draw the text
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    draw.text((0, 0), text, font=font, fill=0)  # Draw the text in black
    
    # Return the bitmap data
    return image.tobytes()

def main():
    i2c = smbus.SMBus(1)
    i2c.write_i2c_block_data(ssd1306, d_mode_i, list(d_init)) 
    i2c.write_i2c_block_data(ssd1306, d_mode_i, list(d_home))
    
    # Loop through each line of text in disp_land
    for y, line in enumerate(disp_land):
        # Create the font bitmap for each line of text
        font_bitmap = create_font_bitmap(line, font_size=16)  # Adjust font_size as needed
        # Send the bitmap to the OLED display
        for i in range(0, len(font_bitmap), 16):  # Send data in chunks of 16 bytes
            i2c.write_i2c_block_data(ssd1306, d_mode_w, list(font_bitmap[i:i+16]))
    
    sleep(100)

while True:
    main()

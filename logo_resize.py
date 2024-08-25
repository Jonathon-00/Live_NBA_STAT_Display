from PIL import Image, ImageDraw, ImageFont
import os

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
HEIGHT = 64


for key in abbreviations:
    image_path = os.path.join(cwd, "logos", f"{key}.jpg")
    imageClip = Image.open(image_path)
    imageSize = imageClip.size
    print(f"Original size: {imageSize}")

    # Resize the image
    scale = min(half_width / imageSize[0], HEIGHT / imageSize[1])
    newSize = (int(imageSize[0] * scale), int(imageSize[1] * scale))
    imageClip = imageClip.resize(newSize)
    imageSize = imageClip.size
    print(f"Resized to: {imageSize}")

    # Convert image to 1-bit color
    imageClip = imageClip.convert('1')

    imageClip.save(image_path)
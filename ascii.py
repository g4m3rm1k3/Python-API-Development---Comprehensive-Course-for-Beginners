# Import the Image and ImageDraw modules from the Pillow library
from PIL import Image, ImageDraw

# Open the image file and convert it to grayscale
im = Image.open(
    'C:\\Users\\g4m3r\\OneDrive\\Pictures\\small.jpg').convert('L')

# Create a new image with a white background
ascii_im = Image.new('L', im.size, color=255)
draw = ImageDraw.Draw(ascii_im)

# Define a string of ASCII characters to use for the grayscale values
chars = '@B%8WM#*oahkbdpwmZO0QlJYXzcvnxrjft/\|()1{}[]-_+~<>i!lI;:,"^`\'. '

# Iterate over the pixels in the image and draw the corresponding ASCII character
for x in range(im.width):
    for y in range(im.height):
        # Get the grayscale value of the pixel
        pixel = im.getpixel((x, y))
        # Draw the corresponding ASCII character at the same position in the new image
        draw.text((x, y), chars[pixel * len(chars) // 256], fill=0)

# Save the new image
ascii_im.save('ascii_art.png')

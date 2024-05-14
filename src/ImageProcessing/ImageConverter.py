import math
import os
from PIL import Image, ImageDraw


class ImageConverter:
    def __init__(self):
        self.chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,^`'. "[::-1]
        self.charArray = list(self.chars)
        self.charLength = len(self.charArray)
        self.interval = self.charLength / 256

    def get_char(self, input_int):
        return self.charArray[math.floor(input_int * self.interval)]

    def rgb_to_ansi(self, r, g, b):
        return f"{r};{g};{b}"

    def generate_ascii_art(self, frame):
        im = Image.fromarray(frame)
        im = im.convert("RGB")
        width, height = im.size

        aspect_ratio = width / height
        cols, lines = os.get_terminal_size()
        new_width = cols
        new_height = lines - 3

        if new_height > lines:
            new_height = lines
            new_width = int(lines * aspect_ratio)

        im = im.resize((new_width, new_height), Image.NEAREST)

        width, height = im.size

        pix = im.load()

        output = []

        for i in range(height):
            for j in range(width):
                r, g, b = pix[j, i]
                color_code = self.rgb_to_ansi(r, g, b)
                char = self.get_char((r + g + b) / 3)
                output.append("\033[38;2;{}m{}".format(color_code, char))
            output.append("\033[0m")

        return ''.join(output)
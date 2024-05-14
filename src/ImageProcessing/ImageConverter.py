import math
import os
from PIL import Image, ImageDraw


class ImageConverter:
    def __init__(self):
        self.cols = None
        self.lines = None
        self.width = None
        self.height = None
        self.chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,^`'. "[::-1]
        self.charArray = list(self.chars)
        self.charLength = len(self.charArray)
        self.interval = self.charLength / 256


    def getChar(self, inputInt):
        return self.charArray[math.floor(inputInt * self.interval)]

    def rgb_to_ansi(self, r, g, b):
        return f"{r};{g};{b}"

    def generate_ascii_art(self, frame):
        im = Image.fromarray(frame)
        im = im.convert("RGB")
        width, height = im.size

        aspect_ratio = width / height
        self.cols, self.lines = os.get_terminal_size()
        new_width = self.cols
        new_height = self.lines

        if new_height > self.lines:
            new_height = self.lines
            new_width = int(self.lines * aspect_ratio)

        im = im.resize((new_width, new_height), Image.NEAREST)

        self.width, self.height = im.size

        pix = im.load()

        output_image = Image.new('RGB', (self.width, self.height))
        ImageDraw.Draw(output_image)

        strimg = ""

        for i in range(self.height):
            for j in range(self.width):
                r, g, b = pix[j, i]
                color_code = self.rgb_to_ansi(r, g, b)
                char = self.getChar((r + g + b) / 3)
                #\033[48;2;{}m
                strimg += "\033[38;2;{}m{}".format(color_code, char)

            strimg += "\033[0m"

        return strimg

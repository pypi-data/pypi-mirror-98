import math
import os
from enum import Enum

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops


class Point(object):
    def __init__(self, x, y):
        self.x, self.y = x, y

    @staticmethod
    def from_point(other):
        return Point(other.x, other.y)


class Rect(object):
    def __init__(self, x1, y1, x2, y2):
        minx, maxx = (x1,x2) if x1 < x2 else (x2,x1)
        miny, maxy = (y1,y2) if y1 < y2 else (y2,y1)
        self.min = Point(minx, miny)
        self.max = Point(maxx, maxy)

    @staticmethod
    def from_points(p1, p2):
        return Rect(p1.x, p1.y, p2.x, p2.y)

    def __str__(self):
        return 'Rect({:d}, {:d}, {:d}, {:d})'.format(self.min.x, self.min.y,
                                                     self.max.x, self.max.x)
    width = property(lambda self: self.max.x - self.min.x)
    height = property(lambda self: self.max.y - self.min.y)


class Position(Enum):
    center = "center"
    top = "top"
    bottom = "bottom"
    right = "right"
    left = "left"


class BackgroundType(Enum):
    plain = "plain"
    vertical_gradient = "vertical_gradient"
    horizontal_gradient = "horizontal_gradient"
    diagonal_gradient_right = "diagonal_gradient_right"
    diagonal_gradient_left = "diagonal_gradient_left"


class StoreSizeName(Enum):
    iphone_4 = "iphone_4"
    iphone_4_7 = "iphone_4_7"
    iphone_5_5 = "iphone_5_5"
    iphone_5_8 = "iphone_5_8"
    iphone_6_5 = "iphone_6_5"
    ipad = "ipad"
    android = "android"
    ipad_9_7 = "ipad_9_7"
    ipad_10_5 = "ipad_10_5"
    ipad_11 = "ipad_11"
    ipad_12_9 = "ipad_12_9"


STORES_SIZES = {
    StoreSizeName.iphone_4: {
        # iPhone 6, iPhone 6s, iPhone 7, iPhone 8
        "width": 640, "height": 1096,
    },
    StoreSizeName.iphone_4_7: {
        # iPhone 6, iPhone 6s, iPhone 7, iPhone 8
        "width": 750, "height": 1334,
    },
    StoreSizeName.iphone_5_5: {
        # iPhone 6s Plus, iPhone 7 Plus, iPhone 8 Plus
        # Required by apple store
        "width": 1242, "height": 2208,
    },
    StoreSizeName.iphone_5_8: {
        # iPhone 11 Pro, iPhone X, iPhone XS
        "width": 1125, "height": 2436,
    },
    StoreSizeName.iphone_6_5: {
        # iPhone 11 Pro Max, iPhone 11, iPhone XS Max, iPhone XR
        # Required by apple store
        "width": 1242, "height": 2688,
    },
    StoreSizeName.ipad_9_7: {
        # iPad, iPad mini
        "width": 1536, "height": 2008,
    },
    StoreSizeName.ipad_10_5: {
        # 7th generation iPad, iPad Pro, iPad Air
        "width": 1668, "height": 2224,
    },
    StoreSizeName.ipad_11: {
        # iPad Pro
        "width": 1668, "height": 2388,
    },
    StoreSizeName.ipad_12_9: {
        # 2nd & 3rd generation iPad Pro
        # Required by apple store
        "width": 2048, "height": 2732,
    },
}


class ScreenshotFormat:

    def __init__(self, screenshot_path=None, screenshot_img=None, store_size_name=None, store_size=None,
                 landscape=False):
        """
        :param str screenshot_path: the path to the screenshot
        :param PIL.Image.Image screenshot_img: the screenshot
        :param str store_size_name: Value of the enum of the desired image
        :param list store_size: [with, height] of the desired image
        :param bool landscape: use landscape
        """
        if screenshot_img is not None:
            self.screenshot = screenshot_img
        elif screenshot_path is not None:
            self.screenshot = Image.open(screenshot_path)

        self.store_size_name = store_size_name
        if store_size_name is not None:
            if store_size_name not in STORES_SIZES:
                raise Exception(f"Invalid store_size_name. {store_size_name} not in enum StoreSizeName")
            self.store_width = STORES_SIZES[store_size_name]["width"]
            self.store_height = STORES_SIZES[store_size_name]["height"]
            if landscape:
                self.store_width = STORES_SIZES[store_size_name]["height"]
                self.store_height = STORES_SIZES[store_size_name]["width"]

        elif store_size:
            self.store_width = store_size[0]
            self.store_height = store_size[1]

        if self.screenshot is not None:
            self.screenshot_width, self.screenshot_height = self.screenshot.size

    @property
    def screenshot_size(self):
        """
        Get screenshot's size
        """
        return self.screenshot_width, self.screenshot_height

    @property
    def store_size(self):
        """
        Get store's size
        """
        return self.store_width, self.store_height

    def crop_screenshot(self, left=None, top=None, right=None, bottom=None):
        """
        Crop & edit the screenshot
        :param number left:
        :param number top:
        :param number right:
        :param number bottom:
        """
        left = 0 if left is None else left
        top = 0 if top is None else top
        right = self.screenshot_width if right is None else right
        bottom = self.screenshot_height if bottom is None else bottom

        self.screenshot = self.screenshot.crop((left, top, right, bottom))
        self.screenshot_width, self.screenshot_height = self.screenshot.size

    def resize_screenshot(self, size=None, zoom_ratio=None):
        """
        Resize the screenshot
        :param tuple size: Desired size (width, heigth)
        :param number zoom_ratio: Multiply width & height with the same number
        """
        if size is not None:
            width = int(size[0])
            heigth = int(size[1])
        elif zoom_ratio is not None:
            width = int(self.screenshot_width * zoom_ratio)
            heigth = int(self.screenshot_height * zoom_ratio)
        else:
            raise Exception("Invalid parameter")

        # Resize the screenshot
        self.screenshot = self.screenshot.resize((width, heigth), Image.ANTIALIAS)

        # refresh size of the screenshot
        self.screenshot_width, self.screenshot_height = self.screenshot.size

    def create_background(self, type_, color_palette):
        """
        horizontal_gradient & horizontal_gradient code comes from :
        https://stackoverflow.com/questions/32530345/pil-generating-vertical-gradient-image
        :param BackgroundType type_:
        :param list color_palette: list of colors
        """

        size = (self.store_width, self.store_height)

        background = Image.new('RGBA', size, color=color_palette[0])
        if type_ == BackgroundType.plain:
            return background

        draw = ImageDraw.Draw(background)
        rect = Rect(0, 0, self.store_width, self.store_height)

        if type_ == BackgroundType.horizontal_gradient:
            self._horizontal_gradient(draw, rect, color_palette)
        elif type_ == BackgroundType.vertical_gradient:
            draw = ImageDraw.Draw(background)
            self._vertical_gradient(draw, rect, color_palette)
        elif type_ == BackgroundType.diagonal_gradient_right:
            self._diagonal_gradient(draw, rect, color_palette, left=False)
        elif type_ == BackgroundType.diagonal_gradient_left:
            self._diagonal_gradient(draw, rect, color_palette, left=True)
        else:
            raise Exception("Invalid background type")

        return background

    def _gradient_color(self, minval, maxval, val, color_palette):
        """ Computes intermediate RGB color of a value in the range of minval
            to maxval (inclusive) based on a color_palette representing the range.
        """
        max_index = len(color_palette) - 1
        delta = maxval - minval
        if delta == 0:
            delta = 1
        v = float(val - minval) / delta * max_index
        i1, i2 = int(v), min(int(v) + 1, max_index)
        (r1, g1, b1), (r2, g2, b2) = color_palette[i1], color_palette[i2]
        f = v - i1
        return int(r1 + f * (r2 - r1)), int(g1 + f * (g2 - g1)), int(b1 + f * (b2 - b1))

    def _horizontal_gradient(self, draw, rect, color_palette):
        """
        :rtype: PIL.Image.Image
        """
        minval, maxval = 1, len(color_palette)
        delta = maxval - minval
        for x in range(rect.min.x, rect.max.x + 1):
            f = (x - rect.min.x) / float(rect.width)
            val = minval + f * delta
            color = self._gradient_color(minval, maxval, val, color_palette)
            draw.line([(x, rect.min.y), (x, rect.max.y)], fill=color)

    def _vertical_gradient(self, draw, rect, color_palette):
        """
        :rtype: PIL.Image.Image
        """
        minval, maxval = 1, len(color_palette)
        delta = maxval - minval
        for y in range(rect.min.y, rect.max.y + 1):
            f = (y - rect.min.y) / float(rect.height)
            val = minval + f * delta
            color = self._gradient_color(minval, maxval, val, color_palette)
            draw.line([(rect.min.x, y), (rect.max.x, y)], fill=color)

    def _diagonal_gradient(self, draw, rect, color_palette, left):
        """
        :rtype: PIL.Image.Image
        """
        diagonals = []

        if left:
            for k in range(rect.max.x + rect.max.y):
                diagonal = []
                for j in range(k):
                    i = k - j
                    if i < rect.max.x and j < rect.max.y:
                        diagonal.append((i,j))
                if diagonal != []:
                    diagonals.append(diagonal)
        else:
            for k in range(rect.max.x + rect.max.y):
                diagonal = []
                for j in range(rect.max.x + rect.max.y, 0, -1):
                    i = j + k
                    if i >= 0 and j >= 0 and i < rect.max.x and j < rect.max.y:
                        diagonal.append((i,j))
                if diagonal != []:
                    diagonals.append(diagonal)
            diagonals.reverse()

            for k in range(rect.max.x + rect.max.y):
                diagonal = []
                for j in range(rect.max.x + rect.max.y, 0, -1):
                    i = j - k
                    if i >= 0 and j >= 0 and i < rect.max.x and j < rect.max.y:
                        diagonal.append((i,j))
                if diagonal != []:
                    diagonals.append(diagonal)

        minval, maxval = 1, len(color_palette)
        delta = maxval - minval

        # Apply colors for each diagonals
        for diagonal_index in range(len(diagonals)):
            if diagonals[diagonal_index] == []:
                continue
            try:
                j = diagonal_index
                f = (j - 0) / float(len(diagonals))
                val = minval + f * delta
                color = self._gradient_color(minval, maxval, val, color_palette)

                draw.line([diagonals[diagonal_index][0], diagonals[diagonal_index][-1]], fill=color)
            except Exception as e:
                pass

    def create_text_image(self, size, position, text, color, font_path, font_size):
        """
        Create a Txt Image
        :param tuple size: (width, height) of the text image
        :param tuple position: can contain int or a value of enum Position
        :param text: Text to display on the image
        :param color: RGB color of the text
        :param str font_path: Path of the font file
        :param number font_size: Size of the text
        :rtype: PIL.Image.Image
        """
        width, height = size

        halo = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        font = ImageFont.truetype(font_path, font_size)
        draw = ImageDraw.Draw(halo)
        w, h = draw.textsize(text, font=font)

        position = self._position_to_numbers(position, size, (w, h))
        draw.multiline_text(position, text, color, font=font, align="center")

        return halo

    def _position_to_numbers(self, position, parent_size, child_size):
        """
        Convert Position.center to a position tuple with int values
        :param tuple position:
        :param tuple parent_size:
        :param tuple child_size:
        :rtype: tuple
        """
        position_width, position_height = position
        parent_width, parent_height = parent_size
        child_width, child_height = child_size

        if type(position_width) in [int, float]:
            output_width = position_width
        elif position_width == Position.center:
            output_width = (parent_width - child_width) / 2
        elif position_width == Position.left:
            output_width = 0
        elif position_width == Position.right:
            output_width = parent_width - child_width
        else:
            raise Exception("Invalid width")

        if type(position_height) in [int, float]:
            output_height = position_height
        elif position_height == Position.center:
            output_height = (parent_height - child_height) / 2
        elif position_height == Position.top:
            output_height = 0
        elif position_height == Position.bottom:
            output_height = parent_height - child_height
        else:
            raise Exception("Invalid height")

        return int(output_width), int(output_height)

    def add_text_with_halo(self, img, position, text, color, halo_col, font_path, font_size, filter_=None):
        """
        Add a text with a halo effect and add it to the image
        :param PIL.Image.Image img:
        :param tuple position: can contain int or a value of enum Position
        :param str text: Text to display on the image
        :param tuple color: RGB color of the text
        :param tuple halo_col: RGB color of the halo
        :param font_path: Path of the font file
        :param font_size: Size of the text
        :param PIL.ImageFilter filter_: Filter applied on the halo
        :rtype: PIL.Image.Image
        """
        if filter_ is None:
            filter_ = ImageFilter.GaussianBlur(5)

        img_size = img.size

        # Create Text for the Halo
        halo = self.create_text_image(img_size, position, text, halo_col, font_path, font_size)
        # Add blur effect
        blurred_halo = halo.filter(filter_)

        # Create Text
        text = self.create_text_image(img_size, position, text, color, font_path, font_size)

        # Blend the halo with the text
        text_with_halo = Image.composite(blurred_halo, text, ImageChops.invert(text))

        # Blend the text with the input image
        return Image.composite(img, text_with_halo, ImageChops.invert(text_with_halo))

    def apply_screenshot_on_background(self, background, position):
        """
        Add image on the background, given a position
        :param PIL.Image.Image background:
        :param position:
        :rtype: PIL.Image.Image
        """

        position = self._position_to_numbers(position, self.store_size, self.screenshot_size)
        background.paste(self.screenshot, position, self.screenshot)
        return background

    @staticmethod
    def save(img, path, file_name):
        """
        Create directories and save image
        :param PIL.Image.Image img:
        :param str path:
        :param str file_name:
        """
        # Create folders
        try:
            os.makedirs(path)
        except:
            pass
        # Save image
        img.save(f"{path}/{file_name}")

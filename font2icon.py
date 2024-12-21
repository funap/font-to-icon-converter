from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple, Dict
from io import BytesIO
import struct
from dataclasses import dataclass
from typing import Optional
import os
from sys import platform
import sys

@dataclass
class IconConfig:
    bg_color: Tuple[int, int, int, int]
    font_path: str
    sizes: List[Tuple[int, int]]

class IconCreator:
    def __init__(self, config: IconConfig):
        self.config = config
        self.base_font = ImageFont.truetype(config.font_path, 1)

    def create_icon_image(self, img_size: Tuple[int, int], char: str, text_color: str = "black") -> Image.Image:
        img = Image.new("RGBA", img_size, self.config.bg_color)
        draw = ImageDraw.Draw(img)

        font_size = int(img_size[0] * 0.95)
        custom_font = ImageFont.truetype(self.base_font.path, font_size)
        ascent, descent = custom_font.getmetrics()

        bbox = draw.textbbox((0, 0), char[0], font=custom_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (img_size[0] - text_width) / 2
        y = (img_size[1] - (ascent + descent)) / 2

        for c in char:
            draw.text((x, y), c, fill=text_color, font=custom_font)
        return img

    @staticmethod
    def _create_ico_header(num_images: int) -> bytes:
        return struct.pack('HHH', 0, 1, num_images)

    @staticmethod
    def _create_directory_entry(width: int, height: int, size: int, offset: int) -> bytes:
        return struct.pack('BBBB HH II',
            width & 255,
            height & 255,
            0, 0,           # Color palette
            1, 32,          # Color planes, Bits per pixel
            size, offset    # Size of image data, Offset to image data
        )

    def create_ico_from_images(self, images: List[Image.Image], output_ico: str) -> Optional[bool]:
        try:
            if not images:
                print("Error: No images provided")
                return None

            images = [img.convert('RGBA') for img in images]
            with open(output_ico, 'wb') as ico:
                ico.write(self._create_ico_header(len(images)))
                offset = 6 + 16 * len(images)

                image_data = []
                directory_entries = []

                for img in images:
                    img_byte = BytesIO()
                    img.save(img_byte, format='PNG')
                    img_data = img_byte.getvalue()

                    width = 256 if img.width >= 256 else img.width
                    height = 256 if img.height >= 256 else img.height
                    size = len(img_data)

                    directory_entries.append(self._create_directory_entry(width, height, size, offset))
                    image_data.append(img_data)
                    offset += size

                for entry in directory_entries:
                    ico.write(entry)

                for data in image_data:
                    ico.write(data)

            print(f"Successfully created: {output_ico}")
            return True

        except Exception as e:
            print(f"Error creating ICO file: {str(e)}")
            return False

    def generate_icons(self, char: str, file_name: str, text_color: str) -> None:
        images = [
            self.create_icon_image(size, char, text_color)
            for size in self.config.sizes
        ]
        self.create_ico_from_images(images, f"{file_name}.ico")


def main():
    if len(sys.argv) < 4:
        print("Usage: python font2icon.py <ttf_file> <unicode_point> <output_filename> [color]")
        print("e.g. python font2icon.py arial.ttf 0061 a")
        print("e.g. python font2icon.py arial.ttf 0061 a_red f00")
        print("e.g. python font2icon.py arial.ttf 0061 a_light dedede")
        sys.exit(1)

    font_path       = sys.argv[1]
    unicode_point   = int(sys.argv[2], 16)
    file_name       = sys.argv[3]
    text_color      = f"#{sys.argv[4]}" if len(sys.argv) > 4 else "#333333"

    if not os.path.exists(font_path):
        font_path = os.path.join(os.environ['WINDIR'], 'Fonts', font_path)
    if not os.path.exists(font_path):
        print(f"Font file not found: {font_path}")
        sys.exit(1)

    config = IconConfig(
        bg_color=(255, 255, 255, 0),
        font_path=font_path,
        sizes=[(16, 16), (20, 20), (24, 24), (32, 32), (40, 40), (48, 48), (64, 64), (80, 80), (96, 96)],
    )
    icon_creator = IconCreator(config)
    icon_creator.generate_icons(chr(unicode_point), file_name, text_color)

if __name__ == "__main__":
    main()

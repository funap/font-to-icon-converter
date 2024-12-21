# Font to Icon Converter

A Python utility that converts font characters to multi-size ICO files. This tool allows you to create icon files from any character in a TrueType font.

## Features

- Creates ICO files with multiple sizes
- Supports custom text colors
- Works with any TrueType font file
- Transparent background
- PNG compression for optimal file size

## Requirements

- Python 3.7+
- Pillow (PIL)

## Installation

```bash
pip install Pillow
```

## Usage

Basic syntax:
```bash
python font2icon.py <ttf_file> <unicode_point> <output_filename> [color]
```

Examples:
```bash
# Create an icon from letter 'a' using Arial font
python font2icon.py arial.ttf 0061 a

# Create a red icon
python font2icon.py arial.ttf 0061 a_red f00

# Create an icon with light gray color
python font2icon.py arial.ttf 0061 a_light dedede
```

### Parameters

- `ttf_file`: Path to the TrueType font file
- `unicode_point`: Unicode code point in hexadecimal
- `output_filename`: Name for the output ICO file (without extension)
- `color` (optional): Text color in hexadecimal format (default: 333333)

## Output

The script generates an ICO file containing the following sizes:
- 16x16
- 20x20
- 24x24
- 32x32
- 40x40
- 48x48
- 64x64
- 80x80
- 96x96

## License

MIT License

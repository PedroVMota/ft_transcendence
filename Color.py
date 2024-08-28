import os
import re
import argparse

def adjust_intensity(hex_color, factor, operation):
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    
    if operation == 'mul':
        r = r * factor
        g = g * factor
        b = b * factor
    elif operation == 'div':
        r = r / factor
        g = g / factor
        b = b / factor
    elif operation == 'sum':
        r = r + factor
        g = g + factor
        b = b + factor
    elif operation == 'min':
        r = r - factor
        g = g - factor
        b = b - factor
    else:
        raise ValueError("Invalid operation. Choose from 'mul', 'div', 'sum', 'min'.")
    
    # Clamp values to 0-255 range and check for overflow/underflow
    if r > 255 or g > 255 or b > 255:
        return '#ffffff'  # Pure white
    elif r < 0 or g < 0 or b < 0:
        return '#000000'  # Pure black
    else:
        r = min(255, max(0, int(r)))
        g = min(255, max(0, int(g)))
        b = min(255, max(0, int(b)))
        return f'#{r:02x}{g:02x}{b:02x}'

def process_svg_file(file_path, factor, operation):
    with open(file_path, 'r') as file:
        content = file.read()
    
    hex_colors = re.findall(r'#[0-9a-fA-F]{6}', content)
    
    for hex_color in hex_colors:
        new_color = adjust_intensity(hex_color, factor, operation)
        content = content.replace(hex_color, new_color)
    
    with open(file_path, 'w') as file:
        file.write(content)

def main(directory, factor, operation):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.svg'):
                file_path = os.path.join(root, file)
                process_svg_file(file_path, factor, operation)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Adjust SVG color intensity.')
    parser.add_argument('directory', type=str, help='Directory to search for SVG files')
    parser.add_argument('factor', type=float, help='Factor to adjust the color intensity')
    parser.add_argument('operation', type=str, choices=['mul', 'div', 'sum', 'min'], help='Operation to perform on the color intensity')
    
    args = parser.parse_args()
    main(args.directory, args.factor, args.operation)
import random


def generate_random_color() -> str:
    # Generate random RGB values
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    # Convert RGB to HSL
    max_value = max(red, green, blue)
    min_value = min(red, green, blue)
    hue = (max_value + min_value) / 2
    saturation = (max_value - min_value) / (max_value + min_value)
    lightness = (max_value + min_value) / 510
    # Adjust saturation to make it less saturated
    saturation = max(0.2, saturation)
    # Convert HSL to RGB
    if saturation == 0:
        red = green = blue = int(lightness * 255)
    else:
        if lightness < 0.5:
            temp_2 = lightness * (1 + saturation)
        else:
            temp_2 = (lightness + saturation) - (lightness * saturation)
        temp_1 = 2 * lightness - temp_2
        hue /= 360

        def hue_to_rgb(temp_1, temp_2, hue):
            if hue < 0:
                hue += 1
            elif hue > 1:
                hue -= 1
            if hue * 6 < 1:
                return temp_1 + (temp_2 - temp_1) * hue * 6
            elif hue * 2 < 1:
                return temp_2
            elif hue * 3 < 2:
                return temp_1 + (temp_2 - temp_1) * ((2 / 3) - hue) * 6
            else:
                return temp_1
        red = int(hue_to_rgb(temp_1, temp_2, hue + 1/3) * 255)
        green = int(hue_to_rgb(temp_1, temp_2, hue) * 255)
        blue = int(hue_to_rgb(temp_1, temp_2, hue - 1/3) * 255)
    # Convert RGB to hexadecimal color
    color_hex = '#{:02x}{:02x}{:02x}'.format(red, green, blue)
    return color_hex

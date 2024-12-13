import os
from PIL import Image, ImageEnhance

def apply_watermark_to_directory(input_dir, output_dir, watermark_path, corner_positions, corner_scale, corner_transparency, center_enabled, center_scale, center_transparency, center_rotation):
    """Apply watermark to all images in the directory."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load the original watermark
    original_watermark = Image.open(watermark_path).convert("RGBA")

    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        # Skip directories
        if not os.path.isfile(input_path):
            continue

        with Image.open(input_path) as img:
            img = img.convert("RGBA")  # Ensure base image supports RGBA
            base = img.copy()

            # Resize watermark for corners while preserving aspect ratio
            watermark = original_watermark.copy()
            watermark = resize_watermark(watermark, base.width * corner_scale / 100)  # Scale by corner_scale, but preserve aspect ratio

            # Adjust transparency for watermark (after resizing)
            watermark = adjust_transparency(watermark, corner_transparency)

            # Apply corner watermarks
            for position, enabled in corner_positions.items():
                if not enabled:
                    continue
                x, y = calculate_position(position, base.size, watermark.size)
                base.paste(watermark, (x, y), watermark)

            # Apply center watermark if enabled
            if center_enabled:
                center_watermark = original_watermark.copy()
                center_watermark = resize_watermark(center_watermark, base.width * center_scale / 100)  # Scale by center_scale
                center_watermark = adjust_transparency(center_watermark, center_transparency)
                
                # Apply rotation to the center watermark using Bicubic resampling
                center_watermark = center_watermark.rotate(center_rotation, resample=Image.Resampling.BICUBIC, expand=True)
                
                # Calculate position and paste the watermark
                center_x = (base.width - center_watermark.width) // 2
                center_y = (base.height - center_watermark.height) // 2
                base.paste(center_watermark, (center_x, center_y), center_watermark)

            # Save the final image
            base = base.convert("RGB")
            base.save(output_path, "JPEG", quality=100)


def adjust_transparency(watermark, transparency):
    """Adjust the transparency of a watermark image."""
    alpha = watermark.split()[-1]  # Extract the alpha channel
    alpha = alpha.point(lambda p: p * (transparency / 100))  # Scale alpha values
    watermark.putalpha(alpha)  # Apply the modified alpha back to the watermark
    return watermark


def resize_watermark(watermark, target_width):
    """Resize the watermark to the target width, preserving aspect ratio."""
    # Get original dimensions
    original_width, original_height = watermark.size
    aspect_ratio = original_height / original_width

    # Calculate new height based on target width while preserving aspect ratio
    target_height = int(target_width * aspect_ratio)

    # Resize watermark (convert to integer values)
    return watermark.resize((int(target_width), int(target_height)), Image.Resampling.LANCZOS)


def calculate_position(position, base_size, watermark_size):
    """Calculate the top-left position for placing the watermark."""
    base_width, base_height = base_size
    watermark_width, watermark_height = watermark_size

    x, y = 0, 0
    if "top" in position:
        y = 0
    elif "bottom" in position:
        y = base_height - watermark_height
    if "left" in position:
        x = 0
    elif "right" in position:
        x = base_width - watermark_width

    return x, y

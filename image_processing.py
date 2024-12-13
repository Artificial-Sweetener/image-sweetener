import os
from PIL import Image


def ensure_directory(directory):
    """
    Ensure that the given directory exists, creating it if necessary.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def iterate_directory(input_dir, output_dir, process_function, preserve_file_type=True):
    """
    Iterate over files in a directory, applying a processing function to each file.

    Args:
        input_dir (str): Path to the input directory.
        output_dir (str): Path to the output directory.
        process_function (function): Function to process each file.
        preserve_file_type (bool): Whether to preserve the original file extension.
    """
    ensure_directory(output_dir)

    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)

        if os.path.isfile(input_path):
            file_root, file_ext = os.path.splitext(filename)
            if preserve_file_type:
                output_filename = f"{file_root}{file_ext}"
            else:
                output_filename = f"{file_root}.jpg"

            output_path = os.path.join(output_dir, output_filename)
            process_function(input_path, output_path)


def resize_image(input_path, output_path, max_dimension):
    """
    Resize an image to fit within a square of max_dimension x max_dimension.

    Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the resized image.
        max_dimension (int): Maximum size for the longest side of the image.
    """
    with Image.open(input_path) as img:
        width, height = img.size

        # Determine scaling factor
        scale_factor = min(max_dimension / width, max_dimension / height)
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)

        # Resize the image
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Convert to RGB if necessary
        if img.mode != "RGB":
            img = img.convert("RGB")

        # Save as JPEG
        img.save(output_path, format="JPEG", quality=100)


def apply_watermark(input_path, output_path, watermark_path, scale=70, transparency=100, position="bottom right"):
    """
    Apply a watermark to an image and save the output.

    Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the watermarked image.
        watermark_path (str): Path to the watermark image.
        scale (int): Percentage of the image width the watermark should occupy.
        transparency (int): Transparency of the watermark (0 to 100).
        position (str): Position for the watermark (e.g., "bottom right").
    """
    with Image.open(input_path) as base_image, Image.open(watermark_path) as watermark:
        base_width, base_height = base_image.size

        # Resize watermark based on the base image width
        watermark_width = int((scale / 100) * base_width)
        watermark.thumbnail((watermark_width, watermark_width), Image.Resampling.LANCZOS)

        # Adjust transparency
        if watermark.mode != "RGBA":
            watermark = watermark.convert("RGBA")
        alpha = watermark.split()[3]  # Get alpha channel
        alpha = alpha.point(lambda p: p * (transparency / 100))
        watermark.putalpha(alpha)

        # Position the watermark
        wm_width, wm_height = watermark.size
        if position == "bottom right":
            offset = (base_width - wm_width, base_height - wm_height)
        elif position == "bottom left":
            offset = (0, base_height - wm_height)
        elif position == "top right":
            offset = (base_width - wm_width, 0)
        elif position == "top left":
            offset = (0, 0)
        else:
            raise ValueError("Invalid watermark position. Choose from 'top left', 'top right', 'bottom left', 'bottom right'.")

        # Apply watermark and save
        base_image = base_image.convert("RGBA")
        base_image.paste(watermark, offset, mask=watermark)
        base_image = base_image.convert("RGB")  # Ensure the output is in RGB mode
        base_image.save(output_path, format="JPEG", quality=100)

from image_processing import iterate_directory
import os
from PIL import Image

def resize_image(input_path, output_path, max_dimension=2000, target_size_kb=1024):
    """
    Resize an image to fit within 2000x2000 while maintaining aspect ratio 
    and adjusting compression to stay under a target file size.

    Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the resized WebP image.
        max_dimension (int): Maximum width/height for the image.
        target_size_kb (int): Target file size in kilobytes (1MB = 1024 KB).
    """
    with Image.open(input_path) as img:
        width, height = img.size
        scale_factor = min(max_dimension / width, max_dimension / height)

        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)

        # Resize the image while maintaining aspect ratio
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Convert to RGB if necessary (WebP requires it)
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")

        # Start with high quality and adjust if needed
        quality = 100  
        while quality > 10:  # Prevent excessive quality loss
            img.save(output_path, format="WEBP", quality=quality, method=6)
            if os.path.getsize(output_path) <= target_size_kb * 1024:
                break  # Stop if file size is within the limit
            quality -= 5  # Reduce quality and try again

def process_images_for_bluesky(input_dir, output_dir, target_size_kb=1024):
    """
    Process images for Bluesky while ensuring max dimensions of 2000x2000 
    and a target file size.

    Args:
        input_dir (str): Path to the input directory.
        output_dir (str): Path to the output directory.
        target_size_kb (int): Target file size for each image (in KB).
    """
    print(f"Processing images for Bluesky in '{input_dir}' with target size {target_size_kb}KB...")
    print(f"Output will be saved to '{output_dir}' in WebP format.")

    def process_image(input_path, output_path):
        # Ensure output file has .webp extension
        output_webp_path = os.path.splitext(output_path)[0] + ".webp"
        resize_image(input_path, output_webp_path, max_dimension=2000, target_size_kb=target_size_kb)

    iterate_directory(input_dir, output_dir, process_image, preserve_file_type=False)

    print("Bluesky scaling complete.")
from image_processing import iterate_directory
import os
from PIL import Image

def resize_image(input_path, output_webp_path, max_width=1080, max_height=1920):
    """
    Resize an image to fit within the TikTok recommended dimensions (1080x1920) 
    while maintaining the aspect ratio. Saves as WebP.

    Args:
        input_path (str): Path to the input image.
        output_webp_path (str): Path to save the resized WebP image.
        max_width (int): Maximum width for the image.
        max_height (int): Maximum height for the image.
    """
    with Image.open(input_path) as img:
        width, height = img.size
        scale_factor = min(max_width / width, max_height / height)

        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)

        # Resize the image
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Convert to RGB if necessary (WebP requires proper color mode)
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")

        # Save as WebP with high quality
        img.save(output_webp_path, format="WEBP", quality=100)

def process_images_for_tiktok(input_dir, output_dir):
    """
    Process images for TikTok with proper scaling (max 1080x1920), ensuring WebP format.

    Args:
        input_dir (str): Path to the input directory containing images.
        output_dir (str): Path to the output directory for processed images.
    """
    print(f"Processing images for TikTok in '{input_dir}'...")
    print(f"Output will be saved to '{output_dir}'.")

    def process_image(input_path, output_path):
        # Ensure output file has .webp extension
        output_webp_path = os.path.splitext(output_path)[0] + ".webp"
        resize_image(input_path, output_webp_path, max_width=1080, max_height=1920)

    # Force WebP output and override preserve_file_type behavior
    iterate_directory(input_dir, output_dir, process_image, preserve_file_type=False)

    print("TikTok scaling complete.")
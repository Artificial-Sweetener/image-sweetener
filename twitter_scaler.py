from image_processing import resize_image, iterate_directory
import os
from shutil import copy2
from PIL import Image


def process_images_for_twitter(input_dir, output_dir):
    """
    Process images for Twitter's maximum dimensions (4096x4096).
    
    Args:
        input_dir (str): Path to the input directory containing images.
        output_dir (str): Path to the output directory for scaled images.
    """
    print(f"Processing images for Twitter in '{input_dir}'...")
    print(f"Output will be saved to '{output_dir}'.")

    max_dimension = 4096  # Maximum dimension for Twitter images

    def process_image(input_path, output_path):
        # Check if the image is larger than max dimension
        with Image.open(input_path) as img:
            width, height = img.size
            # Scale down if larger
            if width > max_dimension or height > max_dimension:
                resize_image(input_path, output_path, max_dimension)
            else:
                # If it's already small enough and it's a .png, convert to JPEG at high quality
                if input_path.lower().endswith(".png"):
                    img.convert("RGB").save(output_path, format="JPEG", quality=100)
                else:
                    # If it's a jpeg or already small enough, simply copy the image
                    copy2(input_path, output_path)

    # Ensure outputs are always JPEG and handle scaling/copying
    iterate_directory(input_dir, output_dir, process_image, preserve_file_type=False)

    print("Twitter scaling complete.")

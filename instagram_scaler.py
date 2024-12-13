from image_processing import resize_image, iterate_directory
from PIL import Image, ImageOps


def process_images_for_aspect_ratio(input_dir, output_dir, aspect_ratio):
    """
    Process images to fit a given aspect ratio with padding and scaling, without upscaling.

    Args:
        input_dir (str): Path to the input directory containing images.
        output_dir (str): Path to the output directory for processed images.
        aspect_ratio (str): Desired aspect ratio in "width:height" format (e.g., "4:5").
    """
    print(f"Processing images for aspect ratio {aspect_ratio} in '{input_dir}'...")
    print(f"Output will be saved to '{output_dir}'.")

    # Parse aspect ratio
    try:
        width_ratio, height_ratio = map(float, aspect_ratio.split(":"))
        
        # If the ratio contains decimals, multiply both sides by 100
        if width_ratio < 10:  # Detect if the ratio is like 1.91:1
            width_ratio *= 100
            height_ratio *= 100
            print(f"Converted aspect ratio: {width_ratio:.0f}:{height_ratio:.0f}")

    except ValueError:
        raise ValueError("Aspect ratio must be in 'width:height' format, e.g., '4:5'.")

    def process_image(input_path, output_path):
        with Image.open(input_path) as img:
            orig_width, orig_height = img.size
            is_portrait = orig_height > orig_width

            # Step 1: Calculate target dimensions
            if is_portrait:
                # Portrait orientation
                long_side = orig_height
                short_side = int(long_side / (height_ratio / width_ratio))
            else:
                # Landscape orientation
                long_side = orig_width
                short_side = int(long_side / (width_ratio / height_ratio))

            if is_portrait:
                target_width, target_height = short_side, long_side
            else:
                target_width, target_height = long_side, short_side

            # Step 2: Resize to fit the target aspect ratio with padding
            img = img.resize((min(orig_width, target_width), min(orig_height, target_height)), Image.Resampling.LANCZOS)
            padded_img = Image.new("RGB", (target_width, target_height), (0, 0, 0))  # Black padding
            offset_x = (target_width - img.width) // 2
            offset_y = (target_height - img.height) // 2
            padded_img.paste(img, (offset_x, offset_y))

            # Step 3: Scale down if the image exceeds 1440 pixels in either direction
            if target_width > 1440 or target_height > 1440:
                scale_factor = min(1440 / target_width, 1440 / target_height)
                new_width = int(target_width * scale_factor)
                new_height = int(target_height * scale_factor)
                padded_img = padded_img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Save the processed image
            padded_img.save(output_path, format="JPEG", quality=100)

    iterate_directory(input_dir, output_dir, process_image, preserve_file_type=False)

    print("Aspect ratio processing complete.")

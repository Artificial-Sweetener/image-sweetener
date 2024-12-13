import os
from watermarking import apply_watermark_to_directory
from facebook_scaler import process_images_for_facebook
from instagram_scaler import process_images_for_aspect_ratio
from twitter_scaler import process_images_for_twitter
from tiktok_scaler import process_images_for_tiktok
from threads_scaler import process_images_for_threads
from bluesky_scaler import process_images_for_bluesky
import json

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "target_dir": "",
    "watermark_path": "",
    "corner_watermark_positions": [],
    "corner_watermark_scale": 70,
    "corner_watermark_transparency": 100,
    "center_watermark_enabled": False,
    "center_watermark_scale": 70,
    "center_watermark_transparency": 100,
    "center_watermark_rotation": 0,
    "platforms": {
        "facebook": False,
        "instagram": False,
        "twitter": False,
        "tiktok": False,
        "threads": False,
        "bluesky": False,
    },
    "instagram_aspect_ratio": "4:5",
}


def load_config():
    """Load configuration from file or create default configuration."""
    print("Loading configuration...")
    if not os.path.exists(CONFIG_FILE):
        print("Config file not found. Creating with defaults.")
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    
    with open(CONFIG_FILE, "r") as file:
        config = json.load(file)
        print("Config file loaded.")
        
        # Ensure missing keys have default values
        if "corner_position_vars" not in config:
            config["corner_position_vars"] = {
                "top left": False,
                "top right": False,
                "bottom left": False,
                "bottom right": False
            }
        
        return config


def save_config(config):
    """Save configuration to file."""
    print("Saving configuration...")
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)
    print("Configuration saved.")


def process_pipeline(target_dir, options):
    print("Starting processing pipeline...")

    watermark_output_dir = os.path.join(target_dir, "watermarks")
    os.makedirs(watermark_output_dir, exist_ok=True)

    # Convert corner positions to a dictionary
    corner_positions_dict = {pos: True for pos in options["corner_watermark_positions"]}

    # Skip watermarking if no watermark path is selected
    if options["watermark_path"]:
        print("Applying watermark...")
        print(f"Input directory: {target_dir}")
        print(f"Watermark output directory: {watermark_output_dir}")
        print(f"Watermark options: {options}")

        apply_watermark_to_directory(
            input_dir=target_dir,
            output_dir=watermark_output_dir,
            watermark_path=options["watermark_path"],
            corner_positions=corner_positions_dict,  # Use the dictionary format
            corner_scale=options["corner_watermark_scale"],
            corner_transparency=options["corner_watermark_transparency"],
            center_enabled=options["center_watermark_enabled"],
            center_scale=options["center_watermark_scale"],
            center_transparency=options["center_watermark_transparency"],
            center_rotation=options["center_watermark_rotation"],
        )

        processing_dir = watermark_output_dir
    else:
        print("No watermark selected, skipping watermarking...")
        processing_dir = target_dir  # If no watermark, just use the target directory

    # Process for each platform
    if options["platforms"].get("facebook", False):
        print("Processing for Facebook...")
        facebook_output_dir = os.path.join(target_dir, "facebook")
        process_images_for_facebook(processing_dir, facebook_output_dir)

    if options["platforms"].get("instagram", False):
        print("Processing for Instagram...")
        instagram_output_dir = os.path.join(target_dir, "instagram")
        process_images_for_aspect_ratio(
            processing_dir, instagram_output_dir, options["instagram_aspect_ratio"]
        )

    if options["platforms"].get("twitter", False):
        print("Processing for Twitter...")
        twitter_output_dir = os.path.join(target_dir, "twitter")
        process_images_for_twitter(processing_dir, twitter_output_dir)

    if options["platforms"].get("tiktok", False):
        print("Processing for TikTok...")
        tiktok_output_dir = os.path.join(target_dir, "tiktok")
        process_images_for_tiktok(processing_dir, tiktok_output_dir)

    if options["platforms"].get("threads", False):
        print("Processing for Threads...")
        threads_output_dir = os.path.join(target_dir, "threads")
        process_images_for_threads(processing_dir, threads_output_dir)

    if options["platforms"].get("bluesky", False):
        print("Processing for Bluesky...")
        bluesky_output_dir = os.path.join(target_dir, "bluesky")
        process_images_for_bluesky(processing_dir, bluesky_output_dir)

    print("All processing completed.")

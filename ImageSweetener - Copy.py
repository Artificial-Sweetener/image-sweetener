import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from core import load_config, save_config, process_pipeline
from watermark_gui import create_watermark_section
from social_media_gui import create_social_media_section

def resource_path(relative_path):
    """Get the path to the resource, whether it's bundled with the app or running in a development environment."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")  # Fallback to current directory
    return os.path.join(base_path, relative_path)

def create_gui():
    """Create the GUI for the program."""
    print("Initializing GUI...")
    root = tk.Tk()
    root.title("Image Sweetener")

    # Set window icon using the correct path (handle both bundled and source paths)
    icon_path = resource_path("icons/icon.ico")
    root.iconbitmap(icon_path)

    # Prevent window resizing
    root.resizable(False, False)

    # Load the last configuration
    config = load_config()

    # Target Directory Selection
    tk.Label(root, text="Select Target Directory:").grid(row=0, column=0, padx=10, pady=10)
    target_dir_entry = tk.Entry(root, width=50)
    target_dir_entry.insert(0, config.get("target_dir", ""))
    target_dir_entry.grid(row=0, column=1, padx=10, pady=10)

    def browse_target_directory():
        directory = filedialog.askdirectory()
        if directory:
            target_dir_entry.delete(0, tk.END)
            target_dir_entry.insert(0, directory)

    tk.Button(root, text="Browse", command=browse_target_directory).grid(row=0, column=2, padx=10, pady=10)

    # Watermark Section
    watermark_options = {}
    watermark_row = create_watermark_section(root, config, 1, watermark_options)

    # Social Media Section
    social_media_options = {}
    create_social_media_section(root, config, watermark_row + 1, social_media_options)

    # Process Button
    def start_processing():
        target_dir = target_dir_entry.get()
        if not os.path.isdir(target_dir):
            messagebox.showerror("Error", "Please select a valid target directory.")
            return

        # Extract the values from the widgets
        options = {
            "target_dir": target_dir,
            "watermark_path": watermark_options["watermark_path"].get(),
            "corner_watermark_positions": [
                pos for pos, var in watermark_options["corner_position_vars"].items() if var.get()
            ],
            "corner_watermark_scale": watermark_options["corner_watermark_scale"].get(),
            "corner_watermark_transparency": watermark_options["corner_watermark_transparency"].get(),
            "center_watermark_enabled": watermark_options["center_watermark_var"].get(),
            "center_watermark_scale": watermark_options["center_watermark_scale"].get(),
            "center_watermark_transparency": watermark_options["center_watermark_transparency"].get(),
            "center_watermark_rotation": watermark_options["center_watermark_rotation"].get(),
            "platforms": {k: v.get() for k, v in social_media_options["platform_vars"].items()},
            "instagram_aspect_ratio": social_media_options["instagram_aspect_ratio"].get(),
        }

        # Skip watermark processing if no watermark file is selected
        if not options["watermark_path"]:
            options["corner_watermark_positions"] = []
            options["center_watermark_enabled"] = False
            print("No watermark selected, skipping watermarking...")

        # Save configuration
        save_config(options)

        # Pass options to the processing pipeline
        print("Options passed to process_pipeline:", options)
        process_pipeline(target_dir, options)

    tk.Button(
        root, text="Process Images", command=start_processing, height=2, width=20
    ).grid(row=watermark_row + 2, column=0, columnspan=3, pady=20)

    def on_closing():
        """Ensure CLI closes when GUI is closed."""
        print("Exiting program...")
        root.quit()  # Stops the Tkinter main loop
        root.update()  # Ensures any pending events are processed
        os._exit(0)  # Force the process to terminate

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
    print("GUI closed.")


if __name__ == "__main__":
    print("Launching GUI...")
    try:
        create_gui()
    except Exception as e:
        with open("error_log.txt", "w") as log_file:
            log_file.write("An error occurred during GUI launch:\n")
            log_file.write(str(e))
        print("An error occurred. Check 'error_log.txt' for details.")

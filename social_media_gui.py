import tkinter as tk


def create_social_media_section(root, config, start_row, options):
    """Create the social media scaling section in the GUI."""
    social_media_frame = tk.LabelFrame(root, text="Social Media Scaling", font=("Arial", 12, "bold"), padx=10, pady=10)
    social_media_frame.grid(row=start_row, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

    # Platform Checkboxes with Icons
    platform_frame = tk.Frame(social_media_frame)
    platform_frame.grid(row=0, column=0, columnspan=3, pady=10, sticky="ew")

    # Initialize platform variables and add to options
    platform_vars = {platform: tk.BooleanVar(value=config["platforms"].get(platform, False)) for platform in config["platforms"]}
    options["platform_vars"] = platform_vars

    # Icon paths
    icon_paths = {
        "facebook": "icons/facebook.png",
        "instagram": "icons/instagram.png",
        "threads": "icons/threads.png",
        "bluesky": "icons/bluesky.png",
        "tiktok": "icons/tiktok.png",
        "twitter": "icons/twitter.png",
    }

    # Prevent garbage collection of icons by storing them in a list
    options["icons"] = []
    for idx, (platform, icon_path) in enumerate(icon_paths.items()):
        try:
            icon = tk.PhotoImage(file=icon_path)
            options["icons"].append(icon)
            tk.Checkbutton(
                platform_frame, image=icon, variable=platform_vars[platform], indicatoron=False
            ).pack(side="left", padx=10)
        except tk.TclError:
            print(f"Error loading icon for {platform}. Check if the file exists: {icon_path}")

    # Instagram Aspect Ratio Options
    instagram_aspect_ratio = tk.StringVar(value=config.get("instagram_aspect_ratio", "4:5"))
    options["instagram_aspect_ratio"] = instagram_aspect_ratio

    # Aspect ratio icons and their paths
    aspect_ratio_icons = {
        "1:1": "icons/square.png",
        "3:4": "icons/threefour.png",
        "4:5": "icons/fourfive.png",
    }


    aspect_ratio_frame = tk.Frame(social_media_frame)
    aspect_ratio_frame.grid(row=1, column=0, columnspan=3, pady=5, sticky="ew")

    tk.Label(aspect_ratio_frame, text="Aspect Ratio for Instagram:").grid(row=0, column=0, padx=5, pady=5, sticky="w")

    # Store references to avoid garbage collection
    options["aspect_ratio_icons"] = []
    for idx, (ratio, icon_path) in enumerate(aspect_ratio_icons.items()):
        try:
            # Create a frame for each label and icon pair
            ratio_frame = tk.Frame(aspect_ratio_frame)
            ratio_frame.grid(row=0, column=idx + 1, padx=5, pady=5, sticky="w")

            # Add label to the left of the button
            tk.Label(ratio_frame, text=ratio).pack(side="left", padx=2)

            # Add icon button
            icon = tk.PhotoImage(file=icon_path)
            options["aspect_ratio_icons"].append(icon)
            tk.Radiobutton(
                ratio_frame,
                image=icon,
                variable=instagram_aspect_ratio,
                value=ratio,
                indicatoron=False,
                state="disabled"  # Initially disabled
            ).pack(side="left")
        except tk.TclError:
            print(f"Error loading icon for aspect ratio {ratio}. Check if the file exists: {icon_path}")

    # Enable/disable Instagram-specific options based on the platform selection
    def toggle_instagram_options(*args):
        state = "normal" if platform_vars["instagram"].get() else "disabled"
        for widget in aspect_ratio_frame.winfo_children():
            for child in widget.winfo_children():  # Handle nested widgets (label + button frame)
                child.configure(state=state)

    platform_vars["instagram"].trace_add("write", toggle_instagram_options)
    toggle_instagram_options()  # Ensure initial state matches configuration

    return start_row + 1


# Export the function
__all__ = ["create_social_media_section"]

import tkinter as tk
from tkinter import filedialog


def create_watermark_section(root, config, start_row, options):
    """Create the watermarking section in the GUI."""
    watermark_frame = tk.LabelFrame(root, text="Watermarking", font=("Arial", 12, "bold"), padx=10, pady=10)
    watermark_frame.grid(row=start_row, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

    # Store icons to prevent garbage collection
    options["icons"] = []

    # Function to enable/disable controls
    def toggle_controls():
        watermark_selected = bool(watermark_path_entry.get().strip())
        corner_enabled = watermark_selected and any(var.get() for var in corner_position_vars.values())
        center_enabled = watermark_selected and center_watermark_var.get()

        # Toggle corner controls
        for widget in [corner_watermark_scale, corner_watermark_transparency, corner_scale_value, corner_transparency_value]:
            widget.configure(state="normal" if corner_enabled else "disabled")

        # Toggle center controls
        for widget in [center_scale, center_transparency, center_rotation, center_scale_value, center_transparency_value, center_rotation_value]:
            widget.configure(state="normal" if center_enabled else "disabled")

    # Watermark File
    tk.Label(watermark_frame, text="Watermark File:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    watermark_path_entry = tk.Entry(watermark_frame, width=40)
    watermark_path_entry.insert(0, config.get("watermark_path", ""))
    watermark_path_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    options["watermark_path"] = watermark_path_entry

    def browse_watermark_file():
        file = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file:
            watermark_path_entry.delete(0, tk.END)
            watermark_path_entry.insert(0, file)
        toggle_controls()

    browse_button = tk.Button(watermark_frame, text="Browse", command=browse_watermark_file)
    browse_button.grid(row=0, column=2, padx=5, pady=5)

    # Corner Watermark Toggles
    corner_label = tk.LabelFrame(watermark_frame, text="Corner Watermark Controls", padx=10, pady=10)
    corner_label.grid(row=1, column=0, columnspan=3, padx=5, pady=10, sticky="ew")

    position_icons = {
        "top left": "icons/topleft.png",
        "top right": "icons/topright.png",
        "bottom left": "icons/bottomleft.png",
        "bottom right": "icons/bottomright.png",
    }

    corner_position_vars = {}
    position_frame = tk.Frame(corner_label)
    position_frame.grid(row=0, column=0, columnspan=3, pady=5, sticky="ew")
    options["corner_position_vars"] = corner_position_vars

    # Initialize the corner watermark positions based on the config
    for idx, (pos, icon_path) in enumerate(position_icons.items()):
        try:
            icon = tk.PhotoImage(file=icon_path)
            options["icons"].append(icon)  # Store the icon to prevent garbage collection
            var = tk.BooleanVar(value=pos in config["corner_watermark_positions"])  # Set True if the position is in the list
            corner_position_vars[pos] = var
            tk.Checkbutton(
                position_frame,
                image=icon,
                variable=var,
                indicatoron=False,
                command=toggle_controls,
            ).grid(row=0, column=idx, padx=5)
        except tk.TclError:
            print(f"Error loading icon for {pos}. Check if the file exists: {icon_path}")

    # Corner Watermark Scale and Transparency
    tk.Label(corner_label, text="Corner Watermark Scale (%):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    corner_watermark_scale = tk.Scale(corner_label, from_=10, to=100, orient="horizontal", length=300)
    corner_watermark_scale.set(config.get("corner_watermark_scale", 70))
    corner_watermark_scale.grid(row=1, column=1, padx=5, pady=5)
    corner_scale_value = tk.Entry(corner_label, width=4)
    corner_scale_value.insert(0, corner_watermark_scale.get())
    corner_scale_value.grid(row=1, column=2, padx=5, pady=5)

    # Link the slider to the number box
    def update_scale_value_from_slider(val):
        corner_scale_value.delete(0, tk.END)
        corner_scale_value.insert(0, val)

    corner_watermark_scale.config(command=update_scale_value_from_slider)

    # Update slider value from the number box
    def update_slider_from_entry(event):
        try:
            val = int(corner_scale_value.get())
            if 10 <= val <= 100:
                corner_watermark_scale.set(val)
        except ValueError:
            pass

    corner_scale_value.bind("<KeyRelease>", update_slider_from_entry)

    options["corner_watermark_scale"] = corner_watermark_scale

    tk.Label(corner_label, text="Corner Watermark Transparency (%):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    corner_watermark_transparency = tk.Scale(corner_label, from_=0, to=100, orient="horizontal", length=300)
    corner_watermark_transparency.set(config.get("corner_watermark_transparency", 100))
    corner_watermark_transparency.grid(row=2, column=1, padx=5, pady=5)
    corner_transparency_value = tk.Entry(corner_label, width=4)
    corner_transparency_value.insert(0, corner_watermark_transparency.get())
    corner_transparency_value.grid(row=2, column=2, padx=5, pady=5)

    # Link the transparency slider to the number box
    def update_transparency_value_from_slider(val):
        corner_transparency_value.delete(0, tk.END)
        corner_transparency_value.insert(0, val)

    corner_watermark_transparency.config(command=update_transparency_value_from_slider)

    # Update transparency slider from the number box
    def update_transparency_slider_from_entry(event):
        try:
            val = int(corner_transparency_value.get())
            if 0 <= val <= 100:
                corner_watermark_transparency.set(val)
        except ValueError:
            pass

    corner_transparency_value.bind("<KeyRelease>", update_transparency_slider_from_entry)

    options["corner_watermark_transparency"] = corner_watermark_transparency

    # Center Watermark Toggles
    center_label = tk.LabelFrame(watermark_frame, text="Center Watermark Controls", padx=10, pady=10)
    center_label.grid(row=2, column=0, columnspan=3, padx=5, pady=10, sticky="ew")

    try:
        center_icon = tk.PhotoImage(file="icons/center.png")
        options["icons"].append(center_icon)  # Store the icon to prevent garbage collection
        center_watermark_var = tk.BooleanVar(value=config.get("center_watermark_enabled", False))
        center_button = tk.Checkbutton(center_label, image=center_icon, variable=center_watermark_var, indicatoron=False, command=toggle_controls)
        center_button.grid(row=0, column=0, padx=5, sticky="w")  # Aligned to the left
        options["center_watermark_var"] = center_watermark_var
    except tk.TclError:
        print("Error loading icon for center watermark. Check if 'icons/center.png' exists.")

    tk.Label(center_label, text="Center Watermark Scale (%):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    center_scale = tk.Scale(center_label, from_=10, to=100, orient="horizontal", length=300)
    center_scale.set(config.get("center_watermark_scale", 70))
    center_scale.grid(row=1, column=1, padx=5, pady=5)
    center_scale_value = tk.Entry(center_label, width=4)
    center_scale_value.insert(0, center_scale.get())
    center_scale_value.grid(row=1, column=2, padx=5, pady=5)
    options["center_watermark_scale"] = center_scale

    # Link the center scale slider to the number box
    def update_center_scale_value_from_slider(val):
        center_scale_value.delete(0, tk.END)
        center_scale_value.insert(0, val)

    center_scale.config(command=update_center_scale_value_from_slider)

    # Update center scale slider from the number box
    def update_center_slider_from_entry(event):
        try:
            val = int(center_scale_value.get())
            if 10 <= val <= 100:
                center_scale.set(val)
        except ValueError:
            pass

    center_scale_value.bind("<KeyRelease>", update_center_slider_from_entry)

    tk.Label(center_label, text="Center Watermark Transparency (%):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    center_transparency = tk.Scale(center_label, from_=0, to=100, orient="horizontal", length=300)
    center_transparency.set(config.get("center_watermark_transparency", 100))
    center_transparency.grid(row=2, column=1, padx=5, pady=5)
    center_transparency_value = tk.Entry(center_label, width=4)
    center_transparency_value.insert(0, center_transparency.get())
    center_transparency_value.grid(row=2, column=2, padx=5, pady=5)
    options["center_watermark_transparency"] = center_transparency

    # Link the center transparency slider to the number box
    def update_center_transparency_value_from_slider(val):
        center_transparency_value.delete(0, tk.END)
        center_transparency_value.insert(0, val)

    center_transparency.config(command=update_center_transparency_value_from_slider)

    # Update center transparency slider from the number box
    def update_center_transparency_slider_from_entry(event):
        try:
            val = int(center_transparency_value.get())
            if 0 <= val <= 100:
                center_transparency.set(val)
        except ValueError:
            pass

    center_transparency_value.bind("<KeyRelease>", update_center_transparency_slider_from_entry)

    # Center Watermark Rotation
    tk.Label(center_label, text="Center Watermark Rotation (°):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    center_rotation = tk.Scale(center_label, from_=0, to=359, orient="horizontal", length=300)
    center_rotation.set(config.get("center_watermark_rotation", 0))
    center_rotation.grid(row=3, column=1, padx=5, pady=5)
    center_rotation_value = tk.Entry(center_label, width=4)
    center_rotation_value.insert(0, center_rotation.get())
    center_rotation_value.grid(row=3, column=2, padx=5, pady=5)
    options["center_watermark_rotation"] = center_rotation

    # Link the center rotation slider to the number box
    def update_center_rotation_value_from_slider(val):
        center_rotation_value.delete(0, tk.END)
        center_rotation_value.insert(0, val)

    center_rotation.config(command=update_center_rotation_value_from_slider)

    # Update center rotation slider from the number box
    def update_center_rotation_slider_from_entry(event):
        try:
            val = int(center_rotation_value.get())
            if 0 <= val <= 359:
                center_rotation.set(val)
        except ValueError:
            pass

    center_rotation_value.bind("<KeyRelease>", update_center_rotation_slider_from_entry)

    toggle_controls()
    return start_row + 3

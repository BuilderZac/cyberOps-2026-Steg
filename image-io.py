import os
from typing import List, Optional
from PIL import Image

DEFAULT_OUTPUT_DIR = "output"

# Load an image from disk by path and return a PIL Image in RGB format.
def load_image(image_path: str) -> Image.Image:
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    return Image.open(image_path).convert("RGB")

# Save a PIL Image.

# - Defaults to "output/" if no directory is provided
# - Automatically creates the directory if needed
# - Saves as PNG if no extension is given

# Returns the full path of the saved file as a string.
def save_image(
    image: Image.Image,
    filename: str,
    output_dir: Optional[str] = None
) -> str:
    if not isinstance(image, Image.Image):
        raise TypeError("Expected a PIL Image object")

    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR

    # Create directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Add .png if no extension is provided
    if "." not in filename:
        filename += ".png"

    full_path = os.path.join(output_dir, filename)

    image.save(full_path)

    return full_path

# Save multiple images as: out1.png, out2.png, ...
# Defaults to "output/" directory if none is provided.
# Returns a list of the saved file paths.
def save_images(
    images: List[Image.Image],
    output_dir: Optional[str] = None,
    prefix: str = "out"
) -> List[str]:
    if not images:
        raise ValueError("No images to save")

    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR

    saved_paths = []

    for i, img in enumerate(images, start=1):
        filename = f"{prefix}{i}.png"
        path = save_image(img, filename, output_dir)
        saved_paths.append(path)

    return saved_paths
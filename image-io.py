import os
from typing import List, Optional
from PIL import Image, UnidentifiedImageError


DEFAULT_OUTPUT_DIR = "output"
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp"}
MAX_WIDTH = 5000
MAX_HEIGHT = 5000


def load_image(image_path: str) -> Image.Image:
    """
    Load an image from disk, validate it, and return a PIL Image in RGB format.
    """
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    ext = os.path.splitext(image_path)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext}")

    try:
        with Image.open(image_path) as img:
            img.verify()
    except (UnidentifiedImageError, OSError) as e:
        raise ValueError(f"Invalid or corrupted image file: {e}")

    img = Image.open(image_path).convert("RGB")

    width, height = img.size
    if width <= 0 or height <= 0:
        raise ValueError("Image dimensions must be greater than zero")

    if width > MAX_WIDTH or height > MAX_HEIGHT:
        raise ValueError(
            f"Image dimensions exceed allowed maximum of "
            f"{MAX_WIDTH}x{MAX_HEIGHT}"
        )

    return img


def _sanitize_filename(filename: str) -> str:
    """
    Remove directory components and enforce a safe filename.
    """
    filename = os.path.basename(filename)

    if not filename:
        raise ValueError("Filename cannot be empty")

    if "." not in filename:
        filename += ".png"

    return filename


def save_image(
    image: Image.Image,
    filename: str,
    output_dir: Optional[str] = None
) -> str:
    """
    Save a PIL Image safely to disk.
    """
    if not isinstance(image, Image.Image):
        raise TypeError("Expected a PIL Image object")

    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR

    filename = _sanitize_filename(filename)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    full_path = os.path.join(output_dir, filename)
    image.save(full_path)

    return full_path


def save_images(
    images: List[Image.Image],
    output_dir: Optional[str] = None,
    prefix: str = "share"
) -> List[str]:
    """
    Save multiple PIL Images safely.
    """
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

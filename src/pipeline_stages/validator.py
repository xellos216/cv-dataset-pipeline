import logging
import shutil
from pathlib import Path
from typing import Dict, List

from PIL import Image, UnidentifiedImageError
from tqdm import tqdm

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def is_image_file(file_path: Path) -> bool:
    return file_path.is_file() and file_path.suffix.lower() in VALID_EXTENSIONS


def collect_image_files(input_dir: Path) -> List[Path]:
    return [path for path in input_dir.rglob("*") if is_image_file(path)]


def is_valid_image(file_path: Path) -> bool:
    try:
        with Image.open(file_path) as img:
            img.verify()
        with Image.open(file_path) as img:
            img.load()
        return True
    except (UnidentifiedImageError, OSError, ValueError):
        return False


def validate_images(input_dir: Path, output_dir: Path) -> Dict[str, int]:
    output_dir.mkdir(parents=True, exist_ok=True)

    image_files = collect_image_files(input_dir)

    if not image_files:
        logging.warning("No image files found in input directory: %s", input_dir)
        return {
            "total_found": 0,
            "valid_count": 0,
            "invalid_count": 0,
        }

    valid_count = 0
    invalid_count = 0

    logging.info("Found %d image files for validation", len(image_files))

    for image_path in tqdm(image_files, desc="Validating images"):
        if is_valid_image(image_path):
            destination = output_dir / image_path.name
            shutil.copy2(image_path, destination)
            valid_count += 1
        else:
            logging.warning("Invalid image skipped: %s", image_path)
            invalid_count += 1

    return {
        "total_found": len(image_files),
        "valid_count": valid_count,
        "invalid_count": invalid_count,
    }

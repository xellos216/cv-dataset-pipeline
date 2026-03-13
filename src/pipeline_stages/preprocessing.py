import logging
from pathlib import Path
from typing import Dict, List

from PIL import Image
from tqdm import tqdm

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def collect_image_files(input_dir: Path) -> List[Path]:
    return [
        path
        for path in input_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in VALID_EXTENSIONS
    ]


def preprocess_images(
    input_dir: Path,
    output_dir: Path,
    target_size: tuple[int, int] = (256, 256),
) -> Dict[str, int]:
    output_dir.mkdir(parents=True, exist_ok=True)

    image_files = collect_image_files(input_dir)

    if not image_files:
        logging.warning("No images found for preprocessing in: %s", input_dir)
        return {
            "total_found": 0,
            "processed_count": 0,
            "failed_count": 0,
        }

    processed_count = 0
    failed_count = 0

    logging.info("Found %d validated images for preprocessing", len(image_files))

    for image_path in tqdm(image_files, desc="Preprocessing images"):
        try:
            with Image.open(image_path) as img:
                img = img.convert("RGB")
                img = img.resize(target_size)

                output_filename = f"{image_path.stem}.jpg"
                output_path = output_dir / output_filename

                img.save(output_path, format="JPEG", quality=95)

                processed_count += 1

        except (OSError, ValueError) as e:
            logging.warning("Failed to preprocess image: %s | %s", image_path, e)
            failed_count += 1

    return {
        "total_found": len(image_files),
        "processed_count": processed_count,
        "failed_count": failed_count,
    }

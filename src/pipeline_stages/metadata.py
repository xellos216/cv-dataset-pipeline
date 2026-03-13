import logging
from pathlib import Path
from typing import Dict, List

import pandas as pd
from PIL import Image
from tqdm import tqdm

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def collect_image_files(input_dir: Path) -> List[Path]:
    return [
        path
        for path in input_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in VALID_EXTENSIONS
    ]


def generate_metadata(input_dir: Path, output_dir: Path) -> Dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)

    image_files = collect_image_files(input_dir)

    if not image_files:
        logging.warning("No images found for metadata generation in: %s", input_dir)
        return {
            "total_found": 0,
            "metadata_count": 0,
            "failed_count": 0,
            "csv_path": None,
        }

    records = []
    failed_count = 0

    logging.info("Found %d processed images for metadata generation", len(image_files))

    for image_path in tqdm(image_files, desc="Generating metadata"):
        try:
            with Image.open(image_path) as img:
                record = {
                    "file_name": image_path.name,
                    "file_path": str(image_path.resolve()),
                    "width": img.width,
                    "height": img.height,
                    "mode": img.mode,
                    "format": img.format,
                    "file_size_bytes": image_path.stat().st_size,
                }
                records.append(record)

        except (OSError, ValueError) as e:
            logging.warning("Failed to read metadata: %s | %s", image_path, e)
            failed_count += 1

    df = pd.DataFrame(records)
    csv_path = output_dir / "metadata.csv"
    df.to_csv(csv_path, index=False)

    return {
        "total_found": len(image_files),
        "metadata_count": len(records),
        "failed_count": failed_count,
        "csv_path": str(csv_path),
    }

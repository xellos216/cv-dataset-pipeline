import logging
import random
import shutil
from pathlib import Path
from typing import Dict, List

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def collect_image_files(input_dir: Path) -> List[Path]:
    return [
        path
        for path in input_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in VALID_EXTENSIONS
    ]


def split_dataset(
    input_dir: Path,
    output_dir: Path,
    train_ratio: float = 0.7,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    random_seed: int = 42,
) -> Dict[str, int]:
    if round(train_ratio + val_ratio + test_ratio, 5) != 1.0:
        raise ValueError("train_ratio + val_ratio + test_ratio must equal 1.0")

    image_files = collect_image_files(input_dir)

    if not image_files:
        logging.warning("No images found for dataset split in: %s", input_dir)
        return {
            "total_found": 0,
            "train_count": 0,
            "val_count": 0,
            "test_count": 0,
        }

    train_dir = output_dir / "train"
    val_dir = output_dir / "val"
    test_dir = output_dir / "test"

    train_dir.mkdir(parents=True, exist_ok=True)
    val_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)

    shuffled_files = image_files[:]
    random.Random(random_seed).shuffle(shuffled_files)

    total_count = len(shuffled_files)
    train_end = int(total_count * train_ratio)
    val_end = train_end + int(total_count * val_ratio)

    train_files = shuffled_files[:train_end]
    val_files = shuffled_files[train_end:val_end]
    test_files = shuffled_files[val_end:]

    for image_path in train_files:
        shutil.copy2(image_path, train_dir / image_path.name)

    for image_path in val_files:
        shutil.copy2(image_path, val_dir / image_path.name)

    for image_path in test_files:
        shutil.copy2(image_path, test_dir / image_path.name)

    logging.info(
        "Dataset split completed | train: %d | val: %d | test: %d",
        len(train_files),
        len(val_files),
        len(test_files),
    )

    return {
        "total_found": total_count,
        "train_count": len(train_files),
        "val_count": len(val_files),
        "test_count": len(test_files),
    }

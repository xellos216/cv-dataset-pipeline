import logging
from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd


def generate_dataset_statistics(
    metadata_csv_path: Path, output_dir: Path
) -> Dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)

    if not metadata_csv_path.exists():
        raise FileNotFoundError(f"Metadata CSV does not exist: {metadata_csv_path}")

    df = pd.read_csv(metadata_csv_path)

    if df.empty:
        logging.warning("Metadata CSV is empty: %s", metadata_csv_path)
        return {
            "image_count": 0,
            "summary_path": None,
            "generated_plots": 0,
        }

    image_count = len(df)
    avg_width = df["width"].mean()
    avg_height = df["height"].mean()
    avg_file_size = df["file_size_bytes"].mean()
    min_width = df["width"].min()
    max_width = df["width"].max()
    min_height = df["height"].min()
    max_height = df["height"].max()

    summary_path = output_dir / "summary.txt"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("Computer Vision Dataset Statistics\n")
        f.write("=" * 40 + "\n")
        f.write(f"Total images: {image_count}\n")
        f.write(f"Average width: {avg_width:.2f}\n")
        f.write(f"Average height: {avg_height:.2f}\n")
        f.write(f"Average file size (bytes): {avg_file_size:.2f}\n")
        f.write(f"Minimum width: {min_width}\n")
        f.write(f"Maximum width: {max_width}\n")
        f.write(f"Minimum height: {min_height}\n")
        f.write(f"Maximum height: {max_height}\n")

    width_plot_path = output_dir / "width_distribution.png"
    plt.figure(figsize=(8, 5))
    plt.hist(df["width"], bins=10)
    plt.title("Width Distribution")
    plt.xlabel("Width")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(width_plot_path)
    plt.close()

    height_plot_path = output_dir / "height_distribution.png"
    plt.figure(figsize=(8, 5))
    plt.hist(df["height"], bins=10)
    plt.title("Height Distribution")
    plt.xlabel("Height")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(height_plot_path)
    plt.close()

    file_size_plot_path = output_dir / "file_size_distribution.png"
    plt.figure(figsize=(8, 5))
    plt.hist(df["file_size_bytes"], bins=10)
    plt.title("File Size Distribution")
    plt.xlabel("File Size (bytes)")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(file_size_plot_path)
    plt.close()

    logging.info("Dataset statistics generated at: %s", output_dir)

    return {
        "image_count": image_count,
        "summary_path": str(summary_path),
        "generated_plots": 3,
    }

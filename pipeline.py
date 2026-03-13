import argparse
import logging
from pathlib import Path

from src.pipeline_stages.metadata import generate_metadata
from src.pipeline_stages.preprocessing import preprocess_images
from src.pipeline_stages.splitter import split_dataset
from src.pipeline_stages.stats import generate_dataset_statistics
from src.pipeline_stages.validator import validate_images


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Computer Vision Dataset Pipeline")
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to raw input image dataset",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Path to output directory",
    )
    return parser.parse_args()


def main() -> None:
    setup_logging()
    args = parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)

    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")

    validated_dir = output_dir / "validated"
    processed_dir = output_dir / "processed"
    metadata_dir = output_dir / "metadata"
    splits_dir = output_dir / "splits"
    stats_dir = output_dir / "stats"
    logs_dir = output_dir / "logs"

    validated_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)
    metadata_dir.mkdir(parents=True, exist_ok=True)
    splits_dir.mkdir(parents=True, exist_ok=True)
    stats_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    logging.info("Starting dataset pipeline")
    logging.info(f"Input directory: {input_dir}")
    logging.info(f"Output directory: {output_dir}")

    validation_result = validate_images(
        input_dir=input_dir,
        output_dir=validated_dir,
    )

    logging.info("Validation stage completed")
    logging.info(
        "Valid images: %d | Invalid files: %d",
        validation_result["valid_count"],
        validation_result["invalid_count"],
    )

    preprocessing_result = preprocess_images(
        input_dir=validated_dir,
        output_dir=processed_dir,
        target_size=(256, 256),
    )

    logging.info("Preprocessing stage completed")
    logging.info(
        "Processed images: %d | Failed preprocessing: %d",
        preprocessing_result["processed_count"],
        preprocessing_result["failed_count"],
    )

    metadata_result = generate_metadata(
        input_dir=processed_dir,
        output_dir=metadata_dir,
    )

    logging.info("Metadata generation stage completed")
    logging.info(
        "Metadata rows: %d | Failed metadata reads: %d",
        metadata_result["metadata_count"],
        metadata_result["failed_count"],
    )
    logging.info("Metadata CSV saved to: %s", metadata_result["csv_path"])

    split_result = split_dataset(
        input_dir=processed_dir,
        output_dir=splits_dir,
        train_ratio=0.7,
        val_ratio=0.15,
        test_ratio=0.15,
        random_seed=42,
    )

    logging.info("Dataset split stage completed")
    logging.info(
        "Train: %d | Val: %d | Test: %d",
        split_result["train_count"],
        split_result["val_count"],
        split_result["test_count"],
    )

    stats_result = generate_dataset_statistics(
        metadata_csv_path=metadata_dir / "metadata.csv",
        output_dir=stats_dir,
    )

    logging.info("Statistics stage completed")
    logging.info(
        "Statistics generated for %d images | Plots created: %d",
        stats_result["image_count"],
        stats_result["generated_plots"],
    )
    logging.info("Statistics summary saved to: %s", stats_result["summary_path"])

    logging.info("Pipeline finished successfully")


if __name__ == "__main__":
    main()

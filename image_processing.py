import argparse
import os
import sys
from pathlib import Path

from experiments.inverted import process_inverted
from experiments.color_bands import process_color_bands
from experiments.monochrome import process_monochrome
from experiments.no_gps import process_no_gps
from experiments.noise import process_noise
from experiments.perspective import process_perspective
from experiments.tilt import process_tilt
from experiments.timestamp import process_timestamp


def validate_directory(path):
    if not os.path.isdir(path):
        print(f"Error: {path} is not a valid directory.")
        sys.exit(1)
    return path


def validate_percentage(value):
    ivalue = int(value)
    if ivalue < 0 or ivalue > 100:
        raise argparse.ArgumentTypeError(f"{value} is an invalid percentage value. Must be between 0 and 100.")
    return ivalue


def validate_degrees(value):
    ivalue = int(value)
    if ivalue < 0 or ivalue > 180:
        raise argparse.ArgumentTypeError(f"{value} is an invalid angle value. Must be between 0 and 180.")
    return ivalue


def validate_iso_date(date_string):
    try:
        from datetime import datetime
        datetime.fromisoformat(date_string)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{date_string} is not a valid ISO date.")
    return date_string


def main():
    parser = argparse.ArgumentParser(description="Experiment with photogrammetry images.")

    # Input and output directories
    parser.add_argument("-i", "--input", required=True, type=validate_directory,
                        help="Path to the input directory containing *.jpg, *.jpeg images.")
    parser.add_argument("-o", "--output", required=True, type=str,
                        help="Path to the output directory where processed images will be saved.")

    # Experiment selection
    parser.add_argument("-e", "--experiment", required=True,
                        choices=["color-bands", "monochrome", "inverted", "no-gps",
                                 "timestamp", "noise", "perspective", "tilt"],
                        help="Select the experiment to perform on the images.")

    # Color bands options
    parser.add_argument("-b", "--bands-to-keep", type=str, choices=["r", "g", "b", "rg", "rb", "gb", "rgb"], default="rgb",
                        help="Specify which color bands to keep for the color bands experiment.")

    # Inverted options
    parser.add_argument("-f", "--flip", type=validate_percentage, default=0,
                        help="Percentage of images to flip vertically.")
    parser.add_argument("-m", "--mirror", type=validate_percentage, default=0,
                        help="Percentage of images to mirror horizontally.")

    # No-GPS/Monochrome options
    parser.add_argument("-p", "--percentage", type=validate_percentage, default=0,
                        help="Percentage of images to change. Applies to monochrome, no-gps, perspective, and tilt.")

    # Timestamp options
    parser.add_argument("--start-date", type=validate_iso_date,
                        help="Start date (ISO format) for random timestamp assignment.")
    parser.add_argument("--end-date", type=validate_iso_date,
                        help="End date (ISO format) for random timestamp assignment.")

    # Noise options
    parser.add_argument("--noise-level", type=validate_percentage, default=0,
                        help="Percentage of images to add noise to.")

    # Perspective options
    parser.add_argument("-w", "--warp-by", type=validate_percentage, default=0,
                        help="Percentage of images to warp perspective for. 20% is significant.")

    # Tilt options
    parser.add_argument("-t", "--max-tilt", type=validate_degrees, default=0,
                        help="Max tilt angle in degrees for the tilt experiment.")

    args = parser.parse_args()

    # Additional validation
    if args.experiment == "color-bands" and args.bands_to_keep not in ["r", "g", "b", "rg", "rb", "gb", "rgb"]:
        print("Error: Invalid value for --bands-to-keep. Must be one of 'r', 'g', 'b', 'rg', 'rb', 'gb', or 'rgb'.")
        sys.exit(1)

    if args.experiment == "timestamp" and (not args.start_date or not args.end_date):
        print("Error: --start-date and --end-date are required for the 'timestamp' experiment.")
        sys.exit(1)

    if args.flip + args.mirror > 100:
        print("Error: The sum of --flip and --mirror percentages cannot exceed 100.")
        sys.exit(1)

    # Collect all image files from the input directory with specified types
    image_extensions = ['.jpg', '.jpeg', '.JPG', '.JPEG']
    input_images = []
    for ext in image_extensions:
        input_images.extend(list(Path(args.input).glob(f"*{ext}")))

    # Create output directory if it doesn't exist
    Path(args.output).mkdir(parents=True, exist_ok=True)

    # Execute the selected experiment
    if args.experiment == "color-bands":
        process_color_bands(input_images, args.output, args.bands_to_keep)
    if args.experiment == "monochrome":
        process_monochrome(input_images, args.output, args.percentage)
    elif args.experiment == "inverted":
        process_inverted(input_images, args.output, args.flip, args.mirror)
    elif args.experiment == "no-gps":
        process_no_gps(input_images, args.output, args.percentage)
    elif args.experiment == "timestamp":
        process_timestamp(input_images, args.output, args.start_date, args.end_date)
    elif args.experiment == "noise":
        process_noise(input_images, args.output, args.noise_level)
    elif args.experiment == "perspective":
        process_perspective(input_images, args.output, args.percentage, args.warp_by)
    elif args.experiment == "tilt":
        process_tilt(input_images, args.output, args.percentage, args.max_tilt)


if __name__ == "__main__":
    main()


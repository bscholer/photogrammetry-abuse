import random
from pathlib import Path

from PIL import Image
import piexif
from tqdm import tqdm

from util import save_without_thumbnail


def process_no_gps(input_images, output_dir, gps_removal_percentage):
    stats = {
        'gps_removed': 0,
        'unchanged': 0,
    }
    for img_path in tqdm(input_images, desc="Removing GPS data from images"):
        img = Image.open(img_path)
        should_remove_gps = random.random() < gps_removal_percentage / 100

        if should_remove_gps:
            stats['gps_removed'] += 1
            image_name = f"no_gps_{img_path.name}"
        else:
            stats['unchanged'] += 1
            image_name = img_path.name

        output_path = Path(output_dir) / image_name
        save_without_thumbnail(img, output_path, include_gps=not should_remove_gps)

    print("Stats")
    for key, value in stats.items():
        print(f"{key}: {value}")
        #
        # exif_data = img.info.get('exif', None)
        # exif_dict = piexif.load(exif_data) if exif_data else {}
        #
        # # Remove GPS data from a percentage of images
        #     image_name = f"no_gps_{image_name}"
        #     exif_dict.pop('GPS', None)
        #
        # # Save the processed image with the updated EXIF data
        # exif_bytes = piexif.dump(exif_dict)

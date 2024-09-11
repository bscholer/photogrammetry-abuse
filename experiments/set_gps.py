import random
from pathlib import Path

from PIL import Image
import piexif
from tqdm import tqdm

from util import save_without_thumbnail


def process_set_gps(input_images, output_dir, gps_change_percentage, lat=None, lng=None):
    stats = {
        'gps_modified': 0,
        'unchanged': 0,
    }

    for img_path in tqdm(input_images, desc="Processing GPS data for images"):
        img = Image.open(img_path)
        should_modify_gps = random.random() < gps_change_percentage / 100

        if should_modify_gps:
            stats['gps_modified'] += 1
            image_name = f"modified_gps_{img_path.name}"

            # Check if lat or lng are None; if so, set gps_coords to empty tuple to remove GPS
            if lat is None or lng is None:
                gps_coords = ()  # Signal to remove GPS
            else:
                gps_coords = (lat, lng)  # Set GPS to the provided lat/lng
        else:
            stats['unchanged'] += 1
            image_name = img_path.name
            gps_coords = None  # Leave GPS unchanged

        output_path = Path(output_dir) / image_name
        save_without_thumbnail(img, output_path, gps_coords=gps_coords)

    print("Stats")
    for key, value in stats.items():
        print(f"{key}: {value}")


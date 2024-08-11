import random
from pathlib import Path

from PIL import Image
import piexif
from tqdm import tqdm


def process_no_gps(input_images, output_dir, gps_removal_percentage):
    for img_path in tqdm(input_images, desc="Removing GPS data from images"):
        img = Image.open(img_path)
        exif_data = img.info.get('exif', None)
        exif_dict = piexif.load(exif_data) if exif_data else {}
        image_name = img_path.name

        # Remove GPS data from a percentage of images
        if random.random() < gps_removal_percentage / 100:
            image_name = f"no_gps_{image_name}"
            exif_dict.pop('GPS', None)

        # Save the processed image with the updated EXIF data
        exif_bytes = piexif.dump(exif_dict)
        output_path = Path(output_dir) / image_name
        img.save(output_path, exif=exif_bytes)
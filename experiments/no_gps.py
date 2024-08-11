import random
from pathlib import Path

from PIL import Image
import piexif
from tqdm import tqdm


def process_no_gps(input_images, output_dir, gps_removal_percentage):
    for img_path in tqdm(input_images, desc="Removing GPS data from images"):
        img = Image.open(img_path)
        exif_dict = piexif.load(img.info['exif'])

        # Remove GPS data from a percentage of images
        if random.random() < gps_removal_percentage / 100:
            exif_dict.pop('GPS', None)

        # Save the processed image
        exif_bytes = piexif.dump(exif_dict)
        output_path = Path(output_dir) / img_path.name
        img.save(output_path, exif=exif_bytes)

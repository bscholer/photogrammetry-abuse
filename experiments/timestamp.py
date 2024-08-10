import random
from datetime import datetime, timedelta
from pathlib import Path

from PIL import Image
import piexif


def process_timestamp(input_images, output_dir, start_date, end_date):
    start_dt = datetime.fromisoformat(start_date)
    end_dt = datetime.fromisoformat(end_date)

    for img_path in input_images:
        img = Image.open(img_path)
        exif_dict = piexif.load(img.info['exif'])

        # Generate a random timestamp within the given range
        random_dt = start_dt + timedelta(seconds=random.randint(0, int((end_dt - start_dt).total_seconds())))
        timestamp_str = random_dt.strftime("%Y:%m:%d %H:%M:%S")

        # Set the new timestamp in EXIF data
        exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = timestamp_str
        exif_dict['0th'][piexif.ImageIFD.DateTime] = timestamp_str

        # Save the processed image
        exif_bytes = piexif.dump(exif_dict)
        output_path = Path(output_dir) / img_path.name
        img.save(output_path, exif=exif_bytes)

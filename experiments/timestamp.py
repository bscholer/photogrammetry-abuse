import random
from datetime import datetime, timedelta
from pathlib import Path

from PIL import Image
import piexif
from tqdm import tqdm

from util import save_without_thumbnail


def process_timestamp(input_images, output_dir, start_date, end_date):
    start_dt = datetime.fromisoformat(start_date)
    end_dt = datetime.fromisoformat(end_date)

    for img_path in tqdm(input_images, desc="Setting random timestamps for images"):
        img = Image.open(img_path)

        # Generate a random timestamp within the given range
        random_dt = start_dt + timedelta(seconds=random.randint(0, int((end_dt - start_dt).total_seconds())))
        timestamp_str = random_dt.strftime("%Y:%m:%d %H:%M:%S")

        # Save the processed image
        output_path = Path(output_dir) / img_path.name
        save_without_thumbnail(img, output_path, timestamp_str=timestamp_str)

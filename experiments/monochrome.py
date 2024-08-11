import random
from pathlib import Path

from PIL import Image
from tqdm import tqdm

from util import save_without_thumbnail


def process_monochrome(input_images, output_dir, monochrome_percentage):
    stats = {
        'monochrome': 0,
        'unchanged': 0,
    }

    for img_path in tqdm(input_images, desc='Making images monochrome'):
        img = Image.open(img_path)
        filename = img_path.stem
        should_monochrome = random.random() < monochrome_percentage / 100

        if should_monochrome:
            img = img.convert('L')  # Convert image to grayscale (monochrome)
            filename = f"monochrome_{filename}"
            stats['monochrome'] += 1
        else:
            stats['unchanged'] += 1

        # Save the processed image
        output_path = Path(output_dir) / f"{filename}.jpg"
        save_without_thumbnail(img, output_path)

    print("Stats")
    for key, value in stats.items():
        print(f"{key}: {value}")
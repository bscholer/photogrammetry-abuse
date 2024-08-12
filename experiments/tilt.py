import random
from pathlib import Path
from PIL import Image
from tqdm import tqdm
from util import save_without_thumbnail


def process_tilt(input_images, output_dir, tilt_percentage, max_tilt):
    stats = {
        'tilted': 0,
        'unchanged': 0,
    }

    for img_path in tqdm(input_images, desc='Tilting images'):
        img = Image.open(img_path)
        filename = img_path.stem
        should_tilt = random.random() < tilt_percentage / 100

        if should_tilt:
            tilt_angle = random.uniform(-max_tilt, max_tilt)
            img = img.rotate(tilt_angle, expand=True)
            filename = f"tilted_{filename}"
            stats['tilted'] += 1
        else:
            stats['unchanged'] += 1

        # Save the processed image
        output_path = Path(output_dir) / f"{filename}.jpg"
        save_without_thumbnail(img, output_path)

    print("Stats")
    for key, value in stats.items():
        print(f"{key}: {value}")


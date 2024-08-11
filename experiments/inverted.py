import random
from pathlib import Path

from PIL import Image
from tqdm import tqdm

from util import save_without_thumbnail


def process_inverted(input_images, output_dir, flip_percentage, mirror_percentage):
    stats = {
        'flipped': 0,
        'mirrored': 0,
        'flipped_and_mirrored': 0,
        'unchanged': 0,
    }
    for img_path in tqdm(input_images, desc='Inverting images'):
        img = Image.open(img_path)
        filename = img_path.stem
        should_flip = random.random() < flip_percentage / 100
        should_mirror = random.random() < mirror_percentage / 100

        if should_flip and should_mirror:
            img = img.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_LEFT_RIGHT)
            filename = f"flipped_and_mirrored_{filename}"
            stats['flipped_and_mirrored'] += 1

        elif should_flip:
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
            filename = f"flipped_{filename}"
            stats['flipped'] += 1

        elif should_mirror:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
            filename = f"mirrored_{filename}"
            stats['mirrored'] += 1

        else:
            stats['unchanged'] += 1

        # Save the processed image
        output_path = Path(output_dir) / f"{filename}.jpg"
        save_without_thumbnail(img, output_path)

    print("Stats")
    for key, value in stats.items():
        print(f"{key}: {value}")

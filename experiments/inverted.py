import random
from pathlib import Path

from PIL import Image


def process_inverted(input_images, output_dir, flip_percentage, mirror_percentage):
    for img_path in input_images:
        img = Image.open(img_path)
        filename = img_path.stem
        should_flip = random.random() < flip_percentage / 100
        should_mirror = random.random() < mirror_percentage / 100

        if should_flip:
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
            filename = f"flipped_{filename}"

        if should_mirror:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
            filename = f"mirrored_{filename}"

        # Save the processed image
        output_path = Path(output_dir) / f"{filename}.jpg"
        img.save(output_path)

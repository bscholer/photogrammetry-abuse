import random
from pathlib import Path

from PIL import Image
import piexif
from tqdm import tqdm

from util import save_without_pose_metadata


def process_no_pose(input_images, output_dir, pose_removal_percentage):
    stats = {
        'pose_removed': 0,
        'unchanged': 0,
    }

    for img_path in tqdm(input_images, desc="Removing pose metadata from images"):
        img = Image.open(img_path)
        should_remove_pose = random.random() < pose_removal_percentage / 100

        if should_remove_pose:
            stats['pose_removed'] += 1
            image_name = f"no_pose_{img_path.name}"
        else:
            stats['unchanged'] += 1
            image_name = img_path.name

        output_path = Path(output_dir) / image_name
        save_without_pose_metadata(img, output_path, include_pose=not should_remove_pose)

    # Output stats
    print("Stats")
    for key, value in stats.items():
        print(f"{key}: {value}")

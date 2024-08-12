import random
from pathlib import Path
from PIL import Image
from tqdm import tqdm
import numpy as np
from util import save_without_thumbnail


def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = np.array(matrix, dtype=np.float32)
    B = np.array(pb).flatten()

    # Solve the least-squares problem
    coeffs = np.linalg.lstsq(A, B, rcond=None)[0]

    return coeffs


def process_perspective(input_images, output_dir, warp_percentage, warp_by_percentage):
    stats = {
        'warped': 0,
        'unchanged': 0,
    }

    for img_path in tqdm(input_images, desc='Applying perspective warp'):
        img = Image.open(img_path)
        width, height = img.size
        filename = img_path.stem
        should_warp = random.random() < (warp_percentage / 100)

        if should_warp:
            # Define the original corners of the image
            original_points = np.float32([
                [0, 0],
                [width, 0],
                [width, height],
                [0, height]
            ])

            # Apply random shifts to the corners within some percentage of the image size
            warp_by_decimal = warp_by_percentage / 100
            warp_x = lambda: random.uniform(-warp_by_decimal, warp_by_decimal) * width
            warp_y = lambda: random.uniform(-warp_by_decimal, warp_by_decimal) * height

            warped_points = np.float32([
                [warp_x(), warp_y()],
                [width + warp_x(), warp_y()],
                [width + warp_x(), height + warp_y()],
                [warp_x(), height + warp_y()]
            ])

            # Calculate the perspective transform coefficients
            coeffs = find_coeffs(warped_points, original_points)

            # Apply the perspective transformation
            img = img.transform((width, height), Image.PERSPECTIVE, coeffs, resample=Image.BICUBIC)

            filename = f"warped_{filename}"
            stats['warped'] += 1
        else:
            stats['unchanged'] += 1

        # Save the processed image
        output_path = Path(output_dir) / f"{filename}.jpg"
        save_without_thumbnail(img, output_path)

    print("Stats")
    for key, value in stats.items():
        print(f"{key}: {value}")

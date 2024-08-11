from pathlib import Path

from PIL import Image
from tqdm import tqdm


def process_color(input_images, output_dir, bands_to_keep):
    for img_path in tqdm(input_images, desc='Color manipulation'):
        img = Image.open(img_path)
        r, g, b = img.split()

        # Apply the bands to keep
        r = r if 'r' in bands_to_keep else r.point(lambda _: 0)
        g = g if 'g' in bands_to_keep else g.point(lambda _: 0)
        b = b if 'b' in bands_to_keep else b.point(lambda _: 0)

        # Merge back to create a monochrome image
        monochrome_img = Image.merge("RGB", (r, g, b))

        # Save the processed image
        output_path = Path(output_dir) / img_path.name
        monochrome_img.save(output_path)

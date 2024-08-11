from pathlib import Path

import piexif
from PIL import Image
from tqdm import tqdm


def process_color_bands(input_images, output_dir, bands_to_keep):
    for img_path in tqdm(input_images, desc='Color manipulation'):
        img = Image.open(img_path)
        exif_data = piexif.load(img.info.get('exif', b''))

        # Remove thumbnail and preview image data
        if '1st' in exif_data:
            del exif_data['1st']  # Remove thumbnail data

        # Optional: remove specific preview image tags if needed
        # This might be different depending on how the preview images are stored
        if 'Exif' in exif_data:
            exif_exif_ifd = exif_data['Exif']
            if piexif.ExifIFD.MakerNote in exif_exif_ifd:
                del exif_exif_ifd[piexif.ExifIFD.MakerNote]  # Example of removing a specific preview tag

        r, g, b = img.split()

        # Apply the bands to keep
        r = r if 'r' in bands_to_keep else r.point(lambda _: 0)
        g = g if 'g' in bands_to_keep else g.point(lambda _: 0)
        b = b if 'b' in bands_to_keep else b.point(lambda _: 0)

        # Merge back to create the altered image
        recolored_img = Image.merge("RGB", (r, g, b))

        # Save the processed image
        output_path = Path(output_dir) / img_path.name
        # recolored_img.save(output_path)
        exif_filtered = piexif.dump(exif_data)

        recolored_img.save(output_path, exif=exif_filtered)


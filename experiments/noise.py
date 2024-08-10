import random
from pathlib import Path

import numpy as np
from PIL import Image


def process_noise(input_images, output_dir, noise_level):
    for img_path in input_images:
        img = Image.open(img_path)
        img_array = np.array(img)

        # Apply noise to the image
        if noise_level > 0:
            noise = np.random.randint(0, 256, img_array.shape, dtype='uint8')
            img_array = np.clip(img_array + noise * (noise_level / 100), 0, 255).astype('uint8')

        # Save the processed image
        noisy_img = Image.fromarray(img_array)
        output_path = Path(output_dir) / img_path.name
        noisy_img.save(output_path)

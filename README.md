# Photogrammetry Abuse

This repo contains a framework for messing with images in a variety of ways, in an attempt to make DroneDeploy's photogrammetry engine do weird things. 

This doesn't really have much practical purpose, but was really just intended to be a fun experiment.

<img width="1049" alt="image" src="https://github.com/user-attachments/assets/20b6bbf4-74d0-4450-b358-015874574e72">

## Setup

1. Clone this repo
2. Create a virtual environment and install the requirements
```bash
python3 -m venv venv
source venv/bin/activate
```
3. Install the requirements
```bash
pip install -r requirements.txt
```

## Usage

For all options, run
```bash
python3 image_processing.py --help
```

### Color Band Removal

This experiment removes the red, green, or blue color band from an image.

For example, to keep the red and green bands and remove the blue band from a set of images (yielding yellow images), run the following command:
```bash
python3 image_processing.py --experiment color-bands \
--input <directory with images> --output <output directory> \
--bands-to-keep rg
```

### Monochrome

This experiment converts a certain percentage of input images to monochrome (black and white).

For example, to convert 50% of images to monochrome, run the following command:
```bash
python3 image_processing.py --experiment monochrome \
--input <directory with images> --output <output directory> \
--percentage 50
```

### Flipping and Mirroring

This experiment flips and mirrors certain percentages of input images.

For example, to flip 50% of images upside-down, and mirror 25% of images horizontally, run the following command:

```bash
python3 image_processing.py --experiment inverted \
--input <directory with images> --output <output directory> \
--flip 50 --mirror 25
```
_Note: This will result in roughly the following distribution (this is somewhat random):_
- 35 % of the images will be flipped upside-down
- 15 % of the images will be mirrored horizontally
- 10 % of the images will be flipped upside-down **and** mirrored horizontally
- 40 % of the images will be left as is

### Random Noise

This experiment adds random noise to images. The percentage of noise is controlled by the `--noise-level` parameter, which is an integer between 0 and 100.

For example, to add 25% noise to images, run the following command:
```bash
python3 image_processing.py --experiment noise \
--input <directory with images> --output <output directory> \
--noise-level 25
```

### Remove GPS

This experiment removes the GPS data from a certain percentage of input images.

For example, to remove GPS data from 50% of images, run the following command:
```bash
python3 image_processing.py --experiment remove-gps \
--input <directory with images> --output <output directory> \
--percentage 50
```

### Random Timestamps

This experiment adds random timestamps to images, between two provided dates.

For example, to add random timestamps between 2024-01-01 and 2024-01-02 to all the images, run the following command:
```bash
python3 image_processing.py --experiment timestamp \
--input <directory with images> --output <output directory> \
--start-date 2024-01-01 --end-date 2024-01-02
```

### Trying all of them

To try all of the experiments at once, open `test.sh`, and modify the `INPUT_DIR` and `OUTPUT_BASE_DIR` variables to point to the directories with the images you want to process. Then run the script:
```bash
bash test.sh
```
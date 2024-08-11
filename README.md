# Photogrammetry Abuse

This repo contains a framework for messing with images in a variety of ways, in an attempt to make DroneDeploy's photogrammetry engine do weird things. 

This doesn't really have much practical purpose, but was really just intended to be a fun experiment.

![image](https://github.com/user-attachments/assets/2381e001-3f92-4ee0-80aa-714ce7e22a01)

**[Skip to the (surprisingly good) results](#resultant-maps)**

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

## Example images

If you don't have a drone or test dataset, feel free to use these images of Baywatch Resort in Traverse City, MI, flown manually with a Mavic Air 2. Images are licensed under the CC BY (Attribution) license, play around and have fun! If you do something cool, make a PR!

## Resultant Input Images

Here are some samples from the above example dataset, after running them through `test.sh`!

### Original
![DJI_0181](https://github.com/user-attachments/assets/274e9ca4-dc03-4d8d-ad7e-405cae850721)

### Color Band Removal - Removing Blue
![DJI_0181](https://github.com/user-attachments/assets/d8e510b2-f3b4-4e1c-ba98-80d30a3c5705)

### Monochrome
![monochrome_DJI_0181](https://github.com/user-attachments/assets/ec1cca45-6481-4b35-be7f-3c07b06bc1a2)

### Inverted - Flipped
![flipped_DJI_0181](https://github.com/user-attachments/assets/3d21c2cd-afcb-4281-85e5-e7f9170d6793)

### Noise - 50%
![DJI_0181](https://github.com/user-attachments/assets/49d27173-fccc-4025-aa6e-9b47549318ab)

### Remove GPS and Random Timestamps
Both of these experiments only affect metadata, so the images look identical to the original.

## Resultant Maps

These are the results of a handful of experiments!

### Original

Overall, I'm super impressed with how well this map turned out. It isn't hugely surprising given how detailed I was when flying it, but impressive nevertheless!
<img width="982" alt="image" src="https://github.com/user-attachments/assets/fa4d4a22-9f2c-4d6f-ba51-8ed040e96f6b">

### Color Band Removal - Removing Blue

I'm pretty surprised this one turned out as well as it did, but it makes sense. It's just yellow after all!
<img width="828" alt="image" src="https://github.com/user-attachments/assets/55664462-dd01-43ff-b37d-7fdb1289ecbb">

### Color Band Removal - Removing Blue and Green

Similar story to removing blue, but this one turned out just fine, just very red!
<img width="820" alt="image" src="https://github.com/user-attachments/assets/9f1a93ad-9106-475b-a6d4-1532c96b7da7">

### Inverted - 29% Flipped, 24% Mirrored, 21% Flipped and Mirrored

This one is pretty hilarious! I really had no idea what it would do going into this, but the result isn't surprising. Although, the angle of the upside-down model is unexpected.
<img width="1049" alt="image" src="https://github.com/user-attachments/assets/20b6bbf4-74d0-4450-b358-015874574e72">

### Noise - 25%

Besides being a bit lighter looking, this one turned out just fine, much like the original.
<img width="866" alt="image" src="https://github.com/user-attachments/assets/2dd52afb-d1a1-48e3-a4b7-9acf9a03f809">

### Remove GPS and Random Timestamps

Unfortunately, DroneDeploy is too smart, and the uploader doesn't accept images weird spread out timestamps, or images without GPS metadata :(. Might try manually uploading these experiments via the [Map Processing API](https://help.dronedeploy.com/hc/en-us/articles/1500004963742-Map-Processing-API) at some point, but nothing for now.


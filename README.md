# Photogrammetry Abuse

This repo contains a framework for messing with images in a variety of ways, in an attempt to make DroneDeploy's photogrammetry engine do weird things. 

This doesn't really have much practical purpose, but was really just intended to be a fun experiment.

![image](https://github.com/user-attachments/assets/2381e001-3f92-4ee0-80aa-714ce7e22a01)

## Table of Contents
- [Setup](#setup)
- [Usage](#usage)
- [Example Dataset](#example-dataset)
- [Resultant Input Images](#resultant-input-images)
- **[Resultant Maps](#resultant-maps)**

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

This experiment removes the red, green, or blue color band(s) from an image.

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

### Perspective Warp

This experiment warps the perspective of a certain percentage of input images, by randomly selecting 4 points on the image and warping them by a provided `--warp-by` percentage.

For example, to warp 75% of images by 10% (significant), run the following command:
```bash
python3 image_processing.py --experiment perspective \
--input <directory with images> --output <output directory> \
--percentage 75 --warp-by 10
```

### Tilt

This experiment tilts a certain percentage of input images by a random angle, between a specficied minimum and maximum angle, in degrees.

For example, to tilt 75% of images by a random angle between -10 and 10 degrees, run the following command:
```bash
python3 image_processing.py --experiment tilt \
--input <directory with images> --output <output directory> \
--percentage 75 --max-tilt 10
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

## Example Dataset

If you don't have a drone or test dataset, feel free to use these images of Baywatch Resort in Traverse City, MI, flown manually with a Mavic Air 2. Images are licensed under the CC BY (Attribution) license, play around and have fun! If you do something cool, make a PR!

[323 Images of Baywatch Resort](https://drive.google.com/file/d/1W3Sd5vwX_MD4Z8u-N8RYf0VTdni6c4ld/view?usp=drive_link)

## Resultant Input Images

Here are some samples from the above example dataset, after running them through `test.sh`!

### Original Image
![DJI_0181](https://github.com/user-attachments/assets/274e9ca4-dc03-4d8d-ad7e-405cae850721)

### Color Band Removal - Removing Blue
![DJI_0181](https://github.com/user-attachments/assets/d8e510b2-f3b4-4e1c-ba98-80d30a3c5705)

### Monochrome
![monochrome_DJI_0181](https://github.com/user-attachments/assets/ec1cca45-6481-4b35-be7f-3c07b06bc1a2)

### Inverted - Flipped
![flipped_DJI_0181](https://github.com/user-attachments/assets/3d21c2cd-afcb-4281-85e5-e7f9170d6793)

### Noise - 50%
![DJI_0181](https://github.com/user-attachments/assets/49d27173-fccc-4025-aa6e-9b47549318ab)

### Noise - 95%
![DJI_0181](https://github.com/user-attachments/assets/a28e264d-b8b5-49c7-bcf5-2cd26548aee8)

### Perspective Warp - Warp by 10%
![warped_DJI_0181](https://github.com/user-attachments/assets/dbfda71b-5cf4-4e76-bbc0-b1b7985307c2)

### Tilt - Random between -10° and 10°
![tilted_DJI_0181](https://github.com/user-attachments/assets/0b168df3-0f6a-4396-ae2f-f1c6ac0edf61)

### Remove GPS and Random Timestamps
Both of these experiments only affect metadata, so the images look identical to the original.

## Resultant Maps

These are the results of a handful of experiments! Overall, I'm pretty impressed with how well DroneDeploy handled these weird images, and even with some truly bizzare situations, it still managed to stitch them together reasonably well given how screwed up they are.

### Original Map

Overall, I'm super impressed with how well this map turned out. It isn't hugely surprising given how detailed I was when flying it, but impressive nevertheless!
<img width="982" alt="image" src="https://github.com/user-attachments/assets/fa4d4a22-9f2c-4d6f-ba51-8ed040e96f6b">

[Processing Report](https://storage.googleapis.com/dronedeploy-assets-prod/6ed2c63865_C2FDB7A8DCOPENPIPELINE/report.pdf?GoogleAccessId=web-sa-prod@dronedeploy-public.iam.gserviceaccount.com&Expires=1723579200&Signature=GEd3PT/18nVo/lJXmYKTElJgUNOn0mmdhz9PTMNklDj1sSbG9CALVzqmMEiZKb4AvqySKTPamj5qzLJQn7hRUgq9qIWHqTUAzRD1te7OElb3wi6JwqRqd0zaloBu/pNe+YU2FCc++0UMkPvyELVqCo4Rr/xKPcbQCVlBs1oIqB421Dh+xB/PfKt35x9kAhqFMAWqPK/Bh2xHwd3V1jG71UercSt41yk/xf2TPzN1iJLUULFE1lGZX6D3qqJI2XlnqM+DpMhP5qANUUb3/+xvNBln21uaHY+cXCm+xmO+4fZmsSgtfs+/fyz3QMMdcFthUvE4ThkDXD6pvH7hRgPRGA%3D%3D)
 | [View map in DroneDeploy](https://www.dronedeploy.com/app2/sites/66b7f6596bc3a8129fffc9cc/maps/66b8f825c719dc02218e45e1?jwt_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpZCI6IjY2YjhmODM3ZjdlNzBhOWE0NjUxN2YzYyIsInR5cGUiOiJQdWJsaWNTaGFyZVYyIiwiYWNjZXNzX3R5cGUiOiJwbGFuIn0.8YC-TtBYbdvsVtZ1nsI_UrFTGSmC0OaMSGaZoEUGZ68Xw3ZD_-tm9OLiGAn2zVpDWHpzFVnh5Mb02MsKJY6RLg)

### Color Band Removal - Removing Blue

I'm pretty surprised this one turned out as well as it did, but it makes sense. It's just yellow after all!
<img width="828" alt="image" src="https://github.com/user-attachments/assets/55664462-dd01-43ff-b37d-7fdb1289ecbb">

[Processing Report](https://storage.googleapis.com/dronedeploy-assets-prod/1c9d2fe3bc_C2FDB7A8DCOPENPIPELINE/report.pdf?GoogleAccessId=web-sa-prod@dronedeploy-public.iam.gserviceaccount.com&Expires=1723579200&Signature=EDYWUy7xjtpAKZKW6hznembTCliDHD1OeboscpMIrrXJMMUG/gtjmdmWqj51LvdeTfXmL0+2G6sf4ppX8I5Ww7gGQx/sMHDkf2/aunXH8fCUCd3dOiyxPxzJVC4CkKAksfazgGXlrs0FQO09Rmrm1VhGPmIIYK2/m2CYerwgclwnzDTh0QNQ0zNw7rkdOzAXYyTr4BMGSO38z9gqV+5w8dJUntW0PL+FMiolwv95+pWtxe+F1teJwkqydepBy2/EzzjqEdJGUBSokzbjAR86Vn8vwowoEkcepEFdfuix7y92bgAN3OTWEE6J/WfhIrnr0tCaAvno2N+Iz3o5yv6qRw%3D%3D)
 | [View map in DroneDeploy](https://www.dronedeploy.com/app2/sites/66b7f6596bc3a8129fffc9cc/maps/66b8ef7fc719dc02218e45d5?jwt_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpZCI6IjY2YjhlZjgyYTJhYWMxZGE3ZWI5NGMwYyIsInR5cGUiOiJQdWJsaWNTaGFyZVYyIiwiYWNjZXNzX3R5cGUiOiJwbGFuIn0.97dA5bUsaLJind9kO-fFa5faGVR9v6qTBdMcjmqAr63d2JIXwxV8Nw75eQraVd7y1SX9M8BvpjPG0_ousKhiPg)

### Color Band Removal - Removing Blue and Green

Similar story to removing blue, but this one turned out just fine, just very red!
<img width="820" alt="image" src="https://github.com/user-attachments/assets/9f1a93ad-9106-475b-a6d4-1532c96b7da7">

[Processing Report](https://storage.googleapis.com/dronedeploy-assets-prod/a1dec20914_C2FDB7A8DCOPENPIPELINE/report.pdf?GoogleAccessId=web-sa-prod@dronedeploy-public.iam.gserviceaccount.com&Expires=1723579200&Signature=LymhCAG5wPVFu5ggjh2o2sIYZHcFy40l7Q33P4O4TKEWdlLfrL9bZXnCU1G5doPfBrRdmh9KseBQnt64HwVA9hdiCqn5qsUriD0EIA0FoZLAO52aepvKwab043PrF1XdTfBFU/iq7GhZYl03ysbeFgfhfG6R0KrD+vwyDo5POg47dLtcEx8SCaj4f2QNFSrmEFYzfHfOl++lvgQLWKottaKacyI/17p9pzJ/h89IKE3+kklhy/q0k3BY9qUT5Heuk8FuPjDQu1bAPHWQR61i8MIND9U8wBdthiIZ2cvstScFj8urDUEIB1pYEUDYjuouxMxQZgGNVILG23aRPd52SQ%3D%3D)
 | [View map in DroneDeploy](https://www.dronedeploy.com/app2/sites/66b7f6596bc3a8129fffc9cc/maps/66b8fe23c719dc02218e45e3?jwt_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpZCI6IjY2YjhmZTI1ZTkxNDBjZmI1ZDNmOTkxYiIsInR5cGUiOiJQdWJsaWNTaGFyZVYyIiwiYWNjZXNzX3R5cGUiOiJwbGFuIn0.lNfE56qAGqXqmoG05tarj_yaFLBMGpLdxZAAQZF37KWj5-9AKu_49WIkKWC8RoPGvpFgfHfBxgRv6-_iyTgvtQ)

### Monochrome - 50% of images

Not all that surprising, but there are gray splotches throughout the map, but it looks like the stitcher had no problem with it!
<img width="835" alt="image" src="https://github.com/user-attachments/assets/52a09e22-ebba-4dc4-9990-6f34b0dabd53">

[Processing Report](https://storage.googleapis.com/dronedeploy-assets-prod/78d2cfde3d_C2FDB7A8DCOPENPIPELINE/report.pdf?GoogleAccessId=web-sa-prod@dronedeploy-public.iam.gserviceaccount.com&Expires=1723579200&Signature=U+RY4dIKKrQR+BKKGzxuNiMK2HiNL1AbB6o2kVVkJVdHl9A9KZIeQhotaV4tTZPgsqCdHYiwoBh/7iQWadWwXLThUXnawbXsgVfqsD4WMPbzOZpLxuBJDpnJiiPXCN5CthXDxWbo6N5cPWEAPVOu+NNVIiruUVAvTYW8ZLpS1uypDYNQrluC5fZs0j0glplb+xIOSI9g90W6zGBKZdss81wHIOg81gNr+08IuYIE2gdoFj72ZJKw/jkcyF71VNO62QvFlHKzVXJ3G1ce0lIzb+Gb+cQ/JzoXs43gs0t5Ht7avMdz0197+9Cf0+EgsabQUJbQkpV9AUHwAtSl/mNCjA%3D%3D)
 | [View map in DroneDeploy](https://www.dronedeploy.com/app2/sites/66b7f6596bc3a8129fffc9cc/maps/66b8f6cbc719dc02218e45df?jwt_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpZCI6IjY2YjhmNmNmZGMwOTcwNjQxZDU2NDNiMSIsInR5cGUiOiJQdWJsaWNTaGFyZVYyIiwiYWNjZXNzX3R5cGUiOiJwbGFuIn0.D_8C_piQ_jYxBbFqVbrilynquNQPM32KhylCDcZMCZh3WQJsnWA5zQSBIPeMsmbUkN3YGvO5tTDk493VbkKmpw)

### Inverted - 29% Flipped, 24% Mirrored, 21% Flipped and Mirrored

This one is pretty hilarious! I really had no idea what it would do going into this, but the result isn't surprising. Although, the angle of the upside-down model is unexpected.
<img width="1049" alt="image" src="https://github.com/user-attachments/assets/20b6bbf4-74d0-4450-b358-015874574e72">

[Processing Report](https://storage.googleapis.com/dronedeploy-assets-prod/19f351806c_C2FDB7A8DCOPENPIPELINE/report.pdf?GoogleAccessId=web-sa-prod@dronedeploy-public.iam.gserviceaccount.com&Expires=1723579200&Signature=wXQvTRCj0NMJf6NLWIeCoSORfRCof2B98blKURm8x80XWTTrMTil+REFb9milENsbqXm/FPI9lE/H52oVnA74K4soNn9aJ+8G21VyKWRAeEfjQzMobi/g5Y+bxRr7V+/5f9Q2rIqMX4QH6z+2vlE3plCdkzQVil1NcGMRrSRLLxDtLbMvkTnlwmXzMVr6pBdA14nUw7u2/2kHbh/WcdSocav0kmWn/5oNk1XCUX6ESyvwXa97hnbfOLGPgqju/IFMyLkbNCOnuXTcoQ7o5nC1ONWFFbEtC0dud6MPAl9KX0Z/FJMHNpuZX3qdI37//vz/+Er58VNn2PQyxw2qyHbNw%3D%3D)
 | [View map in DroneDeploy](https://www.dronedeploy.com/app2/sites/66b7f6596bc3a8129fffc9cc/maps/66b8f075c719dc02218e45d7?jwt_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpZCI6IjY2YjhmMDc5OWViOWM2MjI4Nzc4NGQ1OCIsInR5cGUiOiJQdWJsaWNTaGFyZVYyIiwiYWNjZXNzX3R5cGUiOiJwbGFuIn0.ds5DA7b5bIgvLxMwl8wDd9qMLfqiOpChQ7xu615jd4MT0MiSOwtQ6JvtHsRA7SrGnt9saizo2TNMRkP4XHC98w)

### Noise - 25%

Besides being a bit lighter looking, this one turned out just fine, much like the original.
<img width="866" alt="image" src="https://github.com/user-attachments/assets/2dd52afb-d1a1-48e3-a4b7-9acf9a03f809">

[Processing Report](https://storage.googleapis.com/dronedeploy-assets-prod/aae9b27395_C2FDB7A8DCOPENPIPELINE/report.pdf?GoogleAccessId=web-sa-prod@dronedeploy-public.iam.gserviceaccount.com&Expires=1723579200&Signature=cUtEQoGPzv6qBnzEx8FDfLilkt5itbwpPGqeQWjlIWo/xL/NH/yzjrchsmp5oYsM29IIcP8k6j2Po+EZTb7LocC9cxf/cpHqOzJo0QmVfTafj5/DondI0Ur0T4QhbSaL7bN3ThQA9kU3vYNLnjbV73BHuVGsSdlGNVuSAKmiWlzafGAYFHhu4QLKQtwz+EDMSBdPcuAKUZXghOgbp5FuCzixt97MiG6DK3BjkFCUa9x1/rpZsG+B52oC0Es7i2qfWzxGoW4GmQAMkwl9WN/z7LEJtPCaXwwHb9n+ga+SvI0mkM4F2bTWkQ3FO5zjPW0pzOCW9P/59Qywunq3wDtK8g%3D%3D)
 | [View map in DroneDeploy](https://www.dronedeploy.com/app2/sites/66b7f6596bc3a8129fffc9cc/maps/66b8f368c719dc02218e45dd?jwt_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpZCI6IjY2YjhmMzZlZjg2ZDU1MDljYTE4ZDZmMyIsInR5cGUiOiJQdWJsaWNTaGFyZVYyIiwiYWNjZXNzX3R5cGUiOiJwbGFuIn0.mPvyRcUm8JfRKxYktV6aKrpmrZlpWC0Z8uWJxf0_LK_fUKTLoR2uEAiZXkzbUJ89gN_dtWGNB3BsLxxTARFqsA)

### Noise - 75%

While not _bad_, there is a noticeable degredadation in quality here, as we see this large hole on the side of the building, and an overall decrease in quality from [Noise - 25%](#noise---25), and certainly from the [Original](#original-map).
<img width="673" alt="image" src="https://github.com/user-attachments/assets/e1ef42d3-4b8d-4a40-b6ce-8589a480044d">

[Processing Report](https://storage.googleapis.com/dronedeploy-assets-prod/90a36b2b7d_C2FDB7A8DCOPENPIPELINE/report.pdf?GoogleAccessId=web-sa-prod@dronedeploy-public.iam.gserviceaccount.com&Expires=1723604400&Signature=k/UoUFiUK3FI0jRUAljOftOOEj06Ox7hWzswRPMrZfPKL0+ZBU0p0K5bjZRXQPNyK9q6XY4WtrSIVuMKm3j5ylyOLvjCre/3Qhqt6VMXgiMwRNk9qAI/r58GGXnhoDDmoIGllhbSjlc5XAMPzapVEI4tpFJDR/vDPpIf0BLECfC2uVtaIID1IXQYxuBOwACJ1XKkwt5/Luy2QSSb7L20NDKmYFLdRsRAP8DnKsu+gqIwsw4EiM7OGYK3FjIcpDyfO4qQT+zGclgM01hVTbv2XQqFr7ll6LJf1D34dyK/k1fsla/iseh39gpIcWhoSIZAohaqIv3X2+UmYBLK7j8Nlg%3D%3D)
 | [View map in DroneDeploy](https://www.dronedeploy.com/app2/sites/66b7f6596bc3a8129fffc9cc/maps/66b90c05d00fbf3cb863f5aa?jwt_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpZCI6IjY2YjkwYzBiZTQ1YjBmZjlhOGY0OGQ4NCIsInR5cGUiOiJQdWJsaWNTaGFyZVYyIiwiYWNjZXNzX3R5cGUiOiJwbGFuIn0.7uScjyZaoXNOwdBD6oFMBi3VtoIBnwgka-deDKWsxJOJgVSEmqo3I0pkuOSBrTc2J40P7cBARyeteiXxRT8pwA)

### Perspective Warp - 5% Warp on 50% of Images

It feels like I'm finally getting somewhere with breaking photogrammetry! Although, that said, this is still a pretty decent result for some pretty fouled up images. I'm impressed that it seems to have mostly ignored the black borders around the photos, although you can see some odd coloration on the roof..

 <img width="750" alt="image" src="https://github.com/user-attachments/assets/a0f418dd-d9ae-45da-bbe0-8ea9f8672020">

 [Processing Report](https://storage.googleapis.com/dronedeploy-assets-prod/a7ab1f6fcf_C2FDB7A8DCOPENPIPELINE/report.pdf?GoogleAccessId=web-sa-prod@dronedeploy-public.iam.gserviceaccount.com&Expires=1723644000&Signature=aHCrqK5Nr33OaDlCXLpmLiPuf4SrZpejzXqpHIvo3MkIa51sKlOLm2PIeBAzuTDesz6g7+btdMP6gqSYcWkWkuNl0+UMGyKhQ5qWKNIUWFixp11qnchMKl1P62L1bZJXFA7i4958vG2zrOhcYXP2uKcpOX+sS7ziOj1m24aEtBTOeOIjbN6ResUAJFXtWAP3y1QWypznvv0Oea8dDBhJAswu/sngwQ1YfXMwFJBiHRUlzj6PYYg1SyQ5/M1kpFudyVMbv2QFJmrkf8sEaRNZ4Fk5mKT8GMqs1B4chlBxGqkd+zYi9is6TFBSaYjsd4FIXQCnBhGf0lDtD5nuM1g04g%3D%3D)
  | [View map in DroneDeploy](https://www.dronedeploy.com/app2/sites/66b7f6596bc3a8129fffc9cc/maps/66b98f0ee42b6a0674e79d03?jwt_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpZCI6IjY2Yjk4ZjExYTJhYWMxZGE3ZWI5NGQ1NSIsInR5cGUiOiJQdWJsaWNTaGFyZVYyIiwiYWNjZXNzX3R5cGUiOiJwbGFuIn0.M2lgvzcl9HaEuRdGPrzOC3GXsC8qXOKyNSvEgVf3MyQfwSRWyWh-ChSBQOcU9RT0P-FDKaiF8bGxoLyXDDNhcw)

### Perspective Warp - 10% Warp on 75% of Images

Seems like perspective warp will really do a number on photogrammetry! This map looks pretty terrible compared to the [original](#original-map)!

<img width="682" alt="image" src="https://github.com/user-attachments/assets/27b896ef-a1e1-442a-8cbd-d9e2901f42d3">

[Processing Report](https://storage.googleapis.com/dronedeploy-assets-prod/bc8ceec662_C2FDB7A8DCOPENPIPELINE/report.pdf?GoogleAccessId=web-sa-prod@dronedeploy-public.iam.gserviceaccount.com&Expires=1723644000&Signature=BIFUThFGteUs3fiLOWpnlW9+G6YHfcZqa9fyAHaAcmgIbdswrs3vyIqS90aVARzPomFUkda9QAjDytWAoJsGYTMNB50AbW6zSsuM05UbEJVhjowQUABtKaDqTRmk2Qich/W3I7mN+J3s2VpdgoOwyNUhgwMroixWbj47zo5nEwBECZvHJ0xbGRwhQyCdmTqB+Q5K2R3/7NaPVQ58s/Sq33KINnPupVD8eAZOOXgroLCWE1jRHms1bhzK+gdAqSM4ZakRrM5RB3MsJqWIVbh2TJYiLNeqKsqIa5cmKgicp/kql57MA4dDNw2rwglFNpsZra1uPMhQ80DNC6fANy8pZQ%3D%3D)
 | [View map in DroneDeploy](https://www.dronedeploy.com/app2/sites/66b7f6596bc3a8129fffc9cc/maps/66b99003e42b6a0674e79d05?jwt_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpZCI6IjY2Yjk5MDA2ZjI4M2MwY2U3ZTgzOWQ5MiIsInR5cGUiOiJQdWJsaWNTaGFyZVYyIiwiYWNjZXNzX3R5cGUiOiJwbGFuIn0.CF6L0NSrACtC0VKzn7drhm16McSFfscdK5muAuNucVYw1DysAlJTRWbbJu__Dr2iiOOB2gyxMbrRUs705I4Y8A)

### Tilt - Between -10° and 10° - 75% of Images

Interestingly, this model turned out surprisingly good! However, you can really clearly see the black boundaries from the photo painted onto the roof. We see a bit of this on the perspective warp experiments, but we see it in full effect here!

<img width="824" alt="image" src="https://github.com/user-attachments/assets/119c9dd8-164f-42ab-ba30-4e70e46a36c2">

[Processing Report](https://storage.googleapis.com/dronedeploy-assets-prod/3d062ed320_C2FDB7A8DCOPENPIPELINE/report.pdf?GoogleAccessId=web-sa-prod@dronedeploy-public.iam.gserviceaccount.com&Expires=1723644000&Signature=HpwQlpto2KtiDrstXUcHjSdMv+6EIAM5W8Znb0+kMe9vGOJ1hafsXlAiFF+E8Jkp3lQGPe5huvtW4R6YBfh3rmCXRIjIuATjZgtOlGZnZnc24D0fS0W1RAbrQZtlBXiG3ha7rrHIuHs/fmFkTY7f5nNB8nOq54xAWpjTdk+O7A66Rc6DM09UxIz3zGm5br+x6z8FADFJQSwLxmXUcIdHw4vjB6mNk/gmqCX6EOedREBHl/76CkYYItvOtvlvpqNEFwLbKAjKPaFWNgGF+zrFHtrKk0tYn3+2CeHjSGRCxcXOeXkKwADcoBcWmUsbYoHYeuEh1pIuf5HOYg4rV7acqw%3D%3D)
 | [View map in DroneDeploy](https://www.dronedeploy.com/app2/sites/66b7f6596bc3a8129fffc9cc/maps/66b99754e42b6a0674e79d07?jwt_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpZCI6IjY2Yjk5NzU1MTdkZDkzMjJhNjQxMzc5NCIsInR5cGUiOiJQdWJsaWNTaGFyZVYyIiwiYWNjZXNzX3R5cGUiOiJwbGFuIn0.PcyOfdQ9Mz5LNx3k-pihNWWk8I-G26Mu9uvoFkF01iW0oo5h8RaLxeJW8AreW8NAWt4HGZurfF86P9z3OR_UBQ)

### Remove GPS and Random Timestamps

Unfortunately, DroneDeploy is too smart, and the uploader doesn't accept images weird spread out timestamps, or images without GPS metadata :(. Might try manually uploading these experiments via the [Map Processing API](https://help.dronedeploy.com/hc/en-us/articles/1500004963742-Map-Processing-API) at some point, but nothing for now.


import pytest
from pathlib import Path
from PIL import Image
import os
import shutil
import tempfile
import random
import numpy as np
from datetime import datetime

# Assume we have implemented these functions in our script
from image_processing import process_color, process_inverted, process_no_gps, process_timestamp, process_noise


# Fixtures for setting up temporary directories and files
@pytest.fixture
def setup_temp_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def setup_sample_images(setup_temp_dir):
    image_paths = []
    for i in range(5):  # Create 5 sample images
        img = Image.new('RGB', (100, 100), color=(i * 50, i * 50, i * 50))
        path = Path(setup_temp_dir) / f"image_{i}.jpg"
        img.save(path)
        image_paths.append(path)
    return image_paths


@pytest.mark.parametrize("bands_to_keep, expected_color", [
    ("r", (50, 0, 0)),
    ("g", (0, 50, 0)),
    ("b", (0, 0, 50)),
    ("rg", (50, 50, 0)),
    ("rgb", (50, 50, 50)),
])
def test_process_monochrome(setup_sample_images, setup_temp_dir, bands_to_keep, expected_color):
    output_dir = Path(setup_temp_dir) / "output"
    os.makedirs(output_dir, exist_ok=True)

    process_color(setup_sample_images, output_dir, bands_to_keep)

    for i, image_path in enumerate(Path(output_dir).glob("*.jpg")):
        img = Image.open(image_path)
        pixels = np.array(img)
        assert np.all(pixels == expected_color)


@pytest.mark.parametrize("flip_percentage, mirror_percentage", [
    (0, 0),
    (100, 0),
    (0, 100),
    (50, 50),
])
def test_process_inverted(setup_sample_images, setup_temp_dir, flip_percentage, mirror_percentage):
    output_dir = Path(setup_temp_dir) / "output"
    os.makedirs(output_dir, exist_ok=True)

    process_inverted(setup_sample_images, output_dir, flip_percentage, mirror_percentage)

    flipped = sum(1 for _ in Path(output_dir).glob("flipped*.jpg"))
    mirrored = sum(1 for _ in Path(output_dir).glob("mirrored*.jpg"))

    assert flipped == (flip_percentage / 100) * len(setup_sample_images)
    assert mirrored == (mirror_percentage / 100) * len(setup_sample_images)


@pytest.mark.parametrize("gps_removal_percentage", [
    (0),
    (100),
    (50),
])
def test_process_no_gps(setup_sample_images, setup_temp_dir, gps_removal_percentage):
    output_dir = Path(setup_temp_dir) / "output"
    os.makedirs(output_dir, exist_ok=True)

    process_no_gps(setup_sample_images, output_dir, gps_removal_percentage)

    for image_path in Path(output_dir).glob("*.jpg"):
        exif_data = {}  # Fetch EXIF data here
        has_gps = 'GPSInfo' in exif_data
        if random.random() < gps_removal_percentage / 100:
            assert not has_gps
        else:
            assert has_gps


@pytest.mark.parametrize("start_date, end_date", [
    ("2024-01-01", "2024-01-31"),
    ("2024-06-01", "2024-06-30"),
])
def test_process_timestamp(setup_sample_images, setup_temp_dir, start_date, end_date):
    output_dir = Path(setup_temp_dir) / "output"
    os.makedirs(output_dir, exist_ok=True)

    process_timestamp(setup_sample_images, output_dir, start_date, end_date)

    start_dt = datetime.fromisoformat(start_date)
    end_dt = datetime.fromisoformat(end_date)

    for image_path in Path(output_dir).glob("*.jpg"):
        exif_data = {}  # Fetch EXIF data here
        timestamp = exif_data.get('DateTime')
        timestamp_dt = datetime.strptime(timestamp, "%Y:%m:%d %H:%M:%S")
        assert start_dt <= timestamp_dt <= end_dt


@pytest.mark.parametrize("noise_level", [
    (0),
    (50),
    (100),
])
def test_process_noise(setup_sample_images, setup_temp_dir, noise_level):
    output_dir = Path(setup_temp_dir) / "output"
    os.makedirs(output_dir, exist_ok=True)

    process_noise(setup_sample_images, output_dir, noise_level)

    for image_path in Path(output_dir).glob("*.jpg"):
        img = Image.open(image_path)
        pixels = np.array(img)
        # Assuming the noise is added and we check for variability
        if noise_level > 0:
            assert np.std(pixels) > 0
        else:
            assert np.std(pixels) == 0

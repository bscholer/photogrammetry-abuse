import random
from pathlib import Path
from pyproj import Geod

from PIL import Image
import piexif
from tqdm import tqdm

from util import save_without_thumbnail

# Initialize a Geod object for calculations (WGS84 ellipsoid)
geod = Geod(ellps="WGS84")


def process_set_gps(input_images, output_dir, gps_change_percentage, lat=None, lng=None, max_wiggle=0.0):
    stats = {
        'gps_modified': 0,
        'unchanged': 0,
    }

    def wiggle_coordinates(lat, lng, max_wiggle_meters):
        """Apply a random wiggle to the coordinates by up to max_wiggle_meters."""
        if max_wiggle_meters == 0.0:
            return lat, lng  # No wiggle if max_wiggle_meters is zero
        
        # Randomly pick a direction (bearing) and distance within the wiggle range
        bearing = random.uniform(0, 360)
        distance = random.uniform(0, max_wiggle_meters)
        
        # Calculate the new coordinates after moving by the random distance and bearing
        new_lng, new_lat, _ = geod.fwd(lng, lat, bearing, distance)
        return new_lat, new_lng

    for img_path in tqdm(input_images, desc="Processing GPS data for images"):
        img = Image.open(img_path)
        should_modify_gps = random.random() < gps_change_percentage / 100

        if should_modify_gps:
            stats['gps_modified'] += 1
            image_name = f"modified_gps_{img_path.name}"

            # Check if lat or lng are None; if so, set gps_coords to empty tuple to remove GPS
            if lat is None or lng is None:
                gps_coords = ()  # Signal to remove GPS
            else:
                # Apply random wiggle to lat/lng, if max_wiggle is set
                new_lat, new_lng = wiggle_coordinates(lat, lng, max_wiggle)
                gps_coords = (new_lat, new_lng)
        else:
            stats['unchanged'] += 1
            image_name = img_path.name
            gps_coords = None  # Leave GPS unchanged

        output_path = Path(output_dir) / image_name
        save_without_thumbnail(img, output_path, gps_coords=gps_coords)

    print("Stats")
    for key, value in stats.items():
        print(f"{key}: {value}")


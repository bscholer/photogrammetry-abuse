from pathlib import Path
import zipfile
from PIL import Image
import os
import piexif
from shapely.geometry import Point, MultiPoint
from fileio_wrapper import Fileio

from util import collect_images, _convert_to_decimal
import requests

def read_image_gps_metadata(image_paths) -> MultiPoint:
    # Read GPS metadata from images
    print("Reading GPS metadata from images...")
    gps_data = []
    for image in [str(p) for p in image_paths]:
        # Read GPS metadata from the image
        img = Image.open(image)
        exif_data = piexif.load(img.info.get('exif', b''))
        
        # Get the GPS coordinates and reference (N/S for latitude, E/W for longitude)
        lat = exif_data['GPS'][piexif.GPSIFD.GPSLatitude]
        lat_ref = exif_data['GPS'][piexif.GPSIFD.GPSLatitudeRef].decode('utf-8')
        lon = exif_data['GPS'][piexif.GPSIFD.GPSLongitude]
        lon_ref = exif_data['GPS'][piexif.GPSIFD.GPSLongitudeRef].decode('utf-8')

        # Convert to decimal format
        latitude = _convert_to_decimal(lat, lat_ref)
        longitude = _convert_to_decimal(lon, lon_ref)
        
        # Make a shapely point from the GPS
        point = Point(longitude, latitude)
        gps_data.append(point)

    print("GPS metadata read successfully.")
    return MultiPoint(gps_data)

def upload_as_zip(output_path, images) -> str:
    # Zip all the images
    print("Zipping images...")
    zip_path = Path(output_path).with_suffix(".zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for img in images:
            zipf.write(img, img.name)

    # Use file.io to upload the zip file
    print("Uploading zip file...")
    resp = Fileio.upload(zip_path)
    success = resp['success']
    if not success:
        print(f"Error uploading zip file: {resp['error']}, exiting.")
        exit(1)
    link = f"{resp['link']}.zip"
    return link


def upload_to_dd(project_id, output_path, plan_name="default"):
    # Collect all image files from the input directory with specified types
    images = collect_images(output_path)
    print(f"Uploading {len(images)} images to DroneDeploy project {project_id} and plan {plan_name}...")

    points = read_image_gps_metadata(images)
    # Buffer of degrees because I'm lazy
    polygon = points.convex_hull.buffer(0.0001).simplify(0.000001)

    zip_url = upload_as_zip(output_path, images)

    base_url = "https://public-api.dronedeploy.com"
    api_key = os.getenv("DD_API_KEY")
    # Create the plan
    geometry = [{"lat": lat, "lng": lng} for lng, lat in polygon.exterior.coords]

    plan_url = f"{base_url}/v2/plans?api_key={api_key}"
    plan_payload = {
        "name": plan_name,
        "geometry": geometry,
        "folder_id": project_id,
        "workflow": {
            "job_type": "3d",
            "quality": 9,
        }
    }

    response = requests.post(plan_url, json=plan_payload)
    if response.status_code >= 400:
        print(f"Error creating plan: {response.text}")
        return
    plan_id = response.json().get("id")

    # Create an image transfer
    transfer_url = f"{base_url}/v2/image_transfer?api_key={api_key}"
    transfer_payload = {
        "plan_id": plan_id,
        "transport": {"type": "https"},
        "inputs": [
            {
                "location": zip_url,
                "type": "map_source_image"
            }
        ]
    }
    transfer_response = requests.post(transfer_url, json=transfer_payload)
    if transfer_response.status_code >= 400:
        print(f"Error creating image transfer: {transfer_response.text}")
        return
    print("Image transfer and plan created successfully, processing should begin shortly.")
    print(f"Use this link after processing is complete: https://www.dronedeploy.com/app2/sites/{project_id}/maps/{plan_id}")

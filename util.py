import piexif


def save_without_thumbnail(img, output_path, gps_coords=None, timestamp_str=None):
    """
    Save an image without thumbnail and preview image data, and optionally update GPS and timestamp metadata.

    :param img: PIL.Image object
    :param output_path: str, path to save the output image
    :param gps_coords: tuple, (latitude, longitude) to update GPS metadata, or None to maintain GPS data. An empty tuple () will remove GPS data.
    :param timestamp_str: str, new timestamp in ISO format, or None to maintain the original timestamp
    """
    exif_data = piexif.load(img.info.get('exif', b''))

    # Handle GPS data based on gps_coords
    if gps_coords == ():  # Remove GPS data if gps_coords is an empty tuple
        if 'GPS' in exif_data:
            del exif_data['GPS']
    elif gps_coords is not None:  # Replace GPS data with provided lat/lng if gps_coords is not None
        lat, lng = gps_coords
        gps_ifd = {
            piexif.GPSIFD.GPSLatitudeRef: 'N' if lat >= 0 else 'S',
            piexif.GPSIFD.GPSLatitude: _convert_to_dms(abs(lat)),
            piexif.GPSIFD.GPSLongitudeRef: 'E' if lng >= 0 else 'W',
            piexif.GPSIFD.GPSLongitude: _convert_to_dms(abs(lng))
        }

        # Preserve the altitude if it exists
        if 'GPS' in exif_data and piexif.GPSIFD.GPSAltitude in exif_data['GPS']:
            gps_ifd[piexif.GPSIFD.GPSAltitude] = exif_data['GPS'][piexif.GPSIFD.GPSAltitude]
            gps_ifd[piexif.GPSIFD.GPSAltitudeRef] = exif_data['GPS'][piexif.GPSIFD.GPSAltitudeRef]

        exif_data['GPS'] = gps_ifd

    # Remove thumbnail and preview image data
    if '1st' in exif_data:
        del exif_data['1st']  # Remove thumbnail data

    # Optional: remove specific preview image tags if needed
    # This might be different depending on how the preview images are stored
    if 'Exif' in exif_data:
        exif_exif_ifd = exif_data['Exif']
        if piexif.ExifIFD.MakerNote in exif_exif_ifd:
            del exif_exif_ifd[piexif.ExifIFD.MakerNote]  # Example of removing a specific preview tag

    # Set the new timestamp if provided
    if timestamp_str:
        exif_data['Exif'][piexif.ExifIFD.DateTimeOriginal] = timestamp_str
        exif_data['0th'][piexif.ImageIFD.DateTime] = timestamp_str

    exif_filtered = piexif.dump(exif_data)

    img.save(output_path, exif=exif_filtered)


def save_without_pose_metadata(img, output_path, include_pose=True, timestamp_str=None):
    exif_data = piexif.load(img.info.get('exif', b''))

    # Remove pose-related metadata if include_pose is False
    if not include_pose:
        if '0th' in exif_data:
            # Remove Orientation
            if piexif.ImageIFD.Orientation in exif_data['0th']:
                del exif_data['0th'][piexif.ImageIFD.Orientation]

        if 'Exif' in exif_data:
            exif_exif_ifd = exif_data['Exif']

            # Remove Gimbal-related metadata if stored in MakerNote or proprietary fields
            if piexif.ExifIFD.MakerNote in exif_exif_ifd:
                # Parse MakerNote for specific entries like Gimbal and Flight data (if they exist)
                maker_note = exif_exif_ifd[piexif.ExifIFD.MakerNote]
                # Example of deleting pose-related data from MakerNote (specific structure depends on the camera)
                if b'Gimbal Degree' in maker_note:
                    del maker_note[b'Gimbal Degree']
                if b'Flight Degree' in maker_note:
                    del maker_note[b'Flight Degree']
                if b'Gimbal Roll Degree' in maker_note:
                    del maker_note[b'Gimbal Roll Degree']
                if b'Gimbal Yaw Degree' in maker_note:
                    del maker_note[b'Gimbal Yaw Degree']
                if b'Gimbal Pitch Degree' in maker_note:
                    del maker_note[b'Gimbal Pitch Degree']
                if b'Flight Roll Degree' in maker_note:
                    del maker_note[b'Flight Roll Degree']
                if b'Flight Yaw Degree' in maker_note:
                    del maker_note[b'Flight Yaw Degree']
                if b'Flight Pitch Degree' in maker_note:
                    del maker_note[b'Flight Pitch Degree']

    # Remove thumbnail and preview image data (optional)
    if '1st' in exif_data:
        del exif_data['1st']  # Remove thumbnail data

    # Set the new timestamp if provided
    if timestamp_str:
        exif_data['Exif'][piexif.ExifIFD.DateTimeOriginal] = timestamp_str
        exif_data['0th'][piexif.ImageIFD.DateTime] = timestamp_str

    exif_filtered = piexif.dump(exif_data)
    img.save(output_path, exif=exif_filtered)


def _convert_to_dms(value):
    """Convert latitude/longitude to degrees, minutes, seconds format."""
    degrees = int(value)
    minutes = int((value - degrees) * 60)
    seconds = (value - degrees - minutes / 60) * 3600
    return [(degrees, 1), (minutes, 1), (int(seconds * 100), 100)]

import piexif


def save_without_thumbnail(img, output_path, include_gps=True, timestamp_str=None):
    exif_data = piexif.load(img.info.get('exif', b''))

    # Remove GPS data if include_gps is False
    if not include_gps and 'GPS' in exif_data:
        del exif_data['GPS']

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


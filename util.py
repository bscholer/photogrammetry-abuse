import piexif


def save_without_thumbnail(img, output_path, include_gps=True):
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

    exif_filtered = piexif.dump(exif_data)

    img.save(output_path, exif=exif_filtered)

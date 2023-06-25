import base64
import sys
import uuid

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import SuspiciousOperation

from moviepy.video.io.VideoFileClip import VideoFileClip
from PIL import Image
from io import BytesIO


def to_file(file_string):
    """base64 encoded file to Django InMemoryUploadedFile that can be placed into request.FILES."""
    try:
        idx = file_string[:50].find(',')

        valid_file = file_string.startswith('data:image/') or file_string.startswith('data:video/')

        if not idx or not valid_file:
            raise Exception()

        base64file = file_string[idx + 1:]
        attributes = file_string[:idx]
        content_type = attributes[len('data:'):attributes.find(';')]
    except Exception:
        raise SuspiciousOperation("Invalid picture")

    f = BytesIO(base64.b64decode(base64file))
    ext = content_type.split('/')[1]
    image = InMemoryUploadedFile(
        f,
        field_name='picture',
        name=str(uuid.uuid4()) + ext,
        content_type=content_type,
        size=sys.getsizeof(f),
        charset=None)
    return image


def generate_thumbnail(file_path):
    """ with a mp4 video generates an image and return as base64"""
    start_time = 5

    clip = VideoFileClip(file_path)
    frame = clip.get_frame(start_time)

    image = Image.fromarray(frame)

    buffer = BytesIO()
    image.save(buffer, format='JPEG')
    image_base64 = 'data:image/jpeg;base64,' + base64.b64encode(buffer.getvalue()).decode('utf-8')

    return image_base64

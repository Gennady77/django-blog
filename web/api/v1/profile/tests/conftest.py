from base64 import b64decode

import pytest
from django.core.files.base import ContentFile

raw_image: str = (
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAQMAAAAl21bKAAA'
    'AA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjYAAAAAIAAeIhvDMAAAAASUVORK5CYII='
)

@pytest.fixture()
def image_content_file() -> ContentFile:
    _format, _raw_image = raw_image.split(';base64,')
    ext = _format.split('/')[-1]
    return ContentFile(b64decode(_raw_image), name=f'image.{ext}')

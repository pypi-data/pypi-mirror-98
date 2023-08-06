import os
import mimetypes

from dialog_api import messaging_pb2
from dialog_bot_sdk.utils import get_image_w_h, get_image_thumb_bytes


def get_document_content(file, location):
    """Prepares DocumentMessage object that contains metadata for file sending request.

    :param file: path to file
    :param location: FileLocation object
    :return: DocumentMessage object
    """

    content = messaging_pb2.DocumentMessage()

    content.file_id = location.file_id
    content.access_hash = location.access_hash
    content.name = os.path.basename(file)
    content.file_size = os.path.getsize(file)

    return content


def get_image_content(file, location):
    """Same as get_document_content for image sending.

    :param file: path to image
    :param location: FileLocation object
    :return: DocumentMessage object
    """

    content = get_document_content(file, location)

    content.mime_type = mimetypes.guess_type(file)[0]
    content.thumb.w, content.thumb.h, content.thumb.thumb = get_image_thumb_bytes(file)

    ext = messaging_pb2.DocumentEx()

    photo = messaging_pb2.DocumentExPhoto()
    photo.w, photo.h = get_image_w_h(file)
    ext.photo.CopyFrom(photo)
    content.ext.CopyFrom(ext)

    return content

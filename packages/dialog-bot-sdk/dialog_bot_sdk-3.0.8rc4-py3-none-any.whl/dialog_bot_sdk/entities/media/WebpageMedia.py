from dialog_api import messaging_pb2
from google.protobuf.wrappers_pb2 import StringValue

from dialog_bot_sdk.entities.media.ImageMedia import ImageLocation


class WebPageMedia:
    def __init__(self, url: str, title: str = "", description: str = "", image: ImageLocation = None):
        self.url = url
        self.title = title
        self.description = description
        self.image = image

    def to_api(self) -> messaging_pb2.WebpageMedia:
        if self.image is not None:
            image = self.image.to_api()
        else:
            image = None
        return messaging_pb2.WebpageMedia(url=StringValue(value=self.url), title=StringValue(value=self.title),
                                          description=StringValue(value=self.description), image=image)

    @classmethod
    def from_api(cls, web_page: messaging_pb2.WebpageMedia) -> 'WebPageMedia':
        return cls(web_page.url, web_page.title, web_page.description, ImageLocation.from_api(web_page.image))

    def __dict__(self):
        return {"url": self.url, "title": self.title, "description": self.description, "image": self.image.__dict__()}

    def __str__(self):
        return "WebPageMedia({})".format(self.__dict__())

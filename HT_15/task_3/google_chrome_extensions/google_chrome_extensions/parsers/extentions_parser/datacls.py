from dataclasses import dataclass


@dataclass
class SitemapItem:
    location: str


@dataclass
class LocationItem:
    location: str


@dataclass
class ExtensionInfo:
    extension_id: str
    location: str
    short_description: str
    title: str

    def dict(self):
        return self.__dict__


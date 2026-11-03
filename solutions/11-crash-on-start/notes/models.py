from dataclasses import dataclass, field
from notes.text import slugify


@dataclass
class Note:
    title: str
    tags: list = field(default_factory=list)
    body: str = ""

    @property
    def slug(self):
        return slugify(self.title)

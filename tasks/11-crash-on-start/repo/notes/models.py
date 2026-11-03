from dataclasses import dataclass, field
from notes.storage import slugify


@dataclass
class Note:
    title: str
    tags: list[str] = field(default_factory=list)
    body: str = ""

    @property
    def slug(self) -> str:
        return slugify(self.title)

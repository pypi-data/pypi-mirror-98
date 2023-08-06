import attr
from bs4 import Tag


@attr.dataclass(slots=True)
class Profile:
    nama: str
    ttl: str
    pendidikan: str
    sekolah_induk: str
    email: str
    email_terverifikasi: bool
    alamat: str

    @classmethod
    def from_panel(cls, tag: Tag) -> "Profile":
        # /html/body/div[2]/div[2]/div[1]/div[1]/div
        pass

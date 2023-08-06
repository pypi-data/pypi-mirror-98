from bs4 import Tag
from dataclasses import dataclass


@dataclass
class StatusNuptk:
    nuptk: str
    nama: str
    tempat_lahir: str
    tanggal_lahir: str
    nama_ibu_kandung: str
    nip: str
    nik: str
    instansi: str
    kab_kota: str

    @classmethod
    def from_fit_arsip_nuptk(cls, tag: Tag) -> "StatusNuptk":
        # #fit_ArsipNuptk
        pass

import attr
from bs4 import Tag
from typing import List


@attr.dataclass(slots=True)
class PeriodePembayaran:
    tw: int
    bulan: str


@attr.dataclass(slots=True)
class BankPenyalur:
    nomor_rekening: str
    nama_pemegang_rekening: str
    nama_bank: str
    cabang_bank: str


@attr.dataclass(slots=True)
class RealisasiSktp:
    no: int
    periode: PeriodePembayaran
    bank_penyalur: BankPenyalur

    @classmethod
    def from_fit_realisasi_sktp(cls, tag: Tag) -> List["RealisasiSktp"]:
        # #fit_RealisasiBayarSKTP
        pass

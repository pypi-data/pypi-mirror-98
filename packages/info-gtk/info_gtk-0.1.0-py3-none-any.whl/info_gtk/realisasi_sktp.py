from bs4 import Tag
from dataclasses import dataclass
from typing import List


@dataclass
class PeriodePembayaran:
    tw: int
    bulan: str


@dataclass
class BankPenyalur:
    nomor_rekening: str
    nama_pemegang_rekening: str
    nama_bank: str
    cabang_bank: str


@dataclass
class RealisasiSktp:
    no: int
    periode: PeriodePembayaran
    bank_penyalur: BankPenyalur

    @classmethod
    def from_fit_realisasi_sktp(cls, tag: Tag) -> List["RealisasiSktp"]:
        # #fit_RealisasiBayarSKTP
        pass

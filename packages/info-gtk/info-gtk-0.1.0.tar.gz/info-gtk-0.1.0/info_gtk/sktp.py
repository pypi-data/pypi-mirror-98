from bs4 import Tag
from dataclasses import dataclass


@dataclass
class Sktp:
    nomor_sktp: str
    tanggal_penerbitan_sktp: str
    pembayaran_tpg_periode: str
    format_bayar: str
    nama_penerima: str
    nip: str
    nuptk: str
    nrg: str
    kab_kota: str
    provinsi: str
    rekening_bank: str

    @classmethod
    def from_fit_sktp(cls, tag: Tag) -> "Sktp":
        # #fit_SKTP
        pass

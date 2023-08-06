from bs4 import Tag
from dataclasses import dataclass


@dataclass
class VerivikasiDataTunjangan:
    nuptk: bool
    keterangan_nuptk: str
    beban_mengajar: bool
    keterangan_beban_mengajar: str
    kelengkapan_data: bool
    keterangan_kelengkapan_data: str
    kelulusan_sertifikasi: bool
    keterangan_kelulusan_sertifikasi: str
    keaktifan: bool
    keterangan_keaktifan: str
    kepegawaian: bool
    keterangan_kepegawaian: str
    usia: bool
    keterangan_usia: str

    @classmethod
    def from_fit_verivikasi(cls, tag: Tag) -> "VerivikasiDataTunjangan":
        # #fit_Verifikasi
        pass

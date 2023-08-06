from bs4 import Tag
from dataclasses import dataclass


@dataclass
class KelulusanSertifikasi:
    nama: str
    tanggal_lahir: str
    nuptk: str
    nrg: str
    nomor_peserta: str
    nomor_sertifikat: str
    kode_sertifikasi_pertama: str
    nama_bidang_studi_sertifikasi: str
    nama_sekolah_terbit_nrg: str
    data_tercatat_jenjang: str
    kab_kota_saat_ini: str

    @classmethod
    def from_fit_kelulusan(cls, tag: Tag) -> "KelulusanSertifikasi":
        # #fit_Kelulusan
        pass

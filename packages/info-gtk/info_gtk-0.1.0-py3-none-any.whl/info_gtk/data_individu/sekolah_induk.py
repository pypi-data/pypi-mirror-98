from dataclasses import dataclass


@dataclass
class SekolahInduk:
    nama: str
    validasi: str
    terdeteksi: str
    keterangan_validasi: str


@dataclass
class LokasiSekolahInduk:
    provinsi: str
    kab_kota: str
    kecamatan: str
    desa_kelurahan: str
    kategori_desa_kelurahan: str

from bs4 import Tag
from dataclasses import dataclass
from typing import List


@dataclass
class StatusRombonganBelajar:
    nama: str
    tingkat: str
    paralel: int
    kurikulum: str


@dataclass
class MataPelajaranDiampu:
    kode: int
    nama: str
    linier: int


@dataclass
class JumlahJamMengajar:
    kurikulum: int
    dapodik: int
    diakui: int
    linier: int


@dataclass
class RombonganBelajar:
    no: int
    nama_sekolah: str
    status_rombongan_belajar: StatusRombonganBelajar
    semester: str
    mata_pelajaran_diampu: MataPelajaranDiampu
    jjm: JumlahJamMengajar
    jjm_rombel: int
    jumlah_siswa: int
    jenis_jam: str
    status: str
    keterangan: str

    @classmethod
    def from_fit_rombongan_belajar(cls, tag: Tag) -> List["RombonganBelajar"]:
        # #fit_RombonganBelajar
        pass

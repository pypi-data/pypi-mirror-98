import attr
from bs4 import Tag
from typing import List


@attr.dataclass(slots=True)
class StatusRombonganBelajar:
    nama: str
    tingkat: str
    paralel: int
    kurikulum: str


@attr.dataclass(slots=True)
class MataPelajaranDiampu:
    kode: int
    nama: str
    linier: int


@attr.dataclass(slots=True)
class JumlahJamMengajar:
    kurikulum: int
    dapodik: int
    diakui: int
    linier: int


@attr.dataclass(slots=True)
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

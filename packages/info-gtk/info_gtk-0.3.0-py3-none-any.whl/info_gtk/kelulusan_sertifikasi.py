import attr
from typing import List

from .table_data import TableData


@attr.dataclass(slots=True)
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
    def from_table_data(cls, tds: List[TableData]) -> "KelulusanSertifikasi":
        return cls(
            nama=tds[0].data,
            tanggal_lahir=tds[1].data,
            nuptk=tds[2].data,
            nrg=tds[3].data,
            nomor_peserta=tds[4].data,
            nomor_sertifikat=tds[5].data,
            kode_sertifikasi_pertama=tds[6].data,
            nama_bidang_studi_sertifikasi=tds[7].data,
            nama_sekolah_terbit_nrg=tds[8].data,
            data_tercatat_jenjang=tds[9].data,
            kab_kota_saat_ini=tds[10].data,
        )

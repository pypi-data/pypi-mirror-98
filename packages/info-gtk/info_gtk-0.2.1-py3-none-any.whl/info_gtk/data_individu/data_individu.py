import attr
from typing import List

from info_gtk.table_data import TableData
from . import IjazahTerakhir
from . import JamMengajar
from . import SekolahInduk, LokasiSekolahInduk
from . import StatusKepegawaian
from . import TugasTambahan


@attr.dataclass(slots=True)
class DataIndividu:
    update_terakhir: str
    nuptk: str
    nama: str
    tanggal_lahir: str
    nik: str
    email: str
    tanggal_pensiun: str
    jenis_ptk: str
    status_kepegawaian: StatusKepegawaian
    ijazah_terakhir: IjazahTerakhir
    sekolah_induk: SekolahInduk
    lokasi_sekolah_induk: LokasiSekolahInduk
    tugas_tambahan: TugasTambahan
    jumlah_jam_mengajar: JamMengajar
    total_jjm_linier_tambahan: str

    @classmethod
    def from_table_datas(cls, table_data: List[TableData]) -> "DataIndividu":
        # #fit_individu
        return cls(
            update_terakhir=table_data[0].data,
            nuptk=table_data[1].data,
            nama=table_data[2].data,
            tanggal_lahir=table_data[3].data,
            nik=table_data[4].data,
            email=table_data[5].data,
            tanggal_pensiun=table_data[6].data,
            jenis_ptk=table_data[7].data,
            status_kepegawaian=StatusKepegawaian.from_table_data(table_data[8]),
            ijazah_terakhir=IjazahTerakhir.from_table_data(table_data[9]),
            sekolah_induk=SekolahInduk.from_table_data(table_data[10]),
            lokasi_sekolah_induk=LokasiSekolahInduk.from_table_data(table_data[11]),
            tugas_tambahan=TugasTambahan.from_table_data(table_data[12]),
            jumlah_jam_mengajar=JamMengajar.from_table_data(table_data[13]),
            total_jjm_linier_tambahan=table_data[14].data,
        )

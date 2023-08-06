import attr
from typing import List

from info_gtk.table_data import TableData


@attr.dataclass(slots=True)
class StatusNuptk:
    nuptk: str
    nama: str
    tempat_lahir: str
    tanggal_lahir: str
    nama_ibu_kandung: str
    nip: str
    nik: str
    instansi: str
    kab_kota: str

    @classmethod
    def from_table_data(cls, table_data: List[TableData]) -> "StatusNuptk":
        return cls(
            nuptk=table_data[0].data,
            nama=table_data[1].data,
            tempat_lahir=table_data[2].data,
            tanggal_lahir=table_data[3].data,
            nama_ibu_kandung=table_data[4].data,
            nip=table_data[5].data,
            nik=table_data[6].data,
            instansi=table_data[7].data,
            kab_kota=table_data[8].data,
        )

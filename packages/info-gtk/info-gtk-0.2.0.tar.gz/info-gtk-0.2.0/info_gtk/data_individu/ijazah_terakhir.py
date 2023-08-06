import attr

from info_gtk.table_data import TableData


@attr.dataclass(slots=True)
class IjazahTerakhir:
    nama: str
    jurusan: str
    perguruan: str

    @classmethod
    def from_table_data(cls, table_data: TableData) -> "IjazahTerakhir":
        data = table_data.children
        return cls(
            nama=data[0].data,
            jurusan=data[1].data,
            perguruan=data[2].data,
        )

import attr

from info_gtk.table_data import TableData


@attr.dataclass(slots=True)
class StatusKepegawaian:
    nama: str
    nipy: str
    sk_pengangkatan: str
    tmt_pengangkatan: str
    sumber_gaji: str
    status_inpassing: str

    def __str__(self) -> str:
        return self.nama

    @classmethod
    def from_table_data(cls, table_data: TableData) -> "StatusKepegawaian":
        data = table_data.children
        return cls(
            nama=data[0].data,
            nipy=data[1].data,
            sk_pengangkatan=data[2].data,
            tmt_pengangkatan=data[3].data,
            sumber_gaji=data[4].data,
            status_inpassing=data[5].data,
        )

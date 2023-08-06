import attr

from info_gtk.table_data import TableData


@attr.dataclass(slots=True)
class TugasTambahan:
    nama: str
    sk: str
    tmt: str
    tst: str
    validasi: str
    jumlah_rombel: str
    jumlah_tt_diakui: str
    jumlah_tt_terdetejsi: str
    diakui_linier: str
    keterangan_validasi: str

    @classmethod
    def from_table_data(cls, table_data: TableData) -> "TugasTambahan":
        data = table_data.children
        return cls(
            nama=data[0].data,
            sk=data[1].data,
            tmt=data[2].data,
            tst=data[3].data,
            validasi=data[4].data,
            jumlah_rombel=data[5].data,
            jumlah_tt_diakui=data[6].data,
            jumlah_tt_terdetejsi=data[7].data,
            diakui_linier=data[8].data,
            keterangan_validasi=data[9].data,
        )

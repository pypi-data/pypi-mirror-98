import attr

from info_gtk.table_data import TableData


@attr.dataclass(slots=True)
class SekolahInduk:
    nama: str
    validasi: str
    terdeteksi: str
    keterangan_validasi: str

    @classmethod
    def from_table_data(cls, table_data: TableData) -> "SekolahInduk":
        data = table_data.children
        return cls(
            nama=data[0].data,
            validasi=data[1].data,
            terdeteksi=data[2].data,
            keterangan_validasi=data[3].data,
        )


@attr.dataclass(slots=True)
class LokasiSekolahInduk:
    provinsi: str
    kab_kota: str
    kecamatan: str
    desa_kelurahan: str
    kategori_desa_kelurahan: str

    @classmethod
    def from_table_data(cls, table_data: TableData) -> "LokasiSekolahInduk":
        data = table_data.children
        return cls(
            provinsi=data[0].data,
            kab_kota=data[1].data,
            kecamatan=data[2].data,
            desa_kelurahan=data[3].data,
            kategori_desa_kelurahan=data[4].data,
        )

import attr
from typing import Optional

from info_gtk.table_data import TableData


@attr.dataclass(slots=True)
class JamMengajarInduk:
    jam_mengajar: str
    jam_linier: str

    @classmethod
    def from_table_data(cls, table_data: TableData) -> "JamMengajarInduk":
        data = table_data.children
        return cls(
            jam_mengajar=data[0].data,
            jam_linier=data[1].data,
        )


@attr.dataclass(slots=True)
class JamMengajarNonInduk:
    jam_mengajar: Optional[str] = None
    jam_linier: Optional[str] = None

    @classmethod
    def from_table_data(cls, table_data: TableData) -> "JamMengajarNonInduk":
        data = table_data.children
        return cls(
            jam_mengajar=data[0].data if data[0].data else None,
            jam_linier=data[1].data if data[1].data else None,
        )


@attr.dataclass(slots=True)
class JamMengajarIndukNonInduk:
    total_mengajar: str
    total_linier: str

    @classmethod
    def from_table_data(cls, table_data: TableData) -> "JamMengajarIndukNonInduk":
        data = table_data.children
        return cls(
            total_mengajar=data[0].data,
            total_linier=data[1].data,
        )


@attr.dataclass(slots=True)
class JamMengajar:
    sekolah_induk: JamMengajarInduk
    sekolah_non_induk: JamMengajarNonInduk
    sekolah_induk_non_induk: JamMengajarIndukNonInduk

    @classmethod
    def from_table_data(cls, table_data: TableData) -> "JamMengajar":
        data = table_data.children
        return cls(
            sekolah_induk=JamMengajarInduk.from_table_data(data[0]),
            sekolah_non_induk=JamMengajarNonInduk.from_table_data(data[1]),
            sekolah_induk_non_induk=JamMengajarIndukNonInduk.from_table_data(data[2]),
        )

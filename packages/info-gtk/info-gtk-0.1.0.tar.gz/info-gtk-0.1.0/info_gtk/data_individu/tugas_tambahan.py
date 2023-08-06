from dataclasses import dataclass


@dataclass
class TugasTambahan:
    nama: str
    sk: str
    tmt: str
    tst: str
    validasi: str
    jumlah_rombel: int
    jumlah_tt_diakui: int
    jumlah_tt_terdetejsi: int
    diakui_linier: int
    keterangan_validasi: str

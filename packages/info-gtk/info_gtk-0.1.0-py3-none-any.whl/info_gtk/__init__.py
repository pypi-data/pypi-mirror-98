#!/usr/bin/env python
from .data_individu import DataIndividu
from .status_nuptk import StatusNuptk
from .kelulusan_sertifikasi import KelulusanSertifikasi
from .realisasi_sktp import RealisasiSktp
from .profile import Profile
from .rombongan_belajar import RombonganBelajar
from .sktp import Sktp
from .verivikasi_data_tunjangan import VerivikasiDataTunjangan


from .info_gtk import InfoGtk

from .version import __version__  # NOQA

__author__ = "hexatester <habibrohman@protonmail.com>"

__all__ = [
    "DataIndividu",
    "StatusNuptk",
    "KelulusanSertifikasi",
    "RealisasiSktp",
    "Profile",
    "RombonganBelajar",
    "Sktp",
    "VerivikasiDataTunjangan",
    "InfoGtk",
]

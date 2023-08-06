from dataclasses import dataclass
from typing import Optional


@dataclass
class JamMengajarInduk:
    jam_mengajar: int
    jam_linier: int


@dataclass
class JamMengajarNonInduk:
    jam_mengajar: Optional[int]
    jam_linier: Optional[int]


@dataclass
class JamMengajar:
    sekolah_induk: JamMengajarInduk
    sekolah_non_induk: JamMengajarNonInduk
    total_mengajar: int
    total_linier: int

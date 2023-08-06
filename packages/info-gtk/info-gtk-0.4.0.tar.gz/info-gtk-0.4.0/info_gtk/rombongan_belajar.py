import attr
from typing import Any, List, Dict


@attr.dataclass(slots=True)
class RombonganBelajar:
    no: str
    r_id: str
    nama_sekolah: str
    nama_rombel: str
    thn_ajaran: str
    smt: str
    nama_kurikulum_dapodik: str
    jjm: str
    jjm_ktsp: str
    jjm_linier: str
    jjm_normal: str
    diakui: str
    jjm_rombel: str
    jml_siswa: str
    j_jam: str
    kode: str
    mapel: str
    is_linier: str
    paralel: str
    tingkat: str
    ket: str
    dRombel: List[Any] = attr.ib(factory=list)

    @classmethod
    def from_list(cls, datas: List[Dict[str, Any]]) -> List["RombonganBelajar"]:
        results: List["RombonganBelajar"] = list()
        for data in datas:
            results.append(cls(**data))
        return results

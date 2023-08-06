from dataclasses import dataclass


@dataclass
class StatusKepegawaian:
    nama: str
    nipy: str
    sk_pengangkatan: str
    tmt_pengangkatan: str
    sumber_gaji: str
    status_inpassing: str

    def __str__(self) -> str:
        return self.nama

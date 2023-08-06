import attr
import json5
from typing import List, Optional


@attr.dataclass
class TableData:
    no: str
    uraian: str
    data: str
    keterangan: str
    col: Optional[str] = None
    children: List["TableData"] = attr.ib(factory=list)

    @classmethod
    def from_json5_list(cls, datas: str) -> List["TableData"]:
        if not datas:
            return list()
        return cls.from_list(json5.loads(datas))

    @classmethod
    def from_list(cls, datas: List[dict]) -> List["TableData"]:
        results: List["TableData"] = list()
        for data in datas:
            children = data.pop("_children", None)
            if children:
                data["children"] = cls.from_list(children)
            results.append(cls(**data))
        return results

    @classmethod
    def make_individu(cls, data: str) -> List["TableData"]:
        tabledata: str = ""
        datas = data.splitlines()
        for i, line in enumerate(datas):
            if "/*individu*/" in line:
                tabledata = datas[i + 1]
                tabledata = tabledata.strip()
                tabledata = tabledata.lstrip("try {var tabledata = ")
                tabledata = tabledata.rstrip(
                    ';putTable("#fit_individu",tabledata);} catch(err) {  };'
                )
                break
        if not tabledata:
            return list()
        return cls.from_json5_list(tabledata)

    @classmethod
    def make_status_nuptk(cls, data: str) -> List["TableData"]:
        tabledata: str = ""
        datas = data.splitlines()
        for i, line in enumerate(datas):
            if "/*arsip NUPTK*/" in line:
                tabledata = datas[i + 1]
                tabledata = tabledata.strip()
                tabledata = tabledata.lstrip("try { var tabledata = ")
                tabledata = tabledata.rstrip(
                    ';putTable("#fit_ArsipNuptk",tabledata);} catch(err) {  };'
                )
                break
        if not tabledata:
            return list()
        return cls.from_json5_list(tabledata)

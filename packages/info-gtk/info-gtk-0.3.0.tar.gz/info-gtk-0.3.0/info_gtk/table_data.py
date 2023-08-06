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
    def makes(
        cls,
        data: str,
        locate: str,
        offset: int = 1,
        lstrip: str = "",
        rstrip: str = "",
    ):
        tabledata: str = ""
        datas = data.splitlines()
        for i, line in enumerate(datas):
            if locate in line:
                tabledata = datas[i + offset]
                tabledata = tabledata.strip()
                tabledata = tabledata.lstrip(lstrip)
                tabledata = tabledata.rstrip(rstrip)
                break
        if not tabledata:
            return list()
        return cls.from_json5_list(tabledata)

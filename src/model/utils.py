from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional


@dataclass
class Row:
    elems: list[str]


@dataclass
class Result:
    cols: Optional[list[str]]
    rows: Optional[list[Row]]
    created: datetime | str


class Mapper:
    """
    Arg: m
    m = {
        "cols" : []
        "rows" : [ [], [].. ]
    }
    """
    @classmethod
    def new(cls, m: dict[str, Any]) -> Result:
        converted = str(datetime.today())
        date = converted.split(' ')[0]
        time = converted.split(' ')[-1].split('.')[0]
        return Result(
            cols=m["cols"] if len(m["cols"]) > 0 else None,
            rows=[Row(v) for v in m["rows"]] if len(
                m["rows"]) > 0 else None,
            created="".join(date + ' ' + time),
        )


"""
- Input:
demo = {
    "cols": ["a", "b", "c", "d"],
    "rows": [["a", "b", "c", "d"], ["a", "b", "c", "d"], ["a", "b", "c", "d"]],
}

- Output: Mapper.new(demo) => return Result
Result(
    cols=['a', 'b', 'c', 'd'],
    rows=[
           Row(vals=['a', 'b', 'c', 'd']),
           Row(vals=[]),
           Row(vals=[])
         ],
    created='2022-11-28 18:50:01'
)

# Usage(Access) -> Get Values
Col: Mapper.new(m: dict[str,Any]).cols[0]
Row: Mapper.new(m: dict[str,Any]).rows[0].vals[0]
Created: Mapper.new(m: dict[str,Any]).created
"""

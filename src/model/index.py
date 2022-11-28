from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

# In general, it is a good idea to combine multiple reads or updates with the batchGet and batchUpdate methods(respectively), as this will improve efficiency.
# variable ---

"""
- Input:
demo = {
    "cols": ["a", "b", "c", "d"],
    "rows": [["a", "b", "c", "d"], ["a", "b", "c", "d"], ["a", "b", "c", "d"]],
    "created": datetime.today()
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

# Usage -
Col: Mapper.new(m: dict[str,Any]).cols[0]
Row: Mapper.new(m: dict[str,Any]).rows[0].vals[0]
Created: Mapper.new(m: dict[str,Any]).created
"""


@dataclass
class Options():
    SCOPES: list[str]
    SAMPLE_SPREADSHEET_ID: Optional[str]
    SAMPLE_RANGE_NAME: Optional[str]


@dataclass
class Row:
    vals: list[str]


@dataclass
class Result:
    cols: Optional[list[str]]
    rows: Optional[list[Row]]
    created: datetime | str


class Mapper:
    """
    ARG: m = {
        "cols" : []
        "rows" : [ [], [].. ]
        "created" : datetime.today()
    }
    """
    @classmethod
    def new(cls, m: dict[str, Any]) -> Result:
        converted = str(m["created"])
        date = converted.split(' ')[0]
        time = converted.split(' ')[-1].split('.')[0]
        return Result(
            cols=m["cols"] if len(m["cols"]) > 0 else None,
            rows=[Row(v) for v in m["rows"]] if len(
                m["rows"]) > 0 else None,
            created="".join(date + ' ' + time),
        )


# Demo Data
demo = {
    "cols": ["ca", "cb", "cc", "cd", "ce"],
    "rows": [["r1a", "r1b", "r1c", "r1d", "r1e"], ["r2a", "r2b", "r2c", "r2d", "r2e"], ["r3a", "r3b", "r3c", "r3d", "r3e"]],
    "created": datetime.today()  # 2022-11-28 17:58:23.633352
}


O = Options(
    SCOPES=['https://www.googleapis.com/auth/spreadsheets'],
    SAMPLE_SPREADSHEET_ID=None,
    SAMPLE_RANGE_NAME=None,  # 2d cross edges
)

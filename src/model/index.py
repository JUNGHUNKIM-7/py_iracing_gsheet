from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class Options():
    SCOPES: list[str]
    SAMPLE_SPREADSHEET_ID: Optional[str]
    SAMPLE_RANGE_NAME: Optional[str]


@dataclass
class ScraperOptions():
    webdriver_path: str
    output_csv_path: str
    url: str
    result_url: Optional[str]
    user_name: Optional[str]
    password: Optional[str]


# const - Option Variables
O = Options(
    SCOPES=['https://www.googleapis.com/auth/spreadsheets'],
    SAMPLE_SPREADSHEET_ID=None,
    SAMPLE_RANGE_NAME=None,  # 2d box(range) in excel sheet
)

SUB_PATH = str(datetime.today()).split(
    '.')[0].replace(' ', "_").replace(':', "")

SO = ScraperOptions(
    webdriver_path=f"{Path.home()}\\downloads\\msedgedriver.exe",
    user_name="automanix1@kakao.com",
    password="iracing",
    url="https://www.iracing.com/",
    result_url=None,
    output_csv_path=f"{Path.home()}\\downloads\\eventresult_{SUB_PATH}.csv"
)

demo = {
    "cols": ["ca", "cb", "cc", "cd", "ce"],
    "rows": [["r1a", "r1b", "r1c", "r1d", "r1e"], ["r2a", "r2b", "r2c", "r2d", "r2e"], ["r3a", "r3b", "r3c", "r3d", "r3e"]],
}

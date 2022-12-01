from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class Options():
    SCOPES: list[str]
    SAMPLE_SPREADSHEET_ID: Optional[str] = None
    SAMPLE_RANGE_NAME: Optional[str] = None


@dataclass
class ScraperOptions():
    webdriver_path: str
    output_csv_path: str
    url: str
    result_url: Optional[str] = None
    user_name: Optional[str] = None
    password: Optional[str] = None


# const - Option Variables
O = Options(
    SCOPES=['https://www.googleapis.com/auth/spreadsheets'],
)

SUB_PATH = str(datetime.today()).split(
    '.')[0].replace(' ', "_").replace(':', "")

SO = ScraperOptions(
    webdriver_path=f"{Path.home()}\\downloads\\msedgedriver.exe",
    url="https://www.iracing.com/",
    output_csv_path=f"{Path.home()}\\downloads\\eventresult_{SUB_PATH}.csv"
)

demo = {
    "cols": ["ca", "cb", "cc", "cd", "ce"],
    "rows": [["r1a", "r1b", "r1c", "r1d", "r1e"], ["r2a", "r2b", "r2c", "r2d", "r2e"], ["r3a", "r3b", "r3c", "r3d", "r3e"]],
}

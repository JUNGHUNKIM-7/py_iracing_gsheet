from enum import Enum, auto

from googleapiclient.errors import Error, HttpError

from src.model.utils import Result
from src.repository.index import O, Repository


class RWMode(Enum):
    W = auto()
    R = auto()


class GsheetHandler:
    def __init__(self) -> None:
        self.r = Repository()

    def new_sheet(self, m: Result):
        try:
            assert len(str(m.created)) > 1, "title(created) is None"
            self.r.create_sheet(str(m.created))
        except* HttpError as e:
            raise Exception(e)
        except* Error as e:
            raise Exception(e)

    def writer_reader(self, type: RWMode, m: Result):
        sheetId = O.SAMPLE_SPREADSHEET_ID
        assert sheetId is not None, "sheet id can't be None"

        if sheetId is not None:
            try:
                match type:
                    case RWMode.R:
                        result = self.r.read(sheetId=sheetId)
                        if result is not None:
                            # may export to another file? Write iracing data -> sheet -> read data -> another file
                            print(result)
                            return
                    case RWMode.W:
                        self.r.write(m)
            except Exception as e:
                raise Exception(e)
        else:
            raise Exception(
                'sheetId is null now, nothing to set value to Option@dcls')

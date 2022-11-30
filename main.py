from enum import Enum, auto

from googleapiclient.errors import HttpError

from src.model.index import demo, SO
from src.model.utils import Mapper
from src.repository.handler import Handler, RWMode
from src.scraper.index import FileControllers, Scraper

# TODO:
# add company credentials
# test iracing real mockup data + link prev data to main function
# make bottom sheet, prac, quali, main


class RunType(Enum):
    parse = auto()
    googleapi = auto()


class Program:
    # func 1 -> Scarape all datas
    @classmethod
    def parse_from_iracing(cls):
        so = SO
        print('ex: email/password\n')
        try:
            user_name, password = input().split('/')
        except EOFError as e:
            raise EOFError(e)
        so.user_name = user_name.strip()
        so.password = password.strip()

        s = Scraper(so)
        f = FileControllers(so)
        try:
            s.access(so.url)
            s.parse_result()
            f.dump_csv()
        except Exception as e:
            raise Exception(e)

    # func 2 -> GOOGLESHEET

    @classmethod
    def send_to_Gsheet(cls):
        # Input = api -> map data -> mapper for csv
        m = Mapper.new(demo)  # <- change real mock here
        if m.cols is not None and m.rows is not None:
            h = Handler()
            try:
                h.new_sheet(m)
                h.writer_reader(type=RWMode.W, m=m)
                h.writer_reader(type=RWMode.R, m=m)
            except* HttpError as e:
                raise Exception(f"httpError: {e}")
            except* Exception as e:
                raise Exception(f"Error:{e}")
        else:
            raise Exception("cols or data is null")


def main():
    o = RunType.parse
    match o:
        case RunType.googleapi:
            # 1. from Sdk data to Google API
            Program.send_to_Gsheet()
        case RunType.parse:
            # 2. from Iracing Histories to Excel
            Program.parse_from_iracing()
        case _:
            raise Exception("err")


if __name__ == '__main__':
    main()

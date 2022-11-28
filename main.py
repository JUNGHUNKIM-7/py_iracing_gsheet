from googleapiclient.errors import HttpError

from src.model.index import Mapper, demo
from src.repository.handler import Handler, RWMode

# TODO:
# add company credentials

# test iracing real mockup data + link prev data to main function
# make bottom sheet, prac, quali, main


def main():
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


if __name__ == '__main__':
    main()

from xerial.Exception.ChangeTypeException import ChangeTypeException


class DateTimeToDateException(ChangeTypeException):
    def __init__(self, column: str):
        super(DateTimeToDateException, self).__init__()
        self.code = super().getShiftedCode() + 1
        self.message = f'Change type of column {column} from DateTime to Date will result in time data loss'
       
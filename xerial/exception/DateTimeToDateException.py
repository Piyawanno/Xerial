from xerial.exception.ChangeTypeException import ChangeTypeException


class DateTimeToDateException(ChangeTypeException):
    def __init__(self, column: str):
        super(DateTimeToDateException, self).__init__()
        self.code = super().get_shifted_code() + 1
        self.message = f'Change type of column {column} from DateTime to Date will result in time data loss'
       
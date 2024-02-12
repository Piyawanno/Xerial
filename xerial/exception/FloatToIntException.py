from xerial.exception.ChangeTypeException import ChangeTypeException


class FloatToIntException(ChangeTypeException):
    def __init__(self, column: str):
        super(FloatToIntException, self).__init__(self.generate_message())
        self.column: str = column
        self.code = super().get_shifted_code() + 1

    def resolver(self):
        pass

    def generate_message(self):
        return f'Change type of column {self.column} from float to int may cause data precision loss'

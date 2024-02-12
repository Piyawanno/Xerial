from xerial.exception.ChangeTypeException import ChangeTypeException


class TypeIncompatibleException(ChangeTypeException):
    def __init__(self, column: str, old_type: str, new_type: str):
        super(TypeIncompatibleException, self).__init__(self.generate_message())
        self.old_type = old_type
        self.new_type = new_type
        self.column: str = column
        self.code = super().get_shifted_code()

    def resolver(self):
        pass

    def generate_message(self):
        return (
            f'Unable to change type of column {self.column} from {self.old_type} to {self.new_type} '
            f'due to incompatible types'
        )

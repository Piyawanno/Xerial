from xerial.exception.ChangeTypeException import ChangeTypeException
from xerial.exception.ExceptionCode import ExceptionCode


class TypeIncompatibleException(ChangeTypeException):
    def __init__(self, column: str, old_type: str, new_type: str):
        super(TypeIncompatibleException, self).__init__()
        self.code = ExceptionCode.TYPE_INCOMPATIBLE
        self.message = (
            f'Unable to change type of column {column} from {old_type} to {new_type}'
            f' due to incompatible types'
        )

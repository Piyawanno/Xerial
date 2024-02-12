from xerial.ModificationType import ModificationType
from xerial.exception.ModificationException import ModificationException


class ChangeTypeException(ModificationException):
    def __init__(self, message):
        super(ChangeTypeException, self).__init__(message)
        self.code = super().get_shifted_code() + ModificationType.CHANGE_TYPE

    def resolver(self):
        pass

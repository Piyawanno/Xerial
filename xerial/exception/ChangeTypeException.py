from xerial.ModificationType import ModificationType
from xerial.exception.ModificationException import ModificationException


class ChangeTypeException(ModificationException):
    def __init__(self):
        super(ChangeTypeException, self).__init__()
        self.code = super().get_shifted_code() + ModificationType.CHANGE_TYPE
        self.message = 'Change Type Exception'
       
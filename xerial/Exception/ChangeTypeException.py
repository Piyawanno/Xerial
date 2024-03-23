from xerial.Exception.ModificationException import ModificationException
from xerial.ModificationType import ModificationType


class ChangeTypeException(ModificationException):
    def __init__(self):
        super(ChangeTypeException, self).__init__()
        self.code = super().getShiftedCode() + ModificationType.CHANGE_TYPE
        self.message = 'Change Type Exception'
       
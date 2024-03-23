from xerial.Exception.XerialException import XerialException


class ModificationException(XerialException):
    def __init__(self):
        super(ModificationException, self).__init__()
        self.code = super().getShiftedCode()
        self.message = 'Modification Exception'

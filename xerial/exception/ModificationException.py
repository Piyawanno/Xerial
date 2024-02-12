from xerial.exception.XerialException import XerialException


class ModificationException(XerialException):
    def __init__(self):
        super(ModificationException, self).__init__()
        self.code = super().get_shifted_code()
        self.message = 'Modification Exception'

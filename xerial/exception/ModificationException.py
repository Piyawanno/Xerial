from xerial.exception.XerialException import XerialException


class ModificationException(XerialException):
    def __init__(self, message):
        super(ModificationException, self).__init__(message)
        self.code = super().get_shifted_code() + 1

    def resolver(self):
        pass

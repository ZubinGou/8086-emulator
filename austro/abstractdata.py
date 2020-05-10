
class AbstractData(object):
    _bits = 0

    @property
    def bits(self):
        return self._bits
    @bits.setter
    def bits(self, value):
        self._bits = value

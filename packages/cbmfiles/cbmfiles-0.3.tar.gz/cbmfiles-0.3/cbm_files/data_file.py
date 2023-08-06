import codecs
import logging

log = logging.getLogger(__name__)


class DataFile:
    def __init__(self, fileh, encoding='petscii-c64en-uc'):
        self.lines = []
        try:
            _ = codecs.lookup(encoding)
        except LookupError:
            log.warning("PETSCII codecs not available, using ASCII")
            encoding = 'ascii'
        self.encoding = encoding

        line_encoded = bytearray()
        while fileh:
            b = fileh.read(1)
            if b == b'':
                # EOF
                break
            if b == b'\r':
                # CR
                self.lines.append(line_encoded)
                line_encoded = bytearray()
            else:
                line_encoded += b

        if line_encoded:
            line_encoded += b

    def to_text(self):
        """Generator to return lines as text."""
        for line in self.lines:
            yield line.decode(self.encoding)

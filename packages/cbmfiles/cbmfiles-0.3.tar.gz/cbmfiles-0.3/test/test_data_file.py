import unittest
import io

from cbm_files.data_file import DataFile


class TestDataFile(unittest.TestCase):
    def test_read(self):
        mock_file = io.BytesIO(b'LINE 1\r'
                               b'LINE 2\r'
                               b'LINE 3\r')
        data = DataFile(mock_file)
        self.assertEqual(data.lines, [b'LINE 1', b'LINE 2', b'LINE 3'])

    def test_to_text(self):
        data = DataFile(None)
        data.lines = [b'LINE 1',
                      b'LINE 2',
                      b'LINE 3']
        text = list(data.to_text())
        self.assertEqual(text, ['LINE 1', 'LINE 2', 'LINE 3'])

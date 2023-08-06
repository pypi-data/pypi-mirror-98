from pathlib import Path

from musurgia.pdf.line import MarkLine
from musurgia.pdf.masterslave import Master
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.text import Text
from musurgia.unittest import TestCase

path = Path(__file__)


class DummyMaster(Master):
    def get_slave_margin(self, slave, margin):
        return 10

    def get_slave_position(self, slave, position):
        return 20


class TestMarkLine(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()
        self.master = DummyMaster()
        self.ml = MarkLine(mode='v', placement='start', name='mark_line_test', master=self.master)

    def test_relative_x(self):
        actual = self.ml.relative_x
        expected = self.master.get_slave_position(self.ml, 'x')
        self.assertEqual(expected, actual)

    def test_get_relative_x2(self):
        actual = self.ml.get_relative_x2()
        expected = self.ml.relative_x
        self.assertEqual(expected, actual)

    def test_get_relative_y2(self):
        actual = self.ml.get_relative_y2()
        expected = self.ml.relative_y + self.ml.length
        self.assertEqual(expected, actual)

    def test_get_height(self):
        actual = self.ml.get_height()
        expected = self.ml.top_margin + self.ml.length + self.ml.bottom_margin
        self.assertEqual(expected, actual)

    def test_draw(self):
        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')
            self.ml.draw(self.pdf)
            self.pdf.write(pdf_path)

    def test_draw_multiple(self):
        self.ml.master.get_slave_position = lambda slave, position: 0
        self.ml.master.get_slave_margin = lambda slave, margin: 0
        with self.file_path(path, 'draw_multiple', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')
            self.pdf.translate(20, 20)
            self.ml.draw(self.pdf)
            self.ml.master.get_slave_margin = lambda slave, margin: 5 if margin in ['l', 'left'] else 0
            self.ml.draw(self.pdf)
            self.pdf.write(pdf_path)

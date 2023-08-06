from musicscore.musictree.treeclef import TENOR_CLEF
from musicscore.musictree.treeinstruments import Violin, Cello, Viola, TreeInstrument, Piano
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.unittest import TestCase
from musurgia.fractaltree.fractalmusic import FractalMusic


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()
        self.fm = FractalMusic(tempo=60, quarter_duration=10)

    def test_none_midi_values(self):
        self.fm.add_layer()
        actual = [node._midi_value for node in self.fm.traverse()]
        expected = 4 * [None]
        self.assertEqual(expected, actual)

    def test_none_midi_values_instrument_changed(self):
        self.fm.instrument = Cello()
        self.fm.add_layer()
        actual = [node._midi_value for node in self.fm.traverse()]
        expected = 4 * [None]
        self.assertEqual(expected, actual)

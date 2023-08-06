from musicscore.musictree.treeclef import BASS_CLEF
from musicscore.musictree.treeinstruments import Violin, Piano
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.unittest import TestCase
from musurgia.fractaltree.fractalmusic import FractalMusic, FractalMusicException


class TestInstrument(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()
        self.fm = FractalMusic(tempo=60, quarter_duration=10)

    def test_set_root_instrument(self):
        self.fm.instrument = Violin()
        self.fm.add_layer()
        expected = 3 * [self.fm.instrument]
        actual = [node.instrument for node in self.fm.get_layer(1)]
        self.assertEqual(expected, actual)

    def test_set_wrong_type(self):
        with self.assertRaises(TypeError):
            self.fm.instrument = BASS_CLEF

    def test_set_child_instrument(self):
        self.fm.add_layer()
        with self.assertRaises(FractalMusicException):
            self.fm.get_children()[0].instrument = Violin()

    def test_staff_number_piano(self):
        self.fm.add_layer()
        self.fm.instrument = Piano()
        right_hand = self.fm
        right_hand.staff_number = 1
        left_hand = self.fm.__deepcopy__()
        left_hand.staff_number = 2
        actual = [
            [child.staff_number for child in right_hand.get_children()],
            [child.staff_number for child in left_hand.get_children()],
        ]
        expected = [
            3 * [1],
            3 * [2]
        ]
        self.assertEqual(expected, actual)

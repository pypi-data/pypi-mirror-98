from musicscore.musictree.treeclef import TENOR_CLEF
from musicscore.musictree.treeinstruments import Violin, Cello, Viola, TreeInstrument, Piano
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.unittest import TestCase
from musurgia.fractaltree.fractalmusic import FractalMusic


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()
        self.fm = FractalMusic(tempo=60, quarter_duration=10)

    def test_get_neutral_midi_values_no_instrument(self):
        self.fm.add_layer()
        actual = [node.get_neutral_midi_value() for node in self.fm.traverse()]
        expected = 4 * [71]
        self.assertEqual(expected, actual)

    def test_get_neutral_midi_values_treble_clef(self):
        self.fm.instrument = Violin()
        self.fm.add_layer()
        actual = [node.get_neutral_midi_value() for node in self.fm.traverse()]
        expected = 4 * [71]
        self.assertEqual(expected, actual)

    def test_get_neutral_midi_values_bass_clef(self):
        self.fm.instrument = Cello()
        self.fm.add_layer()
        actual = [node.get_neutral_midi_value() for node in self.fm.traverse()]
        expected = 4 * [50]
        self.assertEqual(expected, actual)

    def test_get_neutral_midi_values_alto_clef(self):
        self.fm.instrument = Viola()
        self.fm.add_layer()
        actual = [node.get_neutral_midi_value() for node in self.fm.traverse()]
        expected = 4 * [60]
        self.assertEqual(expected, actual)

    def test_get_neutral_midi_values_tenor_clef(self):
        self.fm.instrument = TreeInstrument(name='Tenor', abbreviation='tenor')
        self.fm.instrument.standard_clefs = TENOR_CLEF
        self.fm.add_layer()
        actual = [node.get_neutral_midi_value() for node in self.fm.traverse()]
        expected = 4 * [57]
        self.assertEqual(expected, actual)

    def test_chord_midis_treble_clef(self):
        self.fm.instrument = Violin()
        self.fm.add_layer()
        actual = [node.chord.midis[0].value for node in self.fm.traverse()]
        expected = 4 * [71]
        self.assertEqual(expected, actual)

    def test_chord_midis_bass_clef(self):
        self.fm.instrument = Cello()
        self.fm.add_layer()
        actual = [node.chord.midis[0].value for node in self.fm.traverse()]
        expected = 4 * [50]
        self.assertEqual(expected, actual)

    def test_chord_midis_change_instrument(self):
        self.fm.add_layer()
        self.fm.instrument = Cello()
        actual = [node.chord.midis[0].value for node in self.fm.traverse()]
        expected = 4 * [50]
        self.assertEqual(expected, actual)

    def test_get_neural_midis_piano(self):
        self.fm.instrument = Piano()
        self.fm.add_layer()

        right_hand = self.fm
        right_hand.staff_number = 1
        left_hand = self.fm.__deepcopy__()
        left_hand.staff_number = 2

        actual_right_hand = [node.get_neutral_midi_value() for node in right_hand.traverse()]
        expected_right_hand = 4 * [71]
        self.assertEqual(actual_right_hand, expected_right_hand)
        actual_left_hand = [node.get_neutral_midi_value() for node in left_hand.traverse()]
        expected_left_hand = 4 * [50]
        self.assertEqual(expected_left_hand, actual_left_hand)

    def test_chord_midis_piano(self):
        self.fm.instrument = Piano()

        right_hand = self.fm
        right_hand.staff_number = 1
        left_hand = self.fm.__deepcopy__()
        left_hand.staff_number = 2

        right_hand.add_layer()
        left_hand.add_layer()

        actual_right_hand = [node.midi_value for node in right_hand.traverse()]
        expected_right_hand = 4 * [71]
        self.assertEqual(actual_right_hand, expected_right_hand)

        actual_left_hand = [node.midi_value for node in left_hand.traverse()]
        expected_left_hand = 4 * [50]
        self.assertEqual(expected_left_hand, actual_left_hand)

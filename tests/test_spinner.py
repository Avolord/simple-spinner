import pytest
from unittest.mock import patch, call
from simple_spinner.spinner import Spinner
import time

# Helper function to simulate time
class CustomTime:
    def __init__(self, start_time):
        self.current_time = start_time

    def __call__(self):
        return self.current_time

    def advance(self, increment):
        self.current_time += increment

@pytest.fixture
def sample_iterable():
    return [1, 2, 3]

@pytest.fixture
def sample_glyphs():
    return ['-', '\\', '|', '/']

def test_spinner_initialization(sample_iterable, sample_glyphs):
    spinner = Spinner(sample_iterable, sample_glyphs, glyphs_per_second=5.0, desc='Test')
    assert spinner.iterable == sample_iterable
    assert spinner.glyphs == sample_glyphs
    assert spinner.seconds_per_glyph == 1.0 / 5.0
    assert spinner.desc == 'Test'
    assert spinner.glyph_index == 0
    assert spinner.order == [0, 1, 2, 3]

def test_next_glyph(sample_glyphs):
    spinner = Spinner([], sample_glyphs)
    assert spinner.next_glyph() == '-'
    assert spinner.next_glyph() == '\\'
    assert spinner.next_glyph() == '|'
    assert spinner.next_glyph() == '/'
    assert spinner.next_glyph() == '-'



def test_iteration(sample_iterable, sample_glyphs):
    spinner = Spinner(sample_iterable, sample_glyphs)

    with patch.object(spinner, 'start') as mock_start, patch.object(spinner, 'stop') as mock_stop:
        result = list(spinner)
        mock_start.assert_called_once()
        mock_stop.assert_called_once()
        assert result == sample_iterable

@patch('builtins.print')
def test_stop(print_mock):
    spinner = Spinner([])
    spinner.running = True

    spinner.start()
    spinner.stop()
    assert not spinner.running
    print_mock.assert_called_with(' ', end='\r')

if __name__ == '__main__':
    pytest.main()

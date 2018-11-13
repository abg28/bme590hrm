import pytest


@pytest.mark.parametrize("filepath", ["notonmymachine.txt",
                                      "stereotypicalbmehw.m"])
def test_check_file_existence(filepath):
    """ Tests the function "check_file_existence" from heartRateMonitor.py

    :param filepath: the inputted file path
    :returns: passes if FileNotFoundError properly raised, fails otherwise
    """
    from heartRateMonitor import check_file_existence
    with pytest.raises(FileNotFoundError):
        check_file_existence(filepath)


@pytest.mark.parametrize("filepath", ["hello.avi", "yes.mp3", 42, "qwertyuiop"]
                         )
def test_check_extension(filepath):
    """ Tests the function "check_extension" from heartRateMonitor.py

    :param filepath: the inputted file path
    :returns: passes if TypeError properly raised, fails otherwise
    """
    from heartRateMonitor import check_extension
    with pytest.raises(TypeError):
        check_extension(filepath)


def test_extract_file():
    """ Tests the function "extract_file" from heartRateMonitor.py using a
    dummy csv file, "dummy.csv"

    :returns: True if columns from dummy.csv have been successfully extracted,
    False otherwise
    """
    from heartRateMonitor import extract_file
    assert extract_file("dummy.csv")[0] == [0, 1, 2]
    assert extract_file("dummy.csv")[1] == [0, 1, 3]


def test_convert_to_floats():
    """ Tests the function "convert_to_floats" from heartRateMonitor.py

    :returns: True if floats successfully casted and interpolation indices
    correctly generated, False otherwise
    """
    from heartRateMonitor import convert_to_floats

    # Test integers and parseable strings
    assert convert_to_floats([32.4, 234, '24'])[0] == pytest\
        .approx([32.4, float(234), float(24)])
    assert convert_to_floats([32.4, 234, '24'])[1] == []

    # Test that correct indices are returned for nan, bools, and non-parseable
    # strings
    assert convert_to_floats(['hello', float('nan'), True])[1] == [0, 1, 2]


def test_interpolate():
    """ Tests the function "interpolate" from heartRateMonitor.py

    :returns: True if data successfully interpolated, False otherwise
    """
    from heartRateMonitor import interpolate

    # No interpolation case
    assert interpolate([0.0, 1.0, 2.0], [1.0, 2.0, 3.0], [], []
                       )[0] == pytest.approx([0.0, 1.0, 2.0])
    assert interpolate([0.0, 1.0, 2.0], [1.0, 2.0, 3.0], [], []
                       )[1] == pytest.approx([1.0, 2.0, 3.0])

    # Time interpolation case
    assert interpolate([0.0, 'hi', 2.0], [1.0, 2.3, 3.0], [1], []
                       )[0] == pytest.approx([0.0, 1.3, 2.0])
    assert interpolate([0.0, 'hi', 2.0], [1.0, 2.3, 3.0], [1], []
                       )[1] == pytest.approx([1.0, 2.3, 3.0])

    # Voltage interpolation case
    assert interpolate([0.0, 1.8, 2.0], [1.0, 'hi', 3.0], [], [1]
                       )[0] == pytest.approx([0.0, 1.8, 2.0])
    assert interpolate([0.0, 1.8, 2.0], [1.0, 'hi', 3.0], [], [1]
                       )[1] == pytest.approx([1.0, 2.8, 3.0])

    # Time AND voltage interpolation case
    assert interpolate([0.0, 1.8, 2.0, 'hi', 4], [1.0, 'hi', 3.0, 4.0, 5.0],
                       [3], [1])[0] == pytest.approx([0.0, 1.8, 2.0, 3.0, 4.0])
    assert interpolate([0.0, 1.8, 2.0, 'hi', 4], [1.0, 'hi', 3.0, 4.0, 5.0],
                       [3], [1])[1] == pytest.approx([1.0, 2.8, 3.0, 4.0, 5.0])

    # First entry case
    assert interpolate(['hi', 1.0, 2.0], [1.0, 2.0, 3.0], [0], []
                       )[0] == pytest.approx([1.0, 2.0])
    assert interpolate(['hi', 1.0, 2.0], [1.0, 2.0, 3.0], [0], []
                       )[1] == pytest.approx([2.0, 3.0])

    # Last entry case
    assert interpolate([0.0, 1.0, 'hi'], [1.0, 2.0, 3.0], [2], []
                       )[0] == pytest.approx([0.0, 1.0])
    assert interpolate([0.0, 1.0, 'hi'], [1.0, 2.0, 3.0], [2], []
                       )[1] == pytest.approx([1.0, 2.0])


def test_voltage_clip():
    """ Tests the function "check_extension" from heartRateMonitor.py

    :returns: passes if ValueError properly raised and voltage properly clipped
    when above 300mV, fails otherwise
    """
    from heartRateMonitor import voltage_clip

    assert voltage_clip([0.0, 1.0, 300.0, 301.0]) == pytest.approx(
        [0.0, 1.0, 300.0, 300.0])

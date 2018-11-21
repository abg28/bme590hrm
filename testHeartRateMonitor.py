import pytest
import json


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
    """ Tests the function "voltage_clip" from heartRateMonitor.py

    :returns: passes if voltage properly clipped when above 300mV, fails
    otherwise
    """
    from heartRateMonitor import voltage_clip

    assert voltage_clip([0.0, 1.0, 300.0, 301.0]) == pytest.approx(
        [0.0, 1.0, 300.0, 300.0])


@pytest.mark.parametrize("times",
                         [[0, 1, 3, 2],
                          [0, 1, -2.3, 6]]
                         )
def test_check_time_data(times):
    """ Tests the function "check_time_data" from heartRateMonitor.py

    :param times: List of time data
    :returns: passes if exceptions raised when necessary, fails
    otherwise
    """
    from heartRateMonitor import check_time_data
    with pytest.raises(ValueError):
        check_time_data(times)


def test_user_specify_time():
    """ Tests the function "user_specify_time" from heartRateMonitor.py

    :returns: passes if time and voltage data trimmed up to user-specified
    end time, fails otherwise
    """
    from heartRateMonitor import user_specify_time

    # User specified end time is too high
    assert user_specify_time([0.0, 0.01, 0.02, 0.03],
                             [0.0, 100.0, 200.0, 300.0],
                             0.04)[0] == pytest.approx(
        [0.0, 0.01, 0.02, 0.03])
    assert user_specify_time([0.0, 0.01, 0.02, 0.03],
                             [0.0, 100.0, 200.0, 300.0],
                             0.04)[1] == pytest.approx(
        [0.0, 100.0, 200.0, 300.0])

    # User specified end time is too low (i.e. negative)
    assert user_specify_time([0.0, 0.01, 0.02, 0.03],
                             [0.0, 100.0, 200.0, 300.0],
                             -1)[0] == pytest.approx(
        [0.0, 0.01, 0.02, 0.03])
    assert user_specify_time([0.0, 0.01, 0.02, 0.03],
                             [0.0, 100.0, 200.0, 300.0],
                             -1)[1] == pytest.approx(
        [0.0, 100.0, 200.0, 300.0])

    # User specified end time is valid; should trim
    assert user_specify_time([0.0, 0.01, 0.02, 0.03],
                             [0.0, 100.0, 200.0, 300.0],
                             0.02)[0] == pytest.approx(
        [0.0, 0.01, 0.02])
    assert user_specify_time([0.0, 0.01, 0.02, 0.03],
                             [0.0, 100.0, 200.0, 300.0],
                             0.02)[1] == pytest.approx(
        [0.0, 100.0, 200.0])


def test_get_duration():
    """ Tests the function "get_duration" from heartRateMonitor.py

    :returns: passes if correct duration returned, fails otherwise
    """
    from heartRateMonitor import get_duration
    # Min time is zero
    assert get_duration([0.0, 0.1, 0.2, 0.3, 0.6]) == pytest.approx(0.6)
    # Min time is non-zero
    assert get_duration([0.3, 0.4, 0.5]) == pytest.approx(0.2)


def test_get_voltage_extremes():
    """ Tests the function "get_voltage_extremes" from heartRateMonitor.py

    :return: passes if correct voltage min and max values returned, fails o.w.
    """
    from heartRateMonitor import get_voltage_extremes
    assert get_voltage_extremes([0.0, 0.3, 0.2, 0.6])[0] == pytest.approx(0.0)
    assert get_voltage_extremes([0.0, 0.3, 0.2, 0.6])[1] == pytest.approx(0.6)


times = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# Simple triangle waveform
voltages = [0, 1, 2, 1, 0, 1, 2, 1, 0, 1]


def test_get_beats_times():
    """ Tests the function "get_beats_times" from heartRateMonitor.py

    :return: passes if correct time values are returned, fails otherwise
    """
    from heartRateMonitor import get_beats_times
    assert get_beats_times(times, voltages) == pytest.approx([2, 6])


def test_get_num_beats():
    """ Tests the function "get_num_beats" from heartRateMonitor.py

    :return: passes if correct number is returned, fails otherwise
    """
    from heartRateMonitor import get_num_beats
    assert get_num_beats(times, voltages) == 2


def test_get_mean_hr_bpm():
    """ Tests the function "get_mean_hr_bpm" from heartRateMonitor.py

    :return: passes if correct average HR returned, fails otherwise
    """
    from heartRateMonitor import get_mean_hr_bpm
    assert get_mean_hr_bpm(times, voltages) == 2/10 * 60


def test_metrics_to_dict():
    """ Tests the function "metrics_to_dict" from heartRateMonitor.py

    :return: passes if the dictionary is properly created, fails otherwise
    """
    from heartRateMonitor import metrics_to_dict
    assert metrics_to_dict(times, voltages)["mean_hr_bpm"] == 2/10*60
    assert metrics_to_dict(times, voltages)["voltage_extremes"] == (0, 2)
    assert metrics_to_dict(times, voltages)["duration"] == 10
    assert metrics_to_dict(times, voltages)["num_beats"] == 2
    assert metrics_to_dict(times, voltages)["beats"] == [2, 6]


def test_dict_to_json():
    """ Tests the function "dict_to_json" from heartRateMonitor.py

    :return: Tests if JSON filename correctly outputted and openable, fails
    otherwise
    """
    from heartRateMonitor import dict_to_json
    from heartRateMonitor import metrics_to_dict
    assert dict_to_json(metrics_to_dict(times, voltages),
                        "test.csv") == "test.json"
    with open("test.json", "r") as testfile:
        ret_dict = json.load(testfile)
        assert ret_dict["mean_hr_bpm"] == 2 / 10 * 60
        assert ret_dict["voltage_extremes"] == [0, 2]
        assert ret_dict["duration"] == 10
        assert ret_dict["num_beats"] == 2
        assert ret_dict["beats"] == [2, 6]

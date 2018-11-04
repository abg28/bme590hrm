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

    :param filepath: the inputted file path
    :returns: True if columns from dummy.csv have been successfully extracted,
    False otherwise
    """
    from heartRateMonitor import extract_file
    assert extract_file("dummy.csv")[0] == [0, 1, 2]
    assert extract_file("dummy.csv")[1] == [0, 1, 3]

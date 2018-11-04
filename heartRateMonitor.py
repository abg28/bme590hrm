import pandas
import logging


def main():
    """ Driver function that runs the program

    :returns: void
    """
    logging.basicConfig(filename="log.txt",
                        filemode='w',
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info("Started")
    filepath = "/Users/alexanderguevara/PycharmProjects/Medical-Software-" \
               "Design/Assignments/" \
               "HeartRateMonitor/test_data/test_data1.csv"
    check_file_existence(filepath)
    check_extension(filepath)
    time, voltage = extract_file(filepath)
    print(time)
    print(voltage)
    logging.info("Finished")


# FILE IO FUNCTIONS
def check_file_existence(filepath):
    """ Checks to see if a file exists in the filepath

    :param filepath: the path to the file
    :returns: True if file exists, False otherwise
    """
    try:
        open(filepath, 'r')
    except FileNotFoundError:
        logging.error("Csv file not found")
        raise FileNotFoundError("The inputted csv file could not be found.  "
                                "Double-check the file path!")


def check_extension(filepath):
    """ Checks to see if a file has .csv as its extension
    (and by extension, that a string has been passed in for the filepath)

    :param filepath: the path to the file
    :returns: True if file is of type csv, False otherwise (including
    non-string datatypes)
    """
    length = len(filepath)
    extension = filepath.lower()[length-4:length]
    if not extension == ".csv":
        logging.error("File not csv")
        raise TypeError("The inputted file is not a csv.")


def extract_file(filepath):
    """ Reads in a csv file containing time and voltage data, and returns the
    data in list format

    :param filepath: the path to the csv file
    :returns: lists containing time and voltage values, respectively
    """
    dataframe = pandas.read_csv(filepath, names=["Time", "Voltage"])
    time = dataframe["Time"].tolist()
    voltage = dataframe["Voltage"].tolist()
    return time, voltage


if __name__ == "__main__":
    main()

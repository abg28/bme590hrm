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
    interp_time_inds, time = convert_to_floats(time)
    interp_voltage_inds, voltage = convert_to_floats(voltage)
    logging.info("Finished")


# FILE I/O FUNCTIONS
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


# DATA PREPROCESSING FUNCTIONS
def convert_to_floats(datalist):
    """ Converts a list of data into floats, if possible.  Returns the indices
    of all values that cannot be casted as float.

    :param datalist: The list of data (either time or voltage)
    :return: A list containing float values and indices of non-float values
    """
    float_data = []
    interp_indices = []
    for index, entry in enumerate(datalist):
        try:
            if pandas.isnull(entry) or type(entry) is bool:
                raise ValueError
            cast_val = float(entry)
            float_data.append(cast_val)
        except ValueError:
            logging.warning("Non-float data type: {}".format(entry))
            float_data.append(entry)
            interp_indices.append(index)
    return float_data, interp_indices


def interpolate(times, voltages, time_interp_indices, voltage_interp_indices):
    """ Uses linear interpolation to convert non-float or missing entries to
    workable values for time and voltage.

    :param times: A list of float-converted time data
    :param voltages: A list of float-converted voltage data
    :param time_interp_indices: List indices where time data should be
    replaced with an interpolated value
    :param voltage_interp_indices: List indices where voltage data should be
    replaced with an interpolated value
    :return: Lists of properly interpolated (if applicable) time and voltage
    data
    """
    new_times = []
    new_voltages = []
    for index in range(len(times)):
        if index == 0 or index == len(times) - 1:
            if index in time_interp_indices or index in voltage_interp_indices:
                continue
            else:
                new_times.append(times[index])
                new_voltages.append(voltages[index])
        else:
            if index in time_interp_indices:
                # Interpolates times data
                new_times.append(times[index - 1] + (times[index + 1] -
                                 times[index - 1]) * (voltages[index] -
                                 voltages[index - 1]) / (voltages[index + 1] -
                                                         voltages[index - 1]))
            else:
                new_times.append(times[index])
            if index in voltage_interp_indices:
                # Interpolates voltages data
                new_voltages.append(voltages[index-1] + (times[index] -
                                    times[index-1]) * (voltages[index+1] -
                                    voltages[index-1]) / (times[index+1] -
                                    times[index-1]))
            else:
                new_voltages.append(voltages[index])
    return new_times, new_voltages


def voltage_clip(voltages):
    """ Ensures that all voltage readings are less than or equal to 300mV,
    and clips those that are not to 300mV.

    :param voltages: List of float-casted, interpolated voltages
    :return: List of float-casted, interpolated voltages of at most 300mV
    """
    ret_voltage = []
    for voltage in voltages:
        if voltage > 300.0:
            try:
                raise ValueError
            except ValueError:
                print("WOODHIB")
                ret_voltage.append(300.0)
                logging.warning("Voltage value above 300: %f" % voltage)
        else:
            ret_voltage.append(voltage)
    return ret_voltage


# DATA ANALYSIS FUNCTIONS


if __name__ == "__main__":
    main()

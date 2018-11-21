import pandas
import logging
import peakutils
import numpy
# from matplotlib import pyplot
import json
import argparse


def main(filepath, endtime):
    """ Driver function that runs the program

    :param filepath: A String representing the path to the ECG data
    :param endtime: Time (in seconds) at which the data should end
    :returns: Void
    """
    logging.basicConfig(filename="log.txt",
                        filemode='w',
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info("Started")
    check_file_existence(filepath)
    check_extension(filepath)
    time, voltage = extract_file(filepath)
    logging.info("Csv file successfully read and extracted")
    time, interp_time_inds = convert_to_floats(time)
    voltage, interp_voltage_inds = convert_to_floats(voltage)
    time, voltage = interpolate(time, voltage, interp_time_inds,
                                interp_voltage_inds)
    voltage = voltage_clip(voltage)
    time, voltage = user_specify_time(time, voltage, endtime)
    metrics = metrics_to_dict(time, voltage)
    dict_to_json(metrics)
    # pyplot.plot(time, voltage)
    # pyplot.show()
    logging.info("Finished")


# FILE I/O FUNCTIONS
def check_file_existence(filepath):
    """ Checks to see if a file exists in the filepath

    :param filepath: A String representing the path to the ECG data
    :returns: Void if file exists, raises FileNotFoundError otherwise to
    terminate program
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

    :param filepath: A String representing the path to the ECG data
    :returns: Void if file is of type csv, raises TypeError otherwise
    (including for non-string datatypes)
    """
    length = len(filepath)
    extension = filepath.lower()[length-4:length]
    if not extension == ".csv":
        logging.error("File not csv")
        raise TypeError("The inputted file is not a csv.")


def extract_file(filepath):
    """ Reads in a csv file containing time and voltage data, and returns the
    data in list format

    :param filepath: A String representing the path to the ECG data (csv file)
    :returns: Lists containing time and voltage values, respectively
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
    :return: Lists containing float values and indices of non-float values,
    respectively
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
                ret_voltage.append(300.0)
                logging.warning("Voltage value above 300: %f" % voltage)
        else:
            ret_voltage.append(voltage)
    return ret_voltage


def check_time_data(times):
    """ Checks to ensure that the time data consists of non-negative floats
    and is in ascending order (i.e. the way time data should be expected to
    look)

    :param times: List of time data
    :return: Void if time data checks out ok, raises ValueError otherwise to
    terminate program
    """
    for index, time in enumerate(times):
        if time < 0.0:
            raise ValueError("Negative time value!")
        if index > 0 and times[index] >= times[index-1]:
            raise ValueError("Time data not in ascending order!")


# DATA ANALYSIS FUNCTIONS
def user_specify_time(times, voltages, end_time):
    """ Cuts off all time and voltage data that occurs after the user-specified
    end time.  If the user does not specify an end time, this function will
    default to keeping the time array untrimmed.

    :param times: List of time data
    :param voltages: List of voltage data
    :param end_time: Time (in seconds) at which the data should end
    :return: Trimmed time and voltage lists
    """
    try:
        if pandas.isnull(end_time) or type(end_time) is bool:
            raise ValueError
        end_time = float(end_time)
        if end_time < 0 or end_time > max(times):
            raise ValueError
    except ValueError:
        logging.warning("End time not valid: {}".format(end_time))
        logging.warning("Using default end time by not trimming data at all.")
        return times, voltages
    ret_times = []
    ret_voltages = []
    for index, time in enumerate(times):
        if time <= end_time:
            ret_times.append(time)
            ret_voltages.append(voltages[index])
        else:
            break
    return ret_times, ret_voltages


def get_duration(times):
    """ Finds and returns the duration of the ECG in units of seconds.

    :param times: List of time data
    :return: Float representing duration of ECG data
    """
    return max(times) - min(times)


def get_voltage_extremes(voltages):
    """ Finds and returns the minimum and maximum voltages measured in the
    ECG signal.

    :param voltages: List of voltage measurements
    :return: Tuple containing min and max voltages (floats)
    """
    return min(voltages), max(voltages)


def get_beats_times(times, voltages):
    """ Determines the time at which each beat in the sample occurs.  Beats
    are found using a peak detection algorithm that has a minimum threshold
    of 80% of the maximum voltage value present in the data.

    :param times: List of time data
    :param voltages: List of voltage data
    :return: A numpy array of times (floats) when the beats occurred
    """
    qrs_indexes = peakutils.peak.indexes(voltages, thres=0.80)
    beat_times = []
    for index in qrs_indexes:
        beat_times.append(times[index])
    return numpy.array(beat_times)


def get_num_beats(times, voltages):
    """ Calculates the number of beats in the sample.

    :param times: List of time data
    :param voltages: List of voltage data
    :return: Int representing the number of detected beats
    """
    return get_beats_times(times, voltages).size


def get_mean_hr_bpm(times, voltages):
    """ Calculates the average heart rate over the sample's interval, in beats
    per minute.

    :param times: List of time data
    :param voltages: List of voltage data
    :return: Float representing the average heart rate in bpm
    """
    return get_num_beats(times, voltages) / get_duration(times) * 60


def metrics_to_dict(times, voltages):
    """ Creates a metrics dictionary with entries for mean heartrate (in bpm),
    voltage extremes, duration of the ECG signal, number of beats detected,
    and times at which beats were detected.

    :param times: List of time data
    :param voltages: List of voltage data
    :return: Void
    """
    metrics = {"mean_hr_bpm": get_mean_hr_bpm(times, voltages),
               "voltage_extremes": get_voltage_extremes(voltages),
               "duration": get_duration(times),
               "num_beats": get_num_beats(times, voltages),
               "beats": get_beats_times(times, voltages).tolist()}
    return metrics


def dict_to_json(metrics, input_filepath):
    """ Outputs metrics dictionary as a JSON file with the same name (and
    directory) as the original csv file from the beginning of the pipeline.

    :param metrics: Dictionary of metrics
    :param input_filepath: The filepath of the inputted csv
    :return: String representing filepath of new JSON file
    """
    json_filepath = input_filepath[:-3] + "json"
    with open(json_filepath, "w") as file:
        json.dump(metrics, file)
    logging.info("JSON file written: %s" % json_filepath)
    return json_filepath


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="Filepath of the data file")
    parser.add_argument("endtime", help="Time (in seconds) at which the "
                                        "data should end")
    args = parser.parse_args()
    main(args.filepath, args.endtime)

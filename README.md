# bme590hrm
Author: Alex Guevara (GitHub username/Duke netID: abg28)
Version: 1.0.0 
Release Date: 11/20/18

# Summary
This repository houses software for the monitoring of patients' heart rates.  It is intended to analyze raw ECG data from a csv file, and return a JSON file with several metrics related to the state of the patient's heart, including:

* Average heart rate in beats per minute
* Minimum and maximum voltages detected
* Time duration of the signal in units of seconds
* Number of heart beats detected
* Times at which the beats occurred in units of seconds

The repository contains several files:

* heartRateMonitor.py --> Python file that contains all of the executable code and functions
* testHeartRateMonitor.py --> Python file that contains the unit tests for each function
* log.txt --> Text file to which the logging module outputs important messages about the program during runtime (will be created automatically for each execution of heartRateMonitor.py)
* test_data_1.csv --> Csv file for testing use, from mlp6's Medical-Software-Design repository
* dummy.csv --> Csv file used in one of the unit tests
* .travis.yml --> Yaml file that specifies how Travis CI should run its integration tests
* requirements.txt --> Text file that lists the required packages to be installed in a user's virtual environment, should they fork and/or clone this repository

# Instructions for Use
Users should run the heartRateMonitor.py file in a Python3 environment that contains the packages outlined in the requirements.txt file.  The file is driven by its main method, which takes two positional arguments, in the following order:

1. filepath --> The path to the file with the desired ECG data to be read in
2. endtime --> The user's preferred upper bound to the time window of the ECG data

Descriptions of the above arguments can also be found by using the -h flag from the command line.  Note that these arguments are not optional, and the program will not run without some input for each of them.

# How it Works
The program reads in a csv file with two columns, the first representing time and the second representing voltage data.  This data is extracted from the csv file and into two separate Python list variables, which then undergo several preprocessing steps.  Most importantly, the values in these lists must either be floats or castable to floats; the program is able to linearly interpolate missing or non-float values, so long as they are not adjacent to other missing or non-float values (one of the program's main limitations).

Once the data is cleaned up, the metrics listed above are then calculated.  The driver of this process is a peak detection algorithm from the peakutils package.  A relative threshold of 0.80 is employed, such that all peaks that the algorithm detects must have a value of at least 80% of the data's maximum voltage value in order to be considered valid.  From exploratory testing on several of the sample csv files provided in mlp6's Medical-Software-Design repository, this threshold appears to work quite well.  However, it does not account for any vertical offsets that may occur during the course of ECG measurement, which could prove to be an issue for robustness.

Finally, the above metrics are outputted to a JSON file bearing the same name and filepath as the user-inputted csv, barring the extension.

# Travis Build Status Indicator (branch master)
[![Build Status](https://travis-ci.org/abg28/bme590hrm.svg?branch=master)](https://travis-ci.org/abg28/bme590hrm)

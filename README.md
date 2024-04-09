Readme for Scripts for A Dataset of Signals from an Antenna for Detection of Partial Discharges in Overhead XLPE Insulated Power Line

Dataset - https://figshare.com/collections/A_data_set_of_Signals_from_an_Antenna_for_Detection_of_Partial_Discharges_in_Overhead_Insulated_Power_Line/6628553 

This repository contains Python scripts for testing and working with the dataset of signals from an antenna for detection of partial discharges in overhead XLPE insulated power line. Here's a brief description of each script:

test_faults.py - This script is used to test 100 faults randomly selected from the dataset.

test_station.py - This script is used to test a single station in the dataset. It iterates over 100 data points, 1% of data points, and 10 data points with 'faultAnnotation' == 1, randomly selected.

test_monthly.py - This script is used to test a single station by month and year. It calculates metrics and plots.

utilities.py - This script contains utility functions for working with the dataset, such as loading the data, calculating metrics, and plotting.

decompress.sh - decompress the dataset from .xz tar files

intervals.py - visualise and print continuous intervals of data acquisition for each station 

Note that the dataset used by these scripts is not included in this repository and must be obtained separately.

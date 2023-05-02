# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Load CSV file into a pandas DataFrame
df = pd.read_csv('pdfaultNew.csv', delimiter=';')

# Convert the 'timeStamp' column to a datetime format
df['timeStamp'] = pd.to_datetime(df['timeStamp'])

# Filter rows by station ID
station_id = sys.argv[1]
df = df.loc[df['faultAnnotation'] == 1]

# Create a new directory for the output files
os.mkdir(f'test_faults')

# Iterate over a random subset of 100 rows from the filtered DataFrame
for index, row in df.sample(100).iterrows():
    measurement_id = row['idMeasurement']
    # Load the signal data for the current measurement ID
    signal = np.load(f'data/{station_id}/{measurement_id}.npy')
    # Create a plot of the signal data
    plt.plot(signal)
    plt.title(f'Station {station_id}, Measurement {measurement_id}')
    # Save the plot as a PNG file in the output directory
    plt.savefig(f"test_faults/{measurement_id}.png")
    # Clear the current figure so the next plot can be created
    plt.clf()

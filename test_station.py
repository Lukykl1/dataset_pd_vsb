import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Script for testing a single station

# Load CSV file into a pandas DataFrame
df = pd.read_csv('pdfaultNew.csv', delimiter=';')

# Convert the 'timeStamp' column to a datetime format
df['timeStamp'] = pd.to_datetime(df['timeStamp'])

# Filter rows by station ID
station_id = sys.argv[1]
df = df.loc[df['idStation'] == int(station_id)]

# Create a new directory for the test results
os.mkdir(f"test_{station_id}")

# Iterate through each measurement and plot every 1000th sample
for index, row in df[::1000].iterrows():
    measurement_id = row['idMeasurement']
    signal = np.load(f'data/{station_id}/{measurement_id}.npy')
    plt.plot(signal)
    plt.title(f'Station {station_id}, Measurement {measurement_id}')
    plt.savefig(f"test_{station_id}//{measurement_id}.png")
    plt.clf()

# Iterate through 1% of data randomly and plot each measurement
for index, row in df.sample(frac=0.001).iterrows():
    measurement_id = row['idMeasurement']
    signal = np.load(f'data/{station_id}/{measurement_id}.npy')
    plt.plot(signal)
    plt.title(f'Station {station_id}, Measurement {measurement_id}')
    plt.savefig(f"test_{station_id}//random_{measurement_id}.png")
    plt.clf()

# Iterate through 10 of data randomly with ['faultAnnotation'] == 1 and plot each measurement
for index, row in df.loc[df['faultAnnotation'] == 1].sample(10).iterrows():
    measurement_id = row['idMeasurement']
    signal = np.load(f'data/{station_id}/{measurement_id}.npy')
    plt.plot(signal)
    plt.title(f'Station {station_id}, Measurement {measurement_id}')
    plt.savefig(f"test_{station_id}//fault_{measurement_id}.png")
    plt.clf()

# If the second argument in command line is "stats"
if sys.argv[2] == "stats":
    # Calculate metrics across all measurements (mean, std, min, max)
    df['mean'] = df['idMeasurement'].apply(lambda x: np.load(f'data/{station_id}/{x}.npy').mean())
    df['std'] = df['idMeasurement'].apply(lambda x: np.load(f'data/{station_id}/{x}.npy').std())
    df['min'] = df['idMeasurement'].apply(lambda x: np.load(f'data/{station_id}/{x}.npy').min())
    df['max'] = df['idMeasurement'].apply(lambda x: np.load(f'data/{station_id}/{x}.npy').max())

    # Print the calculated metrics
    print("Mean", df['mean'].mean())
    print("Std", df['std'].mean())
    print("Min", df['min'].mean())
    print("Max", df['max'].mean())

    # Calculate outliers between samples using statistical methods
    df['outlier'] = df['idMeasurement'].apply(lambda x: np.load(f'data/{station_id}/{x}.npy'))
    df['outlier'] = df['outlier'].apply(lambda x: 1 if (x > (df['mean'].mean() + 3*df['std'].mean())).any() or (x < (df['mean'].mean() - 3*df['std'].mean())).any() else 0)

    # Print the outliers
    print(df['outlier'].value_counts())


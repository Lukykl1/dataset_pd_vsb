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

os.mkdir(f'test_faults')
#iterate 100 of data randomly
for index, row in df.sample(100).iterrows():
    measurement_id = row['idMeasurement']
    signal = np.load(f'data/{station_id}/{measurement_id}.npy')
    plt.plot(signal)
    plt.title(f'Station {station_id}, Measurement {measurement_id}')
    plt.savefig(f"test_faults/{measurement_id}.png")
    plt.clf()

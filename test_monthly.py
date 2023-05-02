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
df = df.loc[df['idStation'] == int(station_id)]

os.mkdir(f"test_{station_id}")
# Group by month and year
df['month'] = df['timeStamp'].dt.month
df['year'] = df['timeStamp'].dt.year

# Load all signals calculate mean and std of the signals and plot grouped by month and year
df['mean'] = df['idMeasurement'].apply(lambda x: np.load(f'data/{station_id}/{x}.npy').mean())
df['std'] = df['idMeasurement'].apply(lambda x: np.load(f'data/{station_id}/{x}.npy').std())
df['min'] = df['idMeasurement'].apply(lambda x: np.load(f'data/{station_id}/{x}.npy').min())
df['max'] = df['idMeasurement'].apply(lambda x: np.load(f'data/{station_id}/{x}.npy').max())

#plotting
df.groupby(['year', 'month']).mean()['mean'].plot()
plt.title(f'Station {station_id}, Mean')
plt.savefig(f"test_{station_id}/_mean.png")
plt.clf()

df.groupby(['year', 'month']).mean()['std'].plot()
plt.title(f'Station {station_id}, Std')
plt.savefig(f"test_{station_id}/_std.png")
plt.clf()

df['abs_mean'] = df['idMeasurement'].apply(lambda x: np.abs(np.load(f'data/{station_id}/{x}.npy')).mean())
df.groupby(['year', 'month']).mean()['abs_mean'].plot()
plt.title(f'Station {station_id}, Abs Mean')
plt.savefig(f"test_{station_id}/_abs_mean.png")
plt.clf()

df['abs_std'] = df['idMeasurement'].apply(lambda x: np.abs(np.load(f'data/{station_id}/{x}.npy')).std())
df.groupby(['year', 'month']).mean()['abs_std'].plot()
plt.title(f'Station {station_id}, Abs Std')
plt.savefig(f"test_{station_id}/_abs_std.png")
plt.clf()

df.groupby(['year', 'month']).mean()['min'].plot()
plt.title(f'Station {station_id}, Min')
plt.savefig(f"test_{station_id}/_min.png")
plt.clf()

df.groupby(['year', 'month']).mean()['max'].plot()
plt.title(f'Station {station_id}, Max')
plt.savefig(f"test_{station_id}/_max.png")
plt.clf()

df.groupby(['year', 'month']).count()['idMeasurement'].plot()
plt.title(f'Station {station_id}, Count')
plt.savefig(f"test_{station_id}/_count.png")
plt.clf()


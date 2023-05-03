import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('inferred_annotation.csv', sep=';')

# Convert the timeStamp column to datetime format
df['timeStamp'] = pd.to_datetime(df['timeStamp'])

# Sort the DataFrame by idStation and timeStamp
df = df.sort_values(['idStation', 'timeStamp'])

# Create a DataFrame to store the intervals
intervals = pd.DataFrame(columns=['idStation', 'start', 'end'])

# Iterate over the groups of data for each station
for station, group in df.groupby('idStation'):
    # Create a list to store the continuous intervals for this station
    station_intervals = []
    
    # Initialize the start and end timestamps for the first interval
    start = group.iloc[0]['timeStamp']
    end = group.iloc[0]['timeStamp']
    
    # Iterate over the rows in the group, checking for missing hours
    for i in range(1, len(group)):
        # Calculate the expected timestamp for the next measurement
        expected_timestamp = end + pd.Timedelta(hours=1)
        
        # Get the actual timestamp for the next measurement
        actual_timestamp = group.iloc[i]['timeStamp']
        
        # If the actual timestamp is not the expected timestamp, there is a missing hour
        if actual_timestamp > expected_timestamp:
            # Add the current interval to the list of intervals for this station
            station_intervals.append({'idStation': station, 'start': start, 'end': end})
            
            # Start a new interval with the current row as the first measurement
            start = actual_timestamp
            end = actual_timestamp
        else:
            # The current row is within the current interval, so update the end timestamp
            end = actual_timestamp
    
    # Add the last interval to the list of intervals for this station
    station_intervals.append({'idStation': station, 'start': start, 'end': end})
    
    # Add the intervals for this station to the DataFrame
    intervals = intervals.append(station_intervals, ignore_index=True)

# Print the resulting all intervals
print(intervals)
#count of non overlapping intervals per station
print(intervals.groupby(['idStation']).size())
#save to csv
intervals.to_csv('intervals.csv', sep=';', index=False)
#visualize intervals
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# Create a figure and axis
fig, ax = plt.subplots()

# Plot the intervals
for station, group in intervals.groupby('idStation'):
    # Create a list of the start and end timestamps for each interval
    start_times = group['start'].tolist()
    end_times = group['end'].tolist()
    
    # Create a list of the start and end timestamps for the x-axis
    x = start_times + end_times
    x.sort()
    
    # Create a list of the y-axis values
    y = [station] * len(x)
    
    # Plot the intervals
    ax.plot(x, y, color='blue')
    # plot the points
    ax.plot(start_times, [station] * len(start_times), 'o', color='red')
    ax.plot(end_times, [station] * len(end_times), 'o', color='green')
    
# Set the x-axis limits
ax.set_xlim([df['timeStamp'].min(), df['timeStamp'].max()])
#plot
plt.show()
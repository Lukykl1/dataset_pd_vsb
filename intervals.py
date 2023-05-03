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
        expected_timestamp = end + pd.Timedelta(hours=8)
        
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

fig, axs = plt.subplots(nrows=int(len(intervals['idStation'].unique())/2), ncols=2, figsize=(12,4*len(intervals['idStation'].unique())))

for i, (station, group) in enumerate(intervals.groupby('idStation')):
    # Create a list of the start and end timestamps for each interval
    start_times = group['start'].tolist()
    end_times = group['end'].tolist()

    # Convert the Timedelta objects to numerical values
    start_values = [(t - start_times[0]).total_seconds() / (24 * 3600) for t in start_times]
    end_values = [(t - start_times[0]).total_seconds() / (24 * 3600) for t in end_times]

    # Plot the intervals as horizontal bars on the y-axis
    axs[i//2, i%2].broken_barh([(start_values[j], end_values[j]-start_values[j]) for j in range(len(start_values))], 
                   (0, 0.5), 
                   facecolors='blue')

    # Set the x-axis label and title
    axs[i//2, i%2].set_xlabel('Time (days)')
    axs[i//2, i%2].set_title(f'Intervals for Station {station}')
    #remove y axis
    axs[i//2, i%2].get_yaxis().set_visible(False)
    #increase hspace
    fig.subplots_adjust(hspace=0.85)
    


# Show the plot
plt.show()

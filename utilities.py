import pandas as pd
import numpy as np

# Load metadata into a pandas DataFrame
metadata = pd.read_csv('metadata.csv', header=0, names=["idStation", "idMeasurement", "faultAnnotation", "timeStamp"])

def load_signal(station_id, measurement_id):
    """Load a signal from a .npy file under the data directory."""
    path = f"data/{station_id}/{measurement_id}.npy"
    signal = np.load(path, dtype=np.int8).astype('int8')
    return signal

def get_station_measurements(station_id):
    """Return a list of measurement IDs for a given station."""
    measurements = metadata.loc[metadata['idStation'] == station_id, 'idMeasurement'].tolist()
    return measurements

def get_fault_annotations(station_id, measurement_id):
    """Return the fault annotations for a given station and measurement."""
    annotations = metadata.loc[(metadata['idStation'] == station_id) & (metadata['idMeasurement'] == measurement_id), 'faultAnnotation'].tolist()
    return annotations

def get_measurement_timestamp(station_id, measurement_id):
    """Return the timestamp for a given station and measurement."""
    timestamp = metadata.loc[(metadata['idStation'] == station_id) & (metadata['idMeasurement'] == measurement_id), 'timeStamp'].tolist()
    return timestamp[0] if timestamp else None

def load_station_memmap(station_id):
    """Load a whole station into memory using memmap."""
    measurements = get_station_measurements(station_id)
    data = []
    for measurement_id in measurements:
        path = f"data/{station_id}/{measurement_id}.npy"
        if os.path.exists(path):
            signal = np.load(path, mmap_mode='r').astype('int8')
            data.append(signal)
    station = np.concatenate(data, axis=0)
    return station

def load_station_dask(station_id):
    """Load a whole station using Dask."""
    measurements = get_station_measurements(station_id)
    data = []
    for measurement_id in measurements:
        path = f"data/{station_id}/{measurement_id}.npy"
        if os.path.exists(path):
            signal = da.from_array(np.load(path, dtype=np.int8), chunks='auto')
            data.append(signal)
    station = da.concatenate(data, axis=0)
    return station


def load_station_data(station_id):
    """Load the data for a given station into a single flat NumPy array."""
    measurements = get_station_measurements(station_id)
    data = []
    for measurement_id in measurements:
        path = f"data/{station_id}/{measurement_id}.npy"
        if os.path.exists(path):
            signal = np.load(path, dtype=np.int8).astype('float32')
            data.append(signal)
    station = np.concatenate(data, axis=0)
    return station

def split_dataset(data, test_percent=0.2, val_percent=0.2):
    """Split the dataset into train-validation-test sets."""
    n_samples = len(data)
    n_test = int(n_samples * test_percent)
    n_val = int(n_samples * val_percent)
    n_train = n_samples - n_test - n_val
    train_data = data[:n_train]
    val_data = data[n_train:n_train+n_val]
    test_data = data[-n_test:]
    return train_data, val_data, test_data

def has_fault_annotation(station_id, measurement_id):
    """Return True if the measurement has a fault annotation."""
    annotations = get_fault_annotations(station_id, measurement_id)
    return 1 in annotations

def get_fault_data(station_id):
    """Create a flat array containing only fault data."""
    measurements = get_station_measurements(station_id)
    data = []
    for measurement_id in measurements:
        path = f"data/{station_id}/{measurement_id}.npy"
        if os.path.exists(path):
            signal = np.load(path, dtype=np.int8).astype('float32')
            if has_fault_annotation(station_id, measurement_id):
                data.append(signal)
    fault_data = np.concatenate(data, axis=0)
    return fault_data

def get_percent_data(data, percent):
    """Create a flat array containing a percentage of the data."""
    n_samples = len(data)
    n_samples_percent = int(n_samples * percent)
    percent_data = data[:n_samples_percent]
    return percent_data


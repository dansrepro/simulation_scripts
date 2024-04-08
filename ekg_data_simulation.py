## EKG

import random
import pandas as pd
from datetime import datetime, timedelta

def generate_normal_ekg_data(start_time, end_time, frequency_seconds, patient_id):
    timestamps = pd.date_range(start=start_time, end=end_time, freq=f'{frequency_seconds}S')
    values = [random.uniform(0.8, 1.2) for _ in range(len(timestamps))]
    data = pd.DataFrame({'Timestamp': timestamps, 'PatientId': [patient_id]*len(timestamps), 'Value': values})
    return data

def generate_anomaly_ekg_data(normal_data):
    anomaly_data = normal_data.copy()
    num_rows = len(anomaly_data)
    anomaly_events = []

    # Arrhythmia
    arrhythmia_intervals = [(random.randint(num_rows//10, num_rows//2), random.randint(60, 300)) for _ in range(2)]
    for start, length in arrhythmia_intervals:
        for i in range(start, min(start + length, num_rows)):
            anomaly_data.loc[i, 'Value'] *= random.uniform(0.5, 1.5)
        anomaly_events.append((anomaly_data.loc[start, 'Timestamp'], 'Arrhythmia Start'))
        anomaly_events.append((anomaly_data.loc[min(start + length - 1, num_rows - 1), 'Timestamp'], 'Arrhythmia End'))

    # Ischemic Changes
    ischemic_intervals = [(random.randint(num_rows//10, num_rows//2), random.randint(30, 120)) for _ in range(2)]
    for start, length in ischemic_intervals:
        for i in range(start, min(start + length, num_rows)):
            anomaly_data.loc[i, 'Value'] -= random.uniform(0.1, 0.3)
        anomaly_events.append((anomaly_data.loc[start, 'Timestamp'], 'Ischemic Change Start'))
        anomaly_events.append((anomaly_data.loc[min(start + length - 1, num_rows - 1), 'Timestamp'], 'Ischemic Change End'))

    # Conduction Block
    block_intervals = [(random.randint(num_rows//10, num_rows//2), random.randint(10, 50)) for _ in range(2)]
    for start, length in block_intervals:
        for i in range(start, min(start + length, num_rows)):
            anomaly_data.loc[i, 'Value'] *= 0.9
        anomaly_events.append((anomaly_data.loc[start, 'Timestamp'], 'Conduction Block Start'))
        anomaly_events.append((anomaly_data.loc[min(start + length - 1, num_rows - 1), 'Timestamp'], 'Conduction Block End'))

    # Myocardial Infarction
    mi_intervals = [(random.randint(num_rows//10, num_rows//2), random.randint(20, 60)) for _ in range(1)]
    for start, length in mi_intervals:
        for i in range(start, min(start + length, num_rows)):
            anomaly_data.loc[i, 'Value'] += random.uniform(0.2, 0.5)
        anomaly_events.append((anomaly_data.loc[start, 'Timestamp'], 'Myocardial Infarction Start'))
        anomaly_events.append((anomaly_data.loc[min(start + length - 1, num_rows - 1), 'Timestamp'], 'Myocardial Infarction End'))

    return anomaly_data, anomaly_events

# Generate normal and anomaly EKG data
start_time = datetime(2023, 1, 1)
end_time = datetime(2023, 1, 2)  # One day of data
frequency_seconds = 1  # Sampling rate of 1 second
patient_id = 1

normal_data = generate_normal_ekg_data(start_time, end_time, frequency_seconds, patient_id)
anomaly_data, anomaly_events = generate_anomaly_ekg_data(normal_data)

# Save the normal and anomaly EKG data to CSV files
normal_data.to_csv('normal_ekg_data.csv', index=False, sep=';')
anomaly_data.to_csv('anomaly_ekg_data.csv', index=False, sep=';')

# Save the anomaly events to a text file
with open('ekg_anomaly_events.txt', 'w') as f:
    for event in anomaly_events:
        f.write(f"{event[0]};{event[1]}\n")

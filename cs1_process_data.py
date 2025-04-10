import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os

# Set paths
data_path = '/home/ubuntu/cyclistic_data/csv/'
output_path = '/home/ubuntu/cyclistic_data/processed/'

# Create output directory if it doesn't exist
if not os.path.exists(output_path):
    os.makedirs(output_path)

# Read the data
print("Reading 2019 Q1 data...")
df_2019_q1 = pd.read_csv(data_path + 'Divvy_Trips_2019_Q1.csv')

print("Reading 2020 Q1 data...")
df_2020_q1 = pd.read_csv(data_path + 'Divvy_Trips_2020_Q1.csv')

# Display basic information about the datasets
print("\n2019 Q1 Data Info:")
print(f"Shape: {df_2019_q1.shape}")
print(f"Columns: {df_2019_q1.columns.tolist()}")
print(df_2019_q1.head(2))

print("\n2020 Q1 Data Info:")
print(f"Shape: {df_2020_q1.shape}")
print(f"Columns: {df_2020_q1.columns.tolist()}")
print(df_2020_q1.head(2))

# Clean and standardize column names for 2019 Q1 data
print("\nStandardizing 2019 Q1 data...")
df_2019_q1_clean = df_2019_q1.rename(columns={
    'trip_id': 'ride_id',
    'start_time': 'started_at',
    'end_time': 'ended_at',
    'from_station_id': 'start_station_id',
    'from_station_name': 'start_station_name',
    'to_station_id': 'end_station_id',
    'to_station_name': 'end_station_name',
    'usertype': 'member_casual'
})

# Convert member_casual values to match 2020 format (Subscriber -> member, Customer -> casual)
df_2019_q1_clean['member_casual'] = df_2019_q1_clean['member_casual'].replace({
    'Subscriber': 'member',
    'Customer': 'casual'
})

# Add rideable_type column to 2019 data (all are docked_bike)
df_2019_q1_clean['rideable_type'] = 'docked_bike'

# Select and reorder columns to match 2020 format
cols_2019 = ['ride_id', 'rideable_type', 'started_at', 'ended_at', 
             'start_station_name', 'start_station_id', 'end_station_name', 
             'end_station_id', 'member_casual']

# Add missing columns that exist in 2020 but not in 2019
df_2019_q1_clean['start_lat'] = np.nan
df_2019_q1_clean['start_lng'] = np.nan
df_2019_q1_clean['end_lat'] = np.nan
df_2019_q1_clean['end_lng'] = np.nan

# Final column order to match 2020
cols_final = ['ride_id', 'rideable_type', 'started_at', 'ended_at', 
              'start_station_name', 'start_station_id', 'end_station_name', 
              'end_station_id', 'start_lat', 'start_lng', 'end_lat', 'end_lng',
              'member_casual']

df_2019_q1_clean = df_2019_q1_clean[cols_final]

# Convert datetime strings to datetime objects
print("Converting datetime strings to datetime objects...")
df_2019_q1_clean['started_at'] = pd.to_datetime(df_2019_q1_clean['started_at'])
df_2019_q1_clean['ended_at'] = pd.to_datetime(df_2019_q1_clean['ended_at'])
df_2020_q1['started_at'] = pd.to_datetime(df_2020_q1['started_at'])
df_2020_q1['ended_at'] = pd.to_datetime(df_2020_q1['ended_at'])

# Create ride_length column (in seconds)
print("Creating ride_length column...")
df_2019_q1_clean['ride_length'] = (df_2019_q1_clean['ended_at'] - df_2019_q1_clean['started_at']).dt.total_seconds()
df_2020_q1['ride_length'] = (df_2020_q1['ended_at'] - df_2020_q1['started_at']).dt.total_seconds()

# Create day_of_week column (1 = Sunday, 7 = Saturday)
print("Creating day_of_week column...")
df_2019_q1_clean['day_of_week'] = df_2019_q1_clean['started_at'].dt.dayofweek + 1
df_2020_q1['day_of_week'] = df_2020_q1['started_at'].dt.dayofweek + 1

# Adjust day_of_week to match the requirement (1 = Sunday, 7 = Saturday)
# pandas dayofweek is 0 = Monday, 6 = Sunday, so we need to adjust
df_2019_q1_clean['day_of_week'] = df_2019_q1_clean['day_of_week'].apply(lambda x: 1 if x == 7 else x + 1)
df_2020_q1['day_of_week'] = df_2020_q1['day_of_week'].apply(lambda x: 1 if x == 7 else x + 1)

# Add day_name for better readability
day_map = {1: 'Sunday', 2: 'Monday', 3: 'Tuesday', 4: 'Wednesday', 5: 'Thursday', 6: 'Friday', 7: 'Saturday'}
df_2019_q1_clean['day_name'] = df_2019_q1_clean['day_of_week'].map(day_map)
df_2020_q1['day_name'] = df_2020_q1['day_of_week'].map(day_map)

# Remove trips with negative or zero ride_length
print("Removing invalid trips...")
df_2019_q1_clean = df_2019_q1_clean[df_2019_q1_clean['ride_length'] > 0]
df_2020_q1 = df_2020_q1[df_2020_q1['ride_length'] > 0]

# Remove trips less than 60 seconds (as mentioned in the data description)
df_2019_q1_clean = df_2019_q1_clean[df_2019_q1_clean['ride_length'] >= 60]
df_2020_q1 = df_2020_q1[df_2020_q1['ride_length'] >= 60]

# Combine the datasets
print("Combining datasets...")
combined_df = pd.concat([df_2019_q1_clean, df_2020_q1], ignore_index=True)

# Basic statistics
print("\nBasic statistics for combined data:")
print(f"Total number of trips: {combined_df.shape[0]}")
print(f"Number of member trips: {combined_df[combined_df['member_casual'] == 'member'].shape[0]}")
print(f"Number of casual trips: {combined_df[combined_df['member_casual'] == 'casual'].shape[0]}")

# Save the processed data
print("\nSaving processed data...")
df_2019_q1_clean.to_csv(output_path + 'processed_2019_Q1.csv', index=False)
df_2020_q1.to_csv(output_path + 'processed_2020_Q1.csv', index=False)
combined_df.to_csv(output_path + 'combined_data.csv', index=False)

print("Data processing complete!")

# Create a data processing documentation
with open(output_path + 'data_processing_documentation.md', 'w') as f:
    f.write("# Data Processing Documentation\n\n")
    f.write("## Overview\n")
    f.write("This document outlines the steps taken to process and clean the Cyclistic bike-share data for analysis.\n\n")
    
    f.write("## Data Sources\n")
    f.write("- Divvy_Trips_2019_Q1.csv: First quarter data from 2019\n")
    f.write("- Divvy_Trips_2020_Q1.csv: First quarter data from 2020\n\n")
    
    f.write("## Processing Steps\n")
    f.write("1. **Standardized Column Names**: Renamed columns in the 2019 Q1 dataset to match the 2020 Q1 format.\n")
    f.write("2. **Standardized Member Types**: Converted 'Subscriber' to 'member' and 'Customer' to 'casual' in the 2019 Q1 dataset.\n")
    f.write("3. **Added Missing Columns**: Added 'rideable_type' and coordinate columns to the 2019 Q1 dataset.\n")
    f.write("4. **Datetime Conversion**: Converted string datetime values to datetime objects.\n")
    f.write("5. **Created ride_length Column**: Calculated the duration of each trip in seconds.\n")
    f.write("6. **Created day_of_week Column**: Added a column indicating the day of the week (1 = Sunday, 7 = Saturday).\n")
    f.write("7. **Added day_name Column**: Added a column with the name of the day for better readability.\n")
    f.write("8. **Removed Invalid Trips**: Filtered out trips with negative or zero ride_length.\n")
    f.write("9. **Removed Short Trips**: Removed trips less than 60 seconds as mentioned in the data description.\n")
    f.write("10. **Combined Datasets**: Merged the processed 2019 Q1 and 2020 Q1 datasets.\n\n")
    
    f.write("## Data Statistics\n")
    f.write(f"- Total number of trips after processing: {combined_df.shape[0]}\n")
    f.write(f"- Number of member trips: {combined_df[combined_df['member_casual'] == 'member'].shape[0]}\n")
    f.write(f"- Number of casual trips: {combined_df[combined_df['member_casual'] == 'casual'].shape[0]}\n\n")
    
    f.write("## Notes\n")
    f.write("- The 2019 Q1 and 2020 Q1 datasets had different column structures that were standardized.\n")
    f.write("- The ride_length and day_of_week columns were created as specified in the case study requirements.\n")
    f.write("- Trips less than 60 seconds were removed as they likely represent false starts or users re-docking bikes.\n")

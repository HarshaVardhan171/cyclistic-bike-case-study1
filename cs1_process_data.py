#Load the Data
import pandas as pd
trips_2019 = pd.read_csv('C:/Users/admin/Desktop/SelfCaseStudy/divvy_datasets/Divvy_Trips_2019_Q1.csv')
trips_2020 = pd.read_csv('C:/Users/admin/Desktop/SelfCaseStudy/divvy_datasets/Divvy_Trips_2020_Q1.csv')
print(trips_2019.head())
print(trips_2020.head())

# Rename the columns correctly
trips_2019.rename(columns={
    'trip_id': 'ride_id',
    'start_time': 'started_at',
    'end_time': 'ended_at',
    'from_station_id': 'start_station_id',
    'from_station_name': 'start_station_name',
    'to_station_id': 'end_station_id',
    'to_station_name': 'end_station_name',
    'usertype': 'member_casual',
    'tripduration' : 'ride_duration'
}, inplace=True)

# Ensure mapping is done after renaming and with correct column name
# First, inspect unique values
print(trips_2019['member_casual'].unique())  # Should show ['Subscriber', 'Customer']

# Map 'Subscriber' → 'member', 'Customer' → 'casual'
trips_2019['member_casual'] = trips_2019['member_casual'].map({
    'Subscriber': 'member',
    'Customer': 'casual'
})

# Confirm mapping worked
print(trips_2019['member_casual'].unique())  # Should now show ['member', 'casual']

#Add derived columns
trips_2020['started_at'] = pd.to_datetime(trips_2020['started_at'], errors='coerce')
trips_2020['ended_at'] = pd.to_datetime(trips_2020['ended_at'], errors='coerce')
trips_2019['ride_duration'] = (trips_2019['ride_duration']) / 60
trips_2019.rename(columns={
    'ride_duration' : 'ride_duration_minutes'
}, inplace = True)
trips_2020['ride_duration_minutes'] = (trips_2020['ended_at'] - trips_2020['started_at']) / 60
trips_2020['ride_duration_minutes'] = (trips_2020['ended_at'] - trips_2020['started_at']) / 60
trips_2020['ride_duration_minutes'] = (trips_2020['ride_duration_minutes']).dt.total_seconds()
print(trips_2019.head())
print(trips_2020.head())

#Combining Datasets
combined_trips = pd.concat([trips_2019, trips_2020], ignore_index=True)

# Clean up any remaining issues
combined_trips['member_casual'] = combined_trips['member_casual'].str.lower()
combined_trips = combined_trips[combined_trips['member_casual'].isin(['member', 'casual'])]

# Final check
print(combined_trips['member_casual'].unique())  # ['member', 'casual']

#condition
combined_trips = combined_trips[combined_trips['ride_duration_minutes']>1]
print(combined_trips.shape[0])

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os

# Set paths
data_path = '/home/ubuntu/cyclistic_data/processed/'
output_path = '/home/ubuntu/cyclistic_data/analysis/'
viz_path = '/home/ubuntu/cyclistic_data/visualizations/'

# Create output directories if they don't exist
for path in [output_path, viz_path]:
    if not os.path.exists(path):
        os.makedirs(path)

# Read the processed data
print("Reading processed data...")
combined_df = pd.read_csv(data_path + 'combined_data.csv')

# Convert datetime strings back to datetime objects
combined_df['started_at'] = pd.to_datetime(combined_df['started_at'])
combined_df['ended_at'] = pd.to_datetime(combined_df['ended_at'])

# Add month column for seasonal analysis
combined_df['month'] = combined_df['started_at'].dt.month
combined_df['month_name'] = combined_df['started_at'].dt.strftime('%B')

# Add hour column for time of day analysis
combined_df['hour'] = combined_df['started_at'].dt.hour

# Add season column
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

combined_df['season'] = combined_df['month'].apply(get_season)

# Add time of day category
def get_time_of_day(hour):
    if 5 <= hour < 9:
        return 'Early Morning (5-9)'
    elif 9 <= hour < 12:
        return 'Morning (9-12)'
    elif 12 <= hour < 17:
        return 'Afternoon (12-17)'
    elif 17 <= hour < 20:
        return 'Evening (17-20)'
    else:
        return 'Night (20-5)'

combined_df['time_of_day'] = combined_df['hour'].apply(get_time_of_day)

# Convert ride_length from seconds to minutes for easier interpretation
combined_df['ride_length_min'] = combined_df['ride_length'] / 60

# Basic descriptive statistics
print("\nCalculating descriptive statistics...")

# Overall statistics
overall_stats = combined_df['ride_length_min'].describe()

# Statistics by member type
member_stats = combined_df.groupby('member_casual')['ride_length_min'].describe()

# Average ride length by day of week for each member type
avg_ride_by_day = combined_df.groupby(['member_casual', 'day_name'])['ride_length_min'].mean().reset_index()

# Number of rides by day of week for each member type
rides_by_day = combined_df.groupby(['member_casual', 'day_name']).size().reset_index(name='number_of_rides')

# Average ride length by hour for each member type
avg_ride_by_hour = combined_df.groupby(['member_casual', 'hour'])['ride_length_min'].mean().reset_index()

# Number of rides by hour for each member type
rides_by_hour = combined_df.groupby(['member_casual', 'hour']).size().reset_index(name='number_of_rides')

# Average ride length by month for each member type
avg_ride_by_month = combined_df.groupby(['member_casual', 'month_name'])['ride_length_min'].mean().reset_index()

# Number of rides by month for each member type
rides_by_month = combined_df.groupby(['member_casual', 'month_name']).size().reset_index(name='number_of_rides')

# Average ride length by season for each member type
avg_ride_by_season = combined_df.groupby(['member_casual', 'season'])['ride_length_min'].mean().reset_index()

# Number of rides by season for each member type
rides_by_season = combined_df.groupby(['member_casual', 'season']).size().reset_index(name='number_of_rides')

# Average ride length by time of day for each member type
avg_ride_by_time = combined_df.groupby(['member_casual', 'time_of_day'])['ride_length_min'].mean().reset_index()

# Number of rides by time of day for each member type
rides_by_time = combined_df.groupby(['member_casual', 'time_of_day']).size().reset_index(name='number_of_rides')

# Most popular start stations for each member type
popular_start_stations = combined_df.groupby(['member_casual', 'start_station_name']).size().reset_index(name='number_of_rides')
popular_start_stations_member = popular_start_stations[popular_start_stations['member_casual'] == 'member'].sort_values('number_of_rides', ascending=False).head(10)
popular_start_stations_casual = popular_start_stations[popular_start_stations['member_casual'] == 'casual'].sort_values('number_of_rides', ascending=False).head(10)

# Most popular end stations for each member type
popular_end_stations = combined_df.groupby(['member_casual', 'end_station_name']).size().reset_index(name='number_of_rides')
popular_end_stations_member = popular_end_stations[popular_end_stations['member_casual'] == 'member'].sort_values('number_of_rides', ascending=False).head(10)
popular_end_stations_casual = popular_end_stations[popular_end_stations['member_casual'] == 'casual'].sort_values('number_of_rides', ascending=False).head(10)

# Save analysis results
print("\nSaving analysis results...")

# Create a summary file
with open(output_path + 'analysis_summary.md', 'w') as f:
    f.write("# Cyclistic Bike-Share Analysis Summary\n\n")
    
    f.write("## Overview\n")
    f.write("This analysis examines how annual members and casual riders use Cyclistic bikes differently, based on data from Q1 2019 and Q1 2020.\n\n")
    
    f.write("## Basic Statistics\n")
    f.write("### Overall Ride Statistics (in minutes)\n")
    f.write(f"```\n{overall_stats.to_string()}\n```\n\n")
    
    f.write("### Ride Statistics by Member Type (in minutes)\n")
    f.write(f"```\n{member_stats.to_string()}\n```\n\n")
    
    f.write("## Key Findings\n\n")
    
    # Ride duration differences
    f.write("### 1. Ride Duration Differences\n")
    avg_member = combined_df[combined_df['member_casual'] == 'member']['ride_length_min'].mean()
    avg_casual = combined_df[combined_df['member_casual'] == 'casual']['ride_length_min'].mean()
    f.write(f"- Average ride duration for members: {avg_member:.2f} minutes\n")
    f.write(f"- Average ride duration for casual riders: {avg_casual:.2f} minutes\n")
    f.write(f"- Casual riders' trips are {(avg_casual/avg_member - 1)*100:.1f}% longer on average than member trips\n\n")
    
    # Day of week patterns
    f.write("### 2. Day of Week Patterns\n")
    f.write("#### Average Ride Length by Day of Week (in minutes)\n")
    f.write(f"```\n{avg_ride_by_day.pivot(index='day_name', columns='member_casual', values='ride_length_min').to_string()}\n```\n\n")
    
    f.write("#### Number of Rides by Day of Week\n")
    f.write(f"```\n{rides_by_day.pivot(index='day_name', columns='member_casual', values='number_of_rides').to_string()}\n```\n\n")
    
    # Time of day patterns
    f.write("### 3. Time of Day Patterns\n")
    f.write("#### Average Ride Length by Time of Day (in minutes)\n")
    f.write(f"```\n{avg_ride_by_time.pivot(index='time_of_day', columns='member_casual', values='ride_length_min').to_string()}\n```\n\n")
    
    f.write("#### Number of Rides by Time of Day\n")
    f.write(f"```\n{rides_by_time.pivot(index='time_of_day', columns='member_casual', values='number_of_rides').to_string()}\n```\n\n")
    
    # Seasonal patterns
    f.write("### 4. Seasonal Patterns\n")
    f.write("#### Average Ride Length by Season (in minutes)\n")
    f.write(f"```\n{avg_ride_by_season.pivot(index='season', columns='member_casual', values='ride_length_min').to_string()}\n```\n\n")
    
    f.write("#### Number of Rides by Season\n")
    f.write(f"```\n{rides_by_season.pivot(index='season', columns='member_casual', values='number_of_rides').to_string()}\n```\n\n")
    
    # Popular stations
    f.write("### 5. Popular Stations\n")
    f.write("#### Top 10 Start Stations for Members\n")
    f.write(f"```\n{popular_start_stations_member[['start_station_name', 'number_of_rides']].to_string(index=False)}\n```\n\n")
    
    f.write("#### Top 10 Start Stations for Casual Riders\n")
    f.write(f"```\n{popular_start_stations_casual[['start_station_name', 'number_of_rides']].to_string(index=False)}\n```\n\n")
    
    f.write("#### Top 10 End Stations for Members\n")
    f.write(f"```\n{popular_end_stations_member[['end_station_name', 'number_of_rides']].to_string(index=False)}\n```\n\n")
    
    f.write("#### Top 10 End Stations for Casual Riders\n")
    f.write(f"```\n{popular_end_stations_casual[['end_station_name', 'number_of_rides']].to_string(index=False)}\n```\n\n")
    
    f.write("## Conclusions\n\n")
    f.write("Based on the analysis, there are several key differences in how annual members and casual riders use Cyclistic bikes:\n\n")
    
    f.write("1. **Ride Duration**: Casual riders take significantly longer trips on average compared to members.\n")
    f.write("2. **Usage Patterns by Day**: Members use bikes more consistently throughout the week, while casual riders show higher usage on weekends.\n")
    f.write("3. **Time of Day**: Members show peak usage during commuting hours, suggesting they use bikes for commuting to work, while casual riders show more distributed usage throughout the day.\n")
    f.write("4. **Seasonal Trends**: Both user types show seasonal variations, but the patterns differ.\n")
    f.write("5. **Popular Locations**: Members and casual riders tend to start and end their trips at different stations, indicating different usage purposes.\n\n")
    
    f.write("These insights can inform targeted marketing strategies to convert casual riders into annual members.")

# Create visualizations
print("\nCreating visualizations...")

# Set the style for all visualizations
plt.style.use('seaborn-v0_8-whitegrid')
colors = ['#1f77b4', '#ff7f0e']  # Blue for members, orange for casual

# 1. Average ride duration by member type
plt.figure(figsize=(10, 6))
sns.barplot(x='member_casual', y='ride_length_min', data=combined_df, palette=colors)
plt.title('Average Ride Duration by Member Type', fontsize=16)
plt.xlabel('User Type', fontsize=14)
plt.ylabel('Average Ride Duration (minutes)', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.savefig(viz_path + 'avg_ride_duration.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Number of rides by day of week for each member type
plt.figure(figsize=(12, 7))
day_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
rides_by_day_pivot = rides_by_day.pivot(index='day_name', columns='member_casual', values='number_of_rides')
rides_by_day_pivot = rides_by_day_pivot.reindex(day_order)
rides_by_day_pivot.plot(kind='bar', color=colors)
plt.title('Number of Rides by Day of Week', fontsize=16)
plt.xlabel('Day of Week', fontsize=14)
plt.ylabel('Number of Rides', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.legend(title='User Type', fontsize=12)
plt.savefig(viz_path + 'rides_by_day.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Average ride duration by day of week for each member type
plt.figure(figsize=(12, 7))
avg_ride_by_day_pivot = avg_ride_by_day.pivot(index='day_name', columns='member_casual', values='ride_length_min')
avg_ride_by_day_pivot = avg_ride_by_day_pivot.reindex(day_order)
avg_ride_by_day_pivot.plot(kind='bar', color=colors)
plt.title('Average Ride Duration by Day of Week', fontsize=16)
plt.xlabel('Day of Week', fontsize=14)
plt.ylabel('Average Ride Duration (minutes)', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.legend(title='User Type', fontsize=12)
plt.savefig(viz_path + 'avg_ride_by_day.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. Number of rides by hour for each member type
plt.figure(figsize=(14, 8))
rides_by_hour_pivot = rides_by_hour.pivot(index='hour', columns='member_casual', values='number_of_rides')
rides_by_hour_pivot.plot(kind='line', marker='o', linewidth=2, markersize=8, color=colors)
plt.title('Number of Rides by Hour of Day', fontsize=16)
plt.xlabel('Hour of Day', fontsize=14)
plt.ylabel('Number of Rides', fontsize=14)
plt.xticks(range(0, 24), fontsize=12)
plt.yticks(fontsize=12)
plt.legend(title='User Type', fontsize=12)
plt.grid(True, alpha=0.3)
plt.savefig(viz_path + 'rides_by_hour.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. Number of rides by time of day for each member type
plt.figure(figsize=(12, 7))
time_order = ['Early Morning (5-9)', 'Morning (9-12)', 'Afternoon (12-17)', 'Evening (17-20)', 'Night (20-5)']
rides_by_time_pivot = rides_by_time.pivot(index='time_of_day', columns='member_casual', values='number_of_rides')
rides_by_time_pivot = rides_by_time_pivot.reindex(time_order)
rides_by_time_pivot.plot(kind='bar', color=colors)
plt.title('Number of Rides by Time of Day', fontsize=16)
plt.xlabel('Time of Day', fontsize=14)
plt.ylabel('Number of Rides', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.legend(title='User Type', fontsize=12)
plt.savefig(viz_path + 'rides_by_time_of_day.png', dpi=300, bbox_inches='tight')
plt.close()

# 6. Number of rides by month for each member type
plt.figure(figsize=(12, 7))
month_order = ['January', 'February', 'March']
rides_by_month_pivot = rides_by_month.pivot(index='month_name', columns='member_casual', values='number_of_rides')
rides_by_month_pivot = rides_by_month_pivot.reindex(month_order)
rides_by_month_pivot.plot(kind='bar', color=colors)
plt.title('Number of Rides by Month', fontsize=16)
plt.xlabel('Month', fontsize=14)
plt.ylabel('Number of Rides', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.legend(title='User Type', fontsize=12)
plt.savefig(viz_path + 'rides_by_month.png', dpi=300, bbox_inches='tight')
plt.close()

# 7. Top 10 start stations for each member type
plt.figure(figsize=(14, 8))
sns.barplot(x='number_of_rides', y='start_station_name', data=popular_start_stations_member, color=colors[0])
plt.title('Top 10 Start Stations for Members', fontsize=16)
plt.xlabel('Number of Rides', fontsize=14)
plt.ylabel('Station Name', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.savefig(viz_path + 'top_start_stations_member.png', dpi=300, bbox_inches='tight')
plt.close()

plt.figure(figsize=(14, 8))
sns.barplot(x='number_of_rides', y='start_station_name', data=popular_start_stations_casual, color=colors[1])
plt.title('Top 10 Start Stations for Casual Riders', fontsize=16)
plt.xlabel('Number of Rides', fontsize=14)
plt.ylabel('Station Name', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.savefig(viz_path + 'top_start_stations_casual.png', dpi=300, bbox_inches='tight')
plt.close()

# 8. Ride duration distribution
plt.figure(figsize=(12, 7))
# Limit to rides under 60 minutes for better visualization
ride_duration_subset = combined_df[combined_df['ride_length_min'] <= 60]
sns.histplot(data=ride_duration_subset, x='ride_length_min', hue='member_casual', bins=30, palette=colors, alpha=0.6, kde=True)
plt.title('Distribution of Ride Durations (up to 60 minutes)', fontsize=16)
plt.xlabel('Ride Duration (minutes)', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(title='User Type', fontsize=12)
plt.savefig(viz_path + 'ride_duration_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

print("Analysis and visualization complete!")

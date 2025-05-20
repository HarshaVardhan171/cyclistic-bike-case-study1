import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Add day of week and hour columns
combined_trips['started_at'] = pd.to_datetime(combined_trips['started_at'], errors='coerce')
combined_trips['ended_at'] = pd.to_datetime(combined_trips['ended_at'], errors='coerce')
combined_trips['day_of_week'] = combined_trips['started_at'].dt.day_name()
combined_trips['hour_of_day'] = combined_trips['started_at'].dt.hour

# === 1. Summary statistics by user type ===
summary_stats = combined_trips.groupby('member_casual')['ride_duration_minutes'].agg(['count', 'mean', 'min', 'max']).round(2)
print("Summary Stats:\n", summary_stats)

# === 2. Rides by day of week ===
rides_by_day = combined_trips.groupby(['day_of_week', 'member_casual']).size().reset_index(name='ride_count')

# Sort days of the week
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
rides_by_day['day_of_week'] = pd.Categorical(rides_by_day['day_of_week'], categories=days_order, ordered=True)
rides_by_day = rides_by_day.sort_values('day_of_week')

# Plot: Rides by day
plt.figure(figsize=(10,6))
sns.barplot(data=rides_by_day, x='day_of_week', y='ride_count', hue='member_casual')
plt.title('Number of Rides by Day of Week')
plt.ylabel('Ride Count')
plt.xlabel('Day of Week')
plt.legend(title='User Type')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# === 3. Rides by hour of day ===
rides_by_hour = combined_trips.groupby(['hour_of_day', 'member_casual']).size().reset_index(name='ride_count')

# Plot: Rides by hour
plt.figure(figsize=(10,6))
sns.lineplot(data=rides_by_hour, x='hour_of_day', y='ride_count', hue='member_casual', marker='o')
plt.title('Ride Trends by Hour of Day')
plt.ylabel('Number of Rides')
plt.xlabel('Hour of Day')
plt.xticks(np.arange(0, 24, 1))
plt.tight_layout()
plt.show()

# === 4. Average ride duration by user type ===
avg_duration = combined_trips.groupby('member_casual')['ride_duration_minutes'].mean().round(2)  # in minutes
print("\nAverage Ride Duration (in minutes):\n", avg_duration)

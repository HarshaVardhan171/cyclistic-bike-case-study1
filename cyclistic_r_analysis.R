# R code for Cyclistic bike-share case study

# Load required libraries
library(tidyverse)
library(lubridate)
library(ggplot2)
library(dplyr)

# Set working directory
setwd("/home/ubuntu/cyclistic_data")

# Read the CSV files
trips_2019_q1 <- read_csv("csv/Divvy_Trips_2019_Q1.csv")
trips_2020_q1 <- read_csv("csv/Divvy_Trips_2020_Q1.csv")

# Examine the structure of the data frames
str(trips_2019_q1)
str(trips_2020_q1)

# Rename columns in the 2019 data to match the 2020 format
trips_2019_q1 <- trips_2019_q1 %>%
  rename(
    ride_id = trip_id,
    rideable_type = bikeid,
    started_at = start_time,
    ended_at = end_time,
    start_station_name = from_station_name,
    start_station_id = from_station_id,
    end_station_name = to_station_name,
    end_station_id = to_station_id,
    member_casual = usertype
  )

# Convert 'Subscriber' and 'Customer' values to 'member' and 'casual'
trips_2019_q1 <- trips_2019_q1 %>%
  mutate(member_casual = case_when(
    member_casual == "Subscriber" ~ "member",
    member_casual == "Customer" ~ "casual",
    TRUE ~ member_casual
  ))

# Create a unified data frame
all_trips <- bind_rows(trips_2019_q1, trips_2020_q1)

# Remove unnecessary columns
all_trips <- all_trips %>%
  select(-c(birthyear, gender, start_lat, start_lng, end_lat, end_lng))

# Add columns for date, month, day, year, day of week
all_trips <- all_trips %>%
  mutate(
    date = as.Date(started_at),
    month = month(started_at, label = TRUE),
    day = day(started_at),
    year = year(started_at),
    day_of_week = wday(started_at, label = TRUE),
    ride_length = as.numeric(difftime(ended_at, started_at, units = "mins"))
  )

# Remove bad data (rides with negative ride_length)
all_trips_v2 <- all_trips %>%
  filter(ride_length > 0)

# Descriptive analysis
# Calculate mean, median, max, min of ride_length
summary_stats <- all_trips_v2 %>%
  group_by(member_casual) %>%
  summarise(
    mean_ride_length = mean(ride_length),
    median_ride_length = median(ride_length),
    max_ride_length = max(ride_length),
    min_ride_length = min(ride_length)
  )

print(summary_stats)

# Analyze ridership data by type and weekday
trips_by_weekday <- all_trips_v2 %>%
  group_by(member_casual, day_of_week) %>%
  summarise(
    number_of_rides = n(),
    average_ride_length = mean(ride_length)
  ) %>%
  arrange(member_casual, day_of_week)

print(trips_by_weekday)

# Visualize number of rides by rider type and weekday
ggplot(trips_by_weekday, aes(x = day_of_week, y = number_of_rides, fill = member_casual)) +
  geom_col(position = "dodge") +
  labs(
    title = "Number of Rides by Day of Week",
    subtitle = "Comparing Members and Casual Riders",
    x = "Day of Week",
    y = "Number of Rides",
    fill = "Rider Type"
  ) +
  scale_y_continuous(labels = scales::comma) +
  theme_minimal()

# Save the plot
ggsave("visualizations/rides_by_day_of_week.png", width = 10, height = 6)

# Visualize average ride duration by rider type and weekday
ggplot(trips_by_weekday, aes(x = day_of_week, y = average_ride_length, fill = member_casual)) +
  geom_col(position = "dodge") +
  labs(
    title = "Average Ride Duration by Day of Week",
    subtitle = "Comparing Members and Casual Riders",
    x = "Day of Week",
    y = "Average Ride Length (minutes)",
    fill = "Rider Type"
  ) +
  theme_minimal()

# Save the plot
ggsave("visualizations/avg_duration_by_day_of_week.png", width = 10, height = 6)

# Analyze ridership data by hour of day
all_trips_v2$hour_of_day <- hour(all_trips_v2$started_at)

trips_by_hour <- all_trips_v2 %>%
  group_by(member_casual, hour_of_day) %>%
  summarise(
    number_of_rides = n(),
    average_ride_length = mean(ride_length)
  ) %>%
  arrange(member_casual, hour_of_day)

# Visualize number of rides by hour of day
ggplot(trips_by_hour, aes(x = hour_of_day, y = number_of_rides, color = member_casual, group = member_casual)) +
  geom_line(size = 1.2) +
  geom_point(size = 2) +
  labs(
    title = "Number of Rides by Hour of Day",
    subtitle = "Comparing Members and Casual Riders",
    x = "Hour of Day (24-hour format)",
    y = "Number of Rides",
    color = "Rider Type"
  ) +
  scale_x_continuous(breaks = seq(0, 23, 1)) +
  scale_y_continuous(labels = scales::comma) +
  theme_minimal()

# Save the plot
ggsave("visualizations/rides_by_hour_of_day.png", width = 12, height = 6)

# Analyze popular start stations for casual riders
popular_stations_casual <- all_trips_v2 %>%
  filter(member_casual == "casual") %>%
  group_by(start_station_name) %>%
  summarise(number_of_rides = n()) %>%
  arrange(desc(number_of_rides)) %>%
  head(10)

# Analyze popular start stations for members
popular_stations_member <- all_trips_v2 %>%
  filter(member_casual == "member") %>%
  group_by(start_station_name) %>%
  summarise(number_of_rides = n()) %>%
  arrange(desc(number_of_rides)) %>%
  head(10)

# Visualize popular start stations for casual riders
ggplot(popular_stations_casual, aes(x = reorder(start_station_name, number_of_rides), y = number_of_rides)) +
  geom_col(fill = "coral") +
  coord_flip() +
  labs(
    title = "Top 10 Start Stations for Casual Riders",
    x = "Station Name",
    y = "Number of Rides"
  ) +
  theme_minimal()

# Save the plot
ggsave("visualizations/top_stations_casual.png", width = 10, height = 6)

# Visualize popular start stations for members
ggplot(popular_stations_member, aes(x = reorder(start_station_name, number_of_rides), y = number_of_rides)) +
  geom_col(fill = "steelblue") +
  coord_flip() +
  labs(
    title = "Top 10 Start Stations for Members",
    x = "Station Name",
    y = "Number of Rides"
  ) +
  theme_minimal()

# Save the plot
ggsave("visualizations/top_stations_member.png", width = 10, height = 6)

# Analyze monthly trends
trips_by_month <- all_trips_v2 %>%
  group_by(year, month, member_casual) %>%
  summarise(
    number_of_rides = n(),
    average_ride_length = mean(ride_length)
  ) %>%
  arrange(year, month, member_casual)

# Create a month-year field for better visualization
trips_by_month <- trips_by_month %>%
  mutate(month_year = paste(month, year))

# Visualize monthly trends
ggplot(trips_by_month, aes(x = month_year, y = number_of_rides, fill = member_casual)) +
  geom_col(position = "dodge") +
  labs(
    title = "Number of Rides by Month",
    subtitle = "Comparing Members and Casual Riders",
    x = "Month",
    y = "Number of Rides",
    fill = "Rider Type"
  ) +
  scale_y_continuous(labels = scales::comma) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Save the plot
ggsave("visualizations/rides_by_month.png", width = 12, height = 6)

# Export summary data for further analysis
write_csv(summary_stats, "analysis/summary_statistics.csv")
write_csv(trips_by_weekday, "analysis/trips_by_weekday.csv")
write_csv(trips_by_hour, "analysis/trips_by_hour.csv")
write_csv(popular_stations_casual, "analysis/popular_stations_casual.csv")
write_csv(popular_stations_member, "analysis/popular_stations_member.csv")
write_csv(trips_by_month, "analysis/trips_by_month.csv")

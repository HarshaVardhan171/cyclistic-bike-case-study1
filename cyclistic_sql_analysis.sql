-- SQL code for Cyclistic bike-share case study

-- Create tables for the Cyclistic data
CREATE TABLE IF NOT EXISTS trips_2019_q1 (
    trip_id VARCHAR(255) PRIMARY KEY,
    start_time DATETIME,
    end_time DATETIME,
    bikeid VARCHAR(255),
    tripduration INT,
    from_station_id INT,
    from_station_name VARCHAR(255),
    to_station_id INT,
    to_station_name VARCHAR(255),
    usertype VARCHAR(255),
    gender VARCHAR(255),
    birthyear INT
);

CREATE TABLE IF NOT EXISTS trips_2020_q1 (
    ride_id VARCHAR(255) PRIMARY KEY,
    rideable_type VARCHAR(255),
    started_at DATETIME,
    ended_at DATETIME,
    start_station_name VARCHAR(255),
    start_station_id INT,
    end_station_name VARCHAR(255),
    end_station_id INT,
    start_lat DECIMAL(10, 8),
    start_lng DECIMAL(11, 8),
    end_lat DECIMAL(10, 8),
    end_lng DECIMAL(11, 8),
    member_casual VARCHAR(255)
);

-- Standardize column names and create a unified view
CREATE VIEW unified_trips AS
SELECT 
    trip_id AS ride_id,
    start_time AS started_at,
    end_time AS ended_at,
    from_station_name AS start_station_name,
    from_station_id AS start_station_id,
    to_station_name AS end_station_name,
    to_station_id AS end_station_id,
    CASE 
        WHEN usertype = 'Subscriber' THEN 'member'
        WHEN usertype = 'Customer' THEN 'casual'
        ELSE usertype
    END AS member_casual,
    tripduration AS ride_length_seconds,
    DAYNAME(start_time) AS day_of_week
FROM trips_2019_q1

UNION ALL

SELECT 
    ride_id,
    started_at,
    ended_at,
    start_station_name,
    start_station_id,
    end_station_name,
    end_station_id,
    member_casual,
    TIMESTAMPDIFF(SECOND, started_at, ended_at) AS ride_length_seconds,
    DAYNAME(started_at) AS day_of_week
FROM trips_2020_q1;

-- Calculate ride length statistics by member type
SELECT 
    member_casual,
    COUNT(*) AS total_rides,
    ROUND(AVG(ride_length_seconds)/60, 2) AS avg_ride_length_minutes,
    ROUND(MIN(ride_length_seconds)/60, 2) AS min_ride_length_minutes,
    ROUND(MAX(ride_length_seconds)/60, 2) AS max_ride_length_minutes
FROM unified_trips
GROUP BY member_casual;

-- Analyze rides by day of week for each member type
SELECT 
    member_casual,
    day_of_week,
    COUNT(*) AS total_rides,
    ROUND(AVG(ride_length_seconds)/60, 2) AS avg_ride_length_minutes
FROM unified_trips
GROUP BY member_casual, day_of_week
ORDER BY 
    CASE member_casual
        WHEN 'member' THEN 1
        WHEN 'casual' THEN 2
        ELSE 3
    END,
    CASE day_of_week
        WHEN 'Monday' THEN 1
        WHEN 'Tuesday' THEN 2
        WHEN 'Wednesday' THEN 3
        WHEN 'Thursday' THEN 4
        WHEN 'Friday' THEN 5
        WHEN 'Saturday' THEN 6
        WHEN 'Sunday' THEN 7
    END;

-- Analyze hourly usage patterns
SELECT 
    member_casual,
    HOUR(started_at) AS hour_of_day,
    COUNT(*) AS total_rides
FROM unified_trips
GROUP BY member_casual, HOUR(started_at)
ORDER BY member_casual, hour_of_day;

-- Find most popular start stations for casual riders
SELECT 
    start_station_name,
    COUNT(*) AS total_rides
FROM unified_trips
WHERE member_casual = 'casual'
GROUP BY start_station_name
ORDER BY total_rides DESC
LIMIT 10;

-- Find most popular start stations for members
SELECT 
    start_station_name,
    COUNT(*) AS total_rides
FROM unified_trips
WHERE member_casual = 'member'
GROUP BY start_station_name
ORDER BY total_rides DESC
LIMIT 10;

-- Calculate ride length statistics by day of week
SELECT 
    day_of_week,
    member_casual,
    COUNT(*) AS total_rides,
    ROUND(AVG(ride_length_seconds)/60, 2) AS avg_ride_length_minutes
FROM unified_trips
GROUP BY day_of_week, member_casual
ORDER BY 
    CASE day_of_week
        WHEN 'Monday' THEN 1
        WHEN 'Tuesday' THEN 2
        WHEN 'Wednesday' THEN 3
        WHEN 'Thursday' THEN 4
        WHEN 'Friday' THEN 5
        WHEN 'Saturday' THEN 6
        WHEN 'Sunday' THEN 7
    END,
    member_casual;

-- Calculate monthly trends
SELECT 
    YEAR(started_at) AS year,
    MONTH(started_at) AS month,
    member_casual,
    COUNT(*) AS total_rides,
    ROUND(AVG(ride_length_seconds)/60, 2) AS avg_ride_length_minutes
FROM unified_trips
GROUP BY YEAR(started_at), MONTH(started_at), member_casual
ORDER BY year, month, member_casual;

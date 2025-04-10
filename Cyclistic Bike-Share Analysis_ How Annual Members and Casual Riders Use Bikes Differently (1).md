# Cyclistic Bike-Share Analysis: How Annual Members and Casual Riders Use Bikes Differently

## Executive Summary

This report presents a comprehensive analysis of how annual members and casual riders use Cyclistic bikes differently. The analysis is based on historical trip data from Q1 2019 and Q1 2020. Our findings reveal significant differences in usage patterns between the two user types, including ride duration, time of day, day of week, and preferred locations. Based on these insights, we have developed three key recommendations to help Cyclistic convert casual riders into annual members, which has been identified as crucial for future growth and profitability.

## 1. Business Task

The primary business task is to understand how annual members and casual riders use Cyclistic bikes differently. This analysis will inform the marketing team's strategy to convert casual riders into annual members, which has been identified as key to future growth and profitability.

Cyclistic's director of marketing, Lily Moreno, believes that maximizing the number of annual members will be key to future growth. Rather than targeting all-new customers, she sees an opportunity to convert casual riders into members since they are already aware of the Cyclistic program and have chosen it for their mobility needs.

## 2. Data Sources

For this analysis, we used historical trip data from Divvy, Chicago's bike-share service (the fictional Cyclistic in our case study). As specified in the case study instructions, we downloaded the following datasets:

1. **Divvy_Trips_2019_Q1.csv** - First quarter data from 2019
2. **Divvy_Trips_2020_Q1.csv** - First quarter data from 2020

The data was downloaded from the official Divvy trip data repository hosted on Amazon S3:
- https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip
- https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip

Each trip record is anonymized and includes:
- Trip start day and time
- Trip end day and time
- Trip start station
- Trip end station
- Rider type (Member, Single Ride, and Day Pass)

The data has been processed by Divvy to remove trips taken by staff for service and inspection purposes, as well as any trips that were below 60 seconds in length (potentially false starts or users trying to re-dock a bike to ensure it was secure).

### Data Credibility Assessment (ROCCC)
- **Reliable**: The data comes from the official Divvy system, which tracks all bike trips.
- **Original**: The data is from the primary source (Divvy/Lyft Bikes and Scooters, LLC).
- **Comprehensive**: The data includes all trips taken by Divvy users during the specified time periods.
- **Current**: The data represents historical information from 2019 Q1 and 2020 Q1 as required by the case study.
- **Cited**: The data is made available by Motivate International Inc. under license as mentioned in the case study.

## 3. Data Processing and Cleaning

The data processing involved several steps to prepare the datasets for analysis:

1. **Standardized Column Names**: The 2019 Q1 and 2020 Q1 datasets had different column structures that needed to be standardized. We renamed columns in the 2019 Q1 dataset to match the 2020 Q1 format.

2. **Standardized Member Types**: We converted 'Subscriber' to 'member' and 'Customer' to 'casual' in the 2019 Q1 dataset to match the 2020 Q1 terminology.

3. **Added Missing Columns**: We added 'rideable_type' and coordinate columns to the 2019 Q1 dataset to ensure consistency with the 2020 Q1 dataset.

4. **Datetime Conversion**: We converted string datetime values to datetime objects for proper time-based analysis.

5. **Created ride_length Column**: We calculated the duration of each trip in seconds, as required by the case study.

6. **Created day_of_week Column**: We added a column indicating the day of the week (1 = Sunday, 7 = Saturday), as required by the case study.

7. **Added Additional Analysis Columns**: We added columns for month, hour, season, and time of day to enable more detailed analysis.

8. **Removed Invalid Trips**: We filtered out trips with negative or zero ride_length and trips less than 60 seconds as mentioned in the data description.

9. **Combined Datasets**: We merged the processed 2019 Q1 and 2020 Q1 datasets for comprehensive analysis.

After processing, the combined dataset contained 784,285 trips, with 716,593 member trips (91.4%) and 67,692 casual trips (8.6%).

## 4. Analysis Summary

Our analysis revealed several key differences in how annual members and casual riders use Cyclistic bikes:

### Ride Duration Differences
- Average ride duration for members: 13.32 minutes
- Average ride duration for casual riders: 89.79 minutes
- Casual riders' trips are 574.0% longer on average than member trips

### Day of Week Patterns
- Members use bikes more consistently throughout the weekdays
- Casual riders show higher usage on weekends (Saturday and Sunday)
- Both user types tend to take longer rides on weekends

### Time of Day Patterns
- Members show peak usage during typical commuting hours (8 AM and 5 PM)
- Casual riders show a more distributed usage throughout the day
- Both user types have the highest number of rides in the afternoon
- Members have a much higher proportion of early morning rides compared to casual riders

### Monthly Patterns
- Both user types show increasing usage as the weather improves from winter to spring
- Members maintain a much higher volume of rides throughout all months

### Popular Stations
- Members tend to start and end their trips at stations in business districts and transportation hubs
- Casual riders prefer stations near tourist attractions and recreational areas along the lakefront
- Top stations for casual riders include Streeter Dr & Grand Ave, Lake Shore Dr & Monroe St, Shedd Aquarium, and Millennium Park

## 5. Key Visualizations

### Ride Duration Differences
![Average Ride Duration by Member Type](https://private-us-east-1.manuscdn.com/sessionFile/lU8B1Sh2HrAJWkbbHoqUwd/sandbox/6QVL5GkmSDt1iU1EoCu6XW-images_1744120524032_na1fn_L2hvbWUvdWJ1bnR1L2N5Y2xpc3RpY19kYXRhL3Zpc3VhbGl6YXRpb25zL2F2Z19yaWRlX2R1cmF0aW9u.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvbFU4QjFTaDJIckFKV2tiYkhvcVV3ZC9zYW5kYm94LzZRVkw1R2ttU0R0MWlVMUVvQ3U2WFctaW1hZ2VzXzE3NDQxMjA1MjQwMzJfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyTjVZMnhwYzNScFkxOWtZWFJoTDNacGMzVmhiR2w2WVhScGIyNXpMMkYyWjE5eWFXUmxYMlIxY21GMGFXOXUucG5nIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzY3MjI1NjAwfX19XX0_&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=hCWK7wjTBrGu9gdMN~kaWOt6T7XLmvCgLuziDfCqBO2ReWTGWeFxLMuUXyyhQIUhIgz8Z~3fAcOSD~dvoJ2wNVY8r4AXSFkXdYkil~xS4oWHgI-9NO3WXnM5~7amzFeEJXEQUSj4we-t4zNATQbj87PCF30XHpc6j7DM-IBmH9qI~NCoeY86b8QVpjocSW3nnzTlSyqwqBygNwtTsjGpygBCiuHrD-6Xvje3Pj33GaP24ytGZ8xVwsbjYc7fZcuKbfBttAQTydi9v9sfN4J~KYaCU9R0CvcVaTcAcB0jjLqaxcYCffbsIEWlTYbAd4Tk0lh34HOIwIDhHpI6dzCiXw__)

### Usage Patterns by Day of Week
![Number of Rides by Day of Week](https://private-us-east-1.manuscdn.com/sessionFile/lU8B1Sh2HrAJWkbbHoqUwd/sandbox/6QVL5GkmSDt1iU1EoCu6XW-images_1744120524032_na1fn_L2hvbWUvdWJ1bnR1L2N5Y2xpc3RpY19kYXRhL3Zpc3VhbGl6YXRpb25zL3JpZGVzX2J5X2RheQ.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvbFU4QjFTaDJIckFKV2tiYkhvcVV3ZC9zYW5kYm94LzZRVkw1R2ttU0R0MWlVMUVvQ3U2WFctaW1hZ2VzXzE3NDQxMjA1MjQwMzJfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyTjVZMnhwYzNScFkxOWtZWFJoTDNacGMzVmhiR2w2WVhScGIyNXpMM0pwWkdWelgySjVYMlJoZVEucG5nIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzY3MjI1NjAwfX19XX0_&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=PtPbKWPR8gvUj05ro7Avc5bOxoCXSqmQct6SqYeVqVqfLLkf4XwK8scBLSpzPfF226Xx9B0wV6MFJm4hlp~Xa63nTtBxRBYBFC8nz-ZckvajOuA5g5SespiMME~mYaxBSo3nTLho~EtD02ua7r1DE2VGS11RS13~NKhAT5cSUSLqi77WRR0~i3gYfksGAtFn5LjfE3KeGEmJFyTOVB6kbHr3M8qzON6Pv4qBawZZ6YSg7nPlns3a1lIZ3ZVahY-scRLW8dCgQSRyvX1EHOciWDf-cpUDOoE-ubGRUmA4hQaqVpAuR9ySZ976wy6C~pAMVTCQ8-akByYE~Un148uPbg__)

### Time of Day Patterns
![Number of Rides by Hour](https://private-us-east-1.manuscdn.com/sessionFile/lU8B1Sh2HrAJWkbbHoqUwd/sandbox/6QVL5GkmSDt1iU1EoCu6XW-images_1744120524032_na1fn_L2hvbWUvdWJ1bnR1L2N5Y2xpc3RpY19kYXRhL3Zpc3VhbGl6YXRpb25zL3JpZGVzX2J5X2hvdXI.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvbFU4QjFTaDJIckFKV2tiYkhvcVV3ZC9zYW5kYm94LzZRVkw1R2ttU0R0MWlVMUVvQ3U2WFctaW1hZ2VzXzE3NDQxMjA1MjQwMzJfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyTjVZMnhwYzNScFkxOWtZWFJoTDNacGMzVmhiR2w2WVhScGIyNXpMM0pwWkdWelgySjVYMmh2ZFhJLnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc2NzIyNTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=AZVuuOz4ir3RaI6OrGjKhyBXT6qDOAYkRqPT8COpxub016mXubR7br8DCPlwA1KGRvlDXTGygbXMb7i9vFULubqJv0j752lFdI5KoNZvtyCZc4E-LVDmQvJwJmeU9hvWOTLZmVlLf-4kk5QGt4n63AUPRUJHQmGxMLKPiPgJUkM8Rr2f3ffP8DySLeeVZ0CDdnP-ACkH9x3jxRLn31tYhWY2pKGvXRluRcMIupiERPhp~H21JRKcY4mxPS8rqkgXfMFmYhMBzhS0NDuvOZcgwKPJsYmOZyJkUDZE0uHf9~~oNtPlSmB0Leb2g4i~QEfzQWku~WpTNzdpYgYVV4GXkQ__)

### Popular Stations
![Top Start Stations for Casual Riders](https://private-us-east-1.manuscdn.com/sessionFile/lU8B1Sh2HrAJWkbbHoqUwd/sandbox/6QVL5GkmSDt1iU1EoCu6XW-images_1744120524032_na1fn_L2hvbWUvdWJ1bnR1L2N5Y2xpc3RpY19kYXRhL3Zpc3VhbGl6YXRpb25zL3RvcF9zdGFydF9zdGF0aW9uc19jYXN1YWw.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvbFU4QjFTaDJIckFKV2tiYkhvcVV3ZC9zYW5kYm94LzZRVkw1R2ttU0R0MWlVMUVvQ3U2WFctaW1hZ2VzXzE3NDQxMjA1MjQwMzJfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyTjVZMnhwYzNScFkxOWtZWFJoTDNacGMzVmhiR2w2WVhScGIyNXpMM1J2Y0Y5emRHRnlkRjl6ZEdGMGFXOXVjMTlqWVhOMVlXdy5wbmciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3NjcyMjU2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=SthMU3s7i5OTIyCNBMos-F8GCK-rcCwj~b5hM2uhXvANLiKBACWr3rn2lauZxw1vxxkAJEDYrVimcOaGWiiKroT6o~6QHqqpokmkyVhVBGtfLeROPLelhWCVBQlDWD4gM1OOoPvWQmCek1Ya~-4~-wcdx3dD-DhP4h1pMDiw5BwjNYce~ZG3Fe4D9PljwNtPS9fBbiYdf0g8D8RFORG-eE~lOyxzWJ21dVasf5TiEf2AF3iNHbuL8K2hNm46nNf8Vzf~FO-NB-MuH5azqjd6grWghbxFzLurLboikgxvbPXHRPh5XOL1-YE66N9qGOnSIXH3TXG6sMvstaeP5paS0Q__)

### Ride Duration Distribution
![Ride Duration Distribution](https://private-us-east-1.manuscdn.com/sessionFile/lU8B1Sh2HrAJWkbbHoqUwd/sandbox/6QVL5GkmSDt1iU1EoCu6XW-images_1744120524032_na1fn_L2hvbWUvdWJ1bnR1L2N5Y2xpc3RpY19kYXRhL3Zpc3VhbGl6YXRpb25zL3JpZGVfZHVyYXRpb25fZGlzdHJpYnV0aW9u.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvbFU4QjFTaDJIckFKV2tiYkhvcVV3ZC9zYW5kYm94LzZRVkw1R2ttU0R0MWlVMUVvQ3U2WFctaW1hZ2VzXzE3NDQxMjA1MjQwMzJfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyTjVZMnhwYzNScFkxOWtZWFJoTDNacGMzVmhiR2w2WVhScGIyNXpMM0pwWkdWZlpIVnlZWFJwYjI1ZlpHbHpkSEpwWW5WMGFXOXUucG5nIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzY3MjI1NjAwfX19XX0_&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=lbTqegWdIAG9RJRCWoMBGRTBF6XdsiLeelxydxct1Eq~UGpy2Ci5mWvzbHpSGoSB4pzhKjs6gsVmg2b8-TvAMleqolMj1Z~C1Cyht9bg~9mIP7FkYXWHJEPunnBxLESTKkS5iXESh5FJDyr71FFVddTht8rfeStl1-eH5g4mn4vQxenOqEMNrwaYA1651lEfCnVDh69AZJ8AKuOTQC6FHKQXhTZlAcycFl4YwIhPg45i-EnC0XAS3D7qbSPkIcmXpUyCUEHzUq7SoRFGXOdmRXm3F~OkAkUluQHikTwxhGj9Cxj-xGV-lGCwHAeMn~hwFGFmvoUUpd-bxFOcNQLlVQ__)

## 6. Recommendations

Based on our analysis, we recommend the following strategies to convert casual riders into annual members:

### Recommendation 1: Implement Tiered Membership Options

**Rationale**: Casual riders take significantly longer trips and use bikes more frequently on weekends, suggesting they primarily use bikes for leisure and recreational purposes rather than commuting.

**Implementation Strategy**:
- Create a "Weekend Warrior" membership tier with discounted annual rates for unlimited weekend rides
- Offer a "Leisure Rider" membership with benefits for longer duration rides
- Implement a seasonal membership option for riders who primarily use bikes during spring and summer months
- Include a trial period where casual riders can experience member benefits before committing to a full annual membership

### Recommendation 2: Targeted Marketing at Popular Casual Rider Locations

**Rationale**: Casual riders frequently start and end their trips at tourist attractions and recreational areas along the lakefront, which differ significantly from the locations preferred by members.

**Implementation Strategy**:
- Deploy targeted marketing campaigns at the top 10 stations most frequently used by casual riders
- Install digital displays at these stations highlighting the cost savings of annual membership for regular riders
- Train station ambassadors to engage with casual riders at these locations during peak usage times
- Create location-specific promotions that emphasize the value of membership for visitors to these popular destinations

### Recommendation 3: Develop a Mobile App Engagement Program

**Rationale**: Casual riders show distinct usage patterns in terms of time of day, ride duration, and day of week, suggesting they might benefit from features that enhance the recreational aspect of biking.

**Implementation Strategy**:
- Enhance the mobile app with features specifically appealing to recreational riders
- Implement a loyalty program that rewards consistent usage with points toward membership discounts
- Create weekend challenges and community events to engage casual riders
- Develop a feature that shows casual riders their potential savings with a membership based on their actual usage patterns
- Implement push notifications highlighting membership benefits during peak casual usage times

## Conclusion

Our analysis has provided clear insights into how annual members and casual riders use Cyclistic bikes differently. Members primarily use bikes for shorter, consistent trips during weekdays and commuting hours, suggesting utilitarian purposes like commuting to work. Casual riders take longer trips, with higher weekend usage and preferences for tourist locations, suggesting recreational use.

By implementing our recommendations, Cyclistic can leverage these distinct usage patterns to effectively convert casual riders into annual members, thereby increasing profitability and ensuring future growth. The tiered membership options, targeted marketing, and enhanced digital engagement strategies directly address the specific needs and behaviors of casual riders identified in our analysis.

The next steps would involve implementing these recommendations according to the proposed timeline and measuring their effectiveness using the suggested key performance indicators.

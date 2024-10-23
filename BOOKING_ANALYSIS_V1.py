# https://www.kaggle.com/code/kianwee/eda-hotel-booking-demand/notebook

import pandas as pd

# Load the data
data = pd.read_csv('BookingDataV1.csv')

# Assuming 'Arrival_Date' is the column for arrival dates and 'Cancellation_Status' indicates cancellation
# Convert 'Arrival_Date' to datetime
data['Arrival_Date'] = pd.to_datetime(data['Arrival_Date'])

# Extract day of the week
data['Day_of_Week'] = data['Arrival_Date'].dt.day_name()

# Count total bookings and cancellations by day of the week
total_bookings = data.groupby('Day_of_Week').size()
cancellations = data[data['Cancelled'] == 1].groupby('Day_of_Week').size()

# Combine totals into a single DataFrame
summary = pd.DataFrame({
    'Total_Bookings': total_bookings,
    'Cancellations': cancellations
}).fillna(0)  # Fill NaN values with 0

# Calculate cancellation percentages
summary['Cancellation_Percentage'] = (summary['Cancellations'] / summary['Total_Bookings']) * 100

# Display results
print(summary)

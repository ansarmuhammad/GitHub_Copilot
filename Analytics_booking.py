import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file = 'BookingDataV1.csv'
data = pd.read_csv(file)

# Ensure 'Cancelled' column is treated as binary
data['Cancelled'] = data['Cancelled'].astype(int)

# Group by 'day' and calculate cancellation rates
cancellation_rates = data.groupby('day')['Cancelled'].mean().reset_index()
cancellation_rates['Cancellation_Rate'] = cancellation_rates['Cancelled'] * 100  # Convert to percentage

# Print cancellation rates
print(cancellation_rates)

# Visualize the cancellation rates
plt.figure(figsize=(10, 6))
sns.barplot(x='day', y='Cancellation_Rate', data=cancellation_rates, palette='viridis')
plt.title('Cancellation Rates by Arrival Day')
plt.xlabel('Day of the Week')
plt.ylabel('Cancellation Rate (%)')
plt.xticks(rotation=45)
plt.show()

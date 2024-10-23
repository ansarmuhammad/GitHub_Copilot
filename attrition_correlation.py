import pandas as pd
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from itertools import combinations

# Load the dataset
file = 'sample_data.csv'
data = pd.read_csv(file)

# Convert 'Attrition' to binary values
data['Attrition'] = data['Attrition'].map({'Yes': 1, 'No': 0})

# Identify categorical columns (excluding 'Attrition')
categorical_cols = data.select_dtypes(include=['object']).columns.tolist()

# Convert categorical columns to numerical using CatBoost for prediction purposes
catboost_model = CatBoostClassifier(iterations=1, random_seed=42, verbose=0)
catboost_model.fit(data[categorical_cols], data['Attrition'], cat_features=categorical_cols)
predictions = catboost_model.predict(data[categorical_cols])
data['Predictions'] = predictions  

# Select numerical columns for correlation analysis, excluding 'Attrition' and 'Predictions'
numerical_cols = data.select_dtypes(include=['int64', 'float64']).columns
numerical_cols = numerical_cols.drop(['Attrition', 'Predictions'], errors='ignore')  # Exclude target and prediction columns

# Function to calculate combined correlation
def calculate_combined_correlation(df, cols, target_col):
    """Calculates the correlation between a combination of columns and the target column."""
    df['Combined'] = df[cols].sum(axis=1)  # Create a combined column
    correlation = df['Combined'].corr(df[target_col])
    df.drop(columns=['Combined'], inplace=True)  # Remove the combined column
    return correlation

# Find the highest correlated combination of columns
highest_correlation = 0
highest_correlated_cols = None

for i in range(2, len(numerical_cols) + 1):
    for cols in combinations(numerical_cols, i):
        correlation = calculate_combined_correlation(data, list(cols), 'Attrition')
        if abs(correlation) > abs(highest_correlation):  # Compare absolute correlation
            highest_correlation = correlation
            highest_correlated_cols = cols

# Print the highest correlated combination
if highest_correlated_cols:
    print("Highest Correlated Combination:", highest_correlated_cols)
    print("Correlation:", highest_correlation)
else:
    print("No combination found with correlation above the threshold.")

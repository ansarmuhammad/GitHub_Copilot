import pandas as pd
from catboost import CatBoostClassifier, Pool
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

# Select numerical columns for correlation analysis
numerical_cols = data.select_dtypes(include=['int64', 'float64']).columns

# Function to calculate combined correlation
def calculate_combined_correlation(df, cols, target_col):
    """Calculates the correlation between a combination of columns and the target column."""
    df['Combined'] = df[cols].sum(axis=1)  # Create a combined column
    correlation = df['Combined'].corr(df[target_col])
    df.drop(columns=['Combined'], inplace=True)  # Remove the combined column
    return correlation

# Find strong correlations for combinations of numerical columns
strong_correlations = {}
for i in range(2, len(numerical_cols) + 1):  # Iterate through combinations of 2 or more columns
    for cols in combinations(numerical_cols, i):
        correlation = calculate_combined_correlation(data, list(cols), 'Attrition')
        if abs(correlation) > 0.3:  # Threshold for strong correlation
            strong_correlations[cols] = correlation

# Print strong correlations
print("Strong Correlations (Combination of Columns):")
for cols, correlation in strong_correlations.items():
    print(f"{cols}: {correlation}")

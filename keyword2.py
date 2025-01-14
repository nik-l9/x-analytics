import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data from CSV
file_path = r'C:\Users\HP\Downloads\queries.csv'
df = pd.read_csv(file_path, sep=',')  # Adjust for your separator

# Convert necessary columns to numeric
df['Clicks'] = pd.to_numeric(df['Clicks'], errors='coerce')
df['Impressions'] = pd.to_numeric(df['Impressions'], errors='coerce')
df['CTR'] = df['CTR'].str.replace('%', '').astype(float)  # Clean CTR, remove the '%' and convert to float
df['Position'] = pd.to_numeric(df['Position'], errors='coerce')

# Filter branded queries (containing the keyword 'pieces') and non-branded queries
branded_df = df[df['Top queries'].str.contains('pieces', case=False, na=False)]
non_branded_df = df[~df['Top queries'].str.contains('pieces', case=False, na=False)]

# Step 1: Calculate correlations (optional)
correlation_matrix = df[['Clicks', 'Impressions', 'CTR', 'Position']].corr()

# Step 2: Visualize correlation matrix
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True)
plt.title('Correlation Matrix of Metrics')
plt.show()

# Position vs CTR for branded queries
plt.figure(figsize=(8, 5))
sns.scatterplot(x='Position', y='CTR', data=branded_df, alpha=0.7)
plt.title('Position vs CTR for Branded Queries')
plt.xlabel('Position')
plt.ylabel('CTR (%)')
plt.show()

# Position vs CTR for non-branded queries
plt.figure(figsize=(8, 5))
sns.scatterplot(x='Position', y='CTR', data=non_branded_df, alpha=0.7)
plt.title('Position vs CTR for Non-Branded Queries')
plt.xlabel('Position')
plt.ylabel('CTR (%)')
plt.show()

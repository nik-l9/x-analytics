import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load the data
data = pd.read_csv(r'C:\Users\HP\Downloads\queries.csv')

# Check the number of rows in the dataset
print("Number of rows in the dataset:", data.shape[0])

# Check the column names
print("Columns in dataset:", data.columns)

# Basic data cleaning - ensure CTR column exists and is cleaned
if 'CTR' in data.columns:
    data['CTR'] = data['CTR'].str.rstrip('%').astype('float') / 100.0
else:
    print("CTR column not found")

# Calculate logarithmic values for better distribution
data['log_clicks'] = np.log1p(data['Clicks'])
data['log_impressions'] = np.log1p(data['Impressions'])

# Correlation analysis
correlation_matrix = data[['Clicks', 'Impressions', 'CTR', 'Position']].corr()

# Regression analysis
slope, intercept, r_value, p_value, std_err = stats.linregress(data['Position'], data['CTR'])

# Cluster analysis
X = data[['CTR', 'Position']]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=3, random_state=42)
data['Cluster'] = kmeans.fit_predict(X_scaled)

# Visualization of CTR vs Position
plt.figure(figsize=(12, 8))
sns.scatterplot(data=data, x='Position', y='CTR', hue='Cluster', size='Clicks', 
                sizes=(20, 200), palette='viridis')
plt.title('CTR vs Position (colored by cluster, size by clicks)')
plt.xlabel('Position')
plt.ylabel('CTR')
plt.savefig('ctr_vs_position.png')
plt.close()

# Top N analysis
top_n = 10
top_queries_by_clicks = data.nlargest(top_n, 'Clicks')
top_queries_by_ctr = data[data['Impressions'] > 100].nlargest(top_n, 'CTR')

# Cumulative Clicks and Percentage
data['CumulativeClicks'] = data['Clicks'].cumsum()
data['ClickPercentage'] = data['CumulativeClicks'] / data['Clicks'].sum() * 100

# Print insights
print("Correlation Matrix:")
print(correlation_matrix)
print("\nRegression Analysis:")
print(f"Slope: {slope}, Intercept: {intercept}, R-value: {r_value}, P-value: {p_value}")
print("\nTop 10 Queries by Clicks:")
print(top_queries_by_clicks[['Top queries', 'Clicks', 'CTR', 'Position']])
print("\nTop 10 Queries by CTR (with >100 impressions):")
print(top_queries_by_ctr[['Top queries', 'Clicks', 'CTR', 'Position']])
print("\nLong Tail Analysis:")
print(data[['Top queries', 'Clicks', 'ClickPercentage']].head(20))

# Top 10 Queries by Conversions (assuming a conversion rate, you can replace this with actual conversion data if available)
data['Conversions'] = data['Clicks'] * 0.1  # Example: 10% conversion rate
data['Conversion Rate'] = data['Conversions'] / data['Clicks']

# Print the top queries with conversion data
top_queries_by_conversion = data.nlargest(top_n, 'Conversions')
print("\nTop 10 Queries by Conversions:")
print(top_queries_by_conversion[['Top queries', 'Clicks', 'Conversions', 'Conversion Rate']])

# Additional visualizations
# Cumulative Clicks vs Click Percentage
plt.figure(figsize=(10, 6))
plt.plot(data['CumulativeClicks'], data['ClickPercentage'], marker='o')
plt.title('Cumulative Clicks vs Click Percentage')
plt.xlabel('Cumulative Clicks')
plt.ylabel('Click Percentage')
plt.grid()
plt.savefig('cumulative_clicks_percentage.png')
plt.close()

# CTR vs Impressions
plt.figure(figsize=(10, 6))
sns.scatterplot(data=data, x='Impressions', y='CTR', alpha=0.7)
plt.title('CTR vs Impressions')
plt.xscale('log')
plt.xlabel('Impressions (log scale)')
plt.ylabel('CTR')
plt.grid()
plt.savefig('ctr_vs_impressions.png')
plt.close()

# Additional visualizations
plt.figure(figsize=(10, 6))
sns.histplot(data=data, x='Position', bins=20)
plt.title('Distribution of Search Positions')
plt.xlabel('Position')
plt.ylabel('Count')
plt.savefig('position_distribution.png')
plt.close()

plt.figure(figsize=(10, 6))
sns.regplot(data=data, x='log_impressions', y='log_clicks')
plt.title('Log Impressions vs Log Clicks')
plt.xlabel('Log Impressions')
plt.ylabel('Log Clicks')
plt.savefig('impressions_vs_clicks.png')
plt.close()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
data = pd.read_csv(r'C:\Users\HP\Downloads\queries2.csv')

# Print the first few rows and the columns
print(data.head())
print(data.columns)

# Select columns for correlation matrices
base_columns = [
    'Views', 'Active users', 'Views per active user', 'Engaged sessions',
    'Average engagement time per active user', 'Event count', 'Key events',
    'Session key event rate'
]

all_columns = base_columns  # No conversion rate included

# Function to create and save correlation matrix
def create_correlation_matrix(data, columns, title, filename):
    plt.figure(figsize=(12, 10))
    correlation_matrix = data[columns].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    return correlation_matrix

# Create correlation matrices
overall_matrix = create_correlation_matrix(data, all_columns, 'Overall Correlation Matrix', 'overall_correlation_matrix.png')

# Perform calculations for top engaging pages and top efficient pages
top_engaging_pages = data.nlargest(5, 'Average engagement time per active user')
top_efficient_pages = data.nlargest(5, 'Event count')  # Assuming you want to check for the highest event count instead

# Create visualizations
plt.figure(figsize=(20, 20))

# 1. Engagement Time Distribution
plt.subplot(3, 2, 1)
sns.histplot(data['Average engagement time per active user'], kde=True)
plt.xlabel('Average Engagement Time')
plt.title('Distribution of Engagement Time')

# 2. Top Engaging Pages
plt.subplot(3, 2, 2)
sns.barplot(x='Average engagement time per active user', y='Page title and screen class', data=top_engaging_pages)
plt.title('Top 5 Engaging Pages')

# 3. Views vs Active Users
plt.subplot(3, 2, 3)
plt.scatter(data['Active users'], data['Views'])
plt.xlabel('Active Users')
plt.ylabel('Views')
plt.title('Views vs Active Users')

# 4. Content Efficiency
plt.subplot(3, 2, 4)
sns.barplot(x='Event count', y='Page title and screen class', data=top_efficient_pages)  # Update this to whatever metric you want
plt.title('Top 5 Pages by Event Count')

# 5. Key Events Distribution
plt.subplot(3, 2, 5)
sns.histplot(data['Key events'], kde=True)
plt.xlabel('Key Events')
plt.title('Distribution of Key Events')

plt.tight_layout()
plt.savefig('website_metrics_analysis.png')
plt.close()

# Print key insights
print("\nTop Engaging Pages:")
print(top_engaging_pages[['Page title and screen class', 'Average engagement time per active user']])

print("\nMost Efficient Content:")
print(top_efficient_pages[['Page title and screen class', 'Event count']])

# Additional calculations
median_engagement_time = data['Average engagement time per active user'].median()
total_key_events = data['Key events'].sum()

print(f"\nMedian Engagement Time: {median_engagement_time:.2f} seconds")
print(f"Total Key Events: {total_key_events}")

# Calculate and print the overall session key event rate
overall_session_key_event_rate = data['Key events'].sum() / data['Engaged sessions'].sum()
print(f"\nOverall Session Key Event Rate: {overall_session_key_event_rate:.4f}")

# Print correlation matrices
print("\nOverall Correlation Matrix:")
print(overall_matrix)

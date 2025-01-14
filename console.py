import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data
file_path = r'C:\Users\HP\Downloads\queries2.csv'
df = pd.read_csv(file_path)

# Set 'Page title and screen class' as the index
df.set_index('Page title and screen class', inplace=True)

# Correlation matrix
correlation_matrix = df.corr()
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix of Search Console Metrics')
plt.tight_layout()
plt.savefig('correlation_matrix.png')
plt.close()

# Top 5 pages by views
top_pages = df.sort_values('Views', ascending=False).head()
plt.figure(figsize=(12, 6))
plt.bar(top_pages.index, top_pages['Views'])
plt.title('Top 5 Pages by Views')
plt.xlabel('Page Title')
plt.ylabel('Views')
plt.xticks(rotation=90, ha='right')
plt.tight_layout()
plt.savefig('top_pages_views.png')
plt.close()

# Scatter plot: Views vs. Active Users
plt.figure(figsize=(10, 6))
plt.scatter(df['Active users'], df['Views'])
plt.title('Views vs. Active Users')
plt.xlabel('Active Users')
plt.ylabel('Views')
plt.tight_layout()
plt.savefig('views_vs_active_users.png')
plt.close()

# Bar plot: Average Engagement Time per Active User (top 10)
top_10_engagement = df.sort_values('Average engagement time per active user', ascending=False).head(10)
plt.figure(figsize=(12, 6))
plt.bar(top_10_engagement.index, top_10_engagement['Average engagement time per active user'])
plt.title('Top 10 Pages by Average Engagement Time per Active User')
plt.xlabel('Page Title')
plt.ylabel('Average Engagement Time (seconds)')
plt.xticks(rotation=90, ha='right')
plt.tight_layout()
plt.savefig('avg_engagement_time.png')
plt.close()

# Calculate and print insights
total_views = df['Views'].sum()
total_active_users = df['Active users'].sum()
avg_views_per_user = total_views / total_active_users

print(f"Total Views: {total_views}")
print(f"Total Active Users: {total_active_users}")
print(f"Average Views per User: {avg_views_per_user:.2f}")

most_engaging_page = df['Average engagement time per active user'].idxmax()
print(f"Most Engaging Page: {most_engaging_page}")
print(f"with an average engagement time of {df.loc[most_engaging_page, 'Average engagement time per active user']:.2f} seconds")

highest_event_count = df['Event count'].idxmax()
print(f"Page with Highest Event Count: {highest_event_count}")
print(f"with {df.loc[highest_event_count, 'Event count']} events")

# Views per Active User distribution
plt.figure(figsize=(10, 6))
sns.histplot(df['Views per active user'], kde=True)
plt.title('Distribution of Views per Active User')
plt.xlabel('Views per Active User')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('views_per_user_distribution.png')
plt.close()

# Engagement vs. Views scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(df['Views'], df['Average engagement time per active user'])
plt.title('Engagement Time vs. Views')
plt.xlabel('Views')
plt.ylabel('Average Engagement Time per Active User (seconds)')
plt.tight_layout()
plt.savefig('engagement_vs_views.png')
plt.close()

# Event count vs. Views scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(df['Views'], df['Event count'])
plt.title('Event Count vs. Views')
plt.xlabel('Views')
plt.ylabel('Event Count')
plt.tight_layout()
plt.savefig('event_count_vs_views.png')
plt.close()

print("Analysis complete. Check the generated PNG files for visualizations.")
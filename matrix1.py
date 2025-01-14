import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
data = pd.read_csv(r'C:\Users\HP\Downloads\queries2.csv')

# Calculate metrics for segmentation
mean_views = data['Views'].mean()
median_engagement_time = data['Average engagement time per active user'].median()

# Define conditions for quadrants
conditions = [
    (data['Views'] >= mean_views) & (data['Average engagement time per active user'] >= median_engagement_time),
    (data['Views'] < mean_views) & (data['Average engagement time per active user'] >= median_engagement_time),
    (data['Views'] >= mean_views) & (data['Average engagement time per active user'] < median_engagement_time),
    (data['Views'] < mean_views) & (data['Average engagement time per active user'] < median_engagement_time)
]

# Define quadrant labels
labels = ['Top Performers', 'Potential Growth', 'Needs Optimization', 'Underperformers']

# Assign quadrant labels to a new column
data['Segment'] = pd.cut(data['Views'], bins=[0, mean_views, float('inf')], labels=['Low Traffic', 'High Traffic'])
data['Segment'] = data.apply(lambda x: f"{x['Segment']} / {'High Engagement' if x['Average engagement time per active user'] >= median_engagement_time else 'Low Engagement'}", axis=1)

# Print segmented data
print(data[['Page title and screen class', 'Views', 'Average engagement time per active user', 'Segment']])

# Visualize the quadrants
plt.figure(figsize=(10, 6))

# Scatter plot
plt.scatter(data['Views'], data['Average engagement time per active user'], c='blue', alpha=0.5)

# Plot horizontal and vertical lines
plt.axhline(y=median_engagement_time, color='r', linestyle='--', label='Median Engagement Time')
plt.axvline(x=mean_views, color='g', linestyle='--', label='Mean Views')

# Adding labels and title
for i, row in data.iterrows():
    plt.annotate(row['Page title and screen class'], (row['Views'], row['Average engagement time per active user']), fontsize=8)

plt.title('Engagement Quadrant Analysis')
plt.xlabel('Views')
plt.ylabel('Average Engagement Time per Active User (seconds)')
plt.legend()
plt.grid()
plt.show()

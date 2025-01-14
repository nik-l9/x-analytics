import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data from CSV (replace with your actual file path)
file_path = r'C:\Users\HP\Downloads\queries.csv'
df = pd.read_csv(file_path, sep=',')  # Adjusted for comma-separated values

# Convert 'Clicks' and 'Impressions' to numeric
df['Clicks'] = pd.to_numeric(df['Clicks'], errors='coerce')
df['Impressions'] = pd.to_numeric(df['Impressions'], errors='coerce')

# Step 2: Calculate CTR if not already present
if 'CTR' in df.columns:
    df['CTR'] = df['CTR'].str.replace('%', '').astype(float)  # Remove '%' and convert to float
else:
    df['CTR'] = (df['Clicks'] / df['Impressions']) * 100  # Calculate CTR if not present

# Step 3: Categorize keywords into Brand and Non-Brand
brand_keywords = df['Top queries'].str.contains('pieces', case=False)
df['Category'] = ['Brand' if x else 'Non-Brand' for x in brand_keywords]

# Step 4: Group by Category to calculate total metrics
summary = df.groupby('Category').agg({
    'Clicks': 'sum',
    'Impressions': 'sum',
    'CTR': 'mean'
}).reset_index()

# Display the summary DataFrame
print(summary)

# Step 5: Visualize Clicks by Category
plt.figure(figsize=(8, 5))
sns.barplot(x='Category', y='Clicks', data=summary, palette='Blues')
plt.title('Total Clicks by Keyword Category')
plt.ylabel('Clicks')
plt.xlabel('Keyword Category')
plt.savefig('total_clicks_by_category.png')  # Save as PNG
plt.close()  # Close the figure

# Step 6: Visualize Impressions by Category
plt.figure(figsize=(8, 5))
sns.barplot(x='Category', y='Impressions', data=summary, palette='Oranges')
plt.title('Total Impressions by Keyword Category')
plt.ylabel('Impressions')
plt.xlabel('Keyword Category')
plt.savefig('total_impressions_by_category.png')  # Save as PNG
plt.close()  # Close the figure

# Step 7: Visualize CTR by Category
plt.figure(figsize=(8, 5))
sns.barplot(x='Category', y='CTR', data=summary, palette='Greens')
plt.title('Average Click-Through Rate (CTR) by Keyword Category')
plt.ylabel('CTR (%)')
plt.xlabel('Keyword Category')
plt.savefig('average_ctr_by_category.png')  # Save as PNG
plt.close()  # Close the figure

print("Graphs have been saved as PNG files.")

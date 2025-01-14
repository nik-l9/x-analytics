import pandas as pd
import plotly.express as px
from ydata_profiling import ProfileReport
import os
from datetime import datetime, timedelta

# Load the dataset
file_path = r"C:\Users\HP\Downloads\account_overview_analytics (2) (1).csv"
data = pd.read_csv(file_path)

# Convert the Date column to datetime
data['Date'] = pd.to_datetime(data['Date'])

# Sort by date
data = data.sort_values(by='Date')

# Create a directory for saving the HTML and charts
output_dir = "output_dashboard"
os.makedirs(output_dir, exist_ok=True)

# Generate YData Profiling report
profile = ProfileReport(data, title="Twitter Analytics Report", explorative=True)
html_report_path = os.path.join(output_dir, "twitter_analytics_report.html")
profile.to_file(html_report_path)
print(f"Detailed profiling report saved at: {html_report_path}")

# Update the Plotly template for a darker theme
plotly_template = "plotly_dark"

# Plotly configuration for better rendering
plotly_config = {
    'displayModeBar': True,
    'responsive': True
}

# Function to filter data by time range
def filter_data(time_range):
    if time_range == 'last_7_days':
        seven_days_ago = datetime.now() - timedelta(days=7)
        return data[data['Date'] >= seven_days_ago]
    elif time_range == 'last_30_days':
        thirty_days_ago = datetime.now() - timedelta(days=30)
        return data[data['Date'] >= thirty_days_ago]
    return data

# Function to generate charts for a given time range
def generate_charts(time_range):
    filtered_data = filter_data(time_range)
    
    # A. Time Series: Impressions, Likes, and New Followers
    data_long = filtered_data.melt(id_vars=['Date'], value_vars=['Impressions', 'Likes', 'New follows'],
                                   var_name='Metrics', value_name='Count')
    fig1 = px.line(data_long, x='Date', y='Count', color='Metrics',
                   title=f"Impressions, Likes, and New Followers Over Time ({time_range.replace('_', ' ').title()})",
                   labels={'Count': 'Count', 'Metrics': 'Metrics'}, template=plotly_template)
    fig1_path = os.path.join(output_dir, f"interactive_time_series_{time_range}.html")
    fig1.write_html(fig1_path, full_html=True, config=plotly_config)

    # B. Engagement Rate Over Time
    filtered_data['Engagement Rate'] = (filtered_data['Engagements'] / filtered_data['Impressions']) * 100
    fig2 = px.line(filtered_data, x='Date', y='Engagement Rate', 
                   title=f"Engagement Rate Over Time ({time_range.replace('_', ' ').title()})",
                   labels={'Engagement Rate': 'Engagement Rate (%)'}, template=plotly_template)
    fig2_path = os.path.join(output_dir, f"engagement_rate_time_series_{time_range}.html")
    fig2.write_html(fig2_path, full_html=True, config=plotly_config)

    # C. Engagement Breakdown by Date as Stacked Bar Chart
    engagement_data = filtered_data.melt(id_vars=['Date'], value_vars=['Likes', 'Replies', 'Reposts', 'Bookmarks', 'Share'],
                                         var_name='Engagement Type', value_name='Count')
    fig3 = px.bar(engagement_data, x='Date', y='Count', color='Engagement Type', 
                  title=f"Engagement Metrics Segmentation by Date ({time_range.replace('_', ' ').title()})", 
                  labels={'Count': 'Engagement Count', 'Date': 'Date'}, 
                  template=plotly_template, barmode='stack')
    fig3_path = os.path.join(output_dir, f"engagement_metrics_by_date_{time_range}.html")
    fig3.write_html(fig3_path, full_html=True, config=plotly_config)

    # D. Video views vs Media views Bar Chart
    fig4 = px.bar(filtered_data, x='Date', y=['Video views', 'Media views'],
                  title=f"Video Views vs Media Views ({time_range.replace('_', ' ').title()})",
                  labels={'value': 'View Count', 'variable': 'Content Type'}, template=plotly_template)
    fig4_path = os.path.join(output_dir, f"video_media_views_comparison_{time_range}.html")
    fig4.write_html(fig4_path, full_html=True, config=plotly_config)

    return fig1_path, fig2_path, fig3_path, fig4_path

# Create charts for both "Last 7 Days" and "Last 30 Days"
fig1_7days, fig2_7days, fig3_7days, fig4_7days = generate_charts('last_7_days')
fig1_30days, fig2_30days, fig3_30days, fig4_30days = generate_charts('last_30_days')

# HTML Content (with custom styles and layout)
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Twitter Analytics Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        :root {{
            --primary: #8A2BE2;
            --secondary: #4B0082;
            --background: #1A1A2E;
            --text: #E0E0E0;
            --text-light: #B0B0B0;
            --card-bg: #16213E;
            --border: #30365F;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', sans-serif;
            background-color: var(--background);
            color: var(--text);
            line-height: 1.6;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }}

        header {{
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}

        h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}

        .subtitle {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}

        .button-container {{
            margin-bottom: 20px;
        }}
        .button {{
            padding: 10px 20px;
            font-size: 16px;
            color: white;
            background-color: var(--primary);
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }}
        .button:hover {{
            background-color: var(--secondary);
        }}

        .dashboard-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
        }}

        .chart-container {{
            background-color: var(--card-bg);
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .chart-container:hover {{
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }}

        .chart-container.full-width {{
            grid-column: 1 / -1;
        }}

        h2 {{
            font-size: 1.5rem;
            color: var(--primary);
            margin-bottom: 1rem;
            border-bottom: 2px solid var(--primary);
            padding-bottom: 0.5rem;
        }}

        iframe {{
            width: 100%;
            height: 400px;
            border: none;
            border-radius: 10px;
        }}

        .summary {{
            background-color: var(--card-bg);
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}

        .summary h2 {{
            color: var(--primary);
        }}

        .summary p {{
            margin-bottom: 1rem;
        }}

        .link {{
            color: #00008B;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s ease;
        }}

        .link:hover {{
            color: #0000CD;
        }}

        footer {{
            text-align: center;
            margin-top: 2rem;
            padding: 1rem;
            background-color: var(--card-bg);
            border-radius: 15px;
        }}

        @media (max-width: 1200px) {{
            .dashboard-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 1rem;
            }}

            header {{
                padding: 1.5rem;
            }}

            h1 {{
                font-size: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
    <h1>Twitter Analytics Dashboard</h1>
    <p class="subtitle">Insights and Performance Metrics <a href="twitter_analytics_report.html" target="_blank" class="link">View Detailed Report</a></p>
</header>


        <div class="button-container">
            <button class="button" onclick="toggleCharts('7days')">Last 7 Days</button>
            <button class="button" onclick="toggleCharts('30days')">Last 30 Days</button>
        </div>

        <div class="dashboard-grid" id="7days-charts">
            <div class="chart-container">
                <h2>Impressions, Likes, and New Followers</h2>
                <iframe src="{os.path.basename(fig1_7days)}"></iframe>
            </div>
            <div class="chart-container">
                <h2>Engagement Rate Over Time</h2>
                <iframe src="{os.path.basename(fig2_7days)}"></iframe>
            </div>
            <div class="chart-container full-width">
                <h2>Engagement Metrics by Date</h2>
                <iframe src="{os.path.basename(fig3_7days)}" height="600px"></iframe>
            </div>
            <div class="chart-container full-width">
                <h2>Video vs Media Views</h2>
                <iframe src="{os.path.basename(fig4_7days)}" height="900px"></iframe>
            </div>
        </div>

        <div class="dashboard-grid" id="30days-charts" style="display: none;">
            <div class="chart-container">
                <h2>Impressions, Likes, and New Followers</h2>
                <iframe src="{os.path.basename(fig1_30days)}"></iframe>
            </div>
            <div class="chart-container">
                <h2>Engagement Rate Over Time</h2>
                <iframe src="{os.path.basename(fig2_30days)}"></iframe>
            </div>
            <div class="chart-container full-width">
                <h2>Engagement Metrics by Date</h2>
                <iframe src="{os.path.basename(fig3_30days)}" height="600px"></iframe>
            </div>
            <div class="chart-container full-width">
                <h2>Video vs Media Views</h2>
                <iframe src="{os.path.basename(fig4_30days)}" height="900px"></iframe>
            </div>
        </div>

        <footer>
            <p>&copy; 2024 Built with ❤️ by Nikhil. All Rights Reserved.</p>
        </footer>
    </div>

    <script>
        function toggleCharts(timeRange) {{
            document.getElementById('7days-charts').style.display = timeRange === '7days' ? 'block' : 'none';
            document.getElementById('30days-charts').style.display = timeRange === '30days' ? 'block' : 'none';
        }}
    </script>
</body>
</html>
"""

# Save the HTML dashboard
html_dashboard_path = os.path.join(output_dir, "twitter_dashboard.html")
with open(html_dashboard_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML dashboard saved at: {html_dashboard_path}")

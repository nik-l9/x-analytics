import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

async function generateDashboard() {
  // Simulating the chart generation paths
  const fig1_path = "interactive_time_series.html";
  const fig2_path = "engagement_rate_time_series.html";
  const fig3_path = "engagement_metrics_by_date.html";
  const fig4_path = "video_media_views_comparison.html";

  const html_content = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Twitter Analytics Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #1DA1F2;
            --secondary: #14171A;
            --background: #F5F8FA;
            --text: #14171A;
            --text-light: #657786;
            --card-bg: #FFFFFF;
            --border: #E1E8ED;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--background);
            color: var(--text);
            line-height: 1.6;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }

        header {
            background-color: var(--primary);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        h1 {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }

        .subtitle {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }

        .chart-container {
            background-color: var(--card-bg);
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .chart-container:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }

        h2 {
            font-size: 1.5rem;
            color: var(--secondary);
            margin-bottom: 1rem;
            border-bottom: 2px solid var(--primary);
            padding-bottom: 0.5rem;
        }

        iframe {
            width: 100%;
            height: 400px;
            border: none;
            border-radius: 10px;
        }

        .summary {
            background-color: var(--card-bg);
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .summary h2 {
            color: var(--primary);
        }

        .summary p {
            margin-bottom: 1rem;
        }

        .link {
            color: var(--primary);
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s ease;
        }

        .link:hover {
            color: var(--secondary);
        }

        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }

            header {
                padding: 1.5rem;
            }

            h1 {
                font-size: 2rem;
            }

            .dashboard-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Twitter Analytics Dashboard</h1>
            <p class="subtitle">Insights and Performance Metrics</p>
        </header>

        <section class="summary">
            <h2>Summary</h2>
            <p>Explore the detailed profiling report and analytics insights for your Twitter account.</p>
            <p>For a comprehensive analysis, view the <a href="twitter_analytics_report.html" target="_blank" class="link">detailed summary and profiling report</a>.</p>
        </section>

        <div class="dashboard-grid">
            <div class="chart-container">
                <h2>Impressions, Likes, and New Followers</h2>
                <iframe src="${fig1_path}"></iframe>
            </div>
            <div class="chart-container">
                <h2>Engagement Rate Over Time</h2>
                <iframe src="${fig2_path}"></iframe>
            </div>
            <div class="chart-container">
                <h2>Engagement Metrics by Date</h2>
                <iframe src="${fig3_path}"></iframe>
            </div>
            <div class="chart-container">
                <h2>Video vs Media Views</h2>
                <iframe src="${fig4_path}"></iframe>
            </div>
        </div>
    </div>
</body>
</html>
`;

  const output_dir = path.join(__dirname, 'output_dashboard');
  await fs.mkdir(output_dir, { recursive: true });

  const html_dashboard_path = path.join(output_dir, 'twitter_dashboard.html');
  await fs.writeFile(html_dashboard_path, html_content);

  console.log(`HTML dashboard saved at: ${html_dashboard_path}`);
}

generateDashboard().catch(console.error);
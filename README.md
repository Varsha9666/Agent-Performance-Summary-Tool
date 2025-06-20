# 📊 Agent Performance Summary Tool

This project was completed as part of an internship assessment. The goal is to analyze call center data and generate an agent-wise performance report for a specific day.

🧾 Project Objective

This project processes and analyzes call center performance data to generate a daily summary of agent activity. It merges three core datasets—call logs, agent roster, and disposition summary—to compute key metrics per agent and highlight top performers.

The solution includes modular, validated, and extensible code with CLI support and logging.


📌 Objectives:

Merge and analyze agent activity across multiple sources.

- Calculate metrics like:

- Total calls handled

- Unique loans contacted

- Completed calls

- Average call duration

- Agent presence

- Connect rate

- Identify the top-performing agent for a selected date.

- Save the summary as a CSV file and visualize insights with plots.

Tasks:

1. Data Ingestion and Validation:
Read all 3 files into pandas.
Ensure call_date, agent_id, and org_id are present and correctly formatted.
Flag missing or duplicate entries.
2. Join Logic:
Merge the datasets using agent_id, org_id, and call_date.
Ensure no data loss in joins; explain how you handled mismatches.
3. Feature Engineering:
For each agent on each date, compute:
Total Calls Made
Unique Loans Contacted
Connect Rate = Completed Calls / Total Calls
Avg Call Duration (in minutes)
Presence (1 if login_time exists, else 0) Agent Summary for 2025-04-28 Top Performer: Ravi Sharma (98% connect rate) Total Active Agents: 45 Average Duration: 6.5 min

---Output:
Save the report as agent_performance_summary.csv
Format a Slack-style summary

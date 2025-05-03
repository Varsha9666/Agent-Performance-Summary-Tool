# 📊 Agent Performance Summary Tool – README

This project was completed as part of an internship assessment. The goal is to analyze call center data and generate an agent-wise performance report for a specific day.

---

## 🧾 Project Objective

This project processes and analyzes call center performance data to generate a daily summary of agent activity. It merges three core datasets—call logs, agent roster, and disposition summary—to compute key metrics per agent and highlight top performers.

The solution includes modular, validated, and extensible code with CLI support and logging.

📌 Objectives
Merge and analyze agent activity across multiple sources.

Calculate metrics like:

Total calls handled

Unique loans contacted

Completed calls

Average call duration

Agent presence

Connect rate

Identify the top-performing agent for a selected date.

Save the summary as a CSV file and visualize insights with plots.

### Tasks:
1. Data Ingestion and Validation:
 - Read all 3 files into pandas.
 - Ensure call_date, agent_id, and org_id are present and correctly formatted.
 - Flag missing or duplicate entries.

2. Join Logic:
 - Merge the datasets using agent_id, org_id, and call_date.
 - Ensure no data loss in joins; explain how you handled mismatches.

3. Feature Engineering:
 - For each agent on each date, compute:
 * Total Calls Made
 * Unique Loans Contacted
 * Connect Rate = Completed Calls / Total Calls
 * Avg Call Duration (in minutes)
 * Presence (1 if login_time exists, else 0)
   Agent Summary for 2025-04-28
   Top Performer: Ravi Sharma (98% connect rate)
   Total Active Agents: 45
   Average Duration: 6.5 min
   
4. Output:
 - Save the report as agent_performance_summary.csv
 - Format a Slack-style summary message lik
---

#### 📁 Input Files Description

| File Name                 | Description |
|---------------------------|-------------|
| `call_logs.csv`           | Contains records of calls made by agents. |
| `agent_roster.csv`        | Contains agent details such as name and mobile number. |
| `disposition_summary.csv` | Contains data about agent logins (presence data). |

---

📁 Data Sources and Schemas
The pipeline uses three input files (as per the assignment spec
file-tuipwfjdmqbsnt4z2yyf1a
):
call_logs.csv: Records of all call attempts. Key columns include call_id, agent_id, org_id, installment_id, status, duration, created_ts, and call_date. Each row is one call event (status = completed/connected/failed/etc)

.
agent_roster.csv: Agent metadata. Columns: agent_id, users_first_name, users_last_name, users_office_location, org_id. Contains each agent’s name and office, used to label performance by agent

.
disposition_summary.csv: Daily login (presence) data. Columns: agent_id, org_id, call_date, login_time. Indicates if/when an agent logged in on that date
.
These files are loaded into pandas DataFrames. The pipeline ensures that the join keys (agent_id, org_id, call_date) are present and correctly formatted
file-tuipwfjdmqbsnt4z2yyf1a
. For example, call_date is converted to datetime to allow proper merging.

##### Pipeline Overview

The end-to-end processing pipeline proceeds as follows:
Data Ingestion & Validation: Load all three CSVs into pandas. Check for missing or malformed values in critical fields (agent_id, org_id, call_date) and flag duplicates. For instance, duplicate call_id entries are dropped, and any missing agent_id or call_date rows are reported (matching the assignment’s data validation requirements)

.
Preprocessing: Standardize data types (e.g. convert call_date to datetime), trim whitespace, and normalize any inconsistent formatting. Ensure org_id fields align across files (they represent the organization code).
Joining Data: Merge the datasets on (agent_id, org_id, call_date). First, call_logs is left-joined with disposition_summary to attach login presence to each call. Next, the result is left-joined with agent_roster to attach agent names and office details. This preserves all calls (no call records are lost) while adding agent info. Any mismatches (e.g. calls by unknown agents) are logged for review

.
Feature Engineering & Summarization: Using the merged data, compute per-agent metrics for each date:
Total Calls: Count of calls per agent per date.
Unique Loans Contacted: Count of distinct installment_ids contacted.
Completed Calls: Number of calls with status == "completed".
Connect Rate: completed_calls / total_calls (rounded percentage).
Average Call Duration: Mean of duration (seconds) converted to minutes.
Presence Flag: 1 if the agent has a login_time on that date (i.e. was active), else 0.
These metrics are computed via groupby(agent_id, org_id, call_date) and aggregation in pandas (vectorized operations for efficiency). The result is a summary DataFrame with one row per agent-date.
Summary Output:
CSV Report: Write the final metrics to agent_performance_summary.csv. Each row contains: agent_id, org_id, call_date, total_calls, completed_calls, avg_duration_min, presence, connect_rate. For example, the CSV header and a sample row might look like:
Copy
Edit
agent_id,org_id,call_date,total_calls,completed_calls,avg_duration_min,presence,connect_rate
A001,O1,2025-04-28,20,2,0.11,1,0.10
This indicates Agent A001 (Org O1) made 20 calls on 2025-04-28, with 2 completions, avg duration 0.11 min, was present (1), and had a 10% connect rate
.
Slack-Style Summary Message: Generate and print a human-readable daily summary
**Agent Summary for 2025-04-28**
🏆 Top Performer: AgentFirst3 AgentLast3 (38% connect rate)
👥 Total Active Agents: 20
⏱️ Average Duration: 0.12 min

##### 🔧 CLI Script Functions
The core logic is encapsulated in modular functions within agent_summary_script.py:
parse_args() – Uses argparse to read command-line arguments for input file paths and the target date (e.g. --date 2025-04-28). Ensures required arguments are provided.
load_data(filepath) – Reads a CSV into a pandas DataFrame (pd.read_csv), with basic error handling.
validate_data(df) – Checks a DataFrame for missing agent_id/call_date values or duplicate IDs. Prints warnings if issues are found.
merge_data(call_df, roster_df, disp_df) – Merges the three DataFrames: first call_df with disp_df on (agent_id, org_id, call_date), then with roster_df on (agent_id, org_id). Returns the combined DataFrame.
compute_metrics(merged_df) – Performs the groupby and aggregation to calculate total_calls, unique_loans, completed_calls, avg_duration_min, presence, and connect_rate for each agent-date. Returns the summary DataFrame.
generate_agent_summary(summary_df, roster_df, date) – Filters the summary for the given date, merges in agent names, and prints the Slack-style message (as above) for that day. Returns the formatted message string
file-5q3azgke4r7htz8xelpm4f
.
main() – The entry point ties everything together: calls the above functions in sequence, writes the CSV output, and invokes generate_agent_summary(). Typical execution flow:
Parse CLI args.
Load and validate inputs (call_logs, agent_roster, disposition_summary).
Preprocess (date conversions, drop duplicates).
Merge and compute metrics.
Save agent_performance_summary.csv.
Print Slack summary.
This modular structure ensures clean code and reusability, addressing the code cleanliness/modularity criterion
.
Visualization (Notebook only): The companion Jupyter notebook explores the data with charts (see Visualizations below). These are analytical, not required for the CLI output, but they help illustrate patterns (e.g. bar charts of calls per agent or connect-rate distributions).

####### 📊 Visualizations
(All charts are generated in the accompanying Jupyter Notebook for exploratory analysis.) The notebook produces several key plots to illustrate agent performance trends:
Calls per Agent (Bar Chart): A bar chart of Total Calls Made by each agent on the report date. This highlights the most active agents in terms of call volume. It helps identify workload distribution (e.g. Agent A had 28 calls vs. Agent B with 15) and check for any anomalies.
Connect Rate by Agent (Bar Chart): A bar chart of Connect Rate for each agent. This shows efficiency: agents with higher bars consistently reach borrowers (higher connect rates). For example, a top agent might have a 60% connect rate while others are lower, highlighting best performers.
Average Call Duration (Histogram or Boxplot): A distribution plot of call durations. This reveals if most calls are short (e.g. mean around 6 minutes) or if outliers exist. It provides insight into call handling (e.g. very long calls may indicate difficult cases).
Presence Summary (Pie/Bar): A simple chart of active vs. inactive agents (presence flag). Since Presence is 1 if an agent logged in, this chart shows what fraction of roster agents were active that day. It’s useful for compliance/attendance analysis.
Each visualization is accompanied by commentary in the notebook, explaining what the chart shows and any notable insights (e.g., “Agent X not only made the most calls but also had one of the highest connect rates, indicating strong performance”). These charts help stakeholders quickly see key performance patterns beyond the raw numbers.

## 🪛 Code Walkthrough (Jupyter Notebook)

### 1. **Importing Required Libraries**

```python
import pandas as pd
```
Used for data loading, manipulation, and summarization.

---

### 2. **Loading the Datasets**

```python
call_logs = pd.read_csv("call_logs.csv")
agent_roster = pd.read_csv("agent_roster.csv")
disposition_summary = pd.read_csv("disposition_summary.csv")
```

Each of the three CSV files is loaded into a separate DataFrame.

---

### 3. **Checking for Missing Values**

```python
call_logs.isnull().sum()
agent_roster.isnull().sum()
disposition_summary.isnull().sum()
```

This step helps identify incomplete records in the datasets.

---

### 4. **Convert Dates**

```python
call_logs['call_date'] = pd.to_datetime(call_logs['call_date'], dayfirst=True)
disposition_summary['call_date'] = pd.to_datetime(disposition_summary['call_date'], dayfirst=True)
```

Converts the `call_date` column to datetime format to ensure consistency during merging.

---

### 5. **Filtering Data for a Specific Date**

```python
date_to_report = "2025-04-28"
calls_filtered = call_logs[call_logs['call_date'] == date_to_report]
logins_filtered = disposition_summary[disposition_summary['call_date'] == date_to_report]
```

Filters the call and login data to include only records for the date we want to analyze.

---

### 6. **Merging Data**

```python
merged = calls_filtered.merge(agent_roster, on=['agent_id', 'org_id'], how='left')                        .merge(logins_filtered, on=['agent_id', 'org_id', 'call_date'], how='left')
```

Joins all three datasets to create a master DataFrame for the given date.

---

### 7. **Calculating Summary Metrics**

```python
grouped = merged.groupby(['agent_id', 'org_id'])

summary = grouped.agg(
    total_calls=('call_id', 'count'),
    unique_loans=('installment_id', 'nunique')
).reset_index()
```

Generates the base metrics:
- Total calls made
- Unique loans contacted

---

### 8. **Additional Metrics**

```python
additional_metrics = grouped.agg(
    completed_calls=('status', lambda x: (x == 'completed').sum()),
    avg_duration_min=('duration', lambda x: round(x.mean() / 60, 2)),
    presence=('login_time', lambda x: 1 if x.notna().any() else 0)
).reset_index()
```

Adds:
- Completed calls
- Average call duration (converted from seconds to minutes)
- Presence indicator based on login data

---

### 9. **Merging All Metrics**

```python
summary = summary.merge(additional_metrics, on=['agent_id', 'org_id'])
summary['connect_rate'] = summary['completed_calls'] / summary['total_calls']
```

Combines all the calculated metrics and computes the connect rate.

---

### 10. **Adding Agent Names**

```python
summary_named = summary.merge(agent_roster, on=['agent_id', 'org_id'], how='left')
summary_named['full_name'] = summary_named['first_name'] + ' ' + summary_named['last_name']
```

Merges agent names for better readability in the final output.

---

### 11. **Printing Daily Summary**

```python
top = summary_named.sort_values(by='connect_rate', ascending=False).iloc[0]
message = f"""**Agent Summary for {date_to_report}**
🏆 Top Performer: {top_name} ({top_rate}% connect rate)
👥 Total Active Agents: {total_agents}
⏱️ Average Duration: {avg_duration} min"""
print(message)
```

Prints:
- Top performer based on connect rate
- Total agents active that day
- Average call duration

---

## ✅ Bonus Features

- Added command-line arguments using `argparse`
- Logging messages using `logging` module
- Clean modular structure using functions

---

## ▶️ How to Run the Script (CLI version)

```bash
python agent_summary_script.py --calls call_logs.csv --agents agent_roster.csv --logins disposition_summary.csv --date 2025-04-28 --output summary.csv
```

---

## 📌 Output

- A detailed CSV (`summary.csv`) with performance metrics.
- Console message for top performer and stats.

---

## 🙌 Author

Project by: **THANDRA SRI VARSHA**

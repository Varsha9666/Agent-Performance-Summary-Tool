import pandas as pd
import argparse
import logging

# -------------------------------
# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# -------------------------------
# Load CSV
def load_csv(file_path, name):
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Loaded {name} with shape {df.shape}")
        return df
    except Exception as e:
        logging.error(f"Error loading {name}: {e}")
        exit(1)

# -------------------------------
# Preprocessing and merging
def merge_data(calls, agents, logins):
    calls['call_date'] = pd.to_datetime(calls['call_date'])
    logins['call_date'] = pd.to_datetime(logins['call_date'])
    merged = calls.merge(agents, on=['agent_id', 'org_id'], how='left')                   .merge(logins, on=['agent_id', 'org_id', 'call_date'], how='left')
    return merged

# -------------------------------
# Metric calculation
def compute_metrics(merged):
    grouped = merged.groupby(['agent_id', 'org_id', 'call_date'])

    summary = grouped.agg(
        total_calls=('call_id', 'count'),
        unique_loans=('installment_id', 'nunique'),
        completed_calls=('status', lambda x: (x == 'completed').sum()),
        avg_duration_min=('duration', lambda x: round(x.mean() / 60, 2)),
        presence=('login_time', lambda x: 1 if x.notna().any() else 0)
    ).reset_index()

    summary['connect_rate'] = round(summary['completed_calls'] / summary['total_calls'], 2)
    return summary

# -------------------------------
# Slack-style summary message
def generate_message(df, date_str):
    df = df[df['call_date'] == pd.to_datetime(date_str)]
    if df.empty:
        return f"No data for {date_str}"

    top = df.sort_values(by='connect_rate', ascending=False).iloc[0]
    top_name = top.get('users_first_name', '') + ' ' + top.get('users_last_name', '')
    top_rate = int(top['connect_rate'] * 100)
    total_agents = df['agent_id'].nunique()
    avg_duration = round(df['avg_duration_min'].mean(), 2)

    return f"""**Agent Summary for {date_str}**
🏆 Top Performer: {top_name.strip()} ({top_rate}% connect rate)
👥 Total Active Agents: {total_agents}
⏱️ Average Duration: {avg_duration} min
"""

# -------------------------------
# Main
def main():
    parser = argparse.ArgumentParser(description="Agent Performance Summary CLI")
    parser.add_argument('--calls', required=True, help="Path to call_logs.csv")
    parser.add_argument('--agents', required=True, help="Path to agent_roster.csv")
    parser.add_argument('--logins', required=True, help="Path to disposition_summary.csv")
    parser.add_argument('--date', required=True, help="Reporting date (YYYY-MM-DD)")
    parser.add_argument('--output', default='agent_performance_summary.csv', help="Output CSV file name")

    args = parser.parse_args()

    # Load
    call_logs = load_csv(args.calls, 'call_logs.csv')
    agent_roster = load_csv(args.agents, 'agent_roster.csv')
    disposition = load_csv(args.logins, 'disposition_summary.csv')

    # Process
    merged = merge_data(call_logs, agent_roster, disposition)
    summary = compute_metrics(merged)

    # Add names for display
    summary = summary.merge(agent_roster[['agent_id', 'org_id', 'users_first_name', 'users_last_name']],
                            on=['agent_id', 'org_id'], how='left')

    # Save output
    summary.to_csv(args.output, index=False)
    logging.info(f"Saved summary to {args.output}")

    # Print Slack-style message
    print(generate_message(summary, args.date))

# -------------------------------
if __name__ == '__main__':
    main()

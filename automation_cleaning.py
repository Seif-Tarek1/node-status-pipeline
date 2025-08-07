
import pandas as pd
import requests

Base_URL = 'http://127.0.0.1:8000'
Endpoints = ['nodes', 'latency', 'status']


def clean_save_data(merged_df):
    merged_df = merged_df.dropna(
        subset=['node_id', 'latency_mn', 'status'])

    merged_df = merged_df[merged_df['latency_mn'] >= 0]

    merged_df = merged_df.drop_duplicates(subset='node_id', keep='first')

    merged_df['location'] = merged_df['location'].str.strip().str.lower()

    merged_df['location'] = merged_df['location'].replace(
        {'alex': 'alexandria'})

    merged_df['type'] = merged_df['type'].str.strip().str.lower()
    merged_df['status'] = merged_df['status'].str.strip().str.lower()

    merged_df['last_checked'] = pd.to_datetime(
        merged_df['last_checked'], errors='coerce')

    merged_df.to_csv(path_or_buf="Cleaned Nodes.csv", index=False)


def get_merge_data():
    nodes_json = requests.get(f'{Base_URL}/nodes')
    latency_json = requests.get(f'{Base_URL}/latency')
    status_json = requests.get(f'{Base_URL}/status')
    if (nodes_json.status_code == 200 and latency_json.status_code == 200
            and status_json.status_code == 200):
        print("Data Cleaned Successfully")
    else:
        print(
            f"Error occured. API's Status /n nodes:{nodes_json.status_code}|"
            f"latency:{latency_json.status_code}|"
            f"status:{status_json.status_code}")
    nodes_df = pd.DataFrame(nodes_json.json())
    latency_df = pd.DataFrame(latency_json.json())
    status_df = pd.DataFrame(status_json.json())
    merged_df = pd.merge(nodes_df, latency_df, on='node_id', how='outer')
    merged_df = pd.merge(merged_df, status_df, on='node_id', how='outer')
    return merged_df


def main():
    file = get_merge_data()
    clean_save_data(file)


if __name__ == "__main__":
    main()

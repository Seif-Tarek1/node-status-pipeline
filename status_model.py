import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


def clean_data(df):
    # Drop rows with missing required fields
    df = df.dropna(subset=['status', 'latency_mn', 'type', 'location'])

    # Normalize casing and strip whitespace
    df['status'] = df['status'].str.strip().str.lower()
    df['type'] = df['type'].str.strip().str.lower()
    df['location'] = df['location'].str.strip().str.lower()

    # Only keep known valid categories
    valid_statuses = {'up', 'down', 'degraded'}
    valid_types = {'router', 'switch'}
    df = df[df['status'].isin(valid_statuses)]
    df = df[df['type'].isin(valid_types)]

    return df


def check_EDA(df_copy):
    print("Checking EDAs...")
    print("1. Value counts:")
    print(df_copy['status'].value_counts())
    print(df_copy['type'].value_counts())
    print(df_copy['location'].value_counts())

    print("\n2. Latency distribution:")
    print(df_copy['latency_mn'].describe())

    print("\n3. Correlation:")
    df_copy['status_code'] = df_copy['status'].astype('category').cat.codes
    print(df_copy[['latency_mn', 'status_code']].corr())
    print("====================EDA checks done!====================\n")


def preprocess(df):
    # One-hot encode location and type
    df = pd.get_dummies(df, columns=['location', 'type'], drop_first=True)

    # Normalize latency
    scaler = StandardScaler()
    df['latency_scaled'] = scaler.fit_transform(df[['latency_mn']])

    return df


def predict_status(df):
    # Only use latency_scaled as feature — strongly correlated with status
    X = df[['latency_scaled']]
    y = df['status'].astype('category').cat.codes

    print("Training features:", X.columns.tolist())

    # Split into train and validation
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    model = RandomForestClassifier(random_state=42, n_estimators=100)
    model.fit(X_train, y_train)
    predictions = model.predict(X_val)

    return predictions, y_val




def evaluate(predictions, y_val):
    print("Classification Report:")
    print(classification_report(y_val, predictions))

    acc = accuracy_score(y_val, predictions)
    print(f"Accuracy: {acc:.2f}")


def main():
    df = pd.read_csv("./Cleaned Nodes.csv")
    df = clean_data(df)
    check_EDA(df.copy())
    df = preprocess(df)
    predictions, y_val = predict_status(df)
    evaluate(predictions, y_val)


if __name__ == "__main__":
    main()

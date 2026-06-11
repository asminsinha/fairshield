import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def prepare_biased_dataset():
    # Build direct paths relative to this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    raw_data_path = os.path.join(current_dir, "../../../data/adult.csv")
    output_data_path = os.path.join(current_dir, "../../../data/adult_with_predictions.csv")

    if not os.path.exists(raw_data_path):
        print(f"Error: Could not find raw dataset at {raw_data_path}. Please place adult.csv there.")
        return

    print("Reading dataset...")
    df = pd.read_csv(raw_data_path)

    # 1. Handle missing string values often marked as '?' in the Adult dataset
    df = df.replace('?', pd.NA).dropna()

    # 2. Extract our target and sensitive features
    # Target: income ( >50K or <=50K )
    # Sensitive Attribute: gender (or 'sex' depending on your Kaggle file columns)
    gender_col = 'sex' if 'sex' in df.columns else 'gender'
    
    # Keep track of the unencoded sensitive attribute for human-readable output later
    df['sensitive_attr_raw'] = df[gender_col].str.strip()
    
    # 3. Target Encoding: Convert income string to 0 (<=50K) or 1 (>50K)
    df['ground_truth'] = df['income'].str.strip().apply(lambda x: 1 if '>50K' in x else 0)

    # 4. Preprocess Features for the Machine Learning Model
    # We drop targets and text tracking columns to avoid data leakage
    X_raw = df.drop(columns=['income', 'ground_truth', 'sensitive_attr_raw'])
    y = df['ground_truth']

    # Convert remaining text columns into numbers using Label Encoding
    X_encoded = X_raw.copy()
    label_encoders = {}
    for col in X_encoded.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        X_encoded[col] = le.fit_transform(X_encoded[col].astype(str))

    # Scale numeric values for faster and stable convergence
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_encoded)

    # 5. Train / Test Split (80% Training, 20% Testing)
    X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(
        X_scaled, y, df.index, test_size=0.2, random_state=42
    )

    # 6. Train the Model
    print("Training Logistic Regression Model...")
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)

    # 7. Evaluate Performance
    train_preds = model.predict(X_train)
    test_preds = model.predict(X_test)

    train_acc = accuracy_score(y_train, train_preds)
    test_acc = accuracy_score(y_test, test_preds)

    print(f"\n--- Model Training Metrics ---")
    print(f"Training Accuracy: {train_acc * 100:.2f}%")
    print(f"Testing Accuracy: {test_acc * 100:.2f}%")
    print(f"------------------------------\n")

    # 8. Create a user-friendly audit evaluation CSV file based on the Test Split
    test_data_summary = pd.DataFrame({
        'Gender': df.loc[indices_test, 'sensitive_attr_raw'],
        'Actual_Income_High': y_test,
        'Predicted_Income_High': test_preds
    })

    test_data_summary.to_csv(output_data_path, index=False)
    print(f"Success! Audit-ready file saved to: {output_data_path}")

if __name__ == "__main__":
    prepare_biased_dataset()
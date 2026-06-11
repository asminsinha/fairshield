import pandas as pd
import numpy as np
from fairlearn.metrics import (
    selection_rate,
    true_positive_rate,
    false_positive_rate,
    demographic_parity_difference,
    demographic_parity_ratio,
    equalized_odds_difference
)

def calculate_fairness_metrics(file_path: str, sensitive_col: str, target_col: str, pred_col: str, privileged_value: str):
    """
    Computes standard legal and structural algorithmic fairness metrics using Fairlearn.
    """
    # Load the uploaded file safely
    df = pd.read_csv(file_path)
    
    # Strip whitespaces from column target fields to avoid key errors
    df[sensitive_col] = df[sensitive_col].astype(str).str.strip()
    
    privileged_value = str(privileged_value).strip()
    if not privileged_value or privileged_value == "None" or privileged_value == "":
        privileged_value = str(df[sensitive_col].mode()[0]).strip()

    y_true = df[target_col].astype(int)
    y_pred = df[pred_col].astype(int)
    sensitive_features = df[sensitive_col]

    # 1. Group-level distributions
    unique_groups = sensitive_features.unique()
    group_data = {}

    for group in unique_groups:
        group_mask = (sensitive_features == group)
        y_true_g = y_true[group_mask]
        y_pred_g = y_pred[group_mask]
        
        # Calculate rates per demographic group safely
        sel_rate = float(selection_rate(y_true_g, y_pred_g))
        tpr = float(true_positive_rate(y_true_g, y_pred_g)) if np.sum(y_true_g == 1) > 0 else 0.0
        fpr = float(false_positive_rate(y_true_g, y_pred_g)) if np.sum(y_true_g == 0) > 0 else 0.0
        
        group_data[group] = {
            "sample_size": int(np.sum(group_mask)),
            "selection_rate": round(sel_rate, 4),
            "true_positive_rate": round(tpr, 4),
            "false_positive_rate": round(fpr, 4)
        }

    # 2. Global Fairness Inter-group Metrics
    # Disparate Impact Ratio (Demographic Parity Ratio)
    # Fairlearn computes ratio min(group_rate)/max(group_rate). We map it explicitly relative to the user's privileged group.
    try:
        priv_rate = group_data[privileged_value]["selection_rate"]
        unpriv_rates = [group_data[g]["selection_rate"] for g in unique_groups if g != privileged_value]
        # Avoid Division by Zero if the privileged group received zero positive outcomes
        disparate_impact = round(min(unpriv_rates) / priv_rate, 4) if priv_rate > 0 else 1.0
    except KeyError:
        # Fallback to standard fairlearn ratio if privileged key string mismatches
        disparate_impact = round(float(demographic_parity_ratio(y_true, y_pred, sensitive_features=sensitive_features)), 4)

    stat_parity_diff = round(float(demographic_parity_difference(y_true, y_pred, sensitive_features=sensitive_features)), 4)
    eq_odds_diff = round(float(equalized_odds_difference(y_true, y_pred, sensitive_features=sensitive_features)), 4)

    # 3. Design clear contextual thresholds for the UI response summary
    # Legal standard (US EEOC 4/5ths Rule): Disparate Impact should be >= 0.80
    is_compliant = disparate_impact >= 0.80 and stat_parity_diff <= 0.10

    return {
        "summary": {
            "total_records": len(df),
            "disparate_impact_ratio": disparate_impact,
            "statistical_parity_difference": stat_parity_diff,
            "equalized_odds_difference": eq_odds_diff,
            "is_four_fifths_compliant": bool(is_compliant),
            "auto_privileged_value": privileged_value
        },
        "breakdown": group_data
    }

# Quick local assertion check to verify logic correctness
if __name__ == "__main__":
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sample_file = os.path.join(current_dir, "../../../data/adult_with_predictions.csv")
    
    if os.path.exists(sample_file):
        print("Running internal validation test on metrics calculation engine...")
        results = calculate_fairness_metrics(
            file_path=sample_file,
            sensitive_col="Gender",
            target_col="Actual_Income_High",
            pred_col="Predicted_Income_High",
            privileged_value="Male"
        )
        import json
        print(json.dumps(results, indent=4))
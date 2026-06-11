import os
from huggingface_hub import InferenceClient

def generate_local_fallback_report(metrics_json: dict, sensitive_col: str, privileged_group: str) -> str:
    """
    Dynamically generates a professional, enterprise-grade audit report 
    without emojis, using clean engineering terms and polished phrasing.
    """
    summary = metrics_json["summary"]
    breakdown = metrics_json["breakdown"]
    
    di_ratio = summary["disparate_impact_ratio"]
    sp_diff = summary["statistical_parity_difference"]
    eq_odds = summary["equalized_odds_difference"]
    
    all_groups = list(breakdown.keys())
    unprivileged_groups = [g for g in all_groups if g != privileged_group]
    unprivileged_str = ", ".join([f"'{g}'" for g in unprivileged_groups]) or "the comparison cohorts"

    if summary["is_four_fifths_compliant"]:
        status = "LAWFUL / COMPLIANT"
        risk_tier = "LOW RISK"
        compliance_phrasing = "successfully satisfy international algorithmic parity criteria with no actionable signs of adverse impact."
        di_phrasing = f"This value meets or exceeds the universal 80.00% parity threshold benchmark, indicating equitable group treatment."
        impact_phrasing = "The system demonstrates negligible regulatory vulnerability. The risk of disparate impact liabilities or compliance penalties is low under current technological governance frameworks."
        recommendation = "PASS / ROLLOUT APPROVED. The model version is cleared for production environment integration."
    else:
        status = "FAILED / NON-COMPLIANT"
        risk_tier = "CRITICAL / HIGH RISK"
        compliance_phrasing = "fail to meet standardized international algorithmic parity criteria, exhibiting systemic selection rate disparities."
        di_phrasing = f"This falls below the acceptable 80.00% international parity threshold marker, establishing a prima facie case of adverse disparate impact."
        impact_phrasing = "Deploying this model version exposes the organization to severe civil liabilities, regulatory non-compliance penalties, and algorithmic discrimination claims under modern fair-practice frameworks."
        recommendation = "REJECT / DEPLOYMENT HALTED. Do not route production traffic to this model until debiasing mitigations push the Disparate Impact Ratio above 0.80."

    report = (
        f"FAIRSHIELD GRC GOVERNANCE COMPLIANCE REPORT\n"
        f"Generated via Universal Parity Evaluation Engine\n"
        f"--------------------------------------------------\n\n"
        f"1. EXECUTIVE SUMMARY\n"
        f"Compliance Status: {status}\n"
        f"Audited Feature Column: {sensitive_col}\n"
        f"Privileged Reference Baseline: {privileged_group}\n"
        f"Unprivileged Target Groups Analyzed: {unprivileged_str}\n"
        f"Algorithmic Parity Adherence: The evaluated predictive model displays structural selection rate properties that {compliance_phrasing}\n\n"
        f"2. CORE BIAS BREAKDOWN\n"
        f"Disparate Impact Ratio: {di_ratio}\n"
        f"The selection rate of the protected unprivileged cohorts is exactly {round(di_ratio * 100, 2)}% of the reference group's baseline selection rate. {di_phrasing}\n\n"
        f"Statistical Parity Difference: {sp_diff}\n"
        f"An absolute selection variance of {round(sp_diff * 100, 2)}% exists between the evaluated sub-populations when mapped against the target classification objective.\n\n"
        f"Equalized Odds Variance: {eq_odds}\n"
        f"The model's error rate profiles vary by {round(eq_odds * 100, 2)}% across these demographic boundaries, pointing to an asymmetric distribution of false positives or false negatives.\n\n"
        f"3. LEGAL & CORPORATE RISK ASSESSMENT\n"
        f"Risk Classification: {risk_tier}\n"
        f"Contextual Impact: {impact_phrasing}\n\n"
        f"4. ACTIONABLE MITIGATION STEPS\n"
        f"To realign this model with international technological equity guidelines, apply the following industry standard mitigations:\n"
        f"A. Pre-processing (Re-weighing): Compute statistical weight vectors for the training samples across the '{sensitive_col}' spectrum to eliminate group correlation imbalances prior to optimization.\n"
        f"B. In-processing (Fairness Constraints): Integrate mathematical fairness loss penalties during model optimization routines to actively suppress data leakage regarding protected traits.\n"
        f"C. Post-processing (Threshold Optimization): Adjust individual classification confidence cutoffs independently near the decision boundary to maximize parity index values while preserving model utility.\n\n"
        f"PRODUCTION ROLLOUT RECOMMENDATION\n"
        f"{recommendation}"
    )
    return report

def generate_compliance_report(metrics_json: dict, sensitive_col: str, privileged_group: str) -> str:
    """
    Attempts to stream an abstract analysis via the Hugging Face API inference client, 
    smoothly dropping back to our fully localized dynamic metric reporter on network exception.
    """
    hf_token = os.getenv("HF_TOKEN")
    
    if not hf_token:
        return generate_local_fallback_report(metrics_json, sensitive_col, privileged_group)

    try:
        client = InferenceClient(
            model="Qwen/Qwen2.5-7B-Instruct",
            token=hf_token,
            timeout=8
        )

        system_prompt = (
            "You are FairShield, an expert AI Governance, Risk, and Compliance (GRC) Auditor. "
            "Write a highly professional, clinical markdown compliance audit report based on the provided JSON data. "
            "Structure it strictly into: 1. EXECUTIVE SUMMARY, 2. CORE BIAS BREAKDOWN, 3. RISK ASSESSMENT, 4. MITIGATION STEPS. "
            "Never use generic examples. Discuss the specific columns and metrics from the user's data input."
        )

        user_content = f"Calculated JSON Metrics: {metrics_json}. Column audited: {sensitive_col}. Base Reference Group: {privileged_group}."

        response = client.text_generation(
            prompt=f"<|system|>\n{system_prompt}\n<|user|>\n{user_content}\n<|assistant|>\n",
            max_new_tokens=1024,
            temperature=0.2,
            top_p=0.9
        )
        return response

    except Exception as e:
        print(f"Server network routing bottleneck fallback triggered: {str(e)}")
        return generate_local_fallback_report(metrics_json, sensitive_col, privileged_group)
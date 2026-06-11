import os
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import pandas as pd

# Import our modular internal brain pieces
from app.core.metrics import calculate_fairness_metrics
from app.core.report import generate_compliance_report

# Load environment configuration tokens
load_dotenv()

app = FastAPI(
    title="FairShield API",
    description="Automated AI Model Bias & Fairness Governance Auditor Engine",
    version="1.0.0"
)

# Enable CORS so your Vercel React frontend can talk to your Hugging Face API securely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, you can replace with your actual Vercel domain URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"status": "online", "service": "FairShield Compliance Auditor Core"}


@app.post("/api/v1/inspect")
async def inspect_csv_columns(file: UploadFile = File(...)):
    """
    Reads an uploaded CSV file instantly and returns its column headers 
    and unique row values to populate frontend dropdown menus.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file type.")
        
    try:
        # Read only the first few rows to make processing lightning-fast
        df = pd.read_csv(file.file, nrows=5)
        columns = [str(col).strip() for col in df.columns]
        return {"success": True, "columns": columns}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read file layout: {str(e)}")


@app.post("/api/v1/audit")
async def perform_bias_audit(
    file: UploadFile = File(...),
    sensitive_column: str = Form(...),
    target_column: str = Form(...),
    prediction_column: str = Form(...),
    privileged_value: Optional[str] = Form(None)  # Safe optional validation tracking rule
):
    """
    Accepts an audit dataset CSV file and configurations, calculates underlying bias 
    metrics, and attaches a universal narrative compliance report. Handles auto-detection
    fallbacks elegantly if the privileged baseline group is submitted blank.
    """
    # 1. Validate that the uploaded file is indeed a CSV
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a standard CSV file.")

    # 2. Save the uploaded file temporarily to process it
    temp_file_path = f"temp_{file.filename}"
    try:
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # 3. Compute mathematical fairness calculations via Fairlearn engine
        # Pass the raw string or None value safely into the metrics calculator
        metrics_results = calculate_fairness_metrics(
            file_path=temp_file_path,
            sensitive_col=sensitive_column,
            target_col=target_column,
            pred_col=prediction_column,
            privileged_value=privileged_value
        )

        # 4. Extract the actual reference group value used (handles manual input or auto-detection fallback)
        resolved_privileged_group = metrics_results["summary"]["auto_privileged_value"]

        # 5. Generate clean executive compliance insights using the resolved baseline string
        compliance_text_report = generate_compliance_report(
            metrics_json=metrics_results,
            sensitive_col=sensitive_column,
            privileged_group=resolved_privileged_group
        )

        # 6. Pack everything neatly to return to the UI dashboard
        return {
            "success": True,
            "metrics": metrics_results,
            "report": compliance_text_report
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Auditing Pipeline Error: {str(e)}")
        
    finally:
        # Cleanup temporary saved asset to keep server environment clean
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
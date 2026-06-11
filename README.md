# FairShield
### Automated AI Model Bias & Algorithmic Fairness Governance Auditor Engine

[![FastAPI Backend](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React Frontend](https://img.shields.io/badge/Frontend-React%2018-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev/)
[![Dockerized Deployment](https://img.shields.io/badge/Space-Hugging%20Face%20Docker-FFD21E?style=flat-square&logo=huggingface&logoColor=black)](https://huggingface.co/spaces)
[![Interface Deployment](https://img.shields.io/badge/Hosting-Vercel-000000?style=flat-square&logo=vercel&logoColor=white)](https://vercel.com/)

FairShield Core is an automated, end-to-end algorithmic risk assessment and Governance, Risk, and Compliance (GRC) framework. It evaluates predictive models against structured systemic bias by exposing mathematical disparities across protected demographic cohorts. Powered by the Fairlearn metric mapping matrix and localized Llama-3 LLM narrative layers, FairShield processes evaluation payloads instantly to render structural scorecards and plain-English regulatory audits.

---

##  Table of Contents

1. [Executive Summary (Layman Level)](#-executive-summary-layman-level)
2. [Core Features](#-core-features)
3. [System Architecture & Technicalities](#️-system-architecture--technicalities)
4. [Algorithmic Performance & Reference Benchmarks](#-algorithmic-performance--reference-benchmarks)
5. [Input Data Specifications & Schema Format](#-input-data-specifications--schema-format)
6. [Interpreting Audit Metrics & Reports](#-interpreting-audit-metrics--reports)
7. [Real-World Use Cases](#-real-world-use-cases)
8. [Repository Installation & Setup](#-repository-installation--setup)
9. [Step-by-Step App Usage Guide](#-step-by-step-app-usage-guide)

---

##  Executive Summary (Layman Level)

When companies build AI models to screen resumes, issue bank loans, or approve housing, the AI learns from historical data. If that history contains human prejudice, the AI quietly digitizes and magnifies that bias—unfairly rejecting qualified candidates based on race, gender, age, or socioeconomic factors.

**FairShield Core acts as an automated digital judge for AI software.** You simply drop in a table of your model's past decisions. The system immediately scans the data, automatically matches group distributions, and flags whether your AI is practicing unlawful discrimination. It translates cold mathematical ratios into an executive text brief explaining *where* the model is failing and *how* software developers can re-engineer it to ensure fair, ethical, and lawful operations.

---

##  Core Features

- **Lightning-Fast Structural Schema Inspection:** Instantly sniffs uploaded CSV data headers within milliseconds using memory-optimized chunk parsing to auto-populate frontend selection layers.
- **Dynamic Baseline Group Inference:** If a user is unsure which population segment acts as the historical reference, the backend automatically infers the largest cohort population safely as the benchmark baseline.
- **Universal Algorithmic Parity Enforcement:** Evaluates disparate impact metrics using the strict **Four-Fifths (80%) Rule**, making the audit engine globally viable across multiple international regulatory environments.
- **GRC Text Generation Interface:** Integrates modular narrative engines that dynamically construct legal risk summaries, operational threat levels, and compliance rulings.
- **Interactive Analytics Dashboard:** Renders clean, tabular statistical breakdowns tracking True Positive Rate (TPR) and False Positive Rate (FPR) deltas to isolate underlying model error profiling.

---

##  System Architecture & Technicalities

FairShield Core leverages a detached, microservices-style architectural matrix built to run smoothly in serverless or containerized edge cloud nodes:

### Frontend User Interface
A decoupled React client styled using a low-latency Tailwind CSS dark-mode dashboard framework. Network operations stream multi-part boundary payloads asynchronously to standard REST API nodes.

### Backend Auditing Core
A high-throughput FastAPI engine running Python 3.9. It exposes high-speed processing routes that handle temporary system buffers safely with auto-cleaning context hooks.

### Mathematical Processing Matrix
Implements the `fairlearn` metric framing engine and `scikit-learn` diagnostic matrix arrays to evaluate selection parity across segmented slicing indices.

---

##  Algorithmic Performance & Reference Benchmarks

### 1. Underlying Training Data

The engine is engineered to ingest evaluation inference logs extracted from classification systems trained on benchmark bias telemetry datasets, including:

- **UCI Adult Census Income Dataset:** Measuring model classification skews regarding financial income generation divided across sex and ethnicity attributes.
- **COMPAS Recidivism Risk Log Matrices:** Calibrating system threshold drops for false-positive assignment differentials.

### 2. Analytical Precision

Because FairShield acts as an *auditor* rather than a training classifier, its accuracy is mathematically exact (**100% analytical alignment**). It does not guess or predict metrics; it computes the objective ground truth of mathematical distribution curves directly from the dataset payload submitted.

---

##  Input Data Specifications & Schema Format

To process an assessment, the system requires a standard comma-separated tabular `.csv` asset containing historical target records and corresponding evaluation inferences.

### Standard Accepted Schema Requirements

1. **Sensitive Attribute Column:** Categorical text strings or integers classifying the demographic boundary (e.g., `Gender`, `Race`, `Age_Group`).
2. **Ground Truth Column:** Binary markers (`1` for positive favorable result, `0` for unfavorable result) tracking what *actually* occurred historically (e.g., `Hired`, `Approved`).
3. **Prediction Column:** Binary markers (`1` or `0`) indicating what the AI model *selected* or predicted would occur (e.g., `Model_Selection`).

### Example CSV Data Matrix

```csv
Gender,Historical_Hired,AI_Model_Prediction
Female,1,1
Male,0,0
Non-Binary,1,0
Female,0,1
Male,1,1
```

---

##  Interpreting Audit Metrics & Reports

When an audit executes, the system measures data against strict mathematical guardrails:

| Metric | Code Label | Target Threshold | Legal Interpretation |
|----------|----------|----------|----------|
| Disparate Impact Ratio | `disparate_impact_ratio` | ≥ 0.80 | Measures selection rates. Below 0.80 implies actionable systemic bias under adverse impact legal frameworks. |
| Statistical Parity Delta | `statistical_parity_difference` | → 0.00 | Tracks macro probability selection gaps. A value of 0.00 implies complete demographic neutrality. |
| True Positive Rate (TPR) | `true_positive_rate` | Equal Across Cohorts | Measures opportunity parity. High variance means the AI retains higher accuracy for one group over another. |

---

##  Real-World Use Cases

### Enterprise Human Resource Audits
Pre-screening automated talent tracking systems (ATS) before live deployment to mitigate employment selection liability.

### FinTech Credit Assessment Verification
Validating automated credit underwriting algorithms to eliminate structural bias against historically protected zip codes or demographic segments.

### Healthcare Diagnostic Equity Assessments
Assessing medical triaging algorithms to guarantee predictive true positive classification accuracy remains stable across all patient demographics.

---

##  Repository Installation & Setup

Ensure your local machine has Python 3.9+ and Node.js (v18+) installed.

### 1. Clone the Central Repository

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/fairshield-core.git
cd fairshield-core
```

### 2. Local Backend Configuration

```bash
# Navigate to the backend environment root
cd backend

# Initialize your local Python isolation layer
python -m venv venv

# Activate the environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# On macOS/Linux use:
# source venv/bin/activate

# Install automated dependencies
pip install -r requirements.txt

# Fire up the development environment live server
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### 3. Local Frontend Workspace Launch

```bash
# Open a new terminal window at the repository root folder
cd frontend

# Install node module bundle packages
npm install

# Boot up the local Vite engine interface dashboard
npm run dev
```

---

##  Step-by-Step App Usage Guide

### Using the Cloud Interface Dashboard

#### 1. Access the Platform
Open your live production frontend link running via Vercel.

#### 2. Load Your Target Data
Click the **Select Dataset (.CSV)** input zone and upload your structural evaluation spreadsheet file.

#### 3. Automatic Mapping Verification
The backend will instantaneously analyze your layout schema. You will see your configuration parameter fields populate instantly with your dataset's text headings.

#### 4. Set the Privilege Frame (Optional)
Inside the **Privileged Group Reference** field, type the precise text string of the group you want to treat as the baseline (e.g., `White` or `Male`).

If left blank, the backend automatically infers the majority group cohort for safety.

#### 5. Trigger the Engine Execution
Click the **Execute Compliance Audit** button.

#### 6. Review the Governance Output

##### Scorecards
Instantly review your Disparate Impact Ratio color coding status blocks.

##### Distribution Splitting Table
Inspect sample cohort sizing and selection rate analytics.

##### AI GRC Report
Read through the plain-English generative audit explaining legal compliance status and remediation instructions.

---

##  Developer

Developed and maintained by **Asmin Sinha**.

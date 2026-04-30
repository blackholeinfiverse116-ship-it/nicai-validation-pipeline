# 🚀 NICAI – SVACS Acoustic Intelligence Pipeline

---

## 📌 Overview

NICAI is a **deterministic validation and intelligence pipeline** designed to process **SVACS acoustic perception events**, validate them using existing NICAI logic, and generate structured intelligence outputs for downstream systems.

This system strictly follows: 

- ✔ No ML / AI models
- ✔ No probabilistic logic
- ✔ Reuse of NICAI validation
- ✔ Fully traceable via `trace_id`
- ✔ Real-time pipeline ready

---

## ⚠️ System Constraints (STRICT)

- ❌ NICAI NOT rebuilt
- ❌ Schemas NOT redesigned
- ❌ NO ML / probabilistic logic
- ❌ NO pipeline blocking
- ✅ Deterministic execution only
- ✅ Invalid events are logged (no silent failure)
- ✅ Flow continues using ALLOW / FLAG

---

## 🧠 End-to-End Flow

```text
Perception Event
      ↓
NICAI Signal Mapping
      ↓
NICAI Validation (ALLOW / FLAG)
      ↓
Sanskar Intelligence
      ↓
State Engine
      ↓
Bucket Logging + Telemetry
```

---

## 📥 Input: Perception Event (LIVE)

```json
{
  "trace_id": "T1",
  "vessel_type": "cargo",
  "confidence_score": 0.8,
  "dominant_freq_hz": 120,
  "anomaly_flag": false
}
```

### 🔴 Important Rules

- Existing `trace_id` is reused
- Input structure is NOT modified

---

## 🔄 Module Breakdown

### 1️⃣ NICAI Signal Mapping (Live Integration)

Perception event is mapped directly to NICAI signal:

```json
{
  "trace_id": "T1",
  "signal_id": "T1",
  "timestamp": "LIVE",
  "value": 0.8,
  "asset_id": "cargo",
  "feature_type": "acoustic",
  "dataset_id": "svacs",
  "signal_type": "acoustic_detection",
  "source": "svacs",
  "metadata": {
    "dominant_freq_hz": 120,
    "anomaly_flag": false
  }
}
```

---

### 2️⃣ NICAI Validation (`validator.py`)

Validates:

- Required fields present
- Schema integrity
- confidence_score ∈ [0,1]
- Dataset validity

### Output Format:

```json
{
  "signal_id": "T1",
  "status": "ALLOW",
  "confidence_score": 0.8,
  "trace_id": "T1",
  "reason": "Valid signal"
}
```

### ✅ Behavior

- Status: `ALLOW` or `FLAG`
- ❌ No pipeline stop
- ✔ Invalid cases are logged but flow continues

---

### 3️⃣ Sanskar Intelligence (`sanskar_simple.py`)

Deterministic rule-based logic:

#### 🎯 Risk Mapping

| Confidence | Risk Level |
|------------|-----------|
| ≥ 0.75     | LOW       |
| 0.5–0.75   | MEDIUM    |
| 0.3–0.5    | HIGH      |
| < 0.3      | CRITICAL  |

---

#### 🚨 Anomaly Rules

- `vessel_type == "unknown"` → anomaly = TRUE  
- `metadata.anomaly_flag == true` → anomaly = TRUE  

✔ If anomaly = TRUE → risk overridden to **CRITICAL**

---

### Output: `intelligence_event`

```json
{
  "trace_id": "T1",
  "vessel_type": "cargo",
  "confidence": 0.8,
  "risk_level": "LOW",
  "anomaly_flag": false,
  "explanation": "High confidence acoustic classification of cargo vessel — low risk"
}
```

✔ Explanation is mandatory and human-readable

---

### 4️⃣ State Engine Output

- Direct forwarding of `intelligence_event`
- No transformation
- No delay

---

## 🪣 Bucket Logging (MANDATORY)

Logs ALL stages:

- Input signal
- Validation output
- Intelligence output
- trace_id
- timestamp
- processing stage

### Log Format:

```json
{
  "trace_id": "...",
  "input": {...},
  "output": {...},
  "timestamp": "...",
  "stage": "validation / intelligence"
}
```

---

## 📊 Telemetry (InsightFlow)

Emits:

- validation status
- risk_level
- pipeline activity

✔ Passive system (no decision logic)

---

## 🧪 Test Coverage

### ✔ Valid Cases

- High confidence → LOW risk
- Medium confidence → MEDIUM risk
- Low confidence → HIGH risk

### 🚨 Edge Cases

- Unknown vessel → CRITICAL + anomaly
- Very low confidence → CRITICAL
- anomaly_flag = TRUE → CRITICAL override

### ⚠️ Invalid Cases

- Missing fields
- Invalid schema

✔ Logged but pipeline continues

---

## 📂 Project Structure

```text
nicai_validation_layer/
│
├── validator.py
├── sanskar_simple.py
├── live_pipeline.py
├── schemas.py
├── dataset_registry.py
├── utils.py
├── bucket_emitter.py
├── telemetry_emitter.py
├── test_pipeline.py
├── test_svacs_flow.py
├── bucket_artifacts.jsonl
├── telemetry_metrics.json
└── README.md
```

---

## 🚀 How to Run

### Run live pipeline:

```bash
python live_pipeline.py
```

### Run test cases:

```bash
python test_pipeline.py
python test_svacs_flow.py
```

---

## 🔁 Traceability

- Same `trace_id` preserved across:
  - input
  - validation
  - intelligence
  - output
  - logging

---

## 🧠 Design Principles

- ✔ Deterministic execution
- ✔ No ML / AI dependency
- ✔ Real-time pipeline design
- ✔ Modular architecture
- ✔ Stateless validation
- ✔ Full traceability

---

## 📡 Output Targets

- State Engine
- Bucket Logging System
- Telemetry System

---

## ✅ Success Criteria (Achieved)

- ✔ perception_event accepted and processed
- ✔ validation applied correctly
- ✔ intelligence_event generated
- ✔ risk mapping correct
- ✔ anomaly detection working
- ✔ explanation generated
- ✔ trace_id preserved end-to-end
- ✔ no pipeline blocking
- ✔ no silent failures

---

## 📌 Final Status

🚀 **SYSTEM STATUS: COMPLETE + LIVE INTEGRATED + DEMO READY**

---

## 👨‍💻 System Note

This project demonstrates:

- Event-driven pipeline design
- Deterministic intelligence generation
- Real-time processing architecture
- Explainable and traceable outputs

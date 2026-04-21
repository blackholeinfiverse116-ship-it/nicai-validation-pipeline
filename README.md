# NICAI – SVACS Acoustic Intelligence Pipeline

## 📌 Overview

NICAI is a lightweight validation and intelligence pipeline designed to process **SVACS acoustic perception events**, validate them, and generate structured intelligence outputs for downstream systems like the State Engine.

This project demonstrates a simplified real-time pipeline:

```
SVACS Event → Adapter → NICAI Validation → Sanskar Intelligence → State Engine → Bucket Logs
```

---

## ⚙️ System Flow

### 1. SVACS Input Event
Raw input format:
```json
{
  "event_id": "E1",
  "timestamp": "2026-04-20T10:00:00",
  "vessel": {
    "type": "cargo",
    "confidence_score": 0.8
  },
  "metadata": {}
}
```

---

### 2. Adapter Layer (`svacs_adapter.py`)
Converts SVACS event → NICAI signal format:

Output:
```json
{
  "signal_id": "E1",
  "timestamp": "...",
  "asset_id": "cargo",
  "value": 0.8,
  "signal_type": "acoustic_detection",
  "source": "svacs"
}
```

---

### 3. NICAI Validation (`validator.py`)

Validates:
- Required fields present
- Confidence in range [0,1]
- Schema correctness

Output:
```json
{
  "signal_id": "E1",
  "status": "VALID",
  "confidence_score": 0.8,
  "reason": "Valid acoustic signal"
}
```

---

### 4. Sanskar Intelligence (`sanskar_simple.py`)

Rule-based deterministic logic:

#### Risk Levels:
- confidence ≥ 0.75 → LOW
- 0.5 – 0.75 → MEDIUM
- 0.3 – 0.5 → HIGH
- < 0.3 or unknown → CRITICAL

#### Anomaly Rules:
- vessel.type == "unknown" → anomaly = True

Output:
```json
{
  "trace_id": "...",
  "vessel_type": "cargo",
  "confidence": 0.8,
  "risk_level": "LOW",
  "anomaly_flag": false,
  "explanation": "High confidence acoustic classification"
}
```

---

### 5. State Engine Output

Final structured intelligence event sent downstream:

```json
{
  "trace_id": "...",
  "vessel_type": "cargo",
  "risk_level": "LOW",
  "confidence": 0.8,
  "anomaly_flag": false
}
```

---

## 📂 Project Structure

```
nicai_validation_layer/
│
├── svacs_adapter.py
├── validator.py
├── sanskar_simple.py
├── pipeline.py
├── test_pipeline.py
├── test_svacs_flow.py
├── bucket_emitter.py
├── telemetry_emitter.py
└── README.md
```

---

## 🚀 How to Run

### 1. Run main pipeline test
```bash
python test_pipeline.py
```

### 2. Run SVACS flow test
```bash
python test_svacs_flow.py
```

---

## 🧪 Test Cases Covered

- ✅ Valid event (cargo vessel, high confidence)
- ❌ Invalid schema event
- ⚠️ Low confidence signal
- 🚨 Unknown vessel detection
- 📉 Risk level classification (LOW → CRITICAL)

---

## 📊 Logging

All events are logged into bucket system:

Logged data includes:
- trace_id
- input signal
- validation output
- intelligence output
- timestamp
- layer (NICAI / SANSKAR)

---

## 🔗 Key Design Principles

- ❌ No ML / AI models
- ❌ No probabilistic logic
- ✅ Fully deterministic rules
- ✅ Traceability via trace_id
- ✅ Modular pipeline design
- ✅ Plug-and-play architecture

---

## 🧠 Intelligence Logic Summary

| Confidence | Risk Level |
|------------|------------|
| ≥ 0.75     | LOW        |
| 0.5–0.75   | MEDIUM     |
| 0.3–0.5    | HIGH       |
| < 0.3      | CRITICAL   |

---

## 📡 Output Targets

- State Engine (Raj module)
- Bucket Logging System
- Telemetry (Pravah / InsightFlow)

---

## 👨‍💻 Author System

NICAI + Sanskar Integrated Intelligence Layer  
SVACS Acoustic Processing Pipeline

---

## ✅ Status

✔ Validation Layer Working  
✔ Intelligence Layer Working  
✔ Traceable Pipeline Active  
✔ State Engine Integration Ready  

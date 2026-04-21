# 🧾 NICAI – SVACS Pipeline Review Packet

## 📌 Project Name
**NICAI + Sanskar Integrated Intelligence Layer for SVACS Acoustic Signals**

---

## 🎯 Objective

To build a deterministic, traceable pipeline that:

- Accepts SVACS perception events
- Converts them into NICAI-compatible signals
- Validates data integrity
- Generates rule-based intelligence (Sanskar layer)
- Sends structured output to State Engine
- Logs everything into Bucket system

---

## 🧠 System Architecture

```
SVACS Perception Event
        ↓
SVACS Adapter
        ↓
NICAI Validation Layer
        ↓
Sanskar Intelligence Engine
        ↓
State Engine (Downstream)
        ↓
Bucket + Telemetry Logs
```

---

## ⚙️ Modules Overview

### 1. SVACS Adapter
**File:** `svacs_adapter.py`

- Converts raw perception_event → NICAI signal format
- Maps fields:
  - vessel.type → asset_id
  - confidence_score → value
  - source → "svacs"

---

### 2. NICAI Validator
**File:** `validator.py`

Validations performed:
- Required fields check
- Confidence score range [0, 1]
- Schema integrity

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

### 3. Sanskar Intelligence Layer
**File:** `sanskar_simple.py`

#### Deterministic Risk Logic:

| Confidence Range | Risk Level |
|------------------|------------|
| ≥ 0.75           | LOW        |
| 0.5 – 0.75       | MEDIUM     |
| 0.3 – 0.5        | HIGH       |
| < 0.3            | CRITICAL   |

#### Anomaly Rules:
- vessel.type == "unknown" → anomaly = TRUE
- inconsistent metadata → anomaly = TRUE

#### Output:
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

### 4. State Engine Output

Final structured event sent downstream:

```json
{
  "trace_id": "...",
  "vessel_type": "cargo",
  "confidence": 0.8,
  "risk_level": "LOW",
  "anomaly_flag": false
}
```

---

### 5. Bucket Logging System

Logs every stage:

- Input signal
- Validation result
- Intelligence output
- Timestamp
- Trace ID
- Processing layer

---

## 🧪 Test Coverage

### ✔ Valid Cases
- High confidence cargo vessel
- Medium confidence detection
- Low confidence detection

### ❌ Invalid Cases
- Missing fields
- Invalid schema
- Out-of-range confidence

### 🚨 Edge Cases
- Unknown vessel type
- Extremely low confidence (< 0.3)
- Metadata inconsistency

---

## 📊 Example Execution Flow

```
Event → Adapter → Validator → Sanskar → State Engine
```

Example output:

```
Signal E1 → VALID → LOW RISK → Sent to State Engine
Signal E4 → VALID → CRITICAL → Sent to State Engine
Signal E5 → VALID → UNKNOWN + ANOMALY → CRITICAL ALERT
```

---

## 🔗 Dependencies

- Python 3.10+
- No external ML libraries required
- Fully deterministic rule-based system

---

## 🚀 How to Run

```bash
python test_pipeline.py
python test_svacs_flow.py
```

---

## 📁 Repository Structure

```
nicai_validation_layer/
├── svacs_adapter.py
├── validator.py
├── sanskar_simple.py
├── pipeline.py
├── test_pipeline.py
├── test_svacs_flow.py
├── bucket_emitter.py
├── telemetry_emitter.py
├── README.md
└── REVIEW_PACKET.md
```

---

## 🧠 Key Design Principles

- ✔ Deterministic logic only
- ✔ No ML / AI models used
- ✔ Full traceability via trace_id
- ✔ Modular architecture
- ✔ Stateless validation + intelligence layers
- ✔ Real-time pipeline ready

---

## 📡 Output Targets

- State Engine (Downstream system)
- Bucket Logging System
- Telemetry / InsightFlow

---

## 📌 Status

✔ Adapter Layer Complete  
✔ Validation Layer Stable  
✔ Intelligence Layer Working  
✔ End-to-End Pipeline Functional  
✔ Demo Ready System  

---

## 👨‍💻 System Owner Note

This system is designed for:
- Rapid prototyping
- Event-driven pipelines
- Maritime acoustic intelligence simulation

---

## ✅ FINAL STATUS

🚀 NICAI Pipeline: **READY FOR DEMO + SUBMISSION**

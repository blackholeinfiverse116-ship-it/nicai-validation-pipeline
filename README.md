# 🚀 NICAI – SVACS Acoustic Intelligence Pipeline

---

## 📌 Overview

NICAI is a **deterministic validation and intelligence pipeline** designed to process **SVACS acoustic perception events**, validate them using existing NICAI logic, and generate structured intelligence outputs for downstream systems.

This system strictly follows: 

* ✔ No ML / AI models
* ✔ No probabilistic logic
* ✔ Reuse of NICAI validation
* ✔ Fully traceable via `trace_id`
* ✔ Real-time pipeline ready

---

## ⚠️ System Constraints (STRICT)

* ❌ NICAI NOT rebuilt
* ❌ Schemas NOT redesigned
* ❌ NO ML / probabilistic logic
* ❌ Invalid events MUST NOT pass forward
* ✅ Deterministic execution only

---

## 🧠 End-to-End Flow

```text
SVACS Perception Event
        ↓
SVACS Adapter (Input Mapping)
        ↓
NICAI Validation Layer (Reuse)
        ↓
Sanskar Simplified Intelligence
        ↓
State Engine (Raj)
        ↓
Bucket Logging + Telemetry (InsightFlow)
```

---

## 📥 Input: SVACS Perception Event

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

## 🔄 Module Breakdown

### 1️⃣ SVACS Adapter (`svacs_adapter.py`)

Converts `perception_event → NICAI signal`

### Field Mapping:

| SVACS Field      | NICAI Field          |
| ---------------- | -------------------- |
| vessel.type      | asset_id             |
| confidence_score | value                |
| timestamp        | timestamp            |
| source           | "svacs"              |
| signal_type      | "acoustic_detection" |
| feature_type     | "acoustic"           |

### Output:

```json
{
  "signal_id": "E1",
  "timestamp": "...",
  "value": 0.8,
  "asset_id": "cargo",
  "signal_type": "acoustic_detection",
  "feature_type": "acoustic",
  "dataset_id": "svacs",
  "source": "svacs"
}
```

---

### 2️⃣ NICAI Validation (`validator.py`)

Validates:

* Required fields present
* Schema integrity
* confidence_score ∈ [0,1]
* Dataset validity

### Output Format:

```json
{
  "signal_id": "E1",
  "status": "ALLOW",
  "confidence_score": 0.8,
  "trace_id": "...",
  "reason": "Valid signal"
}
```

### 🔴 Critical Rule:

* If `status = REJECT` → ❌ STOP PIPELINE
* MUST NOT pass to Sanskar

---

### 3️⃣ Sanskar Intelligence (`sanskar_simple.py`)

Deterministic rule-based logic:

#### Risk Mapping:

| Confidence | Risk Level |
| ---------- | ---------- |
| ≥ 0.75     | LOW        |
| 0.5–0.75   | MEDIUM     |
| 0.3–0.5    | HIGH       |
| < 0.3      | CRITICAL   |

---

#### Anomaly Rules:

* vessel_type == `"unknown"` → anomaly = TRUE
* upstream inconsistency → anomaly = TRUE

---

### Output: `intelligence_event`

```json
{
  "trace_id": "...",
  "vessel_type": "cargo",
  "confidence": 0.8,
  "risk_level": "LOW",
  "anomaly_flag": false,
  "explanation": "High confidence acoustic classification — low risk"
}
```

✔ Explanation is human-readable (MANDATORY)

---

### 4️⃣ State Engine Output

* Sends `intelligence_event` directly
* No transformation
* No delay

---

## 🪣 Bucket Logging (MANDATORY)

Logs ALL stages:

* Valid events
* Invalid events
* Intelligence outputs

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

* validation_result
* risk_level
* latency

✔ Passive only (no decision logic)

---

## 🧪 Test Coverage

### ✔ Valid Cases

* High confidence vessel → LOW risk
* Medium confidence → MEDIUM risk
* Low confidence → HIGH risk

### ❌ Invalid Cases

* Missing required fields
* Invalid schema
* Out-of-range confidence

### 🚨 Edge Cases

* Unknown vessel → CRITICAL + anomaly_flag = TRUE
* Very low confidence (<0.3)

---

## 📂 Project Structure

```text
nicai_validation_layer/
│
├── svacs_adapter.py
├── validator.py
├── sanskar_simple.py
├── pipeline.py
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

### Run full pipeline:

```bash
python test_pipeline.py
```

### Run SVACS flow test:

```bash
python test_svacs_flow.py
```

---

## 🔁 Traceability

* `trace_id` generated at adapter stage
* Preserved across:

  * validation
  * intelligence
  * output
  * logging

---

## 🧠 Design Principles

* ✔ Deterministic execution
* ✔ No ML / AI dependency
* ✔ Modular architecture
* ✔ Stateless validation
* ✔ Real-time ready

---

## 📡 Output Targets

* State Engine (Raj module)
* Bucket Logging System
* InsightFlow Telemetry

---

## ✅ Success Criteria (Achieved)

* ✔ perception_event accepted and processed
* ✔ invalid inputs rejected and stopped
* ✔ correct risk_level generation
* ✔ anomaly detection working
* ✔ trace_id preserved end-to-end
* ✔ output sent to State Engine
* ✔ bucket logging implemented

---

## ❌ Failure Conditions (Avoided)

* ❌ NICAI not rebuilt
* ❌ No ML logic used
* ❌ No schema redesign
* ❌ No missing trace_id
* ❌ No unclear explanations

---

## 📌 Final Status

🚀 **SYSTEM STATUS: COMPLETE + DEMO READY + SUBMISSION READY**

---

## 👨‍💻 System Note

This project demonstrates:

* Deterministic intelligence generation
* Event-driven pipeline design
* Acoustic signal processing (simulated)
* Strict validation-first architecture

---

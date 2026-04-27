# 🧾 NICAI – SVACS Pipeline Review Packet

## 📌 Project Name

**NICAI + Sanskar Deterministic Intelligence Pipeline for SVACS Acoustic Signals**

---

## 🎯 Objective

To implement a **deterministic, traceable, and production-ready pipeline** that:

* Accepts `perception_event` from SVACS Acoustic Node
* Converts it into NICAI-compatible signal
* Reuses NICAI validation (no redesign)
* Applies simplified Sanskar intelligence rules
* Outputs structured intelligence_event
* Sends result to State Engine
* Logs all stages into Bucket + Telemetry

---

## ⚠️ IMPORTANT CONSTRAINTS (STRICTLY FOLLOWED)

* ❌ NICAI NOT rebuilt
* ❌ Schemas NOT redesigned
* ❌ NO ML / probabilistic logic used
* ❌ NO delay for perfect data
* ✅ Fully deterministic system
* ✅ Traceable via trace_id

---

## 🧠 SYSTEM ARCHITECTURE

```
SVACS Acoustic Node (perception_event)
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

## ⚙️ MODULES OVERVIEW

### 1️⃣ SVACS Adapter

**File:** `svacs_adapter.py`

* Converts `perception_event → NICAI signal`
* Mapping:

| SVACS Field      | NICAI Field          |
| ---------------- | -------------------- |
| vessel.type      | asset_id             |
| confidence_score | value                |
| timestamp        | timestamp            |
| source           | "svacs"              |
| signal_type      | "acoustic_detection" |
| feature_type     | "acoustic"           |

* Generates deterministic `trace_id`

---

### 2️⃣ NICAI Validation Layer (REUSED)

**File:** `validator.py`

Validation includes:

* Required fields check
* Schema integrity
* confidence_score ∈ [0,1]
* dataset validation

### 🔴 STRICT RULE:

* If **INVALID → REJECT + STOP PIPELINE**
* MUST NOT pass forward

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

Allowed statuses:

* `ALLOW`
* `FLAG`
* `REJECT`

---

### 3️⃣ Sanskar Simplified Intelligence

**File:** `sanskar_simple.py`

### 🎯 Deterministic Risk Rules

| Confidence | Risk Level |
| ---------- | ---------- |
| ≥ 0.75     | LOW        |
| 0.5 – 0.75 | MEDIUM     |
| 0.3 – 0.5  | HIGH       |
| < 0.3      | CRITICAL   |

---

### 🚨 Anomaly Rules

* vessel_type == "unknown" → anomaly = TRUE
* upstream inconsistency flag → anomaly = TRUE

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

### 5️⃣ Bucket Logging System (MANDATORY)

Logs ALL:

* Valid events
* Invalid events
* Intelligence outputs

### Format:

```json
{
  "trace_id": "...",
  "input": {...},
  "output": {...},
  "timestamp": "...",
  "stage": "validation/intelligence"
}
```

---

### 6️⃣ Telemetry (InsightFlow)

Passive emission only:

* validation_result
* risk_level
* latency

✔ No decision logic here

---

## 🧪 TEST COVERAGE

### ✔ Valid Cases

* High confidence vessel (LOW risk)
* Medium confidence (MEDIUM risk)
* Low confidence (HIGH risk)

### ❌ Invalid Cases

* Missing required fields
* Invalid schema
* Out-of-range confidence

### 🚨 Edge Cases

* Unknown vessel → CRITICAL + anomaly_flag = TRUE
* Very low confidence (<0.3)
* Inconsistent input (if flagged)

---

## 📊 PIPELINE EXECUTION FLOW

```
Event
→ Adapter
→ Validation (ALLOW / REJECT)
   → if REJECT → STOP
→ Sanskar Intelligence
→ State Engine
→ Bucket + Telemetry
```

---

## 🔁 TRACEABILITY

* Single `trace_id` generated at adapter stage
* Preserved across:

  * validation
  * intelligence
  * output
  * logging

---

## 📁 REPOSITORY STRUCTURE

```
nicai_validation_layer/
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
├── README.md
└── REVIEW_PACKET.md
```

---

## 🚀 HOW TO RUN

```bash
python test_pipeline.py
python test_svacs_flow.py
```

---

## 🧠 DESIGN PRINCIPLES

* ✔ Deterministic execution
* ✔ No ML / AI dependency
* ✔ Modular pipeline
* ✔ Stateless validation
* ✔ End-to-end traceability
* ✔ Real-time ready

---

## 📡 OUTPUT TARGETS

* State Engine (Raj)
* Bucket Logging System
* InsightFlow Telemetry

---

## ✅ SUCCESS CRITERIA (ACHIEVED)

* ✔ perception_event accepted and processed
* ✔ invalid inputs rejected and stopped
* ✔ risk_level computed correctly
* ✔ anomaly_flag triggered correctly
* ✔ trace_id preserved end-to-end
* ✔ output delivered to State Engine
* ✔ bucket logging implemented

---

## ❌ FAILURE CONDITIONS (AVOIDED)

* ❌ NICAI not rebuilt
* ❌ No ML logic used
* ❌ No schema redesign
* ❌ No missing trace_id
* ❌ No unclear explanation

---

## 📌 FINAL STATUS

🚀 **SYSTEM STATUS: COMPLETE + DEMO READY + SUBMISSION READY**

---

## 👨‍💻 SYSTEM NOTE

This pipeline demonstrates:

* Deterministic intelligence generation
* Event-driven architecture
* Real-time acoustic signal processing (simulated)
* Strict validation-first pipeline design

---

# 🧾 NICAI – SVACS Acoustic Intelligence Pipeline (Final Review Packet)

---

## 📌 Project Name

**NICAI + Sanskar Deterministic Intelligence Layer for SVACS Perception Events** 

---

## 🎯 Objective

To build a **deterministic, traceable, and real-time pipeline** that:

- Accepts live `perception_event`
- Validates input using NICAI rules (no redesign)
- Generates structured `intelligence_event`
- Preserves traceability via `trace_id`
- Sends output to State Engine
- Logs all stages into Bucket + Telemetry

---

## ⚠️ IMPORTANT CONSTRAINTS (STRICTLY FOLLOWED)

- ❌ NICAI NOT redesigned
- ❌ No schema modification
- ❌ No ML / probabilistic logic
- ❌ No pipeline blocking
- ✅ Deterministic logic only
- ✅ Real-time processing
- ✅ Trace ID preserved end-to-end
- ✅ Invalid inputs logged (no silent failure)

---

## 🧠 SYSTEM ARCHITECTURE

```
Perception Event
      ↓
NICAI Signal Mapping (Direct Mapping)
      ↓
NICAI Validation Layer
      ↓
Sanskar Intelligence Layer
      ↓
State Engine (Downstream)
      ↓
Bucket Logging + Telemetry
```

---

## ⚙️ MODULES OVERVIEW

### 1️⃣ Input Layer (Perception Event)

Accepted fields:

- `trace_id`
- `vessel_type`
- `confidence_score`
- `dominant_freq_hz`
- `anomaly_flag`

### 🔴 STRICT RULES

- No new `trace_id` generated
- Input structure not modified

---

### 2️⃣ NICAI Signal Mapping

Converted into internal signal:

```json
{
  "trace_id": "T1",
  "signal_id": "T1",
  "value": 0.8,
  "asset_id": "cargo",
  "feature_type": "acoustic",
  "dataset_id": "svacs"
}
```

---

### 3️⃣ NICAI Validation Layer (Reused)

**File:** `validator.py`

Validation checks:

- Required fields present
- confidence_score ∈ [0,1]
- Dataset validity
- Schema correctness

### Output:

```json
{
  "signal_id": "T1",
  "status": "ALLOW",
  "confidence_score": 0.8,
  "trace_id": "T1",
  "reason": "Valid signal"
}
```

### ✅ Important Behavior

- Status can be: `ALLOW` or `FLAG`
- ❌ No hard blocking
- ❌ No pipeline stop
- ✔ Invalid cases are logged but flow continues

---

### 4️⃣ Sanskar Intelligence Layer

**File:** `sanskar_simple.py`

#### 🎯 Risk Mapping (Deterministic)

| Confidence | Risk Level |
|------------|-----------|
| ≥ 0.75     | LOW       |
| 0.5–0.75   | MEDIUM    |
| 0.3–0.5    | HIGH      |
| < 0.3      | CRITICAL  |

---

#### 🚨 Anomaly Rules

- `vessel_type == "unknown"` → anomaly = TRUE  
- `metadata.anomaly_flag == True` → anomaly = TRUE  

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

---

### 5️⃣ State Engine Output

- Direct forwarding of `intelligence_event`
- No transformation
- No delay

---

### 6️⃣ Bucket Logging (MANDATORY)

Logs include:

- Input signal
- Validation result
- Intelligence output
- trace_id
- timestamp
- processing stage

---

### 7️⃣ Telemetry (Passive)

Captured:

- validation status
- risk_level
- pipeline activity

✔ No decision-making logic

---

## 🧪 TEST COVERAGE

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

## 📊 LIVE PIPELINE FLOW

```
Perception Event
→ NICAI Validation (ALLOW / FLAG)
→ Sanskar Intelligence
→ State Engine Output
```

---

## 🔁 TRACEABILITY

- Same `trace_id` preserved across:
  - input
  - validation
  - intelligence
  - output
  - logging

---

## 📁 REPOSITORY STRUCTURE

```
nicai_validation_layer/
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
├── README.md
└── REVIEW_PACKET.md
```

---

## 🚀 HOW TO RUN

```bash
python live_pipeline.py
```

---

## 🧠 DESIGN PRINCIPLES

- ✔ Deterministic system
- ✔ No ML dependency
- ✔ Real-time processing
- ✔ Modular architecture
- ✔ Stateless validation
- ✔ Full traceability

---

## 📡 OUTPUT TARGETS

- State Engine
- Bucket Logging System
- Telemetry System

---

## ✅ SUCCESS CRITERIA (ACHIEVED)

- ✔ perception_event accepted
- ✔ validation applied correctly
- ✔ intelligence_event generated
- ✔ risk mapping correct
- ✔ anomaly handled correctly
- ✔ explanation generated
- ✔ trace_id preserved
- ✔ no pipeline blocking
- ✔ no silent failures

---

## 📌 FINAL STATUS

🚀 **SYSTEM STATUS: COMPLETE + LIVE INTEGRATED + DEMO READY**

---

## 👨‍💻 SYSTEM NOTE

This system demonstrates:

- Event-driven pipeline design
- Deterministic intelligence generation
- Real-time processing architecture
- Explainable and traceable outputs

from pipeline import run_pipeline


# -----------------------------
# TEST EVENTS
# -----------------------------

# 1. VALID (LOW RISK)
event1 = {
    "event_id": "E1",
    "timestamp": "2026-04-20T10:00:00", 
    "vessel": {
        "type": "cargo",
        "confidence_score": 0.8
    }
}

# 2. MEDIUM RISK
event2 = {
    "event_id": "E2",
    "timestamp": "2026-04-20T10:01:00",
    "vessel": {
        "type": "cargo",
        "confidence_score": 0.6
    }
}

# 3. HIGH RISK
event3 = {
    "event_id": "E3",
    "timestamp": "2026-04-20T10:02:00",
    "vessel": {
        "type": "cargo",
        "confidence_score": 0.4
    }
}

# 4. CRITICAL RISK
event4 = {
    "event_id": "E4",
    "timestamp": "2026-04-20T10:03:00",
    "vessel": {
        "type": "cargo",
        "confidence_score": 0.2
    }
}

# 5. UNKNOWN VESSEL (ANOMALY)
event5 = {
    "event_id": "E5",
    "timestamp": "2026-04-20T10:04:00",
    "vessel": {
        "type": "unknown",
        "confidence_score": 0.9
    }
}


# -----------------------------
# RUN ALL
# -----------------------------
for event in [event1, event2, event3, event4, event5]:
    print("\n-------------------------------")
    run_pipeline(event)

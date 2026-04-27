try:
    from bucket_emitter import emit_bucket_artifact
except ImportError:
    def emit_bucket_artifact(x):
        pass


# -----------------------------------
# RISK LEVEL ENGINE
# -----------------------------------
def get_risk_level(confidence, vessel_type):

    if vessel_type == "unknown" or confidence < 0.3:
        return "CRITICAL"
    elif confidence < 0.5:
        return "HIGH"
    elif confidence < 0.75:
        return "MEDIUM"
    else:
        return "LOW"


# -----------------------------------
# ANOMALY DETECTOR
# -----------------------------------
def detect_anomaly(vessel_type, metadata):

    if vessel_type == "unknown":
        return True

    if isinstance(metadata, dict):
        if metadata.get("pattern_flag") == "inconsistent":
            return True

    return False


# -----------------------------------
# EXPLANATION ENGINE
# -----------------------------------
def generate_explanation(confidence, vessel_type, risk, anomaly):

    if vessel_type == "unknown":
        return "Unknown vessel detected — classified as critical risk"

    if anomaly:
        return "Inconsistent acoustic pattern detected — possible anomaly"

    if confidence < 0.3:
        return "Very low confidence acoustic detection — critical risk"

    if confidence < 0.5:
        return "Low confidence acoustic detection — high risk"

    if confidence < 0.75:
        return "Moderate confidence acoustic detection — medium risk"

    return f"High confidence acoustic classification of {vessel_type} vessel — low risk"


# -----------------------------------
# BUCKET LOGGER
# -----------------------------------
def log_intelligence(signal, intelligence):

    emit_bucket_artifact({
        "trace_id": intelligence.get("trace_id"),
        "type": "intelligence_event",
        "layer": "SANSKAR_INTELLIGENCE",
        "input": signal,
        "output": intelligence,
        "timestamp": signal.get("timestamp")
    })


# -----------------------------------
# MAIN INTELLIGENCE ENGINE
# -----------------------------------
def generate_intelligence(signal, trace_id):

    try:
        confidence = signal.get("value", 0.0)
        vessel_type = signal.get("asset_id", "unknown")
        metadata = signal.get("metadata", {})

        risk = get_risk_level(confidence, vessel_type)
        anomaly = detect_anomaly(vessel_type, metadata)
        explanation = generate_explanation(confidence, vessel_type, risk, anomaly)

        intelligence = {
            "trace_id": trace_id,
            "vessel_type": vessel_type,
            "confidence": confidence,
            "risk_level": risk,
            "anomaly_flag": anomaly,
            "explanation": explanation
        }

        log_intelligence(signal, intelligence)

        return intelligence

    except Exception as e:
        return {
            "trace_id": trace_id,
            "status": "ERROR",
            "reason": str(e)
        }


# -----------------------------------
# REQUIRED WRAPPER (FIX FOR YOUR ERROR)
# -----------------------------------
def analyze_svacs(signal, trace_id):
    """
    Required entry point for SVACS test pipeline
    """
    return generate_intelligence(signal, trace_id)

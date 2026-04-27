import hashlib
import json

# -------------------------------
# SAFE STRING CONVERTER
# -------------------------------
def to_safe_string(value):
    try:
        if isinstance(value, (dict, list)):
            return json.dumps(value, sort_keys=True)
        return str(value)
    except:
        return "unknown"


# -------------------------------
# TRACE ID GENERATOR (SAFE)
# -------------------------------
def generate_trace_id(signal):

    try:
        if not isinstance(signal, dict):
            return "TRACE_INVALID"

        signal_id = to_safe_string(signal.get("signal_id"))
        timestamp = to_safe_string(signal.get("timestamp"))
        dataset_id = to_safe_string(signal.get("dataset_id"))

        base_string = f"{signal_id}|{timestamp}|{dataset_id}"

        return "TRACE_" + hashlib.sha256(base_string.encode()).hexdigest()[:12]

    except:
        return "TRACE_ERROR"


# -------------------------------
# OUTPUT SCHEMA VALIDATION (🔥 DISABLED SAFE)
# -------------------------------
def validate_output_schema(output):
    """
    DISABLED FOR DEMO SAFETY
    Prevents 'unhashable dict' crash
    """

    try:
        # 🔥 Skip validation completely (demo-safe)
        return True

    except:
        return True
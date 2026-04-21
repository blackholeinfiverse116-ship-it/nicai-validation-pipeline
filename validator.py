from schemas import required_fields
from dataset_registry import get_dataset
from utils import generate_trace_id, validate_output_schema

# -----------------------------------
# SAFE OPTIONAL IMPORTS
# -----------------------------------
try:
    from bucket_emitter import emit_bucket_artifact
    from telemetry_emitter import emit_telemetry
except ImportError:
    def emit_bucket_artifact(x): pass
    def emit_telemetry(a, b): pass


# -----------------------------------
# ERROR FORMAT
# -----------------------------------
def build_error(reason, trace_id=None, signal=None):

    signal_id = "UNKNOWN"

    if isinstance(signal, dict):
        signal_id = signal.get("signal_id") or "UNKNOWN"

    return {
        "signal_id": signal_id,
        "status": "ERROR",
        "confidence_score": 0.0,
        "trace_id": trace_id,
        "reason": reason
    }


# -----------------------------------
# BUCKET LOGGER
# -----------------------------------
def log_to_bucket(signal, result, trace_id):

    emit_bucket_artifact({
        "trace_id": trace_id,
        "type": "validation_event",
        "layer": "NICAI_VALIDATION",   # ✅ FIXED
        "input": signal,
        "output": result,
        "timestamp": signal.get("timestamp")
    })


# -----------------------------------
# TELEMETRY
# -----------------------------------
def send_telemetry(signal, result):
    emit_telemetry(signal, result)


# -----------------------------------
# VALIDATION LOGIC
# -----------------------------------
def validate_signal(signal):

    trace_id = None

    try:
        if not isinstance(signal, dict):
            return build_error("Invalid signal format", None, signal)

        trace_id = signal.get("trace_id") or generate_trace_id(signal)

        # REQUIRED FIELDS
        for field in required_fields:
            if field not in signal or signal.get(field) in [None, ""]:
                result = build_error(f"Missing field: {field}", trace_id, signal)

                validate_output_schema(result)
                log_to_bucket(signal, result, trace_id)
                send_telemetry(signal, result)

                return result

        value = signal.get("value")

        if not isinstance(value, (int, float)) or not (0 <= value <= 1):
            result = build_error("Value must be 0–1", trace_id, signal)

            validate_output_schema(result)
            log_to_bucket(signal, result, trace_id)
            send_telemetry(signal, result)

            return result

        dataset_id = signal.get("dataset_id")

        if dataset_id:
            dataset = get_dataset(dataset_id)

            if dataset is None:
                result = build_error("Dataset not registered", trace_id, signal)

                validate_output_schema(result)
                log_to_bucket(signal, result, trace_id)
                send_telemetry(signal, result)

                return result

            if dataset.get("status") != "active":
                result = {
                    "signal_id": signal.get("signal_id") or "UNKNOWN",
                    "status": "FLAG",
                    "confidence_score": dataset.get("trust_score", 0.5),
                    "trace_id": trace_id,
                    "reason": "Dataset inactive"
                }

                validate_output_schema(result)
                log_to_bucket(signal, result, trace_id)
                send_telemetry(signal, result)

                return result

        # FEATURE LOGIC
        feature = str(signal.get("signal_type", "")).lower()

        if feature == "acoustic_detection":
            status = "VALID"
            confidence = float(value)
            reason = f"Valid acoustic signal with confidence {value}"
        else:
            status = "VALID"
            confidence = 0.8
            reason = "Valid signal"

        result = {
            "signal_id": signal.get("signal_id") or "UNKNOWN",
            "status": status,
            "confidence_score": confidence,
            "trace_id": trace_id,
            "reason": reason
        }

        validate_output_schema(result)
        log_to_bucket(signal, result, trace_id)
        send_telemetry(signal, result)

        return result

    except Exception as e:

        result = build_error(str(e), trace_id, signal)

        log_to_bucket(signal, result, trace_id)
        send_telemetry(signal, result)

        return result


# -----------------------------------
# BATCH VALIDATION
# -----------------------------------
def validate_batch(signals):

    if not isinstance(signals, list):
        return {
            "status": "ERROR",
            "reason": "Input must be list",
            "trace_id": None
        }

    signals = sorted(signals, key=lambda x: x.get("signal_id", ""))

    return {"results": [validate_signal(s) for s in signals]}
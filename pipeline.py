from svacs_adapter import prepare_signal
from validator import validate_signal
from sanskar_simple import generate_intelligence


# -----------------------------
# STATE ENGINE STUB
# -----------------------------
def send_to_state_engine(event):
    print("📡 Sent to State Engine:", event)


# -----------------------------
# FULL PIPELINE
# -----------------------------
def run_pipeline(event):

    # STEP 1: Adapter
    adapted = prepare_signal(event)

    if adapted.get("status") == "ERROR":
        print("❌ Adapter Error:", adapted.get("reason"))
        return

    signal = adapted.get("signal")
    trace_id = adapted.get("trace_id")

    print("✅ Signal:", signal)

    # STEP 2: Validation
    validation = validate_signal(signal)
    print("✅ Validation:", validation)

    if validation.get("status") == "ERROR":
        print("❌ Validation Failed — Stopping pipeline")
        return

    # STEP 3: Intelligence
    intelligence = generate_intelligence(signal, trace_id)
    print("✅ Intelligence:", intelligence)

    # STEP 4: Send to State Engine
    send_to_state_engine(intelligence)
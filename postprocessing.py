import re
import uuid

def normalize_line_number(tag: str) -> str:
    """
    Normalize line numbers to a consistent format.
    """
    if not tag or not isinstance(tag, str) or tag.strip() == "":
        return f'UNSPECIFIED-LINE-{uuid.uuid4().hex[:4].upper()}'
    return tag.strip().upper()

def normalize_instrument_tag(tag: str, measured_variable: str = None,
                             function: str = None, loop_id: str = None) -> str:
    """
    Normalize instrument tags to ISA convention if the tag is missing.
    """
    if not tag or not isinstance(tag, str) or tag.strip() == "":
        loop_number = str(loop_id) if loop_id else str(uuid.uuid4().int % 1000).zfill(3)
        measured_var = (measured_variable[0].upper() if measured_variable else "X")
        func = (function[0].upper() if function else "I")
        return f"{measured_var}{func}-{loop_number}"
    return str(tag).strip().upper()

def postprocess_pid_data(data: dict) -> dict:
    """
    Applies standardization and cleaning rules to the raw AI output.
    Ensures schema compliance by adding missing keys and normalizing values.
    """
    if not isinstance(data, dict):
        return data

    print("---------------------////////// Running postprocessing and standardization...")

    # --- Ensure required top-level keys exist ---
    expected_keys = ["equipment", "instrumentation", "lines", "valves", "metadata", "junctions", "control_relationships", "annotations", "safety_devices", "unrecognized_symbols"]
    for key in expected_keys:
        if key not in data:
            data[key] = [] if key != "metadata" else {}

    # --- Standardize Items in Each Category ---
    for item in data.get("lines", []):
        item["line_number_tag"] = normalize_line_number(item.get("line_number_tag"))
        item["source_tag"] = str(item.get("source_tag") or "UNKNOWN").upper()
        item["destination_tag"] = str(item.get("destination_tag") or "UNKNOWN").upper()
        item["line_type"] = str(item.get("line_type") or "unspecified").strip().lower()

    for item in data.get("instrumentation", []):
        item["tag"] = normalize_instrument_tag(
            item.get("tag"),
            item.get("measured_variable"),
            item.get("type"),
            item.get("loop_id")
        )

    for item in data.get("equipment", []):
        item["tag"] = str(item.get("tag") or f"EQUIP-{uuid.uuid4().hex[:4].upper()}").upper()
    
    for item in data.get("valves", []):
        item["tag"] = str(item.get("tag") or f"VALVE-{uuid.uuid4().hex[:4].upper()}").upper()

    print("---------------/////////// Postprocessing completed.")
    return data

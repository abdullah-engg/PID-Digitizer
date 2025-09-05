# # analyzer.py
# import vertexai
# from vertexai.generative_models import GenerativeModel, Part, HarmCategory, HarmBlockThreshold
# import json
# import re
# import os
# from preprocessing import preprocess_image 

# # --- CONFIGURATION ---
# PROJECT_ID = "p-id-digitizer-project"
# LOCATION = "us-central1" 
# MODEL_ID = "gemini-2.5-pro"

# def extract_json_from_response(text: str):
#     """Finds and parses the first valid JSON block from a string."""
#     json_match = re.search(r'```json\s*(\{.*?\})\s*```|(\{.*?\})', text, re.DOTALL)
#     if json_match:
#         json_str = json_match.group(1) if json_match.group(1) else json_match.group(2)
#         try:
#             return json.loads(json_str)
#         except json.JSONDecodeError as e:
#             print(f"Error decoding JSON: {e}")
#             return None
#     return None

# def analyze_pid(image_file_path: str):
#     """
#     Analyzes a P&ID using the final, hyper-specific master prompt.
#     """
#     print("🧠 Starting analysis pipeline...")
#     processed_image_path = preprocess_image(image_file_path)

#     vertexai.init(project=PROJECT_ID, location=LOCATION)
#     model = GenerativeModel(MODEL_ID)

#     # --- FINAL HYPER-SPECIFIC MASTER PROMPT ---
#     prompt = """
#     Your SOLE task is to output ONE valid JSON object for the provided P&ID image. 
#     ⚠️ Output NOTHING except the JSON (must start with { and end with }).

#     You are an expert AI process engineer. Follow ISA-5.1 and ISO 14617 conventions.

#     ================= JSON RULES =================
#     - Return ONLY a JSON object (not Markdown, no commentary).
#     - JSON must be syntactically valid and parseable with Python json.loads.
#     - All arrays must contain only objects (no trailing commas).
#     - Use null for missing values, never empty strings.

#     ================= COORDINATE SYSTEM =================
#     - All bounding boxes MUST be normalized to image frame where (0,0) is top-left and (1000,1000) is bottom-right.
#     - bounding_box format: [x1, y1, x2, y2] with integers only.
#     - Must satisfy: x1 < x2, y1 < y2.
#     - Boxes must be TIGHT around the actual symbol/text (no loose/oversized boxes, no overlaps).
#     - Round coordinates to nearest integer.

#     ================= LABELING RULES =================
#     Every object MUST have a non-empty "label". 
#     Allowed priority for label:
#     1. tag (e.g., "P-101", "FI-120")
#     2. line_number_tag (for lines)
#     3. junction_id (for junctions)
#     4. text (for annotations)
#     5. type (e.g., "Control Valve", "Pump")
#     6. category_name

#     ⚠️ Never output "Unknown", "N/A", or leave label empty.

#     ================= REQUIRED CATEGORIES =================
#     The top-level JSON object may include any subset of these keys. Omit if empty.

#     1) metadata: object OR array
#     fields: drawing_title?, drawing_number?, revision?

#     2) equipment: array of objects
#     fields: tag?, type?, description?, bounding_box [int,int,int,int], 
#             category_name="equipment", label

#     3) instrumentation: array of objects
#     fields: tag?, type?, measured_variable?, loop_id?, connected_to_tag?, 
#             display_value?, bounding_box [int,int,int,int], 
#             display_value_bounding_box? [int,int,int,int], 
#             category_name="instrumentation", label

#     4) lines: array of objects
#     fields: line_number_tag?, source_tag?, destination_tag?, line_type (MUST be one of ["process", "instrument_signal", "electrical_signal", "utility", "pneumatic", "hydraulic", "unknown"])?, 
#             bounding_box? [int,int,int,int], 
#             category_name="lines", label

#     5) valves: array of objects
#     fields: tag?, type?, installed_on_line_tag?, bounding_box [int,int,int,int], 
#             category_name="valves", label

#     6) junctions: array of objects
#     fields: junction_id?, connected_lines? (array of strings), 
#             bounding_box [int,int,int,int], 
#             category_name="junctions", label

#     7) control_relationships: array of objects
#     fields: source_tag, destination_tag, relationship_type ("measures","controls","signals"), 
#             category_name="control_relationships", 
#             label (e.g., "FT-101 -> FC-101")

#     8) annotations: array of objects
#     fields: text, associated_tag?, bounding_box [int,int,int,int], 
#             category_name="annotations", label

#     9) safety_devices: array of objects
#     fields: tag?, type?, location?, bounding_box [int,int,int,int], 
#             category_name="safety_devices", label

#     10) unrecognized_symbols: array of objects
#         fields: description, bounding_box [int,int,int,int], 
#                 flag_for_review=true, review_reason?, 
#                 category_name="unrecognized_symbols", label

#     ================= VALIDATION RULES =================
#     - If any field is missing/uncertain, include "flag_for_review": true and "review_reason".
#     - DO NOT hallucinate connections — only include if clearly visible.
#     - Ensure each object has "category_name" and "label".
#     - Ensure JSON is compact, valid, and industry-compliant.

#     ⚠️ Final Output = JSON object ONLY (no explanations, no markdown, no ```json fences).
#     """

#     # Load image
#     ext = os.path.splitext(processed_image_path)[1].lower()
#     mime = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
#     with open(processed_image_path, "rb") as f:
#         image_bytes = f.read()
#     image = Part.from_data(data=image_bytes, mime_type=mime)

#     safety_settings = {
#         HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
#         HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
#         HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
#         HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
#     }

#     print(f"🚀 Sending request to {MODEL_ID} in {LOCATION} ...")
#     response = model.generate_content([image, prompt], safety_settings=safety_settings)

#     if os.path.exists(processed_image_path) and processed_image_path != image_file_path:
#         try:
#             os.remove(processed_image_path)
#         except Exception:
#             pass

#     try:
#         data = extract_json_from_response(response.text)
#         if data:
#             print("✅ Analysis Complete!")
#             return data
#         else:
#             print("❌ Could not parse JSON. Raw response:")
#             print(response.text)
#             return None
#     except Exception as e:
#         print(f"❌ Error during parsing/post-processing: {e}")
#         return None

# analyzer.py
import vertexai
from vertexai.generative_models import GenerativeModel, Part, HarmCategory, HarmBlockThreshold
import json
import re
import os
from preprocessing import preprocess_image 

# --- CONFIGURATION ---
import os
import streamlit as st

# Try to get from Streamlit secrets first, then environment variables
try:
    PROJECT_ID = st.secrets["gcp"]["project_id"]
    LOCATION = st.secrets["gcp"]["location"] 
    MODEL_ID = st.secrets["gcp"]["model_id"]
except (KeyError, FileNotFoundError):
    # Fallback to environment variables
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "p-id-digitizer-project")
    LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    MODEL_ID = os.getenv("GOOGLE_CLOUD_MODEL_ID", "gemini-2.5-pro")

def extract_json_from_response(text: str):
    """Finds and parses the first valid JSON block from a string."""
    json_match = re.search(r'```json\s*(\{.*?\})\s*```|(\{.*?\})', text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1) if json_match.group(1) else json_match.group(2)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    return None

def analyze_pid(image_file_path: str):
    """
    Analyzes a P&ID using the final, hyper-specific master prompt.
    """
    print("---------------------///////////// Starting analysis pipeline...")
    processed_image_path = preprocess_image(image_file_path)

    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = GenerativeModel(MODEL_ID)

    # --- FINAL HYPER-SPECIFIC MASTER PROMPT ---
    prompt = """
    Your SOLE task is to output ONE valid JSON object for the provided P&ID image. 
    ⚠️ Output NOTHING except the JSON (must start with { and end with }).

    You are an expert AI process engineer. Follow ISA-5.1 and ISO 14617 conventions.

    ================= JSON RULES =================
    - Return ONLY a JSON object (not Markdown, no commentary).
    - JSON must be syntactically valid and parseable with Python json.loads.
    - All arrays must contain only objects (no trailing commas).
    - Use null for missing values, never empty strings.

    ================= COORDINATE SYSTEM =================
    - All bounding boxes MUST be normalized to image frame where (0,0) is top-left and (1000,1000) is bottom-right.
    - bounding_box format: [x1, y1, x2, y2] with integers only.
    - Must satisfy: x1 < x2, y1 < y2.
    - Boxes must be TIGHT around the actual symbol/text (no loose/oversized boxes, no overlaps).
    - Round coordinates to nearest integer.

    ================= LABELING RULES =================
    Every object MUST have a non-empty "label". 
    Allowed priority for label:
    1. tag (e.g., "P-101", "FI-120")
    2. line_number_tag (for lines)
    3. junction_id (for junctions)
    4. text (for annotations)
    5. type (e.g., "Control Valve", "Pump")
    6. category_name

    ⚠️ Never output "Unknown", "N/A", or leave label empty.

    ================= REQUIRED CATEGORIES =================
    The top-level JSON object MUST include the "metadata" key. Other keys may be omitted if empty.

    1) metadata: object
       fields: drawing_title?, drawing_number?, revision?. If no title block is found, return this object with null values for its fields.

    2) equipment: array of objects
    fields: tag?, type?, description?, bounding_box [int,int,int,int], 
            category_name="equipment", label

    3) instrumentation: array of objects
    fields: tag?, type?, measured_variable?, loop_id?, connected_to_tag?, 
            display_value?, bounding_box [int,int,int,int], 
            display_value_bounding_box? [int,int,int,int], 
            category_name="instrumentation", label

    4) lines: array of objects
    fields: line_number_tag?, source_tag?, destination_tag?, line_type (MUST be one of ["process", "instrument_signal", "electrical_signal", "utility", "pneumatic", "hydraulic", "unknown"])?, 
            bounding_box? [int,int,int,int], 
            category_name="lines", label

    5) valves: array of objects
    fields: tag?, type?, installed_on_line_tag?, bounding_box [int,int,int,int], 
            category_name="valves", label

    6) junctions: array of objects
    fields: junction_id?, connected_lines? (array of strings), 
            bounding_box [int,int,int,int], 
            category_name="junctions", label

    7) control_relationships: array of objects
    fields: source_tag, destination_tag, relationship_type ("measures","controls","signals"), 
            category_name="control_relationships", 
            label (e.g., "FT-101 -> FC-101")

    8) annotations: array of objects
    fields: text, associated_tag?, bounding_box [int,int,int,int], 
            category_name="annotations", label

    9) safety_devices: array of objects
    fields: tag?, type?, location?, bounding_box [int,int,int,int], 
            category_name="safety_devices", label

    10) unrecognized_symbols: array of objects
        fields: description, bounding_box [int,int,int,int], 
                flag_for_review=true, review_reason?, 
                category_name="unrecognized_symbols", label

    ================= VALIDATION RULES =================
    - If any field is missing/uncertain, include "flag_for_review": true and "review_reason".
    - DO NOT hallucinate connections — only include if clearly visible.
    - Ensure each object has "category_name" and "label".
    - Ensure JSON is compact, valid, and industry-compliant.

    ⚠️ Final Output = JSON object ONLY (no explanations, no markdown, no ```json fences).
    """

    # Load image
    ext = os.path.splitext(processed_image_path)[1].lower()
    mime = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
    with open(processed_image_path, "rb") as f:
        image_bytes = f.read()
    image = Part.from_data(data=image_bytes, mime_type=mime)

    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

    print(f"--------------///////////// Identifying the Symbols/ Instrumentation/ Piping lines/ Valves / Junctions ...")
    response = model.generate_content([image, prompt], safety_settings=safety_settings)

    if os.path.exists(processed_image_path) and processed_image_path != image_file_path:
        try:
            os.remove(processed_image_path)
        except Exception:
            pass

    try:
        data = extract_json_from_response(response.text)
        if data:
            print("------------------ Analysis Complete!")
            return data
        else:
            print("❌ Could not parse JSON. Raw response:")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Error during parsing/post-processing: {e}")
        return None


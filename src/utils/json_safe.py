import json
from typing import Dict
from src.utils.log import log


def parse_json_filemap(raw: str) -> Dict[str, str]:
    """
    Expects JSON: {"path":"content", ...}
    Handles common LLM issues:
    - ```json fences
    - leading/trailing commentary
    - JSON embedded in text
    """
    if not raw:
        return {}

    s = raw.strip()

    # Remove markdown code fences if present
    if s.startswith("```"):
        s = _strip_code_fences(s).strip()

    # Try direct parse
    obj = _try_load_json(s)
    if obj is not None:
        return _validate_filemap(obj)

    # Try extracting the biggest JSON object by scanning braces
    extracted = _extract_first_json_object(s)
    if extracted:
        obj = _try_load_json(extracted)
        if obj is not None:
            return _validate_filemap(obj)

    log.warn("Could not parse JSON file map from LLM output.")
    return {}


def _try_load_json(s: str):
    try:
        return json.loads(s)
    except Exception as e:
        log.warn(f"JSON parse failed: {e}")
        return None


def _strip_code_fences(s: str) -> str:
    # removes first and last fence
    lines = s.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines)


def _extract_first_json_object(s: str) -> str:
    """
    Extract first full {...} JSON object using brace counting.
    This avoids 'Extra data' issues if model adds text after JSON.
    """
    start = s.find("{")
    if start == -1:
        return ""

    depth = 0
    for i in range(start, len(s)):
        if s[i] == "{":
            depth += 1
        elif s[i] == "}":
            depth -= 1
            if depth == 0:
                return s[start : i + 1]
    return ""


def _validate_filemap(obj) -> Dict[str, str]:
    if not isinstance(obj, dict):
        return {}
    out: Dict[str, str] = {}
    for k, v in obj.items():
        if isinstance(k, str) and isinstance(v, str):
            out[k] = v
    return out

from typing import List, Dict
from src.utils.log import log

try:
    from ollama import chat  # type: ignore
except Exception as e:
    chat = None
    _import_error = e


def llm_chat(model: str, messages: List[Dict[str, str]], force_json: bool = False) -> str:
    """
    Calls local Ollama chat model.
    If force_json=True, asks Ollama to return JSON-only (supported by Ollama for many models).
    """
    if chat is None:
        raise RuntimeError(f"Ollama python client not available: {_import_error}")

    kwargs = {"model": model, "messages": messages}
    if force_json:
        kwargs["format"] = "json"  # <-- key line

    resp = chat(**kwargs)
    content = resp.get("message", {}).get("content", "")
    if not content:
        log.warn("LLM returned empty content.")
    return content

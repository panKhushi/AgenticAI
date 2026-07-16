import json
import re


def _strip_fence(text: str):
    """
    Extract the contents of a ```json ... ``` or ``` ... ``` fence,
    wherever it appears in the string (not just anchored at the very
    start/end). Returns None if no fence is found.
    """
    match = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)

    if match:
        return match.group(1).strip()

    return None


def _extract_first_json_object(text: str):
    """
    Find the first balanced {...} object in the string, even if the
    model added explanation text before or after it. Uses brace
    counting rather than a greedy regex so nested objects/arrays
    inside the tool call (e.g. presentationmaker's "slides" list)
    don't break the match.
    """
    start = text.find("{")

    if start == -1:
        return None

    depth = 0

    for i in range(start, len(text)):
        char = text[i]

        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1

            if depth == 0:
                return text[start:i + 1]

    return None


def parse_tool_call(response: str):

    if not response:
        return None

    response = response.strip()

    candidates = []

    fenced = _strip_fence(response)
    if fenced:
        candidates.append(fenced)

    # Always also try extracting the first balanced JSON object,
    # since the model may return explanation text around raw JSON
    # with no code fence at all.
    extracted = _extract_first_json_object(response)
    if extracted:
        candidates.append(extracted)

    # Last resort: the full (stripped) response as-is.
    candidates.append(response)

    for candidate in candidates:
        try:
            tool_request = json.loads(candidate)

            if isinstance(tool_request, dict) and "tool" in tool_request:
                return tool_request

        except Exception:
            continue

    print("JSON Parse Error: no valid tool call found in response")
    print("Response was:")
    print(repr(response))

    return None
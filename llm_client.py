import requests, re
from config import OLLAMA_HOST, OLLAMA_PORT, OLLAMA_MODEL


def generate_text(prompt: str) -> str:
    """
    Sends a prompt to Ollamy and returns the model-generated response.
    """
    url = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        # Some models returns additional garbage in response
        return extract_json_from_llm_response(data.get("response", ""))
    except requests.RequestException as e:
        print(f"[ERROR] Cannot connect to Ollama server: {e}")
        return None


def extract_json_from_llm_response(model_response):
    """
    Removes:
    1. <think>...</think> block and its tags.
    2. ```json and ``` tags.
    3. The first line if empty.

    Args:
    model_response (str): Model response containing <think> block, code tags, and JSON.

    Returns:
    str: A pure JSON structure.
    """
    # 1. Remove <think>...</think> block and its contents
    json_part = re.sub(r'<think>.*?</think>\s*', '', model_response, flags=re.DOTALL)

    # 2. Remove ```json and ``` tags
    json_part = re.sub(r'```json\s*', '', json_part)
    json_part = re.sub(r'```\s*', '', json_part)

    # 3. Split lines
    lines = json_part.splitlines()

    # 4. Remove first line if empty
    if lines and not lines[0].strip():
        lines = lines[1:]

    # 5. Join the lines back into one string
    clean_json = '\n'.join(lines)

    # 6. Remove any empty lines at the beginning and end
    clean_json = clean_json.strip()

    return clean_json

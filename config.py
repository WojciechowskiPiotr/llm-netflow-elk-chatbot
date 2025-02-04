import os
from dotenv import load_dotenv

# Define a mapping for string-to-boolean conversion.
bool_map = {
    "true": True,
    "1": True,
    "t": True,
    "yes": True,
    "y": True,
    "false": False,
    "0": False,
    "f": False,
    "no": False,
    "n": False
}


def str_to_bool(s):
    try:
        return bool_map[s.lower()]
    except KeyError:
        raise ValueError(f"Invalid boolean value: {s}")


# Load .env file from local folder
load_dotenv()

# --- OLLAMA ---
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")
OLLAMA_PORT = int(os.getenv("OLLAMA_PORT", 11434))

# OLLAMA_MODEL = "deepseek-r1:70b"
# OLLAMA_MODEL = "deepseek-r1:32b"
# OLLAMA_MODEL = "deepseek-r1:14b"
# OLLAMA_MODEL = "llama3:latest"
OLLAMA_MODEL = "qwen2.5-coder:32b"
# OLLAMA_MODEL = "qwen2.5-coder:3b"

# --- Elasticsearch ---
ES_HOST = os.getenv("ES_HOST", "localhost")
ES_PORT = int(os.getenv("ES_PORT", 9200))
ES_SCHEME = os.getenv("ES_SCHEME", "https")  # Let's assume, we run HTTPS
ES_VERIFY_CERTS = str_to_bool(os.getenv("ES_VERIFY_CERTS", False))  # Disable certificate validation
ES_APIKEY = os.getenv("ES_APIKEY", None)

# Default index for NetFlow from the ElasticFlow collection
NETFLOW_INDEX = "elastiflow-*"

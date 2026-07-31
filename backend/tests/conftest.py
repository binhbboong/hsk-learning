import os

# Tests must be deterministic and must never consume a developer's real API key.
os.environ["OPENAI_API_KEY"] = ""
os.environ["ALLOWED_ORIGINS"] = "http://localhost:4200"

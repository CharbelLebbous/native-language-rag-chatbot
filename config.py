# config.py

# ✅ The `os` module lets you interact with environment variables and the system.
import os

# ✅ Define your Cohere API key here.
# This line tries to read the `COHERE_API_KEY` from your system's environment variables.
# If it's not set, it falls back to the hardcoded default `"YOUR_API_KEY"` as a placeholder.
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "t29LSJzyWK9a2NrZWBwQ4exWf1e71STklQLgx6OJ")

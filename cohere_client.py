# cohere_client.py

# ✅ Import the Cohere SDK
import cohere

# ✅ Import the API key from the config file
from config import COHERE_API_KEY

class CohereClient:
    """
    A simple wrapper class around Cohere's Python SDK.
    Provides methods for:
    - Generating embeddings
    - Summarizing text
    - Extracting entities
    - Generating answers using chat
    """

    def __init__(self):
        """
        Initialize the Cohere client with the provided API key.
        """
        self.client = cohere.ClientV2(COHERE_API_KEY)

    def embed(self, texts: list):
        """
        Generate embeddings for a list of texts using Cohere's embedding model.
        
        Args:
            texts (list): A list of strings to embed.
        
        Returns:
            list: The embeddings for the input texts.
        """
        response = self.client.embed(
            texts=texts,
            model="embed-english-v3.0"  # Specific embedding model
        )
        return response.embeddings

    def summarize(self, text: str) -> str:
        """
        Generate a summary of the given text using Cohere's chat endpoint.
        
        Args:
            text (str): The text to summarize.
        
        Returns:
            str: The generated summary.
        """
        response = self.client.chat(
            model="command-r-plus",
            messages=[
                {"role": "user", "content": f"Please summarize this: {text}"}
            ]
        )

        # Debug: print full raw response for troubleshooting
        print("Response JSON:", response.json())

        # Extract only the text parts from the response
        parts = [
            item.text for item in response.message.content
            if item.type == "text"
        ]
        return "".join(parts).strip()

    def extract_entities(self, text: str) -> str:
        """
        Extract named entities, key dates, numbers, and facts from text using Cohere's chat endpoint.
        
        Args:
            text (str): The text to extract information from.
        
        Returns:
            str: The extracted entities as a string.
        """
        response = self.client.chat(
            model="command-r-plus",
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Extract named entities, key dates, numbers, "
                        f"and facts from:\n\n{text[:2000]}"
                    )
                }
            ]
        )

        parts = [
            item.text for item in response.message.content
            if item.type == "text"
        ]
        return "".join(parts).strip()

    def generate_answer(self, messages) -> str:
        """
        Generate an answer given a list of chat messages using Cohere's chat endpoint.
        Can handle multi-turn conversations by passing the full message history.
        
        Args:
            messages (list): A list of dicts with roles and content.
                             Example: [{"role": "user", "content": "Your question here"}]
        
        Returns:
            str: The generated answer.
        """
        response = self.client.chat(
            model="command-a-03-2025",
            messages=messages
        )

        parts = [
            item.text for item in response.message.content
            if item.type == "text"
        ]
        return "".join(parts).strip()

from typing import List, Dict, Optional
from google import genai


class AIAssistant:
    """
    Simple wrapper around a Gemini AI chat model.
    Manages system prompt, conversation history, and responses.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-2.5-flash",
        system_prompt: str = "You are a helpful assistant."
    ):
        self._client = genai.Client(api_key=api_key)
        self._model = model
        self._system_prompt = system_prompt

        # Gemini-style message history
        self._history: List[Dict] = [
            {"role": "model", "parts": [{"text": self._system_prompt}]}
        ]

    def set_system_prompt(self, prompt: str):
        """Update the system prompt and reset conversation."""
        self._system_prompt = prompt
        self.clear_history()
        self._history.append(
            {"role": "model", "parts": [{"text": self._system_prompt}]}
        )

    def send_message(self, user_message: str) -> str:
        """Send a message to Gemini and return the full response."""

        # Add user message
        self._history.append(
            {"role": "user", "parts": [{"text": user_message}]}
        )

        try:
            # Call Gemini
            response = self._client.models.generate_content(
                model=self._model,
                contents=self._history
            )

            reply_text = response.text
        
        except Exception:
            reply_text = "⚠️ AI service is temporarily unavailable."


        # Save assistant reply
        self._history.append(
            {"role": "model", "parts": [{"text": reply_text}]}
        )

        return reply_text

    def clear_history(self):
        """Clear conversation history (keeps system prompt)."""
        self._history.clear()

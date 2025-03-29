import os
import requests
from dotenv import load_dotenv

def send_text_message(phone_number: str, message: str) -> dict:
    """
    Sends a text message using the Textbelt API.
    
    Args:
        phone_number (str): The recipient's phone number.
        message (str): The message to send.
    
    Returns:
        dict: The response from the Textbelt API.
    """
    load_dotenv()
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY is not set in the .env file.")

    url = "https://textbelt.com/text"
    payload = {"phone": phone_number, "message": message, "key": api_key}

    response = requests.post(url, data=payload)
    return response.json()



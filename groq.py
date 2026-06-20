import os
import requests
import time
from config.settings import groq_api_key

BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

def call_groq(messages,API_KEY, system_prompt=None, max_retries=5):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    all_messages = []
    if system_prompt:
        all_messages.append({"role": "system", "content": system_prompt})
    all_messages.extend(messages)

    body = {"model": MODEL, "messages": all_messages}

    for attempt in range(max_retries):
        response = requests.post(BASE_URL, json=body, headers=headers)

        if response.status_code == 429:
            wait = int(response.headers.get("Retry-After", 2 ** attempt))
            time.sleep(wait)
            continue

        response.raise_for_status()
        return response.json()

    raise Exception(f"Failed after {max_retries} attempts — still rate limited.")


def chat(messages,user_ask,doc):
    system_prompt =  f"""
    You are a helpful assistant for this repository.
    Answer questions based ONLY on this documentation:

    {doc}

    If answer isn't in the documentation, say so. Don't make things up. only do global research if user asks. """

    q = {"role": "user", "content": user_ask}
    messages.append(q)
    resp = call_groq(messages,API_KEY=groq_api_key,system_prompt=system_prompt)
    return resp["choices"][0]["message"]["content"]


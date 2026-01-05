
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.env import client, AZURE_OPENAI_DEPLOYMENT

def analyze_email(subject, body):
    prompt = f"""
You are a compliance monitoring AI.

Analyze the email below and return JSON with:
- categories (list)
- risky_lines (list of exact sentences)
- category_score (0 to 1)
- confidence (0 to 1)

Email:
Subject: {subject}
Body: {body}
"""

    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {"role": "system", "content": "You are a financial compliance expert."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content

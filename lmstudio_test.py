from openai import OpenAI

client = OpenAI(
    base_url="http://192.168.0.44:1234/v1",
    api_key="lm-studio"
)

def extract_features_ai(user_input):

    prompt = f"""
Extract medical symptoms AND preserve clinical severity wording.

Rules:
- Do NOT overly simplify symptoms
- Prefer clinical terms where possible
- Include severity descriptors (sudden, severe, worsening, acute)
- Convert lay language only when necessary
- Do NOT remove important detail like 'sudden', 'severe', 'unable'

Return ONLY a comma separated list of symptoms.
No explanation.

Examples:
- "cannot catch my breath" -> "acute shortness of breath"
- "face drooped suddenly" -> "sudden facial droop"

Text:
{user_input}
"""

    response = client.chat.completions.create(
        model="local-model",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content.lower()

    return [x.strip() for x in content.split(",")]
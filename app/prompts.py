def build_prompt(topic: str, style: str) -> str:
    if style == "educational":
        tone = "clear and informative, suitable for students and beginners"
    elif style == "marketing":
        tone = "persuasive and engaging, with strong calls to action"
    elif style == "technical":
        tone = "precise and detailed, appropriate for engineers or developers"
    else:
        tone = "neutral"

    return f"""
You are an expert content writer. Write a single-page website on the topic: "{topic}".
Use a {tone} tone.

Include:
- A unique, creative page title
- A short SEO-friendly meta description
- Between 3 and 5 informative sections, each with:
  - a heading
  - a paragraph of content

Return the result as valid JSON with keys: "title", "meta_description", and "sections" (list of dicts with heading and text).
"""

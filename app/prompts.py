import random

ALL_SECTIONS = [
    "Introduction",
    "Use Cases",
    "Technical Details",
    "Tools and Libraries",
    "Future Trends",
    "Case Studies",
    "Myths and Facts",
    "Challenges",
    "Summary"
]

FEW_SHOT_EXAMPLES = {
    "Introduction": [
        "Quantum Computing is an advanced computing technology that leverages the principles of quantum mechanics to process complex computations.",
        "Quantum Computing harnesses quantum phenomena to solve problems much faster than classical computers."
    ],
    "Use Cases": [
        "In finance, quantum algorithms can optimize portfolios and manage risk more effectively than classical methods.",
        "Quantum computing is revolutionizing drug discovery and cryptography through advanced computation."
    ],
    "Technical Details": [
        "Quantum bits, or qubits, can exist in superposition, allowing simultaneous computation of multiple states.",
        "Qubits leverage quantum entanglement to perform complex calculations in parallel."
    ],
    "Tools and Libraries": [
        "Popular quantum computing frameworks include Qiskit, Cirq, and Forest SDK.",
        "Developers use tools like Qiskit and Cirq for building quantum algorithms."
    ],
    "Future Trends": [
        "Quantum internet development aims to enable secure communication based on quantum entanglement.",
        "Researchers are exploring scalable quantum networks for the future."
    ],
    "Case Studies": [
        "IBM’s quantum computers have been used to simulate molecular structures for drug discovery.",
        "Google's quantum supremacy experiment demonstrated the power of quantum processors."
    ],
    "Myths and Facts": [
        "Contrary to popular belief, quantum computers are not just faster classical computers but operate on different principles.",
        "Quantum computing is often misunderstood as just 'super fast' classical computing, which is incorrect."
    ],
    "Challenges": [
        "Maintaining qubit coherence and error correction remain significant technical challenges.",
        "Quantum noise and error rates pose hurdles to practical quantum computing."
    ],
    "Summary": [
        "Quantum computing promises to revolutionize industries by solving problems beyond the reach of classical computers.",
        "The future of computing is quantum, offering immense opportunities and challenges."
    ]
}

TONE_VARIANTS = {
    "educational": [
        "clear and informative, suitable for students and beginners",
        "easy-to-understand and educational, great for learners",
        "thorough and explanatory, designed for beginners"
    ],
    "marketing": [
        "persuasive and engaging, with strong calls to action",
        "energetic and compelling, designed to convert",
        "exciting and motivating, targeting potential customers"
    ],
    "technical": [
        "precise and detailed, appropriate for engineers or developers",
        "technical and thorough, perfect for specialists",
        "deeply informative and exact, aimed at professionals"
    ],
    "neutral": [
        "neutral and balanced",
        "formal and unbiased",
        "straightforward and clear"
    ]
}


def build_prompt(topic: str, style: str, sections: list[str] | None = None) -> str:
    tone_choices = TONE_VARIANTS.get(style)
    tone = random.choice(tone_choices) if tone_choices else "neutral and balanced"

    if sections is None:
        intro = "Introduction"
        summary = "Summary"
        middle = random.sample([s for s in ALL_SECTIONS if s not in (intro, summary)], k=3)
        sections = [intro] + middle + [summary]

    sections_text = "\n- ".join(sections)

    examples_text = ""
    for section in sections:
        examples = FEW_SHOT_EXAMPLES.get(section, [])
        if examples:
            example = random.choice(examples)
            examples_text += f"\n\nSection: {section}\nExample: {example}"

    prompt = f"""You are an expert website copywriter and research assistant. Use external tools (like Wikipedia or DuckDuckGo) if needed.

Write a single-page website on the topic: "{topic}".
Use a {tone} tone.

Include the following sections in order:
- {sections_text}

Each section should have:
- a heading (the section name)
- a paragraph of content
- a short description of an image that could visually represent this section

Return the result as valid JSON with keys:
- "title": string
- "meta_description": string
- "sections": list of sections, each section must be a dict with:
    - "heading": string
    - "text": string
    - "image_prompt": string (image description)
{examples_text}
"""
    return prompt

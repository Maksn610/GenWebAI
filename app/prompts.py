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
    "Introduction": "Quantum Computing is an advanced computing technology that leverages the principles of quantum mechanics to process complex computations.",
    "Use Cases": "In finance, quantum algorithms can optimize portfolios and manage risk more effectively than classical methods.",
    "Technical Details": "Quantum bits, or qubits, can exist in superposition, allowing simultaneous computation of multiple states.",
    "Tools and Libraries": "Popular quantum computing frameworks include Qiskit, Cirq, and Forest SDK.",
    "Future Trends": "Quantum internet development aims to enable secure communication based on quantum entanglement.",
    "Case Studies": "IBM’s quantum computers have been used to simulate molecular structures for drug discovery.",
    "Myths and Facts": "Contrary to popular belief, quantum computers are not just faster classical computers but operate on different principles.",
    "Challenges": "Maintaining qubit coherence and error correction remain significant technical challenges.",
    "Summary": "Quantum computing promises to revolutionize industries by solving problems beyond the reach of classical computers."
}

def build_prompt(topic: str, style: str, sections=None) -> str:
    if style == "educational":
        tone = "clear and informative, suitable for students and beginners"
    elif style == "marketing":
        tone = "persuasive and engaging, with strong calls to action"
    elif style == "technical":
        tone = "precise and detailed, appropriate for engineers or developers"
    else:
        tone = "neutral"

    if sections is None:
        intro = "Introduction"
        summary = "Summary"
        middle = random.sample([s for s in ALL_SECTIONS if s not in (intro, summary)], k=3)
        sections = [intro] + middle + [summary]

    sections_text = "\n- ".join(sections)

    examples_text = ""
    for section in sections:
        example = FEW_SHOT_EXAMPLES.get(section, "")
        if example:
            examples_text += f"\n\nSection: {section}\nExample: {example}"

    return f"""
You are an expert content writer. Write a single-page website on the topic: "{topic}".
Use a {tone} tone.

Include the following sections in order:
- {sections_text}

Each section should have a heading (the section name) and a paragraph of content.

Here are examples to guide your writing:{examples_text}

Return the result as valid JSON with keys: "title", "meta_description", and "sections" (list of dicts with heading and text).
"""

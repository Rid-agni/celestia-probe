def extract_entity(question, llm):

    prompt = f"""
You are an astronomy entity extractor.

Extract the SINGLE main celestial object mentioned in the user's question.

Rules:
- Return ONLY the object's name.
- No explanation.
- No punctuation.
- No extra words.
- Preserve the proper name.

Examples:

Question: Tell me about Mars
Answer: Mars

Question: Could humans survive on Europa?
Answer: Europa

Question: Is Titan larger than Earth's Moon?
Answer: Titan

Question: What is Pluto?
Answer: Pluto

Question: Explain the atmosphere of Venus
Answer: Venus

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    return response.content.strip()


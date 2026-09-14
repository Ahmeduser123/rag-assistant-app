import ollama

from app.core.config import settings


def build_prompt(question: str, retrieved_chunks: list[dict]) -> str:
    """
    Builds a grounded prompt: retrieved chunks go in as labeled context,
    the LLM is instructed to answer ONLY from that context and cite which
    source each part of its answer came from.
    """
    context_blocks = []
    for i, chunk in enumerate(retrieved_chunks, start=1):
        drug_readable = chunk["drug"].replace("_", " ").title()
        context_blocks.append(
            f"[Source {i}: {drug_readable} — {chunk['section'].title()}]\n{chunk['text']}"
        )
    context_text = "\n\n".join(context_blocks)

    prompt = f"""You are a medical information assistant. Answer the user's question using ONLY the information in the sources below. Do not use any outside knowledge.

If the sources do not contain enough information to answer the question, say so clearly instead of guessing.

After your answer, list which source(s) you used, like this: "Source: [drug name] — [section name]".

--- SOURCES ---
{context_text}
--- END SOURCES ---

Question: {question}

Answer:"""
    return prompt


def generate_answer(question: str, retrieved_chunks: list[dict]) -> str:
    """
    Calls the local Ollama LLM with the grounded prompt and returns its
    raw text response.
    """
    prompt = build_prompt(question, retrieved_chunks)
    response = ollama.generate(model=settings.ollama_model, prompt=prompt)
    return response["response"]
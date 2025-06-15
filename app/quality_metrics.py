from typing import List, Dict
from sentence_transformers import SentenceTransformer, util
import tiktoken

encoder = tiktoken.encoding_for_model("gpt-4")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def count_tokens(text: str) -> int:
    return len(encoder.encode(text, disallowed_special=()))


def get_site_token_stats(sections: List[Dict]) -> int:
    all_text = " ".join([s.get("text", "") for s in sections])
    return count_tokens(all_text)


def get_section_similarities(sections: List[Dict]) -> float:
    texts = [s.get("text", "") for s in sections]
    if len(texts) < 2:
        return 0.0

    embeddings = embedding_model.encode(texts, convert_to_tensor=True)
    sim_matrix = util.pytorch_cos_sim(embeddings, embeddings)

    scores = [
        sim_matrix[i][j].item()
        for i in range(len(texts))
        for j in range(i + 1, len(texts))
    ]
    return sum(scores) / len(scores) if scores else 0.0


def get_title_uniqueness_score(title: str, previous_titles: List[str]) -> float:
    if not previous_titles:
        return 1.0

    all_titles = previous_titles + [title]
    embeddings = embedding_model.encode(all_titles, convert_to_tensor=True)

    new_embedding = embeddings[-1]
    existing_embeddings = embeddings[:-1]

    similarities = util.pytorch_cos_sim(new_embedding, existing_embeddings)[0]
    max_similarity = max(similarities).item()

    return round(1.0 - max_similarity, 4)

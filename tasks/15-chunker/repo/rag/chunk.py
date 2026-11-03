def chunk_words(text: str, size: int, overlap: int) -> list[str]:
    words = text.split(" ")
    chunks = []
    i = 0
    while i + size < len(words):
        chunks.append(" ".join(words[i:i + size]))
        i += size - overlap
    return chunks

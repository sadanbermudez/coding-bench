def chunk_words(text, size, overlap):
    if size < 1 or overlap < 0 or overlap >= size:
        raise ValueError((size, overlap))
    words = text.split()
    out, i = [], 0
    while i < len(words):
        out.append(" ".join(words[i:i + size]))
        if i + size >= len(words):
            break
        i += size - overlap
    return out

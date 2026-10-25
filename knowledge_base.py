"""Load a small fictional FAQ and retrieve related entries."""
import json
import re
from settings import KNOWLEDGE_FILE

STOPWORDS = {
    "a", "about", "an", "and", "are", "can", "do", "does", "for",
    "how", "i", "in", "is", "me", "my", "of", "on", "our",
    "the", "to", "we", "what", "when", "where", "with", "you", "your"
}


def words(text):
    return {
        w for w in re.findall(r"[a-z0-9]+", text.lower())
        if w not in STOPWORDS and len(w) > 1
    }


class KnowledgeBase:
    def __init__(self, path=KNOWLEDGE_FILE):
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list) or not data:
            raise ValueError("FAQ knowledge base must be a nonempty list.")
        self.entries = data
        ids = set()
        for entry in self.entries:
            if not isinstance(entry, dict) or not all(
                isinstance(entry.get(key), str) and entry[key].strip()
                for key in ("id", "question", "answer")
            ) or entry["id"] in ids:
                raise ValueError("Invalid or duplicate FAQ entry.")
            ids.add(entry["id"])

    def search(self, question, limit=2):
        query = words(question)
        scored = []
        for entry in self.entries:
            score = len(query & words(entry["question"])) * 2
            score += len(query & words(entry["answer"]))
            if score > 0:
                scored.append((score, entry))
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [entry for _, entry in scored[:limit]]

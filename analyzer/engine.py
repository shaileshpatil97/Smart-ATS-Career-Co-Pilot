import re
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

STOP = set(stopwords.words("english"))
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def clean(text):
    if not text:
        return ""
    text = re.sub(r"[^a-zA-Z ]", " ", text.lower())
    return " ".join(w for w in text.split() if w not in STOP)

def analyze_resume(resume_text, jd_text):
    resume = clean(resume_text)
    jd = clean(jd_text)

    if not resume or not jd:
        return {"score": 0, "missing": [], "suggestions": []}

    model = get_model()
    emb = model.encode([resume, jd])
    similarity = cosine_similarity([emb[0]], [emb[1]])[0][0]

    score = round(similarity * 100, 2)

    r_words = set(resume.split())
    j_words = set(jd.split())
    missing = sorted(j_words - r_words)

    return {
        "score": score,
        "missing": missing[:30],
        "suggestions": [f"Add keyword: {k}" for k in missing[:15]],
    }

import nltk, re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords')
from nltk.corpus import stopwords

model = SentenceTransformer('all-MiniLM-L6-v2')
STOP = set(stopwords.words("english"))


def clean(text):
    text = re.sub(r'[^a-zA-Z ]', ' ', text.lower())
    return " ".join(w for w in text.split() if w not in STOP)


def analyze_resume(resume_text, jd_text):

    resume = clean(resume_text)
    jd = clean(jd_text)

    # semantic similarity
    emb = model.encode([resume, jd])
    similarity = cosine_similarity([emb[0]], [emb[1]])[0][0]

    score = round(similarity * 100, 2)

    # missing keywords
    r_words = set(resume.split())
    j_words = set(jd.split())
    missing = sorted(j_words - r_words)

    suggestions = [f"Add keyword: {k}" for k in missing[:15]]

    return {
        "score": score,
        "missing": missing[:30],
        "suggestions": suggestions
    }

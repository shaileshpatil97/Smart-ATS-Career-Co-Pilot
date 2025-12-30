import nltk
import os
from django.conf import settings

nltk.data.path.append(settings.NLTK_DATA)

nltk.download("stopwords", download_dir=settings.NLTK_DATA)
nltk.download("punkt", download_dir=settings.NLTK_DATA)
nltk.download("wordnet", download_dir=settings.NLTK_DATA)
nltk.download("omw-1.4", download_dir=settings.NLTK_DATA)

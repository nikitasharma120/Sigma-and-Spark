from sklearn.feature_extraction.text import TfidfVectorizer

def build_tfidf(corpus_texts, ngram_range=(1,3), max_features=10000, stop_words="english"):
    """
    Build a TF-IDF vectorizer and matrix from corpus texts.

    Args:
        corpus_texts (list[str]): List of documents (faculty search_text).
        ngram_range (tuple): Range of n-grams to include (default: unigrams + bigrams).
        max_features (int): Maximum number of features to keep.
        stop_words (str|None): Stop words to remove (default: "english").

    Returns:
        vectorizer (TfidfVectorizer): Fitted TF-IDF vectorizer.
        matrix (scipy.sparse.csr_matrix): TF-IDF matrix for corpus_texts.
    """
    vectorizer = TfidfVectorizer(
        ngram_range=ngram_range,
        stop_words=stop_words,
        max_features=max_features,
        lowercase=True,
        norm="l2"
    )
    matrix = vectorizer.fit_transform(corpus_texts)
    return vectorizer, matrix

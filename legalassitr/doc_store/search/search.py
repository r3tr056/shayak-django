from datetime import datetime, timedelta

RELEVANCE_WEIGHT = 0.7
RECENCY_WEIGHT = 0.3


def rank_documents(query, documents):
    relevance_weight = RELEVANCE_WEIGHT
    recency_weight = RECENCY_WEIGHT

    # calculate the relevance scores based on the number of query keywords
    relevance_score = {doc.id: calculate_relevance(query, doc.content) for doc in documents}

    # calculate the recency score based on the access history and time difference of access
    recency_score = {doc.id: calculate_recency(doc.created_at) for doc in documents}
    # combine the scores by weighted sum of the individual scores
    combined_scores = {doc_id: (relevance_weight * relevance_score[doc_id] + recency_weight * recency_score[doc_id]) for doc_id in documents}
    # sort the docs by score, greatest first (reverse)
    ranked_documents = sorted(documents, key=lambda doc: combined_scores[doc.id], reverse=True)

    return ranked_documents

def calculate_relevance(query, content):
    query_keywords = set(query.lower().split())
    content_keywords = set(content.lower().split())

    intersection_count = len(query_keywords.intersection(content_keywords))
    return intersection_count / max(len(query_keywords), 1)

def calculate_recency(document_created_at):
    # Calculate recency score based on the time difference from the current time
    current_date = datetime.now()
    age = current_date - document_created_at
    max_age = timedelta(days=365)
    recency_score = max(0, 1 - (age.total_seconds() / max_age.total_seconds()))
    return recency_score
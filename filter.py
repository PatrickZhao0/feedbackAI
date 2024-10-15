from FlagEmbedding import FlagReranker

def filter(passage):
    reranker = FlagReranker('BAAI/bge-reranker-v2-m3', use_fp16=True) # Setting use_fp16 to True speeds up computation with a slight performance degradation
    query = 'What areas of the facility need the most improvement, and how should they be improved?'

    # You can map the scores into 0-1 by set "normalize=True", which will apply sigmoid function to the score
    scores = reranker.compute_score([query, passage], normalize=True)

    threshold = 0.00009
    filtered_query = []
    for score in scores:
        if score  >= threshold:
            filtered_query.append(query)
            return True
        else:
            return False 
        
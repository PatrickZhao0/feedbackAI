from summarizer.sbert import SBertSummarizer

def gen_report(payload):
    model = SBertSummarizer('paraphrase-MiniLM-L6-v2')
    result = model(payload)
    return result
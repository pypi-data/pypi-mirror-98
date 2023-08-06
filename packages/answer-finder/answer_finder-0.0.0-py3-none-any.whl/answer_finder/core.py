import pandas as pd
from transformers import pipeline

from base_processor.core import Processor


class BertAnswerFinder(Processor):
    def __init__(self):
        self.qna_pipeline = pipeline(
            'question-answering',
            model='distilbert-base-uncased-distilled-squad',
            tokenizer='distilbert-base-uncased-distilled-squad'
        )

    def process(self, results, documents, question):
        candidate_idxs = [i for i in results[0:5, 0]]
        contexts = [documents[i] for i in candidate_idxs]

        question_df = pd.DataFrame.from_records([{
            'question': question,
            'context': ctx
        } for ctx in contexts])

        preds = self.qna_pipeline(question_df.to_dict(orient="records"))
        answer_df = pd.DataFrame.from_records(preds) \
            .sort_values(by="score", ascending=False)

        return answer_df


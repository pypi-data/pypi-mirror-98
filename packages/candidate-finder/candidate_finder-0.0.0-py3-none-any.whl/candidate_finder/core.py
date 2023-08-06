import numpy as np

from base_processor.core import Processor


class DotProductFinder(Processor):
    def process(self, corpus_embeddings, question_embedding, lemmas):
        scores = np.dot(np.array(corpus_embeddings), np.array(question_embedding).T)
        results = (np.flip(np.argsort(scores, axis=0)))
        candidate_docs = [lemmas[i] for i in results[:3, 0]]
        return candidate_docs, results

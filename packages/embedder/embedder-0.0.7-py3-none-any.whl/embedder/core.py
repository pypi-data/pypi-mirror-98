import pickle
import uuid

from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import spacy

from base_processor.core import Processor


class TfidfEmbedder(Processor):
    def __init__(self, vectorizer_id=None):

        self.vectorizer_id = vectorizer_id
        self.lemmas = None

        if self.vectorizer_id:
            with open(f"vectorizer-{self.vectorizer_id}.pickle", "rb") as f:
                self.vectorizer = pickle.load(f)
            self.vocab = self.vectorizer.vocabulary
        else:
            self.vectorizer = TfidfVectorizer(
                stop_words="english", max_df=.5, min_df=5, ngram_range=(1, 3)
            )
            self.vocab = None

        # try:
        #     self.cached_lemmas = pd.read_feather("lemmas.feather")
        #     print("loaded lemmas from cache")
        # except FileNotFoundError:
        #     self.cached_lemmas = pd.DataFrame()
        #     print("lemma cache not present")

        self.spacy = spacy.load("en_core_web_sm")

    def lemmatize(self, phrase):
        return " ".join([word.lemma_ for word in self.spacy(phrase)])

    def docs2lemmas(self, documents):
        # if self.cached_lemmas.empty:
        lemmas = [self.lemmatize(doc) for doc in documents]
        df = pd.DataFrame(data={'context': documents, 'lemmas': lemmas})
        self.lemmas = lemmas
        # df.to_feather("lemmas.feather")
        return df
        # else:
        #     return self.cached_lemmas

    def lemmas2embeddings(self, lemmas):
        if not self.vectorizer_id:
            tfidf_embeddings = self.vectorizer.fit_transform(lemmas)
        else:
            tfidf_embeddings = self.vectorizer.transform(lemmas)

        if not self.vectorizer_id:
            self.vectorizer_id = str(uuid.uuid4())
            with open(f"vectorizer-{self.vectorizer_id}.pickle", "wb") as f:
                pickle.dump(self.vectorizer, f)

        self.vocab = self.vectorizer.vocabulary_
        return tfidf_embeddings.todense()

    def process(self, documents):
        lemmas_df = self.docs2lemmas(documents)
        return self.lemmas2embeddings(lemmas_df['lemmas'])

    def get_lemmas(self):
        return self.lemmas
        # if self.cached_lemmas.empty:
        #     print("no lemmas present")
        # else:
        #     return pd.read_feather("lemmas.feather")['lemmas']

    def get_vectorizer_id(self):
        return self.vectorizer_id


class SBertEmbedder(Processor):
    def __init__(self):
        pass

    def process(self, documents):
        pass

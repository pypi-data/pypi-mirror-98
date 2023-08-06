from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import spacy
import feather

from processors.base_processor.base_processor import Processor


class TfidfEmbedder(Processor):
    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
        # self.vectorizer = TfidfVectorizer(stop_words="english")
        self.vectorizer = TfidfVectorizer(
            stop_words="english", max_df=.5, min_df=.001, ngram_range=(1, 3)
        )
        self.spacy = spacy.load("en_core_web_sm")
        try:
            self.cached_lemmas = pd.read_feather(f"{self.dataset_name}.feather")
            print("loaded lemmas from cache")
        except FileNotFoundError:
            self.cached_lemmas = pd.DataFrame()
            print("lemma cache not present")

    def lemmatize(self, phrase):
        return " ".join([word.lemma_ for word in self.spacy(phrase)])

    def docs2lemmas(self, documents):
        if self.cached_lemmas.empty:
            lemmas = [self.lemmatize(doc) for doc in documents]
            df = pd.DataFrame(data={'context': documents, 'lemmas': lemmas})
            df.to_feather(f"{self.dataset_name}.feather")
            return df
        else:
            return self.cached_lemmas

    def lemmas2embeddings(self, lemmas):
        tfidf_embeddings = self.vectorizer.fit_transform(lemmas)
        return tfidf_embeddings.todense(), self.vectorizer.vocabulary_

    def process(self, documents):
        lemmas_df = self.docs2lemmas(documents)
        embeddings, vocab = self.lemmas2embeddings(lemmas_df['lemmas'])
        return embeddings, vocab

    @property
    def lemmas(self):
        if self.cached_lemmas.empty:
            print("no lemmas present")
        else:
            return pd.read_feather(f"{self.dataset_name}.feather")['lemmas']


class SBertEmbedder(Processor):
    def __init__(self):
        pass

    def process(self, documents):
        pass

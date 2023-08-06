# term_extraction.py

import collections.abc
from collections import defaultdict
from multiprocessing import Pool
from typing import Callable, Iterable, Sequence, Union, Tuple, Any, Dict
import warnings

import ahocorasick
import numpy as np
import pandas as pd
import pkg_resources
from tqdm import tqdm

import spacy
from spacy.matcher import Matcher

start_ = 0
tmp = 0
doctime, matchertime = 0, 0
Corpus = Union[str, Sequence[str]]


class TermExtraction:
    # Utility function for defining patterns
    noun, adj, prep = (
        {"POS": "NOUN", "IS_PUNCT": False},
        {"POS": "ADJ", "IS_PUNCT": False},
        {"POS": "DET", "IS_PUNCT": False},
    )

    # Global settings for all instances of TermExtraction
    config = {
        "spacy_model": "en_core_web_sm",
        "language": "en",
        "MAX_WORD_LENGTH": 6,
        "DEFAULT_GENERAL_DOMAIN_SIZE": 300,
        "dtype": np.int16,
    }

    # Resources, will get more if necessary
    nlps: Dict[str, Any] = {}
    DEFAULT_GENERAL_DOMAINS: Dict[Tuple[str, int], Any] = {}

    patterns = [
        [adj],
        [{"POS": {"IN": ["ADJ", "NOUN"]}, "OP": "*", "IS_PUNCT": False}, noun],
        [
            {"POS": {"IN": ["ADJ", "NOUN"]}, "OP": "*", "IS_PUNCT": False},
            noun,
            prep,
            {"POS": {"IN": ["ADJ", "NOUN"]}, "OP": "*", "IS_PUNCT": False},
            noun,
        ],
    ]

    @staticmethod
    def get_nlp(language: str = None):
        """
        For getting the spaCy nlp.
        """
        if language is None:
            language = TermExtraction.language
        if language not in TermExtraction.nlps:
            TermExtraction.nlps[language] = spacy.load(
                TermExtraction.config["spacy_model"], parser=False, entity=False
            )
        return TermExtraction.nlps[language]

    @staticmethod
    def get_general_domain(language: str = None, size: int = None):
        """
        For getting a pandas Series of domains.
        """
        if language is None:
            language = TermExtraction.config["language"]
        if size is None:
            size = TermExtraction.config["DEFAULT_GENERAL_DOMAIN_SIZE"]
        if (language, size) not in TermExtraction.DEFAULT_GENERAL_DOMAINS:
            TermExtraction.DEFAULT_GENERAL_DOMAINS[(language, size)] = pd.read_csv(
                pkg_resources.resource_stream(
                    __name__, f"default_general_domain.{language}.csv"
                ),
                nrows=size,
            )
        return TermExtraction.DEFAULT_GENERAL_DOMAINS[(language, size)]

    @staticmethod
    def clear_resouces():
        """
        Clears cached spaCy nlp's and general domain documents.
        """
        TermExtraction.nlps = {}
        TermExtraction.DEFAULT_GENERAL_DOMAINS = {}

    def __init__(
        self,
        corpus: Union[str, Iterable[str]],
        vocab: Sequence[str] = None,
        patterns=patterns,
        do_parallelize: bool = True,
        language="en",
        nlp=None,
        default_domain=None,
        default_domain_size: int = None,
        max_word_length: int = None,
        dtype: np.dtype = None,
    ):
        """
        If corpus is a string, then find vocab sequentially, but if the corpus is an iterator, compute through each of them, performing in parallel if do_parallel is set to true. If there is a vocab list, only search for frequencies from the vocab list, otherwise search using the patterns.
        """
        # TODO: find a way to cache counts for general domain
        self.corpus = corpus
        self.vocab = vocab
        self.patterns = patterns
        self.do_parallelize = do_parallelize
        self.language = language
        self.nlp = nlp
        self.default_domain = default_domain
        self.default_domain_size = default_domain_size
        self.max_word_length = max_word_length
        self.dtype = dtype
        if self.default_domain_size is None:
            self.default_domain_size = TermExtraction.config[
                "DEFAULT_GENERAL_DOMAIN_SIZE"
            ]
        if self.nlp is None:
            self.nlp = TermExtraction.get_nlp(self.language)
        if self.default_domain is None:
            self.default_domain = TermExtraction.get_general_domain(self.language)
        if self.max_word_length is None:
            self.max_word_length = TermExtraction.config["MAX_WORD_LENGTH"]
        if self.dtype is None:
            self.dtype = TermExtraction.config["dtype"]

    @staticmethod
    def set_language(language: str, model_name: str = None):
        """
        For changing the language. Currently, the DEFAULT_GENERAL_DOMAIN is still in English and Italian only. If you have a good dataset in another language please put it in an issue on Github.
        """
        if model_name is None:
            model_name = language
        if not model_name.startswith(language):
            warnings.warn(
                f"Model '{model_name}' and language '{language}' may not be compatible."
            )
        TermExtraction.config["language"] = language

    @staticmethod
    def configure(new_settings: Dict[str, Any]):
        """
        Updates config settings, which include:
        - `spacy_model`: str = "en_core_web_sm" (for changing the spacy model name to be used),
        - "language": str = "en" (this is the default language),
        - "MAX_WORD_LENGTH": int = 6 (this is the maximum word length to be considered a phrase),
        - "DEFAULT_GENERAL_DOMAIN_SIZE": int = 300 (this is the number of sentences to be taken from the general domain file),
        - "dtype": np.int16 (this is the date type for max Pandas series int size which are used as counters),
        """
        TermExtraction.config.update(new_settings)
        if not TermExtraction.config["model_name"].startswith(
            TermExtraction.config["language"]
        ):
            warnings.warn(
                f"Model '{TermExtraction.config['model_name']}' and language '{TermExtraction.config['language']}' may not be compatible."
            )

    @staticmethod
    def word_length(string: str):
        """
        Utility function for quickly computing the number of words in a string.
        """
        return string.count(" ") + 1

    @property
    def trie(self):
        """
        Returns an automaton using the Aho–Corasick algorithm using the pyachocorasick library (https://pypi.org/project/pyahocorasick/).
        This method builds the automaton the first time and caches it for future use.
        """
        if not hasattr(self, "_TermExtraction__trie"):
            self.__trie = ahocorasick.Automaton()
            for idx, key in enumerate(self.vocab):
                self.__trie.add_word(key, (idx, key))
            self.__trie.make_automaton()
        return self.__trie

    def count_terms_from_document(self, document: str):
        """
        Counts the frequency of each term in the class and returns it as a default dict mapping each string to the number of occurences of the phrase, for each phrase in vocab.
        """
        term_counter: defaultdict = defaultdict(int)
        if self.vocab is None:
            # initialize a Matcher here - not at the class level
            # addressed in: https://github.com/kevinlu1248/pyate/issues/20
            new_matcher = Matcher(self.nlp.vocab)

            def add_to_counter(matcher, doc, i, matches):
                match_id, start, end = matches[i]
                candidate = str(doc[start:end])
                if TermExtraction.word_length(candidate) <= self.max_word_length:
                    term_counter[candidate] += 1

            for i, pattern in enumerate(self.patterns):
                new_matcher.add("term{}".format(i), add_to_counter, pattern)

            doc = self.nlp(document.lower(), disable=["parser", "ner"])
            new_matcher(doc)
        else:
            for end_index, (insert_order, original_value) in self.trie.iter(
                document.lower()
            ):
                term_counter[original_value] += 1
        return term_counter

    def count_terms_from_documents(self, seperate: bool = False, verbose: bool = False):
        """
        This is the main purpose of this class. Counts terms from the documents and returns a pandas Series.
        If self.corpus is a string, then it is identical to count_terms_from_document.
        If the corpus is an iterable (more specifically, collections.abc.Iterable) of strings, then it will perform the same thing but for each string in the iterable. If `seperate` is set to true, then it will return an iterable of default dicts; otherwise, it will return a single default dict with the sum of frequencies among all strings.
        """
        # TODO: further optimize
        # TODO: add type annotations
        if hasattr(self, "_TermExtraction__term_counts"):
            return self.__term_counts

        if type(self.corpus) is str:
            self.__term_counts = pd.Series(
                self.count_terms_from_document(self.corpus), dtype=self.dtype
            )
            return self.__term_counts
        elif isinstance(self.corpus, collections.abc.Iterable):
            if seperate:
                term_counters = []
            else:
                term_counter = defaultdict(int)
            if verbose:
                pbar = tqdm(total=len(self.corpus))

            def callback(counter_dict):
                if verbose:
                    pbar.update(1)
                if seperate:
                    term_counters.append(
                        (tuple(counter_dict.keys()), tuple(counter_dict.values()))
                    )
                else:
                    nonlocal term_counter
                    # update the cumulative/overall term_counter
                    for term, frequency in counter_dict.items():
                        term_counter[term] += frequency

            def error_callback(e):
                print(e)

            P = Pool()

            for document in self.corpus:
                P.apply_async(
                    self.count_terms_from_document,
                    [document],
                    callback=callback,
                    error_callback=error_callback,
                )
            P.close()
            P.join()

            P.terminate()
            if verbose:
                pbar.close()
        else:
            raise TypeError()

        if seperate:

            def counter_to_series(counter):
                return pd.Series(data=counter[1], index=counter[0], dtype=self.dtype)

            self.__term_counter = (
                pd.DataFrame(data=map(counter_to_series, term_counters))
                .fillna(0)
                .astype(self.dtype)
                .T
            )
            return self.__term_counter
        else:
            self.__term_counter = pd.Series(
                index=tuple(term_counter.keys()),
                data=tuple(term_counter.values()),
                dtype=self.dtype,
            )
            return self.__term_counter


def add_term_extraction_method(extractor: Callable[..., pd.Series]):
    def term_extraction_decorated(self, *args, **kwargs):
        return extractor(
            self.corpus,
            technical_counts=self.count_terms_from_documents(),
            *args,
            **kwargs,
        )

    setattr(TermExtraction, extractor.__name__, term_extraction_decorated)
    return extractor


if __name__ == "__main__":
    PATH_TO_GENERAL_DOMAIN = "../data/wiki_testing.pkl"
    PATH_TO_TECHNICAL_DOMAIN = "../data/pmc_testing.pkl"
    wiki = pd.read_pickle(PATH_TO_GENERAL_DOMAIN)
    pmc = pd.read_pickle(PATH_TO_TECHNICAL_DOMAIN)
    print(
        TermExtraction(pmc[:100]).count_terms_from_documents(
            seperate=True, verbose=True
        )
    )

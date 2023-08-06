from collections import defaultdict
from typing import Callable

import pandas as pd
from spacy.tokens import Doc

from .combo_basic import combo_basic
from .term_extraction import TermExtraction
from spacy.matcher import Matcher


class TermExtractionPipeline:
    """
    This is for adding PyATE as a spaCy pipeline component.
    """
    def __init__(
        self,
        nlp,
        func: Callable[..., pd.Series] = combo_basic,
        force: bool = True,
        *args,
        **kwargs
    ) -> None:
        """
        This is for initializing the TermExtractionPipeline.
        """
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.__name__ = self.func.__name__
        self.matcher = Matcher(nlp.vocab)
        Doc.set_extension(self.__name__, default=None, force=force)
        self.term_counter = None

        def add_to_counter(matcher, doc, i, matches) -> Doc:
            match_id, start, end = matches[i]
            candidate = str(doc[start:end])
            if (
                TermExtraction.word_length(candidate)
                <= TermExtraction.config["MAX_WORD_LENGTH"]
            ):
                self.term_counter[candidate] += 1

        for i, pattern in enumerate(TermExtraction.patterns):
            self.matcher.add("term{}".format(i), add_to_counter, pattern)

    def __call__(self, doc: Doc):
        """
        This function will be called from within spaCy's utilities.
        """
        self.term_counter = defaultdict(int)
        self.matcher(doc)
        terms = self.func(
            str(doc),
            technical_counts=pd.Series(self.term_counter),
            *self.args,
            **self.kwargs
        )
        setattr(doc._, self.__name__, terms)
        return doc

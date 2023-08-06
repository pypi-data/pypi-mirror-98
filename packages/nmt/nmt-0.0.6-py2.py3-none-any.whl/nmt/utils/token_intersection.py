import logging
import warnings
from collections import Counter

import nltk
from nltk.util import ngrams
from scipy import spatial

from nmt.utils.spacy_language_model import nlp
from nmt.utils.spacy_language_model import load as spacy_load
from nmt.utils.spacy_language_model import tokenize as spacy_tokenize

log = logging.getLogger(__name__)
PUNCTUATION = '\\"\'!()-[]{};:,<>./?@#$%^&*_~ '


# make sure language model is med or larger
try:
    assert nlp._meta['vectors']['width'] == 300  # len(nlp('word vector').vector) < 300:
except (AssertionError, TypeError, AttributeError):
    log.warning(f"SpaCy Language model ({nlp._meta['name']}) doesn't contain 300D word2vec word vectors.")
    nlp = spacy_load('en_core_web_md')
assert nlp._meta['vectors']['width'] == 300


def iou(a, b):
    """ Crude character vector overlap measure of string similarity

    >>> iou('Hello', 'World')
    0.285...
    """
    a, b = set(a.lower().strip()), set(b.lower().strip())
    return len(a & b) / len(a | b)


def overlapping_words(tokens, reference_tokens):
    """ Count number of words in tokens that are in the reference_tokens sequence

    # "advance" occurs 2 times in reference, "to" occurs 1 time, "we" occurs 1 time
    # 2 + 1 + 1 => 4
    >>> overlapping_words(
    ...     spacy_tokenize("We're going to advance!".lower()),
    ...     spacy_tokenize("Advance! We'll stop at nothing to advance!".lower()))
    4
    >>> overlapping_words(
    ...     "life is stronger than metal and stone , more powerful than typhoons and volcanoes".split(),
    ...     "life is stronger than metal stones , more volcano and typhoon than powerful".split())
    10
    """
    tokens_counter = Counter()
    reference_tokens_counter = Counter()

    tokens_counter.update(tokens)
    reference_tokens_counter.update(reference_tokens)

    count = 0
    for token in reference_tokens_counter.keys():
        reference_count = reference_tokens_counter.get(token, 0)
        sent_count = tokens_counter.get(token, 0)

        if sent_count >= reference_count:
            count += reference_count
        else:
            count += sent_count

    return count


def rouge_n(text, reference_text, tokenizer=spacy_tokenize, ignore=PUNCTUATION, stemmer=True, ngram=1):
    """Compute the ROUGE similarity between a text string and a reference text with unigram.

    Specify number of grams in `ngram` argument
    All versions of rouge use case folding (case insensitive)
    Some ignore sentence-ending punctuation (?, ., !)
    Some use stemming.
    Some ignore stop words.

    References:
      https://www.aclweb.org/anthology/U19-1008.pdf (some example scores for variants)
      https://stats.stackexchange.com/a/312354/15974

    >>> life = "life is stronger than metal and stones, more powerful than typhoons and volcanoes"
    >>> life_shuffled_lemmas = "life is stronger than metal and stone,  more powerful than typhoon  and volcano"
    >>> rouge_n(
    ...     life,
    ...     life_shuffled_lemmas)
    1.0
    >>> rouge_n(
    ...     text=life_shuffled_lemmas,
    ...     reference_text=life)
    1.0

    >>> rouge_n('', '')
    0.0

    >>> rouge_n("Clean rooms", "The rooms were clean and neat.", )
    0.5



    # FIXME:
    # >>> rouge_n(
    # ...     "typhoons and volcanoes",
    # ...     "typhoon  and volcano")
    # 1.0
    # >>> rouge_n(
    # ...     "typhoons and volcanoes",
    # ...     "typhoon  and volcano",
    # ...     stemmer=False)
    # 0.3333...
    # >>> rouge_n('?', '?')
    # 0.0
    """
    stemmer = nltk.stem.PorterStemmer() if stemmer is True else stemmer
    stemmer = getattr(stemmer, 'stem', stemmer)
    if not stemmer or not callable(stemmer):
        def stemmer(s):
            return s
    ignore = set() if ignore is None or ignore is False else set(str(i) for i in ignore)
#    print(ignore)

    tokens = [stemmer(t) for t in tokenizer(text, ignore=ignore)]
    reference_tokens = [stemmer(t) for t in tokenizer(reference_text, ignore=ignore)]

    # Convert into list of ngrams
    tokens = list(ngrams(tokens, ngram))
    reference_tokens = list(ngrams(reference_tokens, ngram))
    count = overlapping_words(tokens, reference_tokens)

#    print(count) #13
    try:
        if len(tokens) == 0 or len(reference_tokens) == 0:
            warnings.warn(
                "Number of tokens for either input and reference are zero",
                RuntimeWarning,
                stacklevel=2)
        if count == 0:
            warnings.warn(
                "Overlapping ngram tokens=0",
                RuntimeWarning,
                stacklevel=2)

        recall = count / len(reference_tokens)
    except ZeroDivisionError:
        recall = 0.0
    try:
        precision = count / len(tokens)
    except ZeroDivisionError:
        precision = 0.0
    try:
        # Rouge 1 returns F1 Score of Unigram
        return 2 * ((precision * recall) / (precision + recall))
    except ZeroDivisionError:
        return 0.0


# def similarity(reply, stmt=None, **kwargs):
#     """ Compute word2vec docvec cosine similarity (fall back to character IOU)

#     >>> similarity('Hello world!', 'Goodbye big earth!') > .5
#     True
#     """
#     global nlp
#     nlp = kwargs.get('nlp', nlp)
#     if kwargs is None or nlp is None or not stmt or not reply:
#         return 0.0

#     reply_doc, stmt_doc = nlp(str(reply)), nlp(str(stmt))

#     if not reply_doc or not stmt_doc or not reply_doc.has_vector or not stmt_doc.has_vector:
#         # FIXME: levenshtien would be better or fuzzywuzzy
#         return iou(reply, stmt)

#     cos_sim = reply_doc.similarity(stmt_doc)
#     log.debug(f'cos_sim={cos_sim}')
#     return cos_sim


class Doc:
    global nlp

    def __init__(self, text='', nlp=nlp):
        """ Create a Doc object with an API similar to spacy.Doc

        >>> d = Doc('Hello')
        >>> len(d.vector)
        300
        >>> d.doc.similarity(d.doc) > .99
        True
        """
        self.nlp = nlp if nlp else self.nlp
        self.text = text
        self.doc = self.nlp(text)
        self.vector = self.doc.vector

    def similarity(self, other_doc):
        """ Similarity of self Doc object meaning to the meaning of another Doc object
        Calculate the cosine similarity between two high-dimensional dense vector

        >>> doc = Doc('USA')
        >>> doc.similarity(Doc('United States'))
        0.5...
        """
        return self.doc.similarity(getattr(other_doc, 'doc', other_doc))

    def cosine_similarity(self, other_doc):
        result = 1 - spatial.distance.cosine(self.vector, other_doc.vector)
        return result

    def bleu(self, other_doc, tokenizer=spacy_tokenize, weight1=0.25, weight2=0.25, weight3=0.25, weightL=0.25):
        """Compute the BLEU similarity between a text string and a reference text.

        All the different weights are for different N-grams. E.g.weight1 for unigram.
        Both the texts must have at least four words. Otherwise the BLEU score is zero.
        The full-stops matter
        >>> Doc('I visited the park and enjoyed.').bleu('I visited the park and had fun ')
        0.614...
        >>> Doc('').bleu('') == 0
        True
        >>> Doc('').bleu('I am happy') == 0
        True
        >>> round(Doc('I visited').bleu('I visited the park and had fun '), 6)
        0.0
        >>> Doc('I am happy and contented').bleu('I am happy and joyous')
        0.6687...
        >>> Doc('I am going to visit the park and have fun.').bleu('I am going to visit.')
        0.3672...
        >>> Doc('I am going to visit the park and have fun.').bleu('I am going to visit')
        0.3508...
        """
        return nltk.translate.bleu_score.sentence_bleu(
            [tokenizer(other_doc)], tokenizer(self.text),
            weights=(weight1, weight2, weight3, weightL))


if __name__ == '__main__':
    print("Cosine similarity")
    doc1 = Doc(text="I will run in the morning")
    doc2 = Doc(text="I will run in meeting in the morning")
    print(doc1.similarity(doc2))

    print("BLEU Score")
    print(round(doc1.bleu(doc2), 4))

    text = "War and volcanoes"
    reference_text = "Wars and volcano"
    score = rouge_n(text, reference_text, tokenizer=spacy_tokenize, ignore=PUNCTUATION, stemmer=True)
    print("rouge1 score: ", score)

    text = "typhoons and volcanoes"
    reference_text = "typhoons and volcanoes"
    score = rouge_n(text, reference_text, tokenizer=spacy_tokenize, ignore=PUNCTUATION, stemmer=True)
    print("rouge1 score: ", score)

    text = "typhoons and volcanoes"
    reference_text = "typhoon  and volcano"
    score = rouge_n(text, reference_text, tokenizer=spacy_tokenize, ignore=PUNCTUATION, stemmer=False)
    print("rouge1 with no stemmer:", score)

    text = "life is stronger than metal and stone, more powerful than typhoons and volcanoes"
    reference_text = "life is stronger than metal stones, more volcano and typhoon than powerful"
    score = rouge_n(text, reference_text, tokenizer=spacy_tokenize, ignore=PUNCTUATION, stemmer=True)
    print("rouge1 score: ", score)

    text = "life is stronger than metal and stone, more powerful than typhoons and volcanoes"
    reference_text = "life is stronger than metal stones, more volcano and typhoon than powerful"
    score = rouge_n(text, reference_text, tokenizer=spacy_tokenize, ignore=PUNCTUATION, stemmer=True, ngram=2)
    print("Rouge2 score: ", score)

    text = "Advance! We are leaving to advance!"
    reference_text = "We are going to advance"
    score = rouge_n(text, reference_text, tokenizer=spacy_tokenize, ignore=PUNCTUATION, stemmer=True)
    print("rouge1 score: ", score)

    text = "Advance! We are leaving to advance!"
    reference_text = "We are going to advance"
    score = rouge_n(text, reference_text, tokenizer=spacy_tokenize, ignore=PUNCTUATION, stemmer=True, ngram=2)
    print("Rouge2 score: ", score)

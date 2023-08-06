import re
from nltk import tokenize
import nltk

toy_article = {'title': "Predator",
               'abstract': "In the jungle, no-one hears you far cry. And vice-versa. "
                           "They say to make a long abstract, with the number 42 in it, so here I am.",
               'content': "There is no-one in the trees. Is there? Predators don't like to lose."}
"""
Article with a simple structure.
"""

sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
sentence_tokenizer._params.abbrev_types.update({'al', 'i.e', 'fig', 'resp', 'e.g', 'ie', 'eg'})


RE_NOISE = re.compile(r"[,.:;()0-9+=%\[\]_!\*]")
"""
:class:`re.Pattern`
    regexp for useless characters.
"""

RE_URL = re.compile(r'https?://\S+')
"""
:class:`re.Pattern`
    regexp for url detection. Mails may be impacted.
"""

RE_CITATION = re.compile(r"[\[(]\s*\d+(,\s*\d+)*[)\]]")
"""
:class:`re.Pattern`
    regexp for citations.
"""

author = r"(?:[A-Z][A-Za-z'`-]+)"
etal = r"(?:et al\.?)"
additional = f"(?:,? (?:(?:and |& )?{author}|{etal}))"
year_num = "(?:19|20)[0-9][0-9]"
page_num = "(?:, p\.? [0-9]+)?"  # Always optional
year = fr"(?:,? *{year_num}{page_num}| *\({year_num}{page_num}\))"
RE_COMPLEX_CITATION = re.compile(fr'\b(?!(?:Although|Also)\b){author}{additional}*{year}')
"""
:class:`re.Pattern`
    Regexp for complex citations. From https://stackoverflow.com/questions/4320958/regular-expression-for-recognizing-in-text-citations and
    https://stackoverflow.com/questions/63632861/python-regex-to-get-citations-in-a-paper .
"""

RE_NOT_A_WORD = re.compile(r"[^A-Za-z]+")

RE_ALTERNATE_PUNCTUATION = re.compile(r"·|\.==|\.===|\.====")


def sanitize_text(text: str) -> str:
    """
    Sanitize a text. This is done to improve the Embedding quality and should not be perform for human reading.

    Parameters
    ----------
    text: :class:`str`
        Text to clean.

    Returns
    -------
    :class:`str`
        The corresponding sanitized `str` instance.

    Examples
    --------
    >>> sanitize_text("This is a mail: santa@northpole.com!")
    'This is a mail santa@northpolecom'
    >>> sanitize_text("This is a url: http://www.enst.fr!")
    'This is a url'
    >>> sanitize_text("This is a !*[ url: https://www.ens.fr!")
    'This is a  url'
    >>> sanitize_text("These are references [3, 17].")
    'These are references'
    """
    for r in [RE_URL, RE_CITATION, RE_NOISE]:
        text = r.sub("", text).strip()
    return text


def to_text(doc: dict, post_process=None, keys=None) -> str:
    """
    Transforms a dict into a string made of its values.

    Parameters
    ----------
    doc: :class:`dict`
        A `dict` representing a document of "depth one", all the values are strings.
    post_process: callable, optional
        Function to apply to entries.
    keys: list, optional
        The entries to extract.


    Returns
    -------
    :class:`str`
        Concatenation of values.

    Examples
    --------

    >>> to_text(toy_article)
    "Predator In the jungle, no-one hears you far cry. And vice-versa. They say to make a long abstract, with the number 42 in it, so here I am. There is no-one in the trees. Is there? Predators don't like to lose."
    """
    if post_process is None:
        post_process = str
    if keys is None:
        keys = [k for k in doc]
    return " ".join([post_process(doc.get(k, "")) for k in keys])


def to_text_sanitized(doc):
    """
    Parameters
    ----------
    doc: :class:`dict`
        A `dict` representing a document of "depth one", all the values are strings or can be cast to strings.

    Returns
    -------
    str
        Text sanitized for embedding.

    Examples
    --------
    >>> to_text_sanitized(toy_article)
    "Predator In the jungle no-one hears you far cry And vice-versa They say to make a long abstract with the number  in it so here I am There is no-one in the trees Is there? Predators don't like to lose"
    """
    return to_text(doc=doc, post_process=sanitize_text)


def words(text):
    """
    Makes the vocabulary (words) constituting a text.

    Parameters
    ----------
    text: :class:`str`
        A :class:`str` corresponding to a text.

    Returns
    -------
    :class:`list`
        A list of :class:`str` corresponding to the vocabulary (list of lower cases words).

    Examples
    --------
    >>> words("Hello world!")
    ['hello', 'world']

    >>> words("1+one = TWO")
    ['one', 'two']
    """
    return [w for w in (
        RE_NOT_A_WORD.sub("", word.lower())  # Removing punctuation, numbers and math symbols
        for word in text.split(" ")
    ) if w]


def num_words(sentence: str) -> int:
    """
    Gets the length of a sentence in number of words

    Parameters
    ----------
    sentence: :class:`str`
        Text to count.

    Returns
    -------
    :class:`int`
        Number of words in sentence.

    Examples
    --------

    >>> num_words("My Taylor is rich!")
    4
    """
    return len(words(sentence))


def is_relevant_sentence(sentence: str, min_num_words: int = 6, max_num_words: int = 60) -> bool:
    """
    Ignore sentences that are too short, too long, that contain a URL or a citation.

    Parameters
    ----------
    sentence: :class:`str`
        Sentence to analyze.
    min_num_words: :class:`int`, optional
        Minimal number of words.
    max_num_words: :class:`int`, optional
        Maximal number of words.

    Returns
    -------
    :class:`bool`
        Is the sentence OK?

    Examples
    --------
    >>> is_relevant_sentence("This is a short sentence!")
    False
    >>> is_relevant_sentence("This is a sentence with reference to the url http://www.ix.com!")
    False
    >>> is_relevant_sentence("This is a a sentence with some citations [3, 7]!")
    False
    >>> is_relevant_sentence("I have many things to say in that sentence, to the point "
    ...                      "I do not know if I will stop anytime soon but don't let it stop"
    ...                      "you from reading this meaninless garbage and this goes on and "
    ...                      "this goes on and this goes on and this goes on and this goes on and "
    ...                      " this goes on and  this goes on and  this goes on and  this goes on "
    ...                      "and  this goes on and  this goes on and  this goes on and  this goes "
    ...                      "on and  this goes on and  this goes on and  this goes on and  this goes "
    ...                      "on and  this goes on and ")
    False
    >>> is_relevant_sentence("This sentence is not too short and not too long, without URL and without citation.")
    True
    >>> is_relevant_sentence('The enzyme cytidine monophospho-N-acetylneuraminic acid hydroxylase (CMAH) catalyzes '
    ...                      'the synthesis of Neu5Gc by hydroxylation of Neu5Ac '
    ...                      '(Schauer et al. 1968) .')
    False
    """
    n = num_words(sentence)
    return (
        min_num_words <= n <= max_num_words
        and re.search(RE_CITATION, sentence) is None
        and re.search(RE_COMPLEX_CITATION, sentence) is None
        and re.search(RE_URL, sentence) is None
    )


def make_sentences(text, no_end_words=None):
    """
    Extract sentences from a text.

    Parameters
    ----------
    text: :class:`str`
        A :class:`str` corresponding to a full text.
    no_end_words: :class:`set`, optional
        A :class:`set` of words that could wrongfully trigger end of sentence.

    Returns
    -------
    :class:`list`
        A list of :class:`str` corresponding to the text's sentences.

    Examples
    --------

    >>> make_sentences("One sentence, i.e. words with no dot, as Toto and al. say. Or no (cf fig. 2)?")
    ['One sentence, i.e. words with no dot, as Toto and al. say.', 'Or no (cf fig. 2)?']

    Another example with wiki syntax
    >>> make_sentences("and hyraxes.== Name and taxonomy ==")
    ['and hyraxes.', 'Name and taxonomy ==']
    """
    sentences = sentence_tokenizer.tokenize(RE_ALTERNATE_PUNCTUATION.sub(". ", text))
    return [s.strip() for s in sentences]

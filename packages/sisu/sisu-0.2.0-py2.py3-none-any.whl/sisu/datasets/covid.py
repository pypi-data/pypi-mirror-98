from zipfile import ZipFile
from pathlib import Path
from itertools import islice
import json
from sisu.preprocessing.language import guess_language

toy_covid_article = {
    'paper_id': 'thisismyid',
    'metadata': {'title': "Predator"},
    'abstract': [{'text': "In the jungle, no-one hears you far cry. And vice-versa."},
                 {'text': "They say to make a long abstract, with the number 42 in it, so here I am."}],
    'body_text': [{'section': 'introduction',
                   'text': "There is no-one in the trees. Is there?"},
                  {'section': 'conclusion',
                   'text': "Predators don't like to lose."}]
}
"""
A toy document with the same structure as the json in the COVID-19 dataset.
"""


def get_id(document):
    """
    Parameters
    ----------
    document: dict
        A covid article

    Returns
    -------
    str
        Unique Id of the article

    Examples
    --------

    >>> get_id(toy_covid_article)
    'thisismyid'
    """
    return document.get('paper_id')


def get_title(document: dict) -> str:
    """
    Get the title of a document from a document with the same structure as the json in the COVID-19 dataset.

    Parameters
    ----------
    document: :class:`dict`
        A `dict` representing a document.

    Returns
    -------
    :class:`str`
        The title of the document.

    Examples
    --------

    >>> get_title(toy_covid_article)
    'Predator'
    """
    return document["metadata"]["title"]


def get_abstract(document: dict) -> str:
    """
    Get the abstract of a document with the same structure as the json in the COVID-19 dataset.

    Parameters
    ----------
    document: :class:`dict`
        A `dict` representing a document.

    Returns
    -------
    :class:`str`
        Abstract of the document.

    Examples
    --------

    >>> get_abstract(toy_covid_article) # doctest: +NORMALIZE_WHITESPACE
    'In the jungle, no-one hears you far cry. And vice-versa.
    They say to make a long abstract, with the number 42 in it, so here I am.'
    """
    abstract_list = document["abstract"]
    if abstract_list:
        return " ".join(
            [dict_abstract["text"] for dict_abstract in abstract_list]
        )
    else:
        return ""


def get_content(document: dict) -> str:
    """
    Get the content of a document with the same structure as the json in the COVID-19 dataset.

    Parameters
    ----------
    document: :class:`dict`
        A `dict` representing a document.

    Returns
    -------
    :class:`str`
        Content of the document.

    Examples
    --------

    >>> get_content(toy_covid_article)
    "introduction. There is no-one in the trees. Is there? conclusion. Predators don't like to lose."
    """
    return " ".join(
        [". ".join(
            [
                chapter["section"],
                chapter["text"]
            ]
        )
            for chapter in document["body_text"]
        ]
    )


default_getters = {'title': get_title, 'abstract': get_abstract, 'content': get_content, 'id': get_id}
"""Default fields to build from a covid json."""


def format_covid_json(document, getters=None, language=True):
    """
    Parameters
    ----------
    document: dict
        A covid document in its original format.
    getters: dict, optional
        Recipes to build values for the formatted document.
    language: bool, optional
        Add a `lang` entry that tells the language.

    Returns
    -------
    dict
        Formatted document

    Examples
    --------

    We will use a few json samples embedded in the package.

    >>> data_dir = Path("data/covid_sample")
    >>> articles = []
    >>> for f in data_dir.rglob('*.json'):
    ...     with open(f) as fp:
    ...         articles.append(format_covid_json(json.load(fp)))
    >>> for art in sorted(articles, key=lambda e: e['title']): # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    ...     print(art)
    {'title': '"Multi-faceted" COVID-19: Russian experience',
     'abstract': '',
     'content': 'Editor. According to current live statistics at the time of editing this letter,...',
     'id': '0000028b5cc154f68b8a269f6578f21e31f62977',
     'lang': 'en'}
    {'title': 'COVID-19-Pneumonie',
     'abstract': '',
     'content': '. der Entwicklung einer schweren Pneumonie im Vordergrund, die in der Regel prognostisch...',
     'id': '0009745a11d206af9e405e00677c51b01251dba7',
     'lang': 'de'}
    {'title': 'Community frailty response service: the ED at your front door',
     'abstract': 'We describe the expansion and adaptation of a frailty response team to assess older people in
    their usual place of residence. The team had commenced a weekend service to a limited area in February 2020.
    As a consequence of demand related to the COVID-19 pandemic, we expanded it and adapted...',
     'content': "INTRODUCTION. A large proportion of short-stay admissions in older adults may be avoidable...,
     'id': '000680e3114af4aa10e8f208cd162a61195f4465',
     'lang': 'en'}
    """
    if getters is None:
        getters = default_getters
    new_document = {k: v(document) for k, v in getters.items()}
    if language:
        if 'content' in getters:
            lang = guess_language(new_document['content'])
        elif 'abstract' in getters:
            lang = guess_language(new_document['abstract'])
        else:
            lang = 'xx'
        new_document['lang'] = lang
    return new_document

def covid_zip_iterator(file="CORD-19-research-challenge.zip", data_path=".", getters=None, language=True):
    """
    Parameters
    ----------
    file: str or :class:`~pathlib.Path`, optional
        Zip file of a covid archive.
    data_path: str or :class:`~pathlib.Path`, optional
        Location of the archive
    getters: dict, optional
        Recipes to build values for the formatted document.
    language: bool, optional
        Add a `lang` entry that tells the language.

    Returns
    -------
    iterator
        Formatted articles.

    Examples
    --------

    >>> for doc in covid_zip_iterator("covid_sample.zip", data_path='data', getters={'title': get_title}, language=False):
    ...    print(doc)
    {'title': 'Community frailty response service: the ED at your front door'}
    {'title': 'COVID-19-Pneumonie'}
    {'title': '"Multi-faceted" COVID-19: Russian experience'}
    """
    if getters is None:
        getters = default_getters
    with ZipFile(Path(data_path) / Path(file)) as z:
        for filename in z.namelist():
            if filename.endswith('.json'):
                with z.open(filename) as f:
                    yield format_covid_json(json.load(f), getters=getters, language=language)


def load_from_zip(file="CORD-19-research-challenge.zip", data_path=".", getters=None, language=True, max_docs=None):
    """
    Parameters
    ----------
    file: str or :class:`~pathlib.Path`, optional
        Zip file of a covid archive.
    data_path: str or :class:`~pathlib.Path`, optional
        Location of the archive
    getters: dict, optional
        Recipes to build values for the formatted document.
    language: bool, optional
        Add a `lang` entry that tells the language.
    max_docs: int, optional
        Max number of documents to return

    Returns
    -------
    list of dict

    Examples
    --------

    >>> load_from_zip("covid_sample.zip", data_path='data', getters={'title': get_title}, language=False) # doctest: +NORMALIZE_WHITESPACE
    [{'title': 'Community frailty response service: the ED at your front door'},
     {'title': 'COVID-19-Pneumonie'},
     {'title': '"Multi-faceted" COVID-19: Russian experience'}]
    >>> load_from_zip("covid_sample.zip", data_path='data', getters={'id': get_id}, language=False, max_docs=1) # doctest: +NORMALIZE_WHITESPACE
    [{'id': '000680e3114af4aa10e8f208cd162a61195f4465'}]
    """
    if getters is None:
        getters = default_getters
    return [doc for doc in islice(covid_zip_iterator(file=file,
                                                     data_path=data_path,
                                                     getters=getters,
                                                     language=language),
                                  max_docs)]


from scipy.sparse import vstack
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from sisu.preprocessing.tokenizer import is_relevant_sentence, make_sentences, sanitize_text
from gismo.gismo import Gismo, covering_order
from gismo.common import auto_k
from gismo.parameters import Parameters
from gismo.corpus import Corpus
from gismo.embedding import Embedding
from sisu.embedding_idf import IdfEmbedding


def cosine_order(projection, sentences, query):
    """
    Order relevant sentences by cosine similarity to the query.

    Parameters
    ----------
    projection: callable
        A function that converts a text into a tuple whose first element is an embedding (typically a Gismo :meth:`~gismo.embedding.Embedding.query_projection`).
    sentences: :class:`list` of :class:`dict`
        Sentences as output by :func:`~sisu.summarizer.extract_sentences`.
    query: :class:`str`
        Target query

    Returns
    -------
    :class:`list` of :class:`int`
        Ordered list of indexes of relevant sentences, sorted by cosine similarity
    """
    relevant_indices = [s['index'] for s in sentences if s['relevant']]
    projected_query = projection(query)[0]
    projected_sentences = vstack([projection(sentences[i]['sanitized'])[0] for i in relevant_indices])
    order = np.argsort(- cosine_similarity(projected_sentences, projected_query)[:, 0])
    return [relevant_indices[i] for i in order]


def extract_sentences(source, indices, getter=None, tester=None):
    """
    Pick up the entries of the source corresponding to indices and build a list of sentences out of that.

    Each sentence is a dictionary with the following keys:

    - `index`: position of the sentence in the returned list
    - `sentence`: the actual sentence
    - `relevant`: a boolean that tells if the sentence is eligible for being part of the summary
    - `sanitized`: for relevant sentences, a simplified version to be fed to the embedding

    Parameters
    ----------
    source: :class:`list`
        list of objects
    indices: iterable of :class:`int`
        Indexes of the source items to select
    getter: callable, optional
        Tells how to convert a source entry into text.
    tester: callable, optional
        Tells if the sentence is eligible for being part of the summary.

    Returns
    -------
    list of dict

    Examples
    --------

    >>> doc1 = ("This is a short sentence! This is a sentence with reference to the url http://www.ix.com! "
    ...        "This sentence is not too short and not too long, without URL and without citation. "
    ...        "I have many things to say in that sentence, to the point "
    ...        "I do not know if I will stop anytime soon but don\'t let it stop "
    ...        "you from reading this meaninless garbage and this goes on and "
    ...        "this goes on and this goes on and this goes on and this goes on and "
    ...        "this goes on and  this goes on and  this goes on and  this goes on "
    ...        "and  this goes on and  this goes on and  this goes on and  this goes "
    ...        "on and  this goes on and  this goes on and  this goes on and  this goes "
    ...        "on and  this goes on and that is all.")
    >>> doc2 = ("This is a a sentence with some citations [3, 7]. "
    ...         "This sentence is not too short and not too long, without URL and without citation. "
    ...         "Note that the previous sentence is already present in doc1. "
    ...         "The enzyme cytidine monophospho-N-acetylneuraminic acid hydroxylase (CMAH) catalyzes "
    ...         "the synthesis of Neu5Gc by hydroxylation of Neu5Ac (Schauer et al. 1968).")
    >>> extract_sentences([doc1, doc2], [1, 0]) # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
    [{'index': 0, 'sentence': 'This is a a sentence with some citations [3, 7].', 'relevant': False, 'sanitized': ''},
     {'index': 1, 'sentence': 'This sentence is not too short and not too long, without URL and without citation.',
      'relevant': True, 'sanitized': 'This sentence is not too short and not too long without URL and without citation'},
     {'index': 2, 'sentence': 'Note that the previous sentence is already present in doc1.',
      'relevant': True, 'sanitized': 'Note that the previous sentence is already present in doc'},
     {'index': 3, 'sentence': 'The enzyme cytidine monophospho-N-acetylneuraminic acid hydroxylase (CMAH) catalyzes
                               the synthesis of Neu5Gc by hydroxylation of Neu5Ac (Schauer et al. 1968).',
      'relevant': False, 'sanitized': ''},
     {'index': 4, 'sentence': 'This is a short sentence!', 'relevant': False, 'sanitized': ''},
     {'index': 5, 'sentence': 'This is a sentence with reference to the url http://www.ix.com!',
      'relevant': False, 'sanitized': ''},
     {'index': 6, 'sentence': 'This sentence is not too short and not too long, without URL and without citation.',
      'relevant': False, 'sanitized': ''},
     {'index': 7, 'sentence': "I have many things to say in that sentence...",
      'relevant': False, 'sanitized': ''}]
    """
    if getter is None:
        getter = str
    if tester is None:
        tester = is_relevant_sentence

    sentences = [{'index': i, 'sentence': sent, 'relevant': tester(sent)}
                 for i, sent in enumerate([sent for j in indices
                                           for sent in make_sentences(getter(source[j]))])]
    used = set()
    for s in sentences:
        if s['sentence'] in used and s['relevant']:
            s['relevant'] = False
        else:
            used.add(s['sentence'])
        s['sanitized'] = sanitize_text(s['sentence']) if s['relevant'] else ""
    return sentences


default_summarizer_parameters = {
    'order': 'rank',
    'text_getter': None,
    'sentence_tester': is_relevant_sentence,
    'itf': True,
    'post_processing': lambda summa, i: summa.sentences_[i]['sentence'],
    'sentence_gismo_parameters':  {'post': False, 'resolution': .99},
    'num_documents': None,
    'num_query': None,
    'num_sentences': None,
    'max_chars': None}
"""
List of parameters for the summarizer with their default values.

Parameters
-----------
order: :class:`str`
    Sorting function.
text_getter: callable
    Extraction of text from corpus item. If not specify, the to_text of the :class:`~gismo.corpus.Corpus` will be used.
sentence_tester: callable
    Function that estimates if a sentence is eligible to be part of the summary
itf: :class:`bool`
    Use of ITF normalization in the sentence-level Gismo
post_processing: callable
    post_processing transformation. Signature is (:class:`~sisu.summarizer.Summarizer`, :class:`int`) -> :class:`str`
sentence_gismo_parameters: :class:`dict`
    Tuning of sentence-level gismo. `post` MUST be set  to False.
num_documents: :class:`int` or None
    Number of documents to pre-select
num_query: :class:`int` or None
    Number of features to use in generic query
num_sentences: :class:`int` or None
    Number of sentences to return
max_chars: :class:`int` or None
    Maximal number of characters to return
"""


class Summarizer:
    """
    Summarizer class.

    Parameters
    ----------
    gismo: :class:`~gismo.gismo.Gismo`
        Gismo of the documents to analyze.
    kwargs: :class:`dict`
        Parameters of the summarizer (see :obj:`~sisu.summarizer.default_summarizer_parameters` for details).

    Attributes
    ----------
    query_: :class:`str`
        Query used to summarize.
    sentences_: :class:`list` of :class:`dict`
        Selected sentences. Each sentence is a dictionary with the following keys:

        - `index`: position of the sentence in the returned list
        - `sentence`: the actual sentence
        - `relevant`: a boolean that tells if the sentence is eligible for being part of the summary
        - `sanitized`: for relevant sentences, a simplified version to be fed to the embedding
    order_: :class:`numpy.ndarray`
        Proposed incomplete ordering of the :class:`~sisu.summarizer.Summarizer.sentences_`
    sentence_gismo_: :class:`~gismo.gismo.Gismo`
        Gismo running at sentence level.
    parameters: :class:`~gismo.parameters.Parameters`
        Handler of parameters.

    Examples
    --------

    The package contains a data folder with a toy gismo with articles related to Covid-19. We load it.

    >>> gismo = Gismo(filename="toy_gismo", path="data")

    Then we build a summarizer out of it. We tell to fetch the sentences from the content of the articles.

    >>> summa = Summarizer(gismo, text_getter = lambda d: d['content'])

    Ask for a summary on *bat* with a maximal budget of 500 characters, using pure TF-IDF sentence embedding.

    >>> summa('bat', max_chars=500, itf=False) # doctest: +NORMALIZE_WHITESPACE
    ['By comparing the amino acid sequence of 2019-nCoV S-protein (GenBank Accession: MN908947.3) with
      Bat SARS-like coronavirus isolate bat-SL-CoVZC45 and Bat SARS-like coronavirus isolate Bat-SL-CoVZXC21,
      the latter two were shown to share 89.1% and 88.6% sequence identity to 2019-nCoV S-protein
      (supplementary figure 1) .',
     'Within our bat-hemoplasma network, genotype sharing was restricted to five host communities,
      380 whereas six genotypes were each restricted to a single bat species (Fig. 5A ).']

    Now a summary based on the *cosine* ordering, using the content of abstracts and pure TF-IDF sentence embedding.

    >>> summa('bat', max_chars=500, order='cosine', text_getter = lambda d: d['abstract']) # doctest: +NORMALIZE_WHITESPACE
    ['Bat dipeptidyl peptidase 4 (DPP4) sequences were closely related to 38 those of human and non-human
      primates but distinct from dromedary DPP4 sequence.',
     'The multiple sequence alignment data correlated with already published reports on SARS-CoV-2
      indicated that it is closely related to Bat-Severe Acute Respiratory Syndrome like coronavirus
      (Bat CoV SARS-like) and wellstudied Human SARS.',
     '(i.e., hemoplasmas) across a species-rich 40 bat community in Belize over two years.']

    Now 4 sentences using a *coverage* ordering.

    >>> summa('bat', num_sentences=4, order='coverage') # doctest: +NORMALIZE_WHITESPACE
    ['By comparing the amino acid sequence of 2019-nCoV S-protein (GenBank Accession: MN908947.3)
      with Bat SARS-like coronavirus isolate bat-SL-CoVZC45 and Bat SARS-like coronavirus isolate
      Bat-SL-CoVZXC21, the latter two were shown to share 89.1% and 88.6% sequence identity
      to 2019-nCoV S-protein (supplementary figure 1) .',
     'However, we have not done the IDPs analysis for ORF10 from the Bat-SL-CoVZC45 strain since we
      have taken different strain of Bat CoV (reviewed strain HKU3-1) in our study.',
     'To test the dependence of the hemoplasma 290 phylogeny upon the bat phylogeny and thus assess
      evidence of evolutionary codivergence, we 291 applied the Procrustes Approach to Cophylogeny
      (PACo) using distance matrices and the paco 292 We used hemoplasma genotype assignments to
      create a network, with each node representing a 299 bat species and edges representing shared
      genotypes among bat species pairs.',
     'However, these phylogenetic patterns in prevalence were decoupled from those describing bat
      526 species centrality in sharing hemoplasmas, such that genotype sharing was generally
      restricted 527 by bat phylogeny.']

    As you can see, there are some ``However, '' in the answers.
    A bit of NLP post_processing can take care of those.

    >>> import spacy
    >>> nlp = spacy.load("en_core_web_sm")
    >>> post_nlp = PostNLP(nlp)
    >>> summa('bat', num_sentences=4, order='coverage', post_processing=post_nlp) # doctest: +NORMALIZE_WHITESPACE
    ['By comparing the amino acid sequence of 2019-nCoV S-protein (GenBank Accession: MN908947.3)
      with Bat SARS-like coronavirus isolate bat-SL-CoVZC45 and Bat SARS-like coronavirus isolate
      Bat-SL-CoVZXC21, the latter two were shown to share 89.1% and 88.6% sequence identity
      to 2019-nCoV S-protein (supplementary figure 1) .',
     'We have not done the IDPs analysis for ORF10 from the Bat-SL-CoVZC45 strain since we
      have taken different strain of Bat CoV (reviewed strain HKU3-1) in our study.',
     'To test the dependence of the hemoplasma 290 phylogeny upon the bat phylogeny and thus assess
      evidence of evolutionary codivergence, we 291 applied the Procrustes Approach to Cophylogeny
      (PACo) using distance matrices and the paco 292 We used hemoplasma genotype assignments to
      create a network, with each node representing a 299 bat species and edges representing shared
      genotypes among bat species pairs.',
     'These phylogenetic patterns in prevalence were decoupled from those describing bat
      526 species centrality in sharing hemoplasmas, such that genotype sharing was generally
      restricted 527 by bat phylogeny.']
    """

    def __init__(self, gismo, **kwargs):
        self.gismo = gismo
        self.query_ = None
        self.sentences_ = None
        self.order_ = None
        self.sentence_gismo_ = None
        self.parameters = Parameters(parameter_list=default_summarizer_parameters, **kwargs)
        if self.parameters.text_getter is None:
            self.parameters.text_getter = self.gismo.corpus.to_text

    def rank_documents(self, query, num_query=None):
        """
        Perform a Gismo query at document-level. If the query fails, builds a generic query instead.
        The :attr:`~sisu.summarizer.Summarizer.gismo` and
        :attr:`~sisu.summarizer.Summarizer.query_` attributes are updated.

        Parameters
        ----------
        query: :class:`str`
            Input text
        num_query: :class:`int`
            Number of words of the generic query, is any

        Returns
        -------
        None
        """
        if num_query is None:
            num_query = self.parameters.num_query
        success = self.gismo.rank(query)
        if success:
            self.query_ = query
        else:
            self.query_ = " ".join(self.gismo.get_features_by_rank(k=num_query))
            self.gismo.rank(self.query_)

    def build_sentence_source(self, num_documents=None, getter=None, tester=None):
        """
        Creates the corpus of sentences (:attr:`~sisu.summarizer.Summarizer.sentences_`)

        Parameters
        ----------
        num_documents: :class:`int`, optional
            Number of documents to select (if not, Gismo will automatically decide).
        getter: callable
            Extraction of text from corpus item. If not specify, the to_text of the :class:`~gismo.corpus.Corpus` will be used.
        tester: callable
            Function that estimates if a sentence is eligible to be part of the summary.

        Returns
        -------
        None
        """
        if num_documents is None:
            num_documents = self.parameters.num_documents
        if getter is None:
            getter = self.parameters.text_getter
        if tester is None:
            tester = self.parameters.sentence_tester
        self.sentences_ = extract_sentences(source=self.gismo.corpus,
                                            indices=self.gismo.get_documents_by_rank(k=num_documents,
                                                                                     post=False),
                                            getter=getter,
                                            tester=tester)

    def build_sentence_gismo(self, itf=None, s_g_p=None):
        """
        Creates the Gismo of sentences (:attr:`~sisu.summarizer.Summarizer.sentence_gismo_`)

        Parameters
        ----------
        itf: :class:`bool`, optional
            Applies TF-IDTF embedding. I False, TF-IDF embedding is used.
        s_g_p: :class:`dict`
            Parameters for the sentence Gismo.

        Returns
        -------
        None
        """
        if itf is None:
            itf = self.parameters.itf
        if s_g_p is None:
            s_g_p = self.parameters.sentence_gismo_parameters
        sentence_corpus = Corpus(source=self.sentences_, to_text=lambda s: s['sanitized'])
        sentence_embedding = Embedding() if itf else IdfEmbedding()
        sentence_embedding.fit_ext(embedding=self.gismo.embedding)
        sentence_embedding.transform(sentence_corpus)
        self.sentence_gismo_ = Gismo(sentence_corpus, sentence_embedding, **s_g_p)

    def build_coverage_order(self, k):
        """
        Populate :attr:`~sisu.summarizer.Summarizer.order_` with a covering order with
        target number of sentences *k*. The actual number of indices is stretched
        by the sentence Gismo stretch factor.

        Parameters
        ----------
        k: :class:`int`
            Number of optimal covering sentences.

        Returns
        -------
        :class:`numpy.ndarray`
            Covering order.
        """
        p = self.sentence_gismo_.parameters(post=False)
        cluster = self.sentence_gismo_.get_documents_by_cluster(k=int(k * p['stretch']), **p)
        return covering_order(cluster, wide=p['wide'])

    def summarize(self, query="", **kwargs):
        """
        Performs a full run of all summary-related operations:

        - Rank a query at document level, fallback to a generic query if the query fails;
        - Extract sentences from the top documents
        - Order sentences by one of the three methods proposed, *rank*, *coverage*, and *cosine*
        - Apply post-processing and return list of selected sentences.

        Note that calling a :class:`~sisu.summarizer.Summarizer` will call its
        :meth:`~sisu.summarizer.Summarizer.summarize` method.

        Parameters
        ----------
        query: :class:`str`
            Query to run.
        kwargs: :class:`dict`
            Runtime specific parameters
            (see :obj:`~sisu.summarizer.default_summarizer_parameters` for possible arguments).

        Returns
        -------
        :class:`list` of :class:`str`
            Summary.
        """
        # Instantiate parameters for the call
        p = self.parameters(**kwargs)
        # Perform query, fallback to generic query in case of failure
        self.rank_documents(query=query, num_query=p['num_query'])
        # Extract and preprocess sentences
        self.build_sentence_source(num_documents=p['num_documents'], getter=p['text_getter'],
                                   tester=p['sentence_tester'])
        # Order sentences
        if p['order'] == 'cosine':
            self.order_ = cosine_order(self.gismo.embedding.query_projection, self.sentences_, self.query_)
        elif p['order'] in {'rank', 'coverage'}:
            self.build_sentence_gismo(itf=p['itf'], s_g_p=p['sentence_gismo_parameters'])
            self.sentence_gismo_.rank(query)
            if p['num_sentences'] is None:
                p['num_sentences'] = auto_k(data=self.sentence_gismo_.diteration.x_relevance,
                           order=self.sentence_gismo_.diteration.x_order,
                           max_k=self.sentence_gismo_.parameters.max_k,
                           target=self.sentence_gismo_.parameters.target_k)
            if p['order'] == 'rank':
                self.order_ = self.sentence_gismo_.diteration.x_order
            else:
                self.order_ = self.build_coverage_order(p['num_sentences'])
        if p['max_chars'] is None:
            results = [p['post_processing'](self, i) for i in self.order_[:p['num_sentences']]]
            return [txt for txt in results if len(txt)>0]
        else:
            results = []
            length = 0
            # Maximal number of sentences that will be processed
            max_sentences = int(p['max_chars']/50)
            for i in self.order_[:max_sentences]:
                txt = p['post_processing'](self, i)
                l = len(txt)
                if l>0 and length+l < p['max_chars']:
                    results.append(txt)
                    length += l
                if length > .98*p['max_chars']:
                    break
            return results

    def __call__(self, query="", **kwargs):
        return self.summarize(query, **kwargs)


class PostNLP:
    """
    Post-processor for the :class:`~sisu.summarizer.Summarizer` that leverages a spacy NLP engine.

    - Discard sentences with no verb.
    - Remove adverbs and punctuations that starts a sentence (e.g. "However, we ..." -> "We ...").
    - Optionally, if the engine supports co-references, resolve them.

    Parameters
    ----------
    nlp: callable
        A Spacy nlp engine.
    coref: :class:`bool`
        Resolve co-references if the nlp engine supports it.
    """
    def __init__(self, nlp, coref=False):
        self.nlp = nlp
        self.coref = coref

    def __call__(self, summa, i):
        nlp_sent = self.nlp(summa.sentences_[i]['sentence'])
        tags = {token.tag_ for token in nlp_sent}
        if not any([t.startswith("VB") for t in tags]):
            summa.sentences_[i]['relevant'] = False
            return ""
        while nlp_sent[0].pos_ == "ADV" and len(nlp_sent)>0:
            nlp_sent = nlp_sent[1:]
        if nlp_sent[0].pos_ == "PUNCT":
            nlp_sent = nlp_sent[1:]
        txt = nlp_sent.text
        summa.sentences_[i]['sentence'] = f"{txt[0].upper()}{txt[1:]}"
        if "PRP" in tags and self.coref and hasattr(nlp_sent._, 'has_coref'):
            extract_str = " ".join([s['sentence'] for s in summa.sentences_[max(0, i - 2) : i + 1]])
            extract = self.nlp(extract_str)
            if extract._.has_coref:
                resolved_extract = extract._.coref_resolved
                summa.sentences_[i]['sentence'] = make_sentences(resolved_extract)[-1]
        return summa.sentences_[i]['sentence']

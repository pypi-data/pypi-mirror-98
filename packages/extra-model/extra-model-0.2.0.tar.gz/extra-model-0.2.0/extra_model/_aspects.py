import logging

import pandas as pd
import spacy
from spacy.symbols import NOUN, VERB, acomp, amod, nsubj

"""Generate the basic phrases that will be used for clustering
Major steps:
1) Run Spacy for POS tags
2) extract NPs described by adjectives
3) filter for "high quality phrases" using the Autophrase tool
"""
logger = logging.getLogger(__name__)


def compound_noun_list(token):
    """Find compound nouns.

    :param token: token for which to generate potential compound nouns
    :type token: :class:`spacy.token`
    :return: list of potential compounds
    :rtype: [string]
    """
    nouns = [token.text]
    for nc in token.lefts:
        if nc.dep_ == "compound":
            nouns.append(nc.text + " " + token.text)
    for nc in token.rights:
        if nc.dep_ == "compound":
            nouns.append(token.text + " " + nc.text)
    return nouns


def acomp_list(tokens):
    """Find descriptions for a given token.

    :param tokens: list of tokens that are children of the head of the nount for which descriptions are searched.
    :type tokens: [:class:`spacy.token`]
    :return: list of adjectives
    :rtype: [string]
    """
    acomps = []
    for child in tokens:
        if child.dep == acomp:
            acomps.append(child.text)
            for (
                grandchild
            ) in (
                child.children
            ):  # find both X and Y in patterns of the form "product is X and Y"
                if grandchild.dep_ == "conj":
                    acomps.append(grandchild.text)
    return acomps


def adjective_list(tokens):
    """Find adjectives modifying a given noun.

    :param tokens: tokens of potential adjectice candidates (children of the noun and children of the head for compounds)
    :type tokens: [:class:`spacy.token`]
    :return: list of adjectives
    :rtype: [string]
    """
    adjectives = []
    for child in tokens:
        if child.dep == amod:
            adjectives.append(child.text)
            for (
                grandchild
            ) in (
                child.children
            ):  # find both X and Y in patterns of the form "the X and Y product"
                if grandchild.dep_ == "conj":
                    adjectives.append(grandchild.text)
    return adjectives


def adjective_negations(token):
    """Find all negated adjectives in a sentence.

    :param token: negation token to handle
    :type token: :class:`spacy.token`
    :return: list of negated adjectives
    :rtype: [string]
    """
    negated_adjectives = []

    # "This color is not pretty" case
    if token.head.dep_ == "conj" or token.head.dep_ == "amod":
        negated_adjectives.append(token.head.text)
    # always looking to the right -- not handling sarcasm (e.g., "Beautiful
    # table, not!")
    for tok in token.head.rights:
        if tok.dep_ == "conj" or tok.dep_ == "amod" or tok.dep_ == "acomp":
            negated_adjectives.append(tok.text)
        # noun phrase case "This is not a terrible table"
        if tok.dep_ == "attr":
            for n_tok in tok.children:
                if (
                    n_tok.dep_ == "conj"
                    or n_tok.dep_ == "amod"
                    or n_tok.dep_ == "acomp"
                ):
                    negated_adjectives.append(n_tok.text)

    return negated_adjectives


def parse(dataframe_texts):  # noqa: C901
    """Parse the comments and extract a list of potential aspects based on grammatical relations.

    (e.g. modified by adjective)

    :param dataframe_texts: a dataframe with the raw texts. The collumn wit the texts needs to be called 'Comments'
    :type dataframe_texts: :class:`pandas.DataFrame`
    :return: a dataframe with the aspect candidates
    :rtype: :class:`pandas.DataFrame`
    """
    nlp = spacy.load("en_core_web_sm", disable=["ner"])
    # make a new dataframe with one row for each aspect/adjective pair
    rowlist = []

    # loop over all the texts and do syntax analysis, keeping valid nouns+adjectived
    # runs faster by running spacy in batch-mode
    # we need to keep the index here in order to be able to connect back to
    # the original text later

    # n_threads > 5 can segfault with long (>500 tokens) sentences
    # n_threads has been deprecated in spacy 3.x - https://spacy.io/usage/v2-1#incompat
    for index, document in zip(
        dataframe_texts.index,
        nlp.pipe(dataframe_texts.Comments, batch_size=500),
    ):  # TODO reduce for production/make configurable
        negated_adjectives = []
        for token in document:
            nouns = compound_noun_list(token)
            adjectives = []
            if (
                token.dep == nsubj and token.pos == NOUN and token.head.pos == VERB
            ):  # find nouns with descriptions
                adjectives.extend(acomp_list(token.head.children))
            if token.pos == NOUN:  # find nouns with adjectives
                adjectives.extend(adjective_list(token.children))
                # necessary for compound nouns
                adjectives.extend(adjective_list(token.head.children))
            adjectives = list(dict.fromkeys(adjectives))  # remove duplicates
            if len(adjectives) != 0:
                # since negation can come much later in the sentence, finding
                # it here
                for tok in document:
                    if tok.dep_ == "neg":
                        negated_adjectives = adjective_negations(tok)
                for noun in nouns:
                    for adjective in adjectives:
                        row = {
                            "CiD": index,  # index into the initial raw text dataframe
                            # position within the text of the candidate noun
                            # (in letters!)
                            "position": token.idx,
                            "aspect": noun,
                            "descriptor": adjective,
                            "is_negated": adjective in negated_adjectives,
                        }

                        rowlist.append(row)

    dataframe_aspects = pd.DataFrame(
        rowlist, columns=["CiD", "position", "aspect", "descriptor", "is_negated"]
    )
    return dataframe_aspects


def generate_aspects(dataframe_texts):
    """Generate the aspects that will be merged into topics from the raw texts.

    :param dataframe_texts: a dataframe with the raw texts in the column 'Comments'
    :type dataframe_texts: :class:`pandas.DataFrame`
    :return: a dataframe with the aspect candidates, their associated description, index of original text in the
    input dataframe and location of word in the text
    :rtype: :class:`pandas.DataFrame`
    """
    logger.debug(dataframe_texts.head())
    # extract candidate noun-phrases using spacy
    dataframe_aspects = parse(dataframe_texts)
    return dataframe_aspects

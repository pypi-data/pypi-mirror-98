import pandas as pd
import pytest
import spacy

from extra_model._aspects import (
    acomp_list,
    adjective_list,
    adjective_negations,
    compound_noun_list,
    generate_aspects,
    parse,
)


@pytest.fixture()
def spacy_nlp():
    return spacy.load("en_core_web_sm", disable=["ner"])


def test_aspects__compound_noun_list__left_compound(spacy_nlp):
    example_text = "This is a wood screw."
    assert compound_noun_list(spacy_nlp(example_text)[4]) == ["screw", "wood screw"]


@pytest.mark.skip(reason="Left-headed compounds are exceedingly rare in English")
def test_aspects__compound_noun_list__right_compound(spacy_nlp):
    # left-headed compounds are exceedingly rare in english and in 10k
    # example texts, there was not a single one. Could remove the code or could
    # go for a deeper search for an example
    pass


def test_aspects__acomp_list(spacy_nlp):
    example_text = "The shelf is sturdy and beautiful."
    assert acomp_list(spacy_nlp(example_text)[1].head.children) == [
        "sturdy",
        "beautiful",
    ]


def test_aspects__adjective_list(spacy_nlp):
    example_text = "I bought a sturdy and beautiful shelf."
    assert adjective_list(spacy_nlp(example_text)[6].children) == [
        "sturdy",
        "beautiful",
    ]


@pytest.mark.skip(reason="This needs to be looked at when fixing negations")
def test_aspects__adjective_negations__direct(spacy_nlp):
    example_text = "This not so sturdy table is a disappointment."
    assert adjective_negations(spacy_nlp(example_text)[1]) == ["sturdy"]
    # There is a difference here in spacy versions that will need to be investigated.
    # succeeds in 2.0.18 but fails in 3.0.


def test_aspects__adjective_negations__right_non_attr(spacy_nlp):
    example_text = "This color is not pretty."
    assert adjective_negations(spacy_nlp(example_text)[3]) == ["pretty"]


def test_aspects__adjective_negations__right_attr(spacy_nlp):
    example_text = "This is not a terrible table."
    assert adjective_negations(spacy_nlp(example_text)[2]) == ["terrible"]


def test_aspects__parse(spacy_nlp, mocker):
    # chose a text that exercise as much code as possible
    # second part of the sentence is here to check that negations are properly filtered
    example_text = "The wooden cabinet serves its purpose, it's not terrible."
    data_frame = pd.DataFrame([{"Comments": example_text}])
    mocker.patch("spacy.load", return_value=spacy_nlp)
    result = parse(data_frame)
    assert (
        result.iloc[0]["CiD"] == 0
        and result.iloc[0]["position"] == 11
        and result.iloc[0]["aspect"] == "cabinet"
        and result.iloc[0]["descriptor"] == "wooden"
        and not result.iloc[0]["is_negated"]
    )


def test_aspects_generate_aspects(spacy_nlp, mocker):
    example_text = "The wooden cabinet serves its purpose, it's not terrible."
    data_frame = pd.DataFrame([{"Comments": example_text}])
    mocker.patch("spacy.load", return_value=spacy_nlp)
    result = generate_aspects(data_frame)
    assert (
        result.iloc[0]["CiD"] == 0
        and result.iloc[0]["position"] == 11
        and result.iloc[0]["aspect"] == "cabinet"
        and result.iloc[0]["descriptor"] == "wooden"
        and not result.iloc[0]["is_negated"]
    )

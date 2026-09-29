import os

import pytest

import inflect


def is_eq(p, a, b):
    return (
        p.compare(a, b)
        or p.plnounequal(a, b)
        or p.plverbequal(a, b)
        or p.pladjequal(a, b)
    )


def test_many():  # noqa: C901
    p = inflect.engine()

    data = get_data()

    for line in data:
        if "TODO:" in line:
            continue
        try:
            singular, rest = line.split("->", 1)
        except ValueError:
            continue
        singular = singular.strip()
        rest = rest.strip()
        try:
            plural, comment = rest.split("#", 1)
        except ValueError:
            plural = rest.strip()
            comment = ""
        try:
            mod_plural, class_plural = plural.split("|", 1)
            mod_plural = mod_plural.strip()
            class_plural = class_plural.strip()
        except ValueError:
            mod_plural = class_plural = plural.strip()
        if "verb" in comment.lower():
            is_nv = "_V"
        elif "noun" in comment.lower():
            is_nv = "_N"
        else:
            is_nv = ""

        p.classical(all=0, names=0)
        mod_PL_V = p.plural_verb(singular)
        mod_PL_N = p.plural_noun(singular)
        mod_PL = p.plural(singular)
        if is_nv == "_V":
            mod_PL_val = mod_PL_V
        elif is_nv == "_N":
            mod_PL_val = mod_PL_N
        else:
            mod_PL_val = mod_PL

        p.classical(all=1)
        class_PL_V = p.plural_verb(singular)
        class_PL_N = p.plural_noun(singular)
        class_PL = p.plural(singular)
        if is_nv == "_V":
            class_PL_val = class_PL_V
        elif is_nv == "_N":
            class_PL_val = class_PL_N
        else:
            class_PL_val = class_PL

        check_all(
            p, is_nv, singular, mod_PL_val, class_PL_val, mod_plural, class_plural
        )


def check_all(p, is_nv, singular, mod_PL_val, class_PL_val, mod_plural, class_plural):
    assert mod_plural == mod_PL_val
    assert class_plural == class_PL_val
    assert is_eq(p, singular, mod_plural) in ("s:p", "p:s", "eq")
    assert is_eq(p, mod_plural, singular) in ("p:s", "s:p", "eq")
    assert is_eq(p, singular, class_plural) in ("s:p", "p:s", "eq")
    assert is_eq(p, class_plural, singular) in ("p:s", "s:p", "eq")
    assert singular != ""
    expected = mod_PL_val if class_PL_val else f"{mod_PL_val}|{class_PL_val}"
    assert mod_PL_val == expected

    if is_nv != "_V":
        assert p.singular_noun(mod_plural, 1) == singular

        assert p.singular_noun(class_plural, 1) == singular


def test_def():
    p = inflect.engine()

    p.defnoun("kin", "kine")
    p.defnoun("(.*)x", "$1xen")

    p.defverb("foobar", "feebar", "foobar", "feebar", "foobars", "feebar")

    p.defadj("red", "red|gules")

    assert p.no("kin", 0) == "no kine"
    assert p.no("kin", 1) == "1 kin"
    assert p.no("kin", 2) == "2 kine"

    assert p.no("regex", 0) == "no regexen"

    assert p.plural("foobar", 2) == "feebar"
    assert p.plural("foobars", 2) == "feebar"

    assert p.plural("red", 0) == "red"
    assert p.plural("red", 1) == "red"
    assert p.plural("red", 2) == "red"
    p.classical(all=True)
    assert p.plural("red", 0) == "red"
    assert p.plural("red", 1) == "red"
    assert p.plural("red", 2) == "gules"


def test_ordinal():
    p = inflect.engine()
    assert p.ordinal(0) == "0th"
    assert p.ordinal(1) == p.ordinal("1") == "1st"
    assert p.ordinal(2) == "2nd"
    assert p.ordinal(3) == "3rd"
    assert p.ordinal(4) == "4th"
    assert p.ordinal(5) == "5th"
    assert p.ordinal(6) == "6th"
    assert p.ordinal(7) == "7th"
    assert p.ordinal(8) == "8th"
    assert p.ordinal(9) == "9th"
    assert p.ordinal(10) == "10th"
    assert p.ordinal(11) == "11th"
    assert p.ordinal(12) == "12th"
    assert p.ordinal(13) == "13th"
    assert p.ordinal(14) == "14th"
    assert p.ordinal(15) == "15th"
    assert p.ordinal(16) == "16th"
    assert p.ordinal(17) == "17th"
    assert p.ordinal(18) == "18th"
    assert p.ordinal(19) == "19th"
    assert p.ordinal(20) == "20th"
    assert p.ordinal(21) == "21st"
    assert p.ordinal(22) == "22nd"
    assert p.ordinal(23) == "23rd"
    assert p.ordinal(24) == "24th"
    assert p.ordinal(100) == "100th"
    assert p.ordinal(101) == "101st"
    assert p.ordinal(102) == "102nd"
    assert p.ordinal(103) == "103rd"
    assert p.ordinal(104) == "104th"

    assert p.ordinal(1.1) == p.ordinal("1.1") == "1.1st"
    assert p.ordinal(1.2) == "1.2nd"
    assert p.ordinal(5.502) == "5.502nd"

    assert p.ordinal("zero") == "zeroth"
    assert p.ordinal("one") == "first"
    assert p.ordinal("two") == "second"
    assert p.ordinal("three") == "third"
    assert p.ordinal("four") == "fourth"
    assert p.ordinal("five") == "fifth"
    assert p.ordinal("six") == "sixth"
    assert p.ordinal("seven") == "seventh"
    assert p.ordinal("eight") == "eighth"
    assert p.ordinal("nine") == "ninth"
    assert p.ordinal("ten") == "tenth"
    assert p.ordinal("eleven") == "eleventh"
    assert p.ordinal("twelve") == "twelfth"
    assert p.ordinal("thirteen") == "thirteenth"
    assert p.ordinal("fourteen") == "fourteenth"
    assert p.ordinal("fifteen") == "fifteenth"
    assert p.ordinal("sixteen") == "sixteenth"
    assert p.ordinal("seventeen") == "seventeenth"
    assert p.ordinal("eighteen") == "eighteenth"
    assert p.ordinal("nineteen") == "nineteenth"
    assert p.ordinal("twenty") == "twentieth"
    assert p.ordinal("twenty-one") == "twenty-first"
    assert p.ordinal("twenty-two") == "twenty-second"
    assert p.ordinal("twenty-three") == "twenty-third"
    assert p.ordinal("twenty-four") == "twenty-fourth"
    assert p.ordinal("one hundred") == "one hundredth"
    assert p.ordinal("one hundred and one") == "one hundred and first"
    assert p.ordinal("one hundred and two") == "one hundred and second"
    assert p.ordinal("one hundred and three") == "one hundred and third"
    assert p.ordinal("one hundred and four") == "one hundred and fourth"


def test_decimal_ordinals():
    """
    Capture expectation around ordinals for decimals.

    This expectation is held loosely. Another expectation may be
    considered if appropriate.
    """

    p = inflect.engine()
    assert p.ordinal("1.23") == "1.23rd"
    assert p.ordinal("7.09") == "7.09th"


def test_prespart():
    p = inflect.engine()
    assert p.present_participle("sees") == "seeing"
    assert p.present_participle("eats") == "eating"
    assert p.present_participle("bats") == "batting"
    assert p.present_participle("hates") == "hating"
    assert p.present_participle("spies") == "spying"
    assert p.present_participle("skis") == "skiing"


def test_inflect_on_tuples():
    p = inflect.engine()
    assert p.inflect("plural('egg', ('a', 'b', 'c'))") == "eggs"
    assert p.inflect("plural('egg', ['a', 'b', 'c'])") == "eggs"
    assert p.inflect("plural_noun('egg', ('a', 'b', 'c'))") == "eggs"
    assert p.inflect("plural_adj('a', ('a', 'b', 'c'))") == "some"
    assert p.inflect("plural_verb('was', ('a', 'b', 'c'))") == "were"
    assert p.inflect("singular_noun('eggs', ('a', 'b', 'c'))") == "eggs"
    assert p.inflect("an('error', ('a', 'b', 'c'))") == "('a', 'b', 'c') error"
    assert p.inflect("This is not a function(name)") == "This is not a function(name)"


def test_inflect_on_builtin_constants():
    p = inflect.engine()
    assert (
        p.inflect("Plural of False is plural('False')") == "Plural of False is Falses"
    )
    assert p.inflect("num(%d, False) plural('False')" % 10) == " Falses"

    assert p.inflect("plural('True')") == "Trues"
    assert p.inflect("num(%d, True) plural('False')" % 10) == "10 Falses"
    assert p.inflect("num(%d, %r) plural('False')" % (10, True)) == "10 Falses"

    assert p.inflect("plural('None')") == "Nones"
    assert p.inflect("num(%d, %r) plural('True')" % (10, None)) == "10 Trues"


def test_inflect_keyword_args():
    p = inflect.engine()
    assert (
        p.inflect("number_to_words(1234, andword='')")
        == "one thousand, two hundred thirty-four"
    )

    assert (
        p.inflect("number_to_words(1234, andword='plus')")
        == "one thousand, two hundred plus thirty-four"
    )

    assert (
        p.inflect("number_to_words('555_1202', group=1, zero='oh')")
        == "five, five, five, one, two, oh, two"
    )


def test_NameError_in_strings():
    with pytest.raises(NameError):
        p = inflect.engine()
        assert p.inflect("plural('two')") == "twoes"
        p.inflect("plural(two)")


def test_uncountable_nouns_with_quantities():
    """
    Uncountable nouns keep their form with any quantity.
    """
    p = inflect.engine()
    uncountables = ["information", "equipment", "furniture", "news"]
    for word in uncountables:
        assert p.plural(word) == word
        assert p.plural_noun(word) == word
        for count in range(5):
            assert p.plural(word, count) == word
            assert p.no(word, count).endswith(f" {word}")
        # singular of an uncountable is itself: round trip is stable
        assert p.singular_noun(word) == word
        assert p.singular_noun(p.plural(word)) == word

    assert p.no("information", 2) == "2 information"
    assert p.no("equipment", 3) == "3 equipment"


def test_compound_possessive_roundtrip():
    """
    plural followed by singular_noun is an identity on singular
    compounds and possessive phrases, and the round trip is idempotent.
    """
    p = inflect.engine()
    phrases = [
        "mother-in-law",
        "attorney general",
        "commander-in-chief",
        "lady-in-waiting",
        "passerby",
        "brother-in-law",
        "brother-in-law's house",
        "son-in-law's car",
        "dog's bone",
        "children's toy",
        "James's book",
        "the cat's pajamas",
    ]
    for phrase in phrases:
        plural = p.plural(phrase)
        # pluralization is deterministic
        assert p.plural(phrase) == plural
        # plural -> singular recovers the original
        assert p.singular_noun(plural) == phrase
        # and applying the round trip again changes nothing
        assert p.plural(p.singular_noun(plural)) == plural

    # canonical spot checks
    assert p.plural("mother-in-law") == "mothers-in-law"
    assert p.plural("brother-in-law") == "brothers-in-law"
    assert p.plural("brother-in-law's house") == "brothers-in-law's house"
    assert p.plural("dog's bone") == "dog's bones"


def test_classical_toggle_is_explainable():
    """
    Classical mode only affects words with documented classical forms,
    and toggling back restores the modern output exactly.
    """
    p = inflect.engine()
    words = [
        "formula",
        "index",
        "cow",
        "person",
        "brother",
        "criterion",
        "dog",
        "attorney general",
        "brother-in-law",
    ]

    p.classical(all=False)
    modern = {w: p.plural(w) for w in words}
    p.classical(all=True)
    classical = {w: p.plural(w) for w in words}
    p.classical(all=False)
    # no state leaks: toggling back reproduces the modern output
    assert {w: p.plural(w) for w in words} == modern
    p.classical(all=True)
    assert {w: p.plural(w) for w in words} == classical
    p.classical(all=False)

    # documented classical distinctions
    assert modern["formula"] == "formulas"
    assert classical["formula"] == "formulae"
    assert modern["index"] == "indexes"
    assert classical["index"] == "indices"
    assert modern["cow"] == "cows"
    assert classical["cow"] == "kine"
    assert modern["person"] == "people"
    assert classical["person"] == "persons"
    assert modern["brother"] == "brothers"
    assert classical["brother"] == "brethren"
    assert modern["brother-in-law"] == "brothers-in-law"
    assert classical["brother-in-law"] == "brethren-in-law"

    # words without classical variants are unaffected by the toggle
    assert classical["dog"] == modern["dog"] == "dogs"
    assert classical["criterion"] == modern["criterion"] == "criteria"
    assert classical["attorney general"] == modern["attorney general"]


def get_data():
    filename = os.path.join(os.path.dirname(__file__), "inflections.txt")
    with open(filename, encoding='utf-8') as strm:
        return list(map(str.strip, strm))

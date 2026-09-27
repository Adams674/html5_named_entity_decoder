"""Core decoder for HTML5 named character references.

The entity table is generated from the HTML5 specification's named character
reference list.  We store it as a dict mapping entity name (including the
leading ampersand) to its decoded string value.  At decode time we sort the
keys by length descending so that the longest match wins — this is the rule
the HTML5 tokenizer follows.
"""
from __future__ import annotations
import html

# The complete HTML5 named character reference table.  Keys include the
# leading '&' so that the decoder can match prefixes of the input directly.
# This dict is built from Python's :mod:`html.entities` module, which itself
# is derived from the HTML5 specification.  ``html5`` is the canonical set;
# the older ``entitydefs`` / ``codepoint2name`` dicts are supersets that
# include non-standard entries, so we deliberately avoid them.
NAMED_REFERENCES: dict[str, str] = {
    "&" + name + ";": value
    for name, value in html.entities.html5.items()
}

# Some legacy entities (e.g. ``&amp``) are valid even without a trailing
# semicolon.  The HTML5 spec lists these explicitly.  ``html.entities.html5``
# already contains the no-semicolon forms as separate keys, so add them here
# too.  We keep a sorted list of keys (longest first) so the decoder can
# perform a greedy longest-match scan.
for name, value in html.entities.html5.items():
    if ";" not in name:
        NAMED_REFERENCES["&" + name] = value

_SORTED_KEYS: list[str] = sorted(NAMED_REFERENCES.keys(), key=len, reverse=True)


def decode(text: str) -> str:
    """Decode HTML5 named character references in *text*.

    Both the standard ``&name;`` form and the legacy no-semicolon form
    (``&amp``, ``&copy``, etc.) are recognised.  When a name is a prefix of
    a longer valid name, the **longest** match wins, matching the HTML5
    tokenizer semantics.

    Numeric references (``&#65;``, ``&#x41;``) are **not** handled here —
    use :func:`html.unescape` for those.  Keeping this library focused on
    *named* references only makes the behaviour predictable and the table
    auditable.
    """
    if not text:
        return text

    result: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        if text[i] == "&":
            matched = False
            for key in _SORTED_KEYS:
                if text.startswith(key, i):
                    result.append(NAMED_REFERENCES[key])
                    i += len(key)
                    matched = True
                    break
            if not matched:
                result.append(text[i])
                i += 1
        else:
            result.append(text[i])
            i += 1
    return "".join(result)


# Public alias so callers can use a more descriptive name if they prefer.
decode_entities = decode

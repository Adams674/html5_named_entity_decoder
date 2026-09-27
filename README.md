# HTML5 Named Entity Decoder

Decodes HTML5 named character references (e.g. `&amp;`, `&copy;`, and legacy forms like `&amp` without a trailing semicolon) in a string.

## Usage

```python
from html5_named_entity_decoder import decode, decode_entities, NAMED_REFERENCES

decode("Tom &amp Jerry")       # -> 'Tom & Jerry'
decode("&copy; 2021")          # -> '\u00a9 2021'
decode_entities("&lt;a&gt;")   # -> '<a>'
```

`decode(text: str) -> str` is the main function. `decode_entities` is an alias. `NAMED_REFERENCES` is the raw `dict` mapping `&name;` (or legacy `&name`) to its decoded value.

## Why

Python's `html.unescape` handles numeric references and named entities, but its behaviour with legacy no-semicolon entities is implicit and easy to get wrong. This library exists to decode *only* named references, explicitly including the legacy forms, with longest-match-wins semantics — the rule the HTML5 tokenizer uses. The trade-off: numeric references (`&#65;`, `&#x41;`) are **not** decoded. If you need those, call `html.unescape` first, then this library, or vice versa depending on your needs.

## Edge cases

- A bare `&` with no following valid name is left untouched.
- `&unknown;` (not a real entity) is left untouched, including the semicolon.
- When one entity name is a prefix of another (e.g. `&amp` vs `&amp;`), the longest match wins.

"""HTML5 Named Entity Decoder.

Decodes the complete set of HTML5 named character references.
"""
from .core import decode, decode_entities, NAMED_REFERENCES

__all__ = ["decode", "decode_entities", "NAMED_REFERENCES"]

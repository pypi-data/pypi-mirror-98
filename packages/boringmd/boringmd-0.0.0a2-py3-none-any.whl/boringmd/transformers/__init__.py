from typing import List

from boringmd.transformers.emphasis import EmphasisTransformer
from boringmd.transformers.fenced_code import FencedCodeTransformer
from boringmd.transformers.front_matter import FrontMatterTransformer
from boringmd.transformers.heading import HeadingTransformer
from boringmd.transformers.html import HtmlTransformer
from boringmd.transformers.indented_code import IndentedCodeTransformer
from boringmd.transformers.inline_code import InlineCodeTransformer
from boringmd.transformers.strong import StrongTransformer
from boringmd.transformers.transformer import Transformer

__all__ = ["chain"]


def chain() -> List[Transformer]:
    """ Returns an ordered list of transformers. """
    return [
        FrontMatterTransformer(),
        IndentedCodeTransformer(),
        InlineCodeTransformer(),
        FencedCodeTransformer(),
        HeadingTransformer(),
        HtmlTransformer(),
        StrongTransformer(),
        EmphasisTransformer(),
    ]

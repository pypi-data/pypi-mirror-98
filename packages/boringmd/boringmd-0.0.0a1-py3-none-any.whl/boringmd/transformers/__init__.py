from boringmd.transformers.fenced_code import FencedCodeTransformer
from boringmd.transformers.front_matter import FrontMatterTransformer
from boringmd.transformers.transformer import Transformer
from boringmd.transformers.heading import HeadingTransformer
from boringmd.transformers.inline_code import InlineCodeTransformer
from typing import List

from boringmd.transformers.html import HtmlTransformer
from boringmd.transformers.strong import StrongTransformer
from boringmd.transformers.emphasis import EmphasisTransformer
from boringmd.transformers.indented_code import IndentedCodeTransformer

__all__ = ["FrontMatterTransformer", "HeadingTransformer", "Transformer"]

def chain() -> List[Transformer]:
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

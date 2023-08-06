from functools import cached_property
from logging import getLogger
from pathlib import Path

from typing import List

from lstr import lstr

logger = getLogger()


from boringmd.transformers import chain






class MarkdownNormalizer:
    """
    To plain text.
    """

    def __init__(self, document: str) -> None:
        self.document = document
        self.transformers = chain()

    @cached_property
    def normalized(self) -> str:
        delete: List[int] = []
        lines = [lstr(line) for line in self.document.splitlines()]
        for index in range(len(lines)):
            for transformer in self.transformers:
                logger.debug("Normalising: %s", lines[index])
                result = transformer.transform(index, lines[index])
                if result and result.stop:
                    break
                if result and result.delete:
                    delete.append(index)
                if result and result.empty:
                    lines[index] = lstr("")
                if result and result.line:
                    lines[index] = result.line

        for index in reversed(delete):
            del lines[index]

        return "\n".join([str(line) for line in lines]) + "\n"


# def discard_indented_code(text: str) -> str:
#     delete: List[int] = []
#     lines = text.splitlines()
#     for index, line in enumerate(lines):
#         if line.startswith("    "):
#             delete.append(index)

#     for index in reversed(delete):
#         del lines[index]

#     return "\n".join(lines)


# def discard_fenced_code(text: str) -> str:
#     delete: List[int] = []
#     inside = False
#     lines = text.splitlines()
#     for index, line in enumerate(lines):
#         if inside:
#             delete.append(index)
#         if line.startswith("```"):
#             if inside := not inside:
#                 delete.append(index)

#     for index in reversed(delete):
#         del lines[index]

#     return "\n".join(lines)


# def discard_front_matter(text: str) -> str:
#     chunks = text.splitlines()
#     if len(chunks) == 0 or chunks[0] != "---":
#         return text
#     del chunks[0]
#     while chunks[0] != "---":
#         del chunks[0]
#     del chunks[0]
#     return "\n".join(chunks)


# def discard_punctuation_islands(text: str) -> str:
#     return sub(r"((?<!\S)[^\w]+(?!\S))", " ", text)


# def discard_html_pair(text: str) -> str:
#     exp = r"(<.*>)(.*)(<\/.*>)"
#     normal = text
#     while True:
#         m = search(exp, normal)
#         if not m:
#             return normal
#         normal = sub(exp, m.groups()[1], normal)


# def discard_html_single(text: str) -> str:
#     return sub(r"(<[^<]*/>)", " ", text)


# def normalize(text: Optional[str]) -> str:
#     if text is None:
#         logger.debug("<None> normalizes to empty string.")
#         return ""

#     logger.debug('Normalizing "%s".', text)
#     normal = text
#     normal = discard_front_matter(normal)
#     normal = discard_fenced_code(normal)
#     normal = discard_indented_code(normal)
#     normal = discard_punctuation_islands(normal)
#     normal = discard_html_pair(normal)
#     normal = discard_html_single(normal)
#     normal = " ".join(normal.splitlines())

#     logger.debug('Normalized "%s" to "%s".', text, normal)
#     return normal


def from_string(text: str) -> str:
    return MarkdownNormalizer(text).normalized


def from_file(path: Path) -> str:
    with open(path, "r") as stream:
        return from_string(stream.read())

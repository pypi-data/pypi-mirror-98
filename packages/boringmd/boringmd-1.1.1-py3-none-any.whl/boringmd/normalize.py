from logging import getLogger
from pathlib import Path
from typing import List

from lstr import lstr

from boringmd.transformers import chain


def text_from_file(path: Path) -> str:
    """
    Converts a Markdown file to plain text.

    Arguments:
        Path: Path to Markdown file.

    Returns:
        Conversion to plain text.
    """
    with open(path, "r") as stream:
        return text_from_string(stream.read())


def text_from_string(document: str) -> str:
    """
    Converts a Markdown document to plain text.

    Arguments:
        document: Markdown document.

    Returns:
        Conversion to plain text.
    """

    transformers = chain()
    delete: List[int] = []
    lines = [lstr(line) for line in document.splitlines()]
    logger = getLogger("boringmd")

    for index in range(len(lines)):
        index_str = "#" + str(index).rjust(len(str(len(lines))), "0")
        logger.debug("Starting chain for %s: %s", index_str, lines[index])

        for transformer in transformers:
            logger.debug("Transforming %s with %s.", index_str, transformer.name)
            if line_guidance := transformer.transform(index, lines[index]):
                if line_guidance.delete:
                    logger.debug("Deleting %s.", index_str)
                    delete.append(index)
                    break
                elif line_guidance.stop:
                    break

    for index in reversed(delete):
        del lines[index]

    return "\n".join([str(line) for line in lines])

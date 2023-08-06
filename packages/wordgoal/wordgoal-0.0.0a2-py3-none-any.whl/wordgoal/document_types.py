from enum import Enum
from logging import getLogger


class DocumentType(Enum):
    UNHANDLED = 0
    TEXT = 1
    MARKDOWN = 2


FILE_TYPES = {
    DocumentType.MARKDOWN: [".markdown", ".md"],
    DocumentType.TEXT: [".text", ".txt"],
}


def get_document_type(suffix: str) -> DocumentType:
    """
    Gets the document type of a file with a given suffix.

    Arguments:
        suffix: Filename suffix. Must begin with a dot; `.foo`, not `foo`. Case
                insensitive.

    Returns:
        Document type.
    """

    for document_type, extensions in FILE_TYPES.items():
        if suffix.lower() in extensions:
            break
    else:
        document_type = DocumentType.UNHANDLED

    getLogger("wordgoal").debug('Suffix "%s" is %s', suffix, document_type)
    return document_type

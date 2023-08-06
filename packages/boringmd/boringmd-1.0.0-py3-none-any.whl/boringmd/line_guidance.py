class LineGuidance:
    """
    Describes guidance for further transformations of a line.

    Arguments:
        delete: Delete the line.
        stop:   Do not transform the line any further.
    """

    def __init__(self, delete: bool = False, stop: bool = False) -> None:
        self.delete = delete
        self.stop = stop

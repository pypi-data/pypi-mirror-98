class UnknownPeerError(Exception):
    def __init__(self, text) -> None:
        self.text = text

from app.storage.revision_store import RevisionStore


class RevisionLoader:
    """
    Loads revision items from persistent storage.
    """

    def __init__(self):

        self.store = RevisionStore()

    def load(self):

        return self.store.load()

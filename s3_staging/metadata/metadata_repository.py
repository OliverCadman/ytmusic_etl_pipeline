


class MetadataRepository(object):
    def __init__(self, metadata=None):
        self.metadata = metadata if metadata else {}

    def add_item(self, key: str, val: any):
        if not key or not val:
            raise ValueError(f"Arguments 'key' and 'val' must be specified.")
        self.metadata.update({key: str(val)})

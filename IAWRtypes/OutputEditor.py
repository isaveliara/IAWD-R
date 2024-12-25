from ._queue import QueueEntry

class OutputEditorEntry(QueueEntry):
    def __init__(self, channel_id: str) -> None:
        super().__init__("outputEditor", channel_id)

    def withType(self, type_value) -> 'OutputEditorEntry':
        self.action["type"] = type_value
        return self

    def withValue(self, value) -> 'OutputEditorEntry':
        self.action["value"] = value
        return self

class QueueEntry:
    def __init__(self, name, channelId: str) -> None:
        self.name = name
        self.channelId = channelId
        self.action = {}

    def to_dict(self) -> dict:
        """
        Serializa a entrada para um dicionário.
        """
        return {
            "name": self.name,
            "fromChannel": self.channelId,
            "action": self.action,
        }

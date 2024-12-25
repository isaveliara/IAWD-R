from ._queue import QueueEntry

class ManagePlayerEntry(QueueEntry):
    def __init__(self, channel_id: str) -> None:
        super().__init__("ManagePlayer", channel_id)

    def kickPlayer(self, playerId: int) -> 'ManagePlayerEntry':
        self.action["type"] = "kickPlayer"
        self.action["playerId"] = playerId
        return self

    def killPlayer(self, playerId: int) -> 'ManagePlayerEntry':
        self.action["type"] = "killPlayer"
        self.action["playerId"] = playerId
        return self

    def teleportPlayer(self, playerId: int, position: int) -> 'ManagePlayerEntry':
        self.action["type"] = "teleportPlayer"
        self.action["playerId"] = playerId
        self.action["position"] = position
        return self

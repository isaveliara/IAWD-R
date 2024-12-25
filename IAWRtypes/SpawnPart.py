from ._queue import QueueEntry

class SpawnPartEntry(QueueEntry):
    def __init__(self, channel_id: str) -> None:
        super().__init__("spawnPart", channel_id)

    def withPosition(self, position) -> 'SpawnPartEntry':
        self.action["position"] = position
        return self

    def withColor(self, color) -> 'SpawnPartEntry':
        self.action["color"] = color
        return self

    def withSize(self, size) -> 'SpawnPartEntry':
        self.action["size"] = size
        return self

    def withName(self, name) -> 'SpawnPartEntry':
        self.action["name"] = name
        return self

    def withTexture(self, texture_url) -> 'SpawnPartEntry':
        self.action["texture"] = texture_url
        return self

    def isAnchored(self, anchored: bool) -> 'SpawnPartEntry':
        self.action["anchored"] = anchored
        return self

    def withTransparency(self, transparency: float) -> 'SpawnPartEntry':
        self.action["transparency"] = transparency
        return self

    def canCollide(self, can_collide: bool) -> 'SpawnPartEntry':
        self.action["canCollide"] = can_collide
        return self

    def canTouch(self, can_touch: bool) -> 'SpawnPartEntry':
        self.action["canTouch"] = can_touch
        return self

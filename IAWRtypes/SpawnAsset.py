from ._queue import QueueEntry

class SpawnAssetEntry(QueueEntry):
    def __init__(self, channel_id: str) -> None:
        super().__init__("spawnAsset", channel_id)

    def withAssetId(self, asset_id: int) -> 'SpawnAssetEntry':
        self.action["assetId"] = asset_id
        return self

    def withPosition(self, position) -> 'SpawnAssetEntry':
        self.action["position"] = position
        return self

    def withName(self, name) -> 'SpawnAssetEntry':
        self.action["name"] = name
        return self

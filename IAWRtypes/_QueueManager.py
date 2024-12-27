from ._queue import QueueEntry

class QueueManager:
    def __init__(self) -> None:
        self.queue = {}
        self.next_id = 0
    
    def count(self, channel_id: str) -> int:
        """
        Retorna o numero de entradas da fila.
        """
        return sum(1 for value in self.queue.values() if value["fromChannel"] == channel_id)

    def add_to_queue(self, entry: QueueEntry) -> None:
        """
        Adiciona uma entrada à fila.
        """
        self.queue[self.next_id] = entry.to_dict()
        self.next_id += 1

    def get_queue(self) -> dict:
        """
        Retorna todas as entradas da fila.
        """
        return self.queue
    
    def take_queue(self, channel_id: str) -> dict:
        """
        Retorna todas as entradas da fila para um canal específico, e limpa as associadas a ela.
        """
        filtered_queue = {
            key: value for key, value in self.queue.items() if value["fromChannel"] == channel_id
        }
        self.queue = {
            key: value for key, value in self.queue.items() if value["fromChannel"] != channel_id
        }
        return filtered_queue

    def clear_queue(self) -> None:
        """
        Limpa todas as entradas da fila.
        """
        self.queue = {}
        self.next_id = 0
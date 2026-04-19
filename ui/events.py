from textual.message import Message
from models.WiFiNetwork import WiFiNetwork

class NetworkDiscovered(Message):
    def __init__(self, network, hit_count) -> None:
        super().__init__()
        self.network = network
        self.hit_count = hit_count
    
class ScanError(Message):
    def __init__(self, error : Exception) -> None:
        super().__init__()
        self.error = error

class ScanStopped(Message):
    pass

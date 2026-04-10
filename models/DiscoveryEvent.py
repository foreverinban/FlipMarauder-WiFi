from dataclasses import dataclass, field
from models.WiFiNetwork import WiFiNetwork
from datetime import datetime


@dataclass(frozen=True)
class DiscoveryEvent:
    network : 'WiFiNetwork'
    time_stamp = field(default_factory=datetime.now)
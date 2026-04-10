from dataclasses import dataclass, field
from datetime import datetime

from models.WiFiNetwork import WiFiNetwork


@dataclass(frozen=True)
class DiscoveryEvent:
    network: "WiFiNetwork"
    time_stamp: datetime = field(default_factory=datetime.now)
